#!/bin/bash
# Linux/macOS 本地启动脚本

echo "=========================================="
echo "  扣款失败信息处理工具 - 本地版本"  
echo "=========================================="
echo ""

# 检查Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python未安装"
    exit 1
fi

echo "✅ Python环境: $($PYTHON_CMD --version)"

# 检查依赖
echo "📦 检查Python依赖..."
$PYTHON_CMD -c "import flask, pandas, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  安装缺失的依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

echo "✅ 依赖检查完成"

# 创建目录
mkdir -p uploads output logs
echo "✅ 目录结构确认"

echo ""
echo "🚀 启动应用..."
echo "📍 本地访问: http://localhost:4009"
echo "📍 网络访问: http://$(hostname -I | awk '{print $1}'):4009"
echo "⏹️  按 Ctrl+C 停止应用"
echo ""

# 设置权限
chmod +x start-local.py

# 启动应用
$PYTHON_CMD start-local.py
