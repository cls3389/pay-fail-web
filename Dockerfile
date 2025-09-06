FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 使用官方镜像源，确保在GitHub Actions中可靠构建
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        gcc g++ curl ca-certificates && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn && \
    apt-get purge -y gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 非 root 用户
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .
RUN mkdir -p uploads output logs && chown -R appuser:appgroup /app

USER appuser
EXPOSE 4009

# 健康检查端点
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:4009/health || exit 1

# 启动命令
CMD ["gunicorn", "-w", "2", "--threads", "2", "--max-requests", "1000", "--max-requests-jitter", "100", "-b", "0.0.0.0:4009", "excel_web:app"]