# 扣款失败信息处理工具 (Excel Web Processor)

一个用于处理扣款失败信息的Web应用，支持Excel文件上传、数据处理、透视分析和结果下载。

## 功能特性

- 📊 **Excel文件处理**: 支持上传和处理扣款失败信息Excel文件
- 🔍 **数据透视**: 按团队、业务经理进行数据汇总分析  
- 📋 **表格预览**: 在线预览处理结果
- 📥 **文件下载**: 导出处理后的Excel文件
- 🐳 **容器化**: 支持Docker部署
- ⚡ **响应式界面**: 现代化Web界面，支持移动端

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

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 创建必要目录
mkdir -p uploads output logs

# 启动应用
python excel_web.py
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
├── .github/workflows/     # GitHub Actions配置
├── static/               # 静态资源 (CSS/JS)
├── templates/            # HTML模板
├── excel_processor.py    # 核心处理逻辑
├── excel_web.py         # Flask Web应用
├── config.py            # 应用配置
├── Dockerfile           # Docker镜像配置
├── docker-compose.yml   # Docker编排
├── requirements.txt     # Python依赖
└── README.md           # 项目说明
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

## 开发

```bash
# 安装开发依赖
pip install -r requirements.txt

# 启动开发服务器
export FLASK_ENV=development
python excel_web.py
```

## 许可证

MIT License

## 贡献

欢迎提交Issues和Pull Requests！