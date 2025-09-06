# 🚀 扣款失败信息处理工具 - 部署指南

## 📦 正式镜像信息

- **镜像地址**: `ghcr.io/cls3389/koukuanshibai-web:latest`
- **仓库地址**: https://github.com/cls3389/koukuanshibai-web/pkgs/container/koukuanshibai-web
- **版本**: 1.0.0
- **架构**: linux/amd64
- **镜像大小**: ~150MB（基于Alpine Linux）
- **内存占用**: ~80MB（运行时，2个worker进程）
- **并发能力**: 支持多用户同时处理文件

## 🔧 快速部署

### 方法1：直接运行（推荐）
```bash
# 拉取最新镜像
docker pull ghcr.io/cls3389/koukuanshibai-web:latest

# 运行容器
docker run -d \
  --name excel-processor \
  -p 4009:4009 \
  -v ./uploads:/app/uploads \
  -v ./output:/app/output \
  -v ./logs:/app/logs \
  ghcr.io/cls3389/koukuanshibai-web:latest
```

### 方法2：使用Docker Compose
创建 `docker-compose.yml` 文件：
```yaml
version: '3.8'
services:
  excel-processor:
    image: ghcr.io/cls3389/koukuanshibai-web:latest
    container_name: excel-processor
    ports:
      - "4009:4009"
    volumes:
      - ./uploads:/app/uploads
      - ./output:/app/output
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4009/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

然后运行：
```bash
docker-compose up -d
```

## 🌐 访问应用

部署完成后，访问：
- **主页**: http://localhost:4009
- **健康检查**: http://localhost:4009/health
- **API统计**: http://localhost:4009/api/stats

## 📊 管理命令

### 查看容器状态
```bash
# 查看运行状态
docker ps | grep excel-processor

# 查看容器日志
docker logs excel-processor

# 查看实时日志
docker logs -f excel-processor
```

### 停止和重启
```bash
# 停止容器
docker stop excel-processor

# 启动容器
docker start excel-processor

# 重启容器
docker restart excel-processor

# 删除容器
docker rm excel-processor
```

### 更新镜像
```bash
# 拉取最新镜像
docker pull ghcr.io/cls3389/koukuanshibai-web:latest

# 停止并删除旧容器
docker stop excel-processor
docker rm excel-processor

# 运行新容器
docker run -d \
  --name excel-processor \
  -p 4009:4009 \
  -v ./uploads:/app/uploads \
  -v ./output:/app/output \
  -v ./logs:/app/logs \
  ghcr.io/cls3389/koukuanshibai-web:latest
```

## 🔒 安全配置

### 生产环境建议
1. **使用HTTPS**: 配置反向代理（Nginx/Apache）
2. **防火墙**: 限制4009端口访问
3. **数据备份**: 定期备份uploads和output目录
4. **监控**: 设置健康检查监控

### Nginx反向代理配置
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:4009;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📁 目录结构

```
项目目录/
├── uploads/          # 上传文件目录
├── output/           # 处理结果目录
├── logs/             # 日志文件目录
└── docker-compose.yml # Docker编排文件（可选）
```

## 🔍 故障排除

### 常见问题

**1. 端口被占用**
```bash
# 检查端口占用
netstat -tulpn | grep 4009

# 使用不同端口
docker run -d -p 4010:4009 ghcr.io/cls3389/koukuanshibai-web:latest
```

**2. 权限问题**
```bash
# 创建目录并设置权限
mkdir -p uploads output logs
chmod 755 uploads output logs
```

**3. 容器启动失败**
```bash
# 查看详细日志
docker logs excel-processor

# 检查镜像
docker images | grep koukuanshibai-web
```

**4. 健康检查失败**
```bash
# 手动测试健康检查
curl http://localhost:4009/health

# 检查容器内部
docker exec -it excel-processor curl http://localhost:4009/health
```

## 📈 性能优化

### 资源限制（已优化）
```bash
# 轻量级运行（推荐配置）
docker run -d \
  --name excel-processor \
  --memory="200m" \
  --cpus="0.5" \
  -p 4009:4009 \
  ghcr.io/cls3389/koukuanshibai-web:latest

# 标准运行（支持并发）
docker run -d \
  --name excel-processor \
  --memory="400m" \
  --cpus="1.0" \
  -p 4009:4009 \
  ghcr.io/cls3389/koukuanshibai-web:latest
```

### 环境变量
```bash
# 设置环境变量
docker run -d \
  --name excel-processor \
  -e FLASK_ENV=production \
  -e MAX_CONTENT_LENGTH=16777216 \
  -p 4009:4009 \
  ghcr.io/cls3389/koukuanshibai-web:latest
```

## 🔄 自动更新

### 使用Watchtower自动更新
```bash
# 安装Watchtower
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --interval 3600 \
  excel-processor
```

## 📞 技术支持

- **GitHub Issues**: https://github.com/cls3389/koukuanshibai-web/issues
- **文档**: 查看项目README.md
- **健康检查**: http://localhost:4009/health

## 🎯 功能特性

- ✅ Web界面文件上传
- ✅ Excel文件处理
- ✅ 自动文件清理
- ✅ 健康检查监控
- ✅ Docker容器化部署
- ✅ 自动CI/CD流程
- ✅ 多架构支持

---

**🎉 恭喜！您的扣款失败信息处理工具已成功部署！**
