# 发布说明

## v1.0.1 - 修复版本 (2025-09-07)

### 🔧 修复内容
- 修复GitHub Actions Docker测试问题
- 同步程序名称、镜像名称与仓库名称
- 更新所有文档中的镜像地址为 pay-fail-web

## v1.0.0 - 正式发布 (2025-01-27)

### 🎉 新功能

- **Web应用界面** - 基于Flask的现代化Web界面，支持多用户同时使用
- **Excel文件处理** - 支持在线上传和处理扣款失败信息Excel文件
- **智能数据分析** - 自动按团队、业务经理等维度进行分组统计
- **一键下载** - 处理结果可直接下载，支持多种格式
- **Docker容器化** - 完整的Docker支持，一键部署
- **自动文件清理** - 智能清理过期文件，节省存储空间

### 🔧 技术特性

- **Python 3.11** - 使用最新的Python版本
- **Flask 2.3.3** - 轻量级Web框架
- **Pandas + OpenPyXL** - 强大的数据处理能力
- **Gunicorn** - 多进程并发处理，支持高并发
- **Docker镜像** - 基于python:3.11-slim，轻量级设计
- **GitHub Actions** - 完整的CI/CD自动化流程

### 📦 部署信息

- **Docker镜像**: `ghcr.io/cls3389/koukuanshibai-web:latest`
- **端口**: 4009
- **健康检查**: `/health`
- **API统计**: `/api/stats`
- **镜像大小**: ~200MB
- **内存占用**: ~80MB

### 🚀 快速开始

```bash
# 拉取镜像
docker pull ghcr.io/cls3389/koukuanshibai-web:latest

# 运行容器
docker run -d \
  --name koukuanshibai-web \
  -p 4009:4009 \
  ghcr.io/cls3389/koukuanshibai-web:latest

# 访问应用
open http://localhost:4009
```

### 📋 系统要求

- Docker 20.10+
- 内存: 最低128MB，推荐256MB
- 存储: 最低500MB可用空间
- 网络: 需要访问GitHub Container Registry

### 🔒 安全特性

- 动态SECRET_KEY生成
- 文件上传大小限制
- 自动清理临时文件
- 健康检查监控

### 📊 性能指标

- **启动时间**: < 10秒
- **内存占用**: 80MB
- **并发处理**: 支持多用户同时使用
- **文件处理**: 支持大型Excel文件
- **响应时间**: < 100ms (静态页面)

### 🐛 已知问题

- 无

### 🔄 升级说明

这是首个正式版本，无需升级。

### 📞 支持

- **GitHub Issues**: [提交问题](https://github.com/cls3389/koukuanshibai-web/issues)
- **文档**: [README.md](README.md)
- **部署指南**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**感谢使用扣款失败信息处理工具！** 🎉
