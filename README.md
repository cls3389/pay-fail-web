# 扣款失败信息处理工具 - Web版本

基于原始Excel处理工具开发的Web应用版本，专为服务器部署和多用户在线使用设计。

## 功能特性

- 🌐 **Web界面**: 现代化的浏览器操作界面，支持多用户同时使用
- 📊 **Excel文件处理**: 在线上传和处理扣款失败信息Excel文件
- 🔍 **数据透视**: 按直营中心、团队、业务经理进行智能分组分析
- 📋 **在线预览**: 实时预览处理结果，无需下载查看
- 📥 **文件下载**: 一键下载完整的Excel处理结果
- 🐳 **Docker部署**: 一键部署到任何支持Docker的服务器
- 🧹 **自动清理**: 自动清理超过1天的处理文件，节省存储空间
- ⚡ **高性能**: 优化的多进程架构，支持并发处理

## 快速开始

### 使用Docker (推荐)

#### 方式1：使用预构建镜像（推荐）
```bash
# 直接使用GitHub自动构建的镜像
docker run -d \
  -p 4009:4009 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  --name excel-processor \
  ghcr.io/cls3389/koukuanshibai-web:latest

# 访问应用
# http://localhost:4009
```

#### 方式2：使用Docker Compose
```bash
# 克隆项目
git clone https://github.com/cls3389/koukuanshibai-web.git
cd koukuanshibai-web

# 启动服务（会自动创建必要目录）
docker-compose up -d

# 访问应用
# http://localhost:4009

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 方式3：本地构建Docker镜像

##### Linux/macOS用户：
```bash
# 1. 克隆项目
git clone https://github.com/cls3389/koukuanshibai-web.git
cd koukuanshibai-web

# 2. 创建必要目录（重要！）
mkdir -p uploads output logs

# 3. 构建镜像
docker build -t excel-processor:local .

# 4. 检查镜像构建成功
docker images | grep excel-processor

# 5. 运行容器
docker run -d \
  -p 4009:4009 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  --name excel-processor-local \
  --restart unless-stopped \
  excel-processor:local

# 6. 验证运行状态
docker ps | grep excel-processor
curl http://localhost:4009/health

# 7. 查看日志
docker logs excel-processor-local

# 8. 停止和清理
docker stop excel-processor-local
docker rm excel-processor-local
```

##### Windows用户（PowerShell/CMD）：
```cmd
# 1. 克隆项目
git clone https://github.com/cls3389/koukuanshibai-web.git
cd koukuanshibai-web

# 2. 创建必要目录
mkdir uploads
mkdir output  
mkdir logs

# 3. 构建镜像
docker build -t excel-processor:local .

# 4. 运行容器
docker run -d ^
  -p 4009:4009 ^
  -v %cd%/uploads:/app/uploads ^
  -v %cd%/output:/app/output ^
  -v %cd%/logs:/app/logs ^
  --name excel-processor-local ^
  --restart unless-stopped ^
  excel-processor:local

# 5. 验证运行
docker ps
curl http://localhost:4009/health

# 访问应用：http://localhost:4009
```

##### 构建参数优化：
```bash
# 加速构建（使用buildkit）
DOCKER_BUILDKIT=1 docker build -t excel-processor:local .

# 多平台构建（需要buildx）
docker buildx build --platform linux/amd64,linux/arm64 -t excel-processor:local .

# 构建时指定代理（国内用户）
docker build --build-arg HTTP_PROXY=http://proxy:8080 -t excel-processor:local .
```

##### 故障排查：
```bash
# 检查构建日志
docker build -t excel-processor:local . 2>&1 | tee build.log

# 检查容器日志
docker logs excel-processor-local

# 进入容器调试
docker exec -it excel-processor-local sh

# 检查健康状态
curl -v http://localhost:4009/health
```

### 群晖NAS部署

#### 方式1：Docker部署（推荐）
```bash
# SSH登录群晖NAS
ssh admin@your-nas-ip

