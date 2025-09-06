#!/bin/sh
# 优雅停止
PIDFILE=/volume2/Cursor/excel/koukuanshibai-web/run.pid
if [ -f "$PIDFILE" ]; then
    kill -TERM "$(cat "$PIDFILE")" && rm -f "$PIDFILE"
    echo "已发送 TERM，等待 worker 退出…"
else
    echo "未找到 PID 文件，可能未运行"
fi