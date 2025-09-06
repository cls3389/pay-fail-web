# GitHub Actions CI/CD 配置说明

## 概述

本项目已配置了完整的GitHub Actions CI/CD流程，包括：
- 代码测试
- Docker镜像构建
- 自动部署（可选）

## 工作流程

### 1. 测试阶段 (test)
- 使用Python 3.11环境
- 安装项目依赖
- 运行pytest测试
- 执行代码质量检查（flake8）

### 2. Docker构建阶段 (build-docker)
- 构建Docker镜像
- 测试容器启动
- 验证健康检查端点

### 3. 部署阶段 (deploy)
- 仅在main/master分支触发
- 可配置实际部署逻辑

## 配置文件

### GitHub Actions工作流
- `.github/workflows/ci-cd.yml` - 主要CI/CD配置

### Docker相关
- `Dockerfile` - 优化的Docker构建配置
- `.dockerignore` - Docker构建忽略文件

### 测试相关
- `test_app.py` - 基础测试用例
- `requirements.txt` - 包含pytest依赖

## 使用方法

1. **推送代码到GitHub**
   ```bash
   git add .
   git commit -m "添加GitHub Actions配置"
   git push origin main
   ```

2. **查看构建状态**
   - 访问GitHub仓库的Actions标签页
   - 查看工作流执行状态和日志

3. **本地测试**
   ```bash
   # 运行测试
   python -m pytest test_app.py -v
   
   # 构建Docker镜像
   docker build -t excel-processor:latest .
   
   # 测试Docker容器
   docker run -p 4009:4009 excel-processor:latest
   ```

## 故障排除

### 常见问题

1. **构建失败 - 依赖安装问题**
   - 检查requirements.txt中的包版本
   - 确保所有依赖都可以在Ubuntu环境中安装

2. **Docker构建失败**
   - 检查Dockerfile语法
   - 确保所有COPY的文件存在

3. **测试失败**
   - 检查test_app.py中的测试用例
   - 确保应用配置正确

4. **健康检查失败**
   - 确保Flask应用有/health端点
   - 检查应用启动时间是否超过健康检查超时

### 调试步骤

1. **查看GitHub Actions日志**
   - 点击失败的工作流
   - 展开失败的步骤查看详细日志

2. **本地复现问题**
   ```bash
   # 使用相同的Python版本
   python --version  # 应该是3.11
   
   # 安装依赖
   pip install -r requirements.txt
   
   # 运行测试
   python -m pytest -v
   ```

3. **Docker调试**
   ```bash
   # 构建镜像
   docker build -t excel-processor:test .
   
   # 交互式运行容器
   docker run -it --rm excel-processor:test /bin/bash
   ```

## 自定义配置

### 修改Python版本
在`.github/workflows/ci-cd.yml`中修改：
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # 修改为所需版本
```

### 添加环境变量
```yaml
env:
  SECRET_KEY: ${{ secrets.SECRET_KEY }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### 配置部署
在deploy阶段添加实际的部署脚本，例如：
- 推送到Docker Hub
- 部署到云平台（AWS、Azure、GCP）
- 触发服务器更新

## 安全注意事项

1. **敏感信息**
   - 使用GitHub Secrets存储敏感信息
   - 不要在代码中硬编码密码或API密钥

2. **权限控制**
   - 限制工作流的权限范围
   - 使用最小权限原则

3. **依赖安全**
   - 定期更新依赖包
   - 使用安全扫描工具
