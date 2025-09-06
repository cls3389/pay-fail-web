#!/bin/sh
# 群晖DSM停止脚本 - 扣款失败信息处理工具Web版

echo "========================================="
echo "  扣款失败信息处理工具 - 群晖DSM停止"
echo "========================================="

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIR="$(dirname "$SCRIPT_DIR")"  # 项目根目录
PIDFILE="$DIR/run.pid"

echo "项目目录: $DIR"

if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "🛑 正在停止应用 (PID: $PID)..."
        
        # 优雅停止
        kill -TERM "$PID"
        
        # 等待进程结束
        for i in $(seq 1 10); do
            if ! kill -0 "$PID" 2>/dev/null; then
                echo "✅ 应用已成功停止"
                rm -f "$PIDFILE"
                exit 0
            fi
            echo "⏳ 等待进程结束... ($i/10)"
            sleep 1
        done
        
        # 如果优雅停止失败，强制停止
        echo "⚠️  优雅停止超时，强制停止..."
        kill -KILL "$PID" 2>/dev/null
        rm -f "$PIDFILE"
        echo "✅ 应用已强制停止"
    else
        echo "⚠️  PID文件存在但进程不存在，清理PID文件"
        rm -f "$PIDFILE"
    fi
else
    echo "ℹ️  应用未运行 (未找到PID文件)"
fi

echo "🏁 停止操作完成"