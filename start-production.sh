#!/bin/bash
# 生产环境启动脚本 - 适合服务器部署
# 使用Gunicorn提供更好的性能和稳定性

echo "=========================================="
echo "  扣款失败信息处理工具 - 生产环境启动"
echo "=========================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    exit 1
fi

echo "✅ Python环境检查通过"

# 检查依赖
echo "📦 检查Python依赖..."
python3 -c "import flask, pandas, openpyxl, gunicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  安装缺失的依赖..."
    pip3 install -r requirements.txt
    pip3 install gunicorn
fi

echo "✅ 依赖检查完成"

# 创建必要目录
mkdir -p uploads output logs
echo "✅ 目录结构确认"

# 设置环境变量
export FLASK_ENV=production
export PYTHONPATH=$(pwd)

echo ""
echo "🚀 启动生产环境服务..."
echo "📍 访问地址: http://localhost:4009"
echo "📊 配置: 2个worker进程，每个2个线程 (适合小用户量)"
echo "🔧 内存优化: 启用请求回收机制"
echo "⏹️  按 Ctrl+C 停止服务"
echo ""

# 启动Gunicorn (优化配置)
exec gunicorn \
    --workers 2 \
    --threads 2 \
    --bind 0.0.0.0:4009 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    --timeout 300 \
    excel_web:app
