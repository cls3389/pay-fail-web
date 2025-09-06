
#!/bin/sh
# 启动 Flask + Gunicorn 后台守护
PATH=/root/.local/bin:$PATH                 # 找到 gunicorn
DIR=/volume2/Cursor/excel/koukuanshibai-web
PIDFILE=$DIR/run.pid
LOG=$DIR/logs/gunicorn.log

cd $DIR
# 如果已存在 PID 且进程还在，就不再重复启动
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "已运行，PID=$(cat "$PIDFILE")"
    exit 0
fi

# 后台启动并把 PID 记下来
nohup gunicorn -w 4 -b 0.0.0.0:4009 excel_web:app > "$LOG" 2>&1 & echo $! > "$PIDFILE"
echo "Flask 已启动，PID=$(cat "$PIDFILE")"