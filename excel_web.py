#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扣款失败信息处理工具 - Web版本
基于Flask的Web界面，支持文件上传和在线处理
"""

import os
import json
import traceback
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from config import Config
from excel_processor import excel_service
from file_cleaner import start_file_cleaner, stop_file_cleaner, cleanup_files_now, get_file_stats

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 启用CORS
    CORS(app)
    
    # 初始化目录
    Config.init_app()
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # 启动文件清理服务
    start_file_cleaner()
    
    return app

app = create_app()

def allowed_file(filename):
    """检查文件类型是否允许"""
    return Path(filename).suffix.lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """主页"""
    return render_template('index.html', config={
        'max_file_size': app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024),  # MB
        'allowed_extensions': list(app.config['ALLOWED_EXTENSIONS']),
        'required_columns': app.config['REQUIRED_COLUMNS']
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """文件上传和预览处理接口"""
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': '没有选择文件'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': '没有选择文件'
            }), 400
        
        # 验证文件类型
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': f'不支持的文件格式，请上传 {", ".join(app.config["ALLOWED_EXTENSIONS"])} 文件'
            }), 400
        
        # 保存上传的文件
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(upload_path)
        
        print(f"📁 处理文件: {upload_path}")
        
        # 处理Excel文件并获取预览数据
        result = excel_service.process_excel_for_preview(upload_path)
        print(f"📊 预览处理结果: {result.get('success', False)}")
        
        # 同时生成Excel文件用于下载
        if result['success']:
            print("🔄 开始生成Excel文件...")
            excel_result = excel_service.process_excel_file(
                input_path=upload_path, 
                output_dir=app.config['OUTPUT_FOLDER']
            )
            print(f"✅ Excel生成结果: {excel_result.get('success', False)}")
            if excel_result['success']:
                output_filename = os.path.basename(excel_result['output_file'])
                result['download_url'] = url_for('download_file', filename=output_filename)
                result['excel_file_name'] = output_filename
        
        # 清理上传的临时文件
        try:
            os.remove(upload_path)
        except Exception:
            pass  # 忽略删除临时文件的错误
        
        # 处理完成后触发文件清理
        try:
            cleanup_files_now()
        except Exception as e:
            print(f"⚠️ 文件清理失败: {e}")
        
        return jsonify(result)
        
    except RequestEntityTooLarge:
        return jsonify({
            'success': False,
            'message': f'文件太大，请上传小于 {app.config["MAX_CONTENT_LENGTH"] // (1024*1024)}MB 的文件'
        }), 413
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'处理文件时发生错误: {str(e)}',
            'errors': [str(e), traceback.format_exc()]
        }), 500

@app.route('/download/<filename>')
def download_file(filename):
    """文件下载接口"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """获取系统统计信息"""
    try:
        upload_dir = Path(app.config['UPLOAD_FOLDER'])
        output_dir = Path(app.config['OUTPUT_FOLDER'])
        
        upload_files = list(upload_dir.glob('*')) if upload_dir.exists() else []
        output_files = list(output_dir.glob('*')) if output_dir.exists() else []
        
        # 添加文件清理统计
        file_stats = get_file_stats()
        
        return jsonify({
            'upload_folder_size': len(upload_files),
            'output_folder_size': len(output_files),
            'supported_formats': list(app.config['ALLOWED_EXTENSIONS']),
            'max_file_size_mb': app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024),
            'required_columns': app.config['REQUIRED_COLUMNS'],
            'optional_columns': app.config.get('OPTIONAL_COLUMNS', []),
            'file_cleanup_stats': file_stats,
            'cleanup_retention_days': 1
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """健康检查端点 - 用于Docker健康检查和监控"""
    try:
        # 检查应用基本功能
        from config import Config
        from excel_processor import excel_service
        
        # 简单的状态检查
        status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'excel-processor-web',
            'version': '1.0.0'
        }
        
        return jsonify(status)
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/admin/cleanup', methods=['POST'])
def admin_cleanup():
    """手动清理文件接口"""
    try:
        cleanup_files_now()
        file_stats = get_file_stats()
        return jsonify({
            'success': True,
            'message': '文件清理完成',
            'file_stats': file_stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'清理失败: {str(e)}'
        })

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return render_template('500.html'), 500

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """文件过大错误处理"""
    return jsonify({
        'success': False,
        'message': f'文件太大，请上传小于 {app.config["MAX_CONTENT_LENGTH"] // (1024*1024)}MB 的文件'
    }), 413

if __name__ == '__main__':
    # 开发环境运行
    app.run(
        host='0.0.0.0',
        port=4009,
        debug=True
    )
