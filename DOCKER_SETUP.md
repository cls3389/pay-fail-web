# Docker镜像构建和发布说明

## 📦 镜像信息

- **镜像地址**: `ghcr.io/cls3389/koukuanshibai-web:latest`
- **仓库地址**: https://github.com/cls3389/koukuanshibai-web/pkgs/container/koukuanshibai-web

## 🔧 权限设置

如果遇到 "installation not allowed to Write organization package" 错误，需要设置包权限：

### 方法1：通过GitHub网页设置
1. 访问 https://github.com/cls3389/koukuanshibai-web/pkgs/container/koukuanshibai-web
2. 点击 "Package settings"
3. 在 "Danger Zone" 部分，点击 "Change visibility"
4. 选择 "Public" 或 "Private" 并确认

### 方法2：通过GitHub CLI设置
```bash
# 设置包为公开
gh api -X PATCH /orgs/cls3389/packages/container/koukuanshibai-web -f visibility=public

# 或者设置为私有
gh api -X PATCH /orgs/cls3389/packages/container/koukuanshibai-web -f visibility=private
```

## 🚀 使用方法

### 拉取镜像
```bash
# 拉取最新版本
docker pull ghcr.io/cls3389/koukuanshibai-web:latest

# 拉取特定版本
docker pull ghcr.io/cls3389/koukuanshibai-web:sha-<commit-hash>
```

### 运行容器
```bash
# 基本运行
docker run -d -p 4009:4009 ghcr.io/cls3389/koukuanshibai-web:latest

# 带数据卷运行
docker run -d -p 4009:4009 \
  -v ./uploads:/app/uploads \
  -v ./output:/app/output \
  -v ./logs:/app/logs \
  ghcr.io/cls3389/koukuanshibai-web:latest
```

### 查看容器状态
```bash
# 查看运行中的容器
docker ps

# 查看容器日志
docker logs <container-id>

# 停止容器
docker stop <container-id>
```

## 🔍 故障排除

### 权限问题
如果遇到权限错误，确保：
1. GitHub Actions有 `packages: write` 权限
2. 包设置为公开或对组织成员可见
3. 使用正确的GITHUB_TOKEN

### 网络问题
如果拉取失败，尝试：
```bash
# 登录到GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_ACTOR --password-stdin

# 然后拉取镜像
docker pull ghcr.io/cls3389/koukuanshibai-web:latest
```

## 📊 镜像标签说明

- `latest`: 主分支的最新版本
- `sha-<hash>`: 特定提交的版本
- 其他标签根据GitHub Actions配置生成

## 🔄 自动更新

每次推送到main分支时，GitHub Actions会自动：
1. 运行测试
2. 构建Docker镜像
3. 推送到GitHub Container Registry
4. 更新latest标签
