# Pay Fail Web - 扣款失败信息处理工具

[![Version](https://img.shields.io/badge/version-v1.0.1-blue.svg)](https://github.com/cls3389/pay-fail-web/releases)
[![Docker](https://img.shields.io/badge/docker-ghcr.io%2Fcls3389%2Fpay--fail--web-blue.svg)](https://github.com/cls3389/pay-fail-web/pkgs/container/pay-fail-web)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

基于Flask的Web应用，支持在线处理Excel文件，自动分析扣款失败信息。

## ✨ 功能特性

- 🌐 **Web界面** - 现代化浏览器操作，支持多用户
- 📊 **Excel处理** - 在线上传和处理扣款失败信息
- 🔍 **智能分析** - 按团队、业务经理分组统计
- 📥 **一键下载** - 处理结果直接下载
- 🐳 **Docker部署** - 一键部署，开箱即用
- 🧹 **自动清理** - 智能清理过期文件

## 🚀 快速开始

### 使用Docker（推荐）

**超轻量级镜像** - 仅150MB，内存占用80MB

```bash
# 拉取镜像
docker pull ghcr.io/cls3389/pay-fail-web:latest

# 运行容器
docker run -d \
  --name pay-fail-web \
  -p 4009:4009 \
  -v ./uploads:/app/uploads \
  -v ./output:/app/output \
  -v ./logs:/app/logs \
  ghcr.io/cls3389/pay-fail-web:latest
```

访问：http://localhost:4009

### 使用Python（开发）

```bash
# 安装依赖
pip install -r requirements.txt

# 创建目录
mkdir -p uploads output logs

# 启动应用
python excel_web.py
```

## 📋 使用说明

1. **上传文件** - 选择Excel文件（.xlsx/.xls）
2. **预览数据** - 查看处理结果预览
3. **下载结果** - 获取完整的Excel文件

### 必需列
- 应还款金额
- 所属直营中心
- 所属团队
- 所属业务经理
- 客户姓名

## 🔧 配置选项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| 端口 | 4009 | Web服务端口 |
| 文件大小 | 16MB | 最大上传文件大小 |
| 清理时间 | 1天 | 自动清理过期文件 |

## 📊 性能指标

- **镜像大小**: ~150MB
- **内存占用**: ~80MB
- **并发支持**: 2个worker进程
- **处理速度**: 支持大文件快速处理

## 🛠️ 开发部署

### 本地开发
```bash
git clone https://github.com/cls3389/pay-fail-web.git
cd pay-fail-web
pip install -r requirements.txt
python excel_web.py
```

### 生产部署
```bash
# 使用Docker Compose
docker-compose up -d

# 或直接运行
docker run -d -p 4009:4009 ghcr.io/cls3389/pay-fail-web:latest
```

## 📁 项目结构

```
pay-fail-web/
├── excel_web.py          # Flask应用主文件
├── excel_processor.py    # Excel处理核心逻辑
├── file_cleaner.py       # 自动文件清理
├── config.py             # 应用配置
├── requirements.txt      # Python依赖
├── Dockerfile.github     # Docker镜像配置
└── static/               # 前端资源
    ├── css/
    └── js/
```

## 🔍 故障排除

### 常见问题

**Q: 端口4009被占用？**
```bash
# 使用其他端口
docker run -d -p 4010:4009 ghcr.io/cls3389/pay-fail-web:latest
```

**Q: 文件上传失败？**
- 检查文件格式（仅支持.xlsx/.xls）
- 检查文件大小（限制16MB）
- 确认包含所有必需列

**Q: 容器启动失败？**
```bash
# 查看日志
docker logs excel-processor

# 检查镜像
docker images | grep pay-fail-web
```

## 📞 技术支持

- **GitHub Issues**: [提交问题](https://github.com/cls3389/pay-fail-web/issues)
- **健康检查**: http://localhost:4009/health
- **API文档**: http://localhost:4009/api/stats

## 📋 版本历史

### v1.0.0 (2025-01-27) - 正式发布 🎉

**新功能**
- ✨ 基于Flask的Web应用
- 📊 支持Excel文件在线处理
- 🔍 智能分析扣款失败信息
- 🐳 Docker容器化部署
- 🚀 GitHub Actions CI/CD

**技术特性**
- Python 3.11 + Flask 2.3.3
- Pandas + OpenPyXL数据处理
- Gunicorn多进程并发
- 轻量级Docker镜像（~200MB）
- 内存占用仅80MB

**部署方式**
- Docker镜像：`ghcr.io/cls3389/pay-fail-web:latest`
- 端口：4009
- 健康检查：`/health`

## 📄 许可证

MIT License

---

**🎉 快速开始，一键部署，立即使用！**