#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动文件清理服务
自动删除超过指定天数的上传和输出文件
"""

import os
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FileCleanerService:
    """文件自动清理服务"""
    
    def __init__(self, cleanup_days=1):
        """
        初始化清理服务
        
        Args:
            cleanup_days (int): 文件保留天数，默认1天
        """
        self.cleanup_days = cleanup_days
        self.cleanup_interval = 24 * 3600  # 每24小时运行一次
        self.running = False
        self.cleanup_thread = None
        
        # 需要清理的目录
        self.cleanup_dirs = [
            'uploads',
            'output', 
            'logs'
        ]
        
        # 需要清理的文件扩展名
        self.cleanup_extensions = {'.xlsx', '.xls', '.log', '.tmp'}
        
    def start(self):
        """启动自动清理服务"""
        if self.running:
            return
            
        self.running = True
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        logger.info(f"🧹 文件清理服务已启动，将每{self.cleanup_days}天清理一次旧文件")
        
        # 立即执行一次清理
        self._cleanup_old_files()
    
    def stop(self):
        """停止自动清理服务"""
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=5)
        logger.info("🛑 文件清理服务已停止")
    
    def _cleanup_loop(self):
        """清理循环线程"""
        while self.running:
            try:
                # 等待清理间隔
                for _ in range(int(self.cleanup_interval)):
                    if not self.running:
                        break
                    time.sleep(1)
                
                if self.running:
                    self._cleanup_old_files()
                    
            except Exception as e:
                logger.error(f"❌ 清理循环出错: {e}")
                time.sleep(60)  # 出错后等待1分钟再试
    
    def _cleanup_old_files(self):
        """清理超过指定天数的旧文件"""
        try:
            cutoff_time = datetime.now() - timedelta(days=self.cleanup_days)
            total_cleaned = 0
            total_size = 0
            
            logger.info(f"🧹 开始清理 {cutoff_time.strftime('%Y-%m-%d %H:%M:%S')} 之前的文件...")
            
            for dir_name in self.cleanup_dirs:
                if not os.path.exists(dir_name):
                    continue
                
                cleaned_count, cleaned_size = self._cleanup_directory(dir_name, cutoff_time)
                total_cleaned += cleaned_count
                total_size += cleaned_size
                
                if cleaned_count > 0:
                    logger.info(f"📁 {dir_name}: 清理了 {cleaned_count} 个文件，释放 {self._format_size(cleaned_size)}")
            
            if total_cleaned > 0:
                logger.info(f"✅ 清理完成：共清理 {total_cleaned} 个文件，释放 {self._format_size(total_size)} 空间")
            else:
                logger.info("✨ 没有需要清理的文件")
                
        except Exception as e:
            logger.error(f"❌ 文件清理失败: {e}")
    
    def _cleanup_directory(self, dir_path, cutoff_time):
        """清理指定目录中的旧文件"""
        cleaned_count = 0
        cleaned_size = 0
        
        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = Path(root) / file
                    
                    # 检查文件扩展名
                    if file_path.suffix.lower() not in self.cleanup_extensions:
                        continue
                    
                    # 跳过.gitkeep文件
                    if file == '.gitkeep':
                        continue
                    
                    try:
                        # 检查文件修改时间
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        
                        if mtime < cutoff_time:
                            file_size = file_path.stat().st_size
                            file_path.unlink()
                            cleaned_count += 1
                            cleaned_size += file_size
                            logger.debug(f"🗑️  删除: {file_path} ({mtime.strftime('%Y-%m-%d %H:%M:%S')})")
                            
                    except Exception as e:
                        logger.warning(f"⚠️  删除文件失败 {file_path}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"❌ 清理目录 {dir_path} 失败: {e}")
        
        return cleaned_count, cleaned_size
    
    def cleanup_now(self):
        """立即执行一次清理"""
        logger.info("🧹 手动触发文件清理...")
        self._cleanup_old_files()
    
    def get_file_stats(self):
        """获取各目录的文件统计信息"""
        stats = {}
        
        for dir_name in self.cleanup_dirs:
            if not os.path.exists(dir_name):
                stats[dir_name] = {'count': 0, 'size': 0}
                continue
            
            count = 0
            size = 0
            
            try:
                for root, dirs, files in os.walk(dir_name):
                    for file in files:
                        if file == '.gitkeep':
                            continue
                        
                        file_path = Path(root) / file
                        if file_path.suffix.lower() in self.cleanup_extensions:
                            count += 1
                            size += file_path.stat().st_size
                            
            except Exception as e:
                logger.warning(f"⚠️  获取 {dir_name} 统计信息失败: {e}")
            
            stats[dir_name] = {
                'count': count, 
                'size': size,
                'size_formatted': self._format_size(size)
            }
        
        return stats
    
    @staticmethod
    def _format_size(size):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"


# 全局清理服务实例
file_cleaner = FileCleanerService(cleanup_days=1)

def start_file_cleaner():
    """启动文件清理服务"""
    file_cleaner.start()

def stop_file_cleaner():
    """停止文件清理服务"""
    file_cleaner.stop()

def cleanup_files_now():
    """立即清理文件"""
    file_cleaner.cleanup_now()

def get_file_stats():
    """获取文件统计信息"""
    return file_cleaner.get_file_stats()
