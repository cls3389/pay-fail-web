
#!/bin/sh
# 群晖DSM启动脚本 - 扣款失败信息处理工具Web版
# 适配套件中心安装的Python 3.11环境

echo "========================================="
echo "  扣款失败信息处理工具 - 群晖DSM启动"
echo "========================================="

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIR="$(dirname "$SCRIPT_DIR")"  # 项目根目录
PIDFILE="$DIR/run.pid"
LOG="$DIR/logs/gunicorn.log"

echo "项目目录: $DIR"

cd "$DIR" || {
    echo "❌ 无法进入项目目录: $DIR"
    exit 1
}

# 检测群晖套件中心Python 3.11路径
PYTHON_PATHS="/var/packages/Python3.11/target/bin/python3.11 /usr/local/python311/bin/python3.11 /usr/bin/python3.11 /usr/local/bin/python3.11 /opt/bin/python3.11"

PYTHON_CMD=""
for path in $PYTHON_PATHS; do
    if [ -x "$path" ]; then
        VERSION=$($path --version 2>&1 | grep -oE '3\.11\.[0-9]+')
        if [ -n "$VERSION" ]; then
            PYTHON_CMD="$path"
            echo "✅ 找到Python $VERSION: $path"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ 未找到Python 3.11"
    echo "请在套件中心安装Python 3.11"
    exit 1
fi

# 检查gunicorn是否已安装
GUNICORN_CMD=""
PIP_CMD="$PYTHON_CMD -m pip"

# 检查pip
if ! $PYTHON_CMD -m pip --version > /dev/null 2>&1; then
    echo "❌ pip不可用，请确保Python 3.11正确安装"
    exit 1
fi

# 安装/检查依赖
echo "📦 检查Python依赖..."
$PIP_CMD install --user gunicorn flask pandas openpyxl pypinyin > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 依赖检查完成"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 设置PATH以找到gunicorn
HOME_DIR=$(eval echo "~$(whoami)")
export PATH="$HOME_DIR/.local/bin:$PATH"

# 检查是否已运行
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "⚠️  应用已运行，PID=$(cat "$PIDFILE")"
    echo "📍 访问地址: http://$(hostname):4009"
    exit 0
fi

# 创建必要目录
mkdir -p logs uploads output

echo "🚀 启动应用..."

# 使用gunicorn启动应用 - 群晖优化配置
GUNICORN="$HOME_DIR/.local/bin/gunicorn"
if [ ! -x "$GUNICORN" ]; then
    # 如果用户目录没有gunicorn，尝试直接用python -m
    GUNICORN="$PYTHON_CMD -m gunicorn"
fi

# 启动应用（群晖优化：2个worker进程）
nohup $GUNICORN \
    --workers 2 \
    --threads 2 \
    --bind 0.0.0.0:4009 \
    --timeout 300 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile "$LOG" \
    --error-logfile "$LOG" \
    --log-level info \
    --daemon \
    --pid "$PIDFILE" \
    --pythonpath "$DIR" \
    excel_web:app

# 检查启动是否成功
sleep 3
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "✅ 应用启动成功，PID=$(cat "$PIDFILE")"
    echo "📍 访问地址: http://$(hostname):4009"
    echo "📍 内网访问: http://$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | head -1):4009"
    echo ""
    echo "🔧 管理命令:"
    echo "  停止: $SCRIPT_DIR/stop.sh"
    echo "  查看日志: tail -f $LOG"
else
    echo "❌ 应用启动失败，请检查日志: $LOG"
    exit 1
fi