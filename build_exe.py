#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建exe文件的辅助脚本
使用PyInstaller将命令行版本打包成独立的exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def 构建exe():
    """构建exe文件"""
    print("🚀 开始构建exe文件...")
    print("=" * 50)
    
    # 检查PyInstaller是否已安装
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller安装完成")
    
    # 清理之前的构建文件
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("🧹 清理旧的build目录")
    
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        print("🧹 清理旧的dist目录")
    
    # 使用spec文件构建（更精确的配置）
    if os.path.exists("excel_processor_cli.spec"):
        print("✅ 使用现有spec文件进行构建")
        cmd = ["pyinstaller", "excel_processor_cli.spec"]
    else:
        # 备用的直接构建命令
        cmd = [
            "pyinstaller",
            "--onefile",  # 单文件模式
            "--console",  # 显示控制台
            "--name", "扣款失败信息处理工具",
            "--strip",    # 去除符号信息，减小体积
            "--noupx",    # 禁用UPX压缩（加快构建速度）
            "--hidden-import", "pandas",
            "--hidden-import", "openpyxl",
            "--hidden-import", "pypinyin",
            # 排除Web相关模块以减少构建时间和大小
            "--exclude-module", "flask",
            "--exclude-module", "werkzeug", 
            "--exclude-module", "jinja2",
            "--exclude-module", "click",
            "--exclude-module", "itsdangerous",
            "--exclude-module", "markupsafe",
            "excel_processor_cli.py"
        ]
    
    # 添加图标（如果存在）
    if os.path.exists("icon.ico"):
        cmd.extend(["--icon", "icon.ico"])
    
    print("📦 执行构建命令:")
    print(" ".join(cmd))
    print()
    
    try:
        # 执行构建
        result = subprocess.run(cmd, check=True)
        print("\n✅ exe文件构建成功！")
        
        # 检查生成的文件
        exe_path = Path("dist/扣款失败信息处理工具.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📄 生成的文件: {exe_path}")
            print(f"📊 文件大小: {size_mb:.1f} MB")
            
            # 创建使用说明
            readme_path = Path("dist/使用说明.txt")
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("""扣款失败信息处理工具 - 使用说明

📋 使用方法：
1. 直接将Excel文件拖拽到"扣款失败信息处理工具.exe"上
2. 或者双击exe文件，然后拖拽Excel文件到终端窗口

📄 支持的文件格式：
• .xlsx (Excel 2007+)
• .xls (Excel 97-2003)

📊 处理功能：
• 自动创建数据透视表
• 按直营中心、团队、业务经理分组
• 智能排序和格式化
• 专业表格样式

📁 输出：
• 处理后的文件会保存在output目录中
• 文件名包含处理时间戳
• 处理完成后会自动打开结果文件

⚠️ 注意事项：
• 确保Excel文件包含必要的列（应还款金额、所属直营中心、所属团队、所属业务经理、客户姓名）
• 处理大文件时请耐心等待
• 程序会自动清理超过1天的旧文件

💡 如有问题，请联系技术支持
""")
            print(f"📚 使用说明: {readme_path}")
            
        else:
            print("❌ 未找到生成的exe文件")
    
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 构建过程中发生错误: {e}")
        return False
    
    return True

def 创建spec文件():
    """创建PyInstaller spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['excel_processor_cli.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
    ],
    hiddenimports=['pandas', 'openpyxl', 'flask', 'pypinyin'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='扣款失败信息处理工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('excel_processor_cli.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ 已创建 excel_processor_cli.spec 文件")
    print("💡 你也可以使用: pyinstaller excel_processor_cli.spec")

if __name__ == "__main__":
    print("📦 Excel处理工具 - exe构建脚本")
    print("=" * 50)
    
    choice = input("选择操作:\n1. 构建exe文件\n2. 创建spec文件\n3. 两个都执行\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        构建exe()
    elif choice == "2":
        创建spec文件()
    elif choice == "3":
        创建spec文件()
        构建exe()
    else:
        print("❌ 无效选择")
