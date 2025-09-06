FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 1. 写入一条可用源并安装编译工具 → 装 gunicorn → 卸编译工具
RUN echo 'deb http://mirrors.aliyun.com/debian bookworm main non-free contrib' > /etc/apt/sources.list && \
    echo 'deb http://mirrors.aliyun.com/debian-security bookworm-security main' >> /etc/apt/sources.list && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        gcc g++ curl && \
    /usr/local/bin/pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn && \
    apt-get purge -y gcc g++ && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 2. 非 root 用户
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
WORKDIR /app

# 3. 装依赖 + 拷代码
COPY requirements.txt .
RUN /usr/local/bin/pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY . .
RUN mkdir -p uploads output logs && chown -R appuser:appgroup /app

USER appuser
EXPOSE 4009

# 4. 启动 - 优化配置：少量用户场景
CMD ["gunicorn", "-w", "2", "--threads", "2", "--max-requests", "1000", "--max-requests-jitter", "100", "-b", "0.0.0.0:4009", "excel_web:app"]