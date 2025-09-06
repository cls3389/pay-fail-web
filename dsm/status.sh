#!/bin/sh
# 群晖DSM状态检查脚本 - 扣款失败信息处理工具Web版

echo "========================================="
echo "  扣款失败信息处理工具 - 状态检查"
echo "========================================="

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIR="$(dirname "$SCRIPT_DIR")"  # 项目根目录
PIDFILE="$DIR/run.pid"
LOG="$DIR/logs/gunicorn.log"

echo "项目目录: $DIR"

# 检查PID文件和进程状态
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "✅ 应用正在运行"
        echo "   PID: $PID"
        
        # 显示进程信息
        PROCESS_INFO=$(ps -p "$PID" -o pid,ppid,cmd --no-headers 2>/dev/null)
        if [ -n "$PROCESS_INFO" ]; then
            echo "   进程信息: $PROCESS_INFO"
        fi
        
        # 显示内存使用情况
        MEM_INFO=$(ps -p "$PID" -o pid,rss --no-headers 2>/dev/null | awk '{print $2}')
        if [ -n "$MEM_INFO" ]; then
            MEM_MB=$((MEM_INFO / 1024))
            echo "   内存使用: ${MEM_MB}MB"
        fi
        
        # 显示启动时间
        if command -v stat >/dev/null 2>&1; then
            START_TIME=$(stat -c %Y "$PIDFILE" 2>/dev/null)
            if [ -n "$START_TIME" ]; then
                echo "   启动时间: $(date -d @$START_TIME 2>/dev/null || date -r $START_TIME 2>/dev/null)"
            fi
        fi
        
        echo ""
        echo "📍 访问地址:"
        echo "   本机: http://$(hostname):4009"
        INTERNAL_IP=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | head -1)
        if [ -n "$INTERNAL_IP" ]; then
            echo "   内网: http://$INTERNAL_IP:4009"
        fi
        
        # 测试端口连通性
        if command -v nc >/dev/null 2>&1; then
            if nc -z localhost 4009 2>/dev/null; then
                echo "   端口状态: ✅ 4009端口可访问"
            else
                echo "   端口状态: ❌ 4009端口无响应"
            fi
        elif command -v netstat >/dev/null 2>&1; then
            if netstat -ln | grep ":4009 " >/dev/null 2>&1; then
                echo "   端口状态: ✅ 4009端口正在监听"
            else
                echo "   端口状态: ❌ 4009端口未监听"
            fi
        fi
        
    else
        echo "❌ PID文件存在但进程已停止"
        echo "   PID文件: $PIDFILE (包含PID: $PID)"
        echo "   建议运行: $SCRIPT_DIR/start.sh"
        rm -f "$PIDFILE" 2>/dev/null && echo "   已清理无效PID文件"
    fi
else
    echo "❌ 应用未运行"
    echo "   未找到PID文件: $PIDFILE"
    echo "   启动命令: $SCRIPT_DIR/start.sh"
fi

echo ""

# 显示日志信息
if [ -f "$LOG" ]; then
    echo "📋 最近日志 (最后10行):"
    echo "----------------------------------------"
    tail -n 10 "$LOG" 2>/dev/null || echo "无法读取日志文件"
    echo "----------------------------------------"
    echo "完整日志: tail -f $LOG"
else
    echo "📋 日志文件不存在: $LOG"
fi

echo ""

# 显示文件统计
echo "📊 文件统计:"
for dir in uploads output logs; do
    if [ -d "$DIR/$dir" ]; then
        count=$(find "$DIR/$dir" -type f | wc -l)
        size=$(du -sh "$DIR/$dir" 2>/dev/null | awk '{print $1}')
        echo "   $dir/: $count 个文件, $size"
    else
        echo "   $dir/: 目录不存在"
    fi
done

echo ""
echo "🔧 管理命令:"
echo "   启动: $SCRIPT_DIR/start.sh"
echo "   停止: $SCRIPT_DIR/stop.sh"
echo "   状态: $SCRIPT_DIR/status.sh"
echo "   日志: tail -f $LOG"