# 确保Docker已安装并启动（套件中心）

# 首次部署：克隆项目
git clone https://github.com/cls3389/koukuanshibai-web.git
cd koukuanshibai-web

# Docker部署（可选择是否更新代码）
./dsm/docker-start.sh
# 脚本会询问是否拉取最新代码，5秒后自动跳过

# 手动更新代码后部署
git pull
./dsm/docker-start.sh

# 查看Docker状态  
./dsm/docker-status.sh

# 停止Docker服务
./dsm/docker-stop.sh

# 访问地址：http://your-nas-ip:4009
```

#### 方式2：Python直接部署
```bash
# SSH登录群晖NAS
ssh admin@your-nas-ip

# 安装Python 3.11（套件中心）
# 然后克隆项目
git clone https://github.com/cls3389/koukuanshibai-web.git
cd koukuanshibai-web

# 使用Python脚本启动
./dsm/start.sh

# 查看状态
./dsm/status.sh

# 停止服务
./dsm/stop.sh

# 访问地址：http://your-nas-ip:4009
```

### 本地开发调试

```bash
# 安装依赖
pip install -r requirements.txt

# 创建必要目录
mkdir -p uploads output logs

# 启动开发服务器
python excel_web.py

# 访问地址
http://localhost:4009
```

## GitHub Actions

项目已配置GitHub Actions自动化流程：

- **Docker CI**: 语法检查、Docker构建测试、容器启动验证
- **Docker Build**: 自动构建Docker镜像并发布到GitHub Container Registry  
- **Multi-platform**: 支持AMD64和ARM64架构 (linux/amd64, linux/arm64)
- **Artifact Attestation**: 镜像构建溯源和安全验证

## API接口

- `GET /` - 首页界面
- `POST /upload` - 文件上传和处理
- `GET /download/<filename>` - 文件下载
- `GET /health` - 健康检查

## 项目结构

```
koukuanshibai-web/
├── .github/workflows/     # GitHub Actions自动化
│   ├── ci.yml            # 持续集成测试
│   └── docker-build.yml  # Docker镜像构建
├── static/               # 前端资源
│   ├── css/              # 样式文件
│   └── js/               # JavaScript文件
├── templates/            # HTML模板
├── dsm/                  # 群晖NAS运行脚本
├── excel_processor.py    # Excel处理核心逻辑
├── excel_web.py         # Flask Web应用入口
├── file_cleaner.py      # 自动文件清理服务
├── config.py            # 应用配置
├── Dockerfile           # Docker镜像配置
├── docker-compose.yml   # Docker编排文件
└── requirements.txt     # Python依赖包
```

## 环境变量

| 变量名 | 默认值 | 说明 |
|-------|--------|------|
| FLASK_PORT | 4009 | 应用监听端口 |
| SECRET_KEY | 随机生成 | Flask密钥 |
| MAX_CONTENT_LENGTH | 16MB | 最大文件大小 |

## 部署

### Docker部署

```bash
# 构建镜像
docker build -t excel-processor .

# 运行容器
docker run -d \
  --name excel-processor-web \
  -p 4009:4009 \
  -v ./uploads:/app/uploads \
  -v ./output:/app/output \
  excel-processor
```

### 从GitHub Container Registry部署

```bash
# 拉取镜像
docker pull ghcr.io/your-username/koukuanshibai-web:latest

# 运行
docker run -d -p 4009:4009 ghcr.io/your-username/koukuanshibai-web:latest
```

## 项目说明

### 版本区别
- **Web版本** (当前项目): 用于服务器部署，支持多用户在线使用
- **本地版本**: 独立的exe可执行文件，适合单机使用

### 技术特点
- 基于Flask框架的现代Web应用
- Docker容器化部署，支持跨平台
- 自动化CI/CD流程，支持多CPU架构
- 智能文件清理，自动维护存储空间

## 许可证

MIT License

## 贡献

欢迎提交Issues和Pull Requests！