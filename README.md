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

```bash
# 克隆项目
git clone https://github.com/your-username/koukuanshibai-web.git
cd koukuanshibai-web

# 使用Docker Compose启动
docker-compose up -d

# 访问应用
# http://localhost:4009
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

- **CI/CD**: 自动测试Python 3.9和3.11
- **Docker Build**: 自动构建Docker镜像并发布到GitHub Container Registry
- **Multi-platform**: 支持AMD64和ARM64架构

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