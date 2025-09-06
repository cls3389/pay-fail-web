#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地启动脚本 - 直接运行Flask开发服务器
适合本地开发和小用户量部署
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from excel_web import app
from config import Config

if __name__ == '__main__':
    print("=" * 60)
    print("  扣款失败信息处理工具 - 本地版本")
    print("=" * 60)
    print()
    
    # 检查依赖
    print("📦 检查运行环境...")
    try:
        import flask
        import pandas
        import openpyxl
        print("✅ 所有依赖包正常")
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        sys.exit(1)
    
    # 创建必要目录
    print("📁 检查目录结构...")
    Config.init_app()
    print("✅ 目录结构正常")
    
    print()
    print("🚀 启动应用...")
    print("📍 访问地址: http://localhost:4009")
    print("📍 网络访问: http://{}:4009".format("你的IP地址"))
    print("⏹️  按 Ctrl+C 停止应用")
    print()
    
    try:
        # 开发模式运行
        app.run(
            host='0.0.0.0',  # 允许网络访问
            port=4009,
            debug=False,      # 生产模式
            threaded=True     # 开启多线程
        )
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)
