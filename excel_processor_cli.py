#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扣款失败信息处理工具 - 独立命令行版本
结合Web版本的核心功能与原始版本的用户体验
支持拖拽文件运行和PyInstaller打包
"""

import os
import sys
import time
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from excel_processor_standalone import process_excel_file

def 处理Excel文件(文件路径):
    """处理Excel文件的主要函数"""
    print(f"📁 正在处理文件: {文件路径}")
    
    try:
        # 使用独立版本的核心处理逻辑 - 输出到当前目录
        result = process_excel_file(文件路径)
        
        if result['success']:
            print(f"✅ 处理成功！")
            print(f"📊 统计信息:")
            for key, value in result['stats'].items():
                print(f"   • {key}: {value}")
            print(f"📄 输出文件: {result['output_file']}")
            
            # 尝试自动打开输出文件
            try:
                import subprocess
                import platform
                
                output_path = result['output_file']
                if platform.system() == "Windows":
                    os.startfile(output_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", output_path])
                else:  # Linux
                    subprocess.run(["xdg-open", output_path])
                print("📂 输出文件已自动打开")
            except Exception as e:
                print(f"⚠️  无法自动打开文件: {e}")
            
            return True
        else:
            print(f"❌ 处理失败: {result['message']}")
            if 'errors' in result:
                for error in result['errors']:
                    print(f"   • {error}")
            return False
            
    except Exception as e:
        print(f"❌ 处理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def 主程序():
    """主程序入口"""
    print("🚀 扣款失败信息处理工具 - 命令行版本")
    print("=" * 60)
    print("📋 功能说明：")
    print("   • 处理扣款失败信息Excel文件")
    print("   • 自动处理贷后BP字段逻辑")
    print("   • 格式化应还款金额为数字格式")
    print("   • 创建透视表，按直营中心、团队、业务经理、客户姓名分组")
    print("   • 智能排序：按团队和业务经理的去重客户数量排序")
    print("   • 专业表格样式：条件格式、千分位分隔符")
    print("   • 输出文件：保存到exe文件所在目录，带时间戳命名")
    print("=" * 60)
    
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("💡 使用方法:")
        print("   方式1: 直接拖拽Excel文件到exe文件上")
        print("   方式2: 将Excel文件拖拽到此终端窗口")
        print("   方式3: python excel_processor_cli.py <Excel文件路径>")
        
        # 等待用户拖拽文件或输入
        print("\n📁 请将Excel文件拖拽到终端窗口，然后按回车键开始处理...")
        print("💡 提示：拖拽文件后，路径会显示在终端中，此时按回车键即可开始处理")
        try:
            user_input = input().strip()
            if user_input:
                # 处理拖拽的文件路径（去除引号）
                文件路径 = user_input.strip('"').strip("'")
                print(f"📂 检测到文件路径: {文件路径}")
                print("⏳ 开始处理文件...")
                
                # 检查文件是否存在
                if not os.path.exists(文件路径):
                    print(f"❌ 文件不存在: {文件路径}")
                    try:
                        input("按回车键退出...")
                    except (EOFError, RuntimeError):
                        time.sleep(3)
                    return
                
                # 检查文件扩展名
                if not 文件路径.lower().endswith(('.xlsx', '.xls')):
                    print(f"❌ 不支持的文件格式: {文件路径}")
                    print("   请使用 .xlsx 或 .xls 格式的Excel文件")
                    try:
                        input("按回车键退出...")
                    except (EOFError, RuntimeError):
                        time.sleep(3)
                    return
                
                print(f"✅ 开始处理文件: {文件路径}")
                # 处理文件
                if 处理Excel文件(文件路径):
                    print("\n🎉 文件处理完成！")
                    print("⏰ 5秒后自动关闭终端...")
                    time.sleep(5)
                else:
                    print("\n❌ 文件处理失败！")
                    try:
                        input("按回车键退出...")
                    except (EOFError, RuntimeError):
                        time.sleep(3)
            else:
                print("👋 程序退出")
        except (EOFError, RuntimeError):
            time.sleep(3)
        return
    
    文件路径 = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(文件路径):
        print(f"❌ 文件不存在: {文件路径}")
        try:
            input("按回车键退出...")
        except (EOFError, RuntimeError):
            time.sleep(3)
        return
    
    # 检查文件扩展名
    if not 文件路径.lower().endswith(('.xlsx', '.xls')):
        print(f"❌ 不支持的文件格式: {文件路径}")
        print("   请使用 .xlsx 或 .xls 格式的Excel文件")
        try:
            input("按回车键退出...")
        except (EOFError, RuntimeError):
            time.sleep(3)
        return
    
    # 处理文件
    if 处理Excel文件(文件路径):
        print("\n🎉 文件处理完成！")
        print("⏰ 5秒后自动关闭终端...")
        time.sleep(5)
    else:
        print("\n❌ 文件处理失败！")
        # 失败时等待用户确认
        try:
            input("\n按回车键退出...")
        except (EOFError, RuntimeError):
            time.sleep(3)

if __name__ == "__main__":
    主程序()
