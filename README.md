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

## 前置要求

### 系统要求
- **操作系统**: Windows 10/11、macOS、Linux、群晖NAS (DSM 7.0+)
- **网络**: 能访问GitHub和Docker Hub的网络环境
- **硬件**: 至少1GB内存，500MB存储空间

### 软件要求（根据部署方式选择）

#### Docker部署（推荐，适合所有用户）
- **Docker**: 最新版本的Docker Desktop (Windows/Mac) 或 Docker Engine (Linux)
- **获取方式**: 
  - Windows/Mac: [Docker官网下载Docker Desktop](https://www.docker.com/products/docker-desktop)
  - 群晖: 套件中心搜索"Docker"安装
  - Linux: `curl -fsSL https://get.docker.com | sh`

#### Python直接部署（适合开发者）
- **Python**: 3.11版本 (不支持其他版本)
- **获取方式**: [Python官网下载](https://www.python.org/downloads/)

#### Git（代码管理，可选）
- 用于获取最新代码和接收更新
- **获取方式**: [Git官网下载](https://git-scm.com/downloads)

---

## 快速开始

> 💡 **新手建议**: 如果是第一次使用，推荐按顺序阅读每个部署方式，选择最适合你的方案。

### 使用Docker (推荐)

#### 方式1：使用预构建镜像（推荐给新手）

> 🎯 **适合人群**: 不想折腾，直接使用的用户  
> ⏰ **部署时间**: 3-5分钟  
> 📦 **镜像大小**: ~200MB  

**第一步：创建工作目录**
```bash
# Windows用户在CMD或PowerShell中执行：
mkdir excel-processor
cd excel-processor
mkdir uploads
mkdir output  
mkdir logs

# macOS/Linux用户在终端中执行：
mkdir excel-processor
cd excel-processor
mkdir -p uploads output logs
```

**第二步：拉取并运行镜像**
```bash
# Linux/macOS用户执行：
docker run -d \
  -p 4009:4009 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  --name excel-processor \
  --restart unless-stopped \
  ghcr.io/cls3389/koukuanshibai-web:latest

# Windows用户执行：
docker run -d -p 4009:4009 -v %cd%/uploads:/app/uploads -v %cd%/output:/app/output -v %cd%/logs:/app/logs --name excel-processor --restart unless-stopped ghcr.io/cls3389/koukuanshibai-web:latest
```

**第三步：验证部署**
```bash
# 1. 检查容器是否运行
docker ps

# 2. 检查应用健康状态  
curl http://localhost:4009/health
# 如果没有curl，直接在浏览器打开：http://localhost:4009/health

# 3. 访问应用界面
# 在浏览器输入：http://localhost:4009
```

**说明解释**:
- `-d`: 后台运行容器
- `-p 4009:4009`: 将容器4009端口映射到本机4009端口
- `-v`: 挂载目录，让容器能访问本机文件
- `--restart unless-stopped`: 开机自启动

#### 方式2：使用Docker Compose（推荐给熟悉命令行的用户）

> 🎯 **适合人群**: 需要自定义配置，或想了解项目结构的用户  
> ⏰ **部署时间**: 5-10分钟  
> 📁 **需要**: 下载项目源码  

**第一步：获取项目源码**
```bash
# 使用Git克隆（推荐）
git clone https://github.com/cls3389/koukuanshibai-web.git
cd koukuanshibai-web

# 或者手动下载：
# 1. 访问 https://github.com/cls3389/koukuanshibai-web
# 2. 点击绿色"Code"按钮 → "Download ZIP"  
# 3. 解压到任意目录，进入该目录
```

**第二步：启动服务**
```bash
# 一键启动（会自动创建必要目录）
docker-compose up -d

# 上面命令做了什么：
# 1. 自动创建uploads、output、logs目录
# 2. 构建或拉取Docker镜像
# 3. 启动Web服务
# 4. 配置健康检查
```

**第三步：验证和管理**
```bash
# 查看服务状态
docker-compose ps

# 查看实时日志
docker-compose logs -f
# (按Ctrl+C退出日志查看)

# 访问应用：http://localhost:4009

# 停止服务  
docker-compose down

# 重启服务
docker-compose restart
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
  --name excel-processor-web \
  --restart unless-stopped \
  excel-processor:local

# 6. 验证运行状态
docker ps | grep excel-processor
curl http://localhost:4009/health

# 7. 查看日志
docker logs excel-processor-web

# 8. 停止和清理
docker stop excel-processor-web
docker rm excel-processor-web
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
  --name excel-processor-web ^
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
docker logs excel-processor-web

# 进入容器调试
docker exec -it excel-processor-web sh

# 检查健康状态
curl -v http://localhost:4009/health
```

### 群晖NAS部署（详细教程）

> 🏠 **适合人群**: 群晖NAS用户，想在家庭网络内部署  
> ⚙️ **前置条件**: 群晖DSM 7.0+，开启SSH服务  
> 📺 **访问方式**: 局域网内所有设备都能访问  

#### 准备工作（必读！）

**第一步：开启SSH服务**
1. 登录群晖管理界面
2. 控制面板 → 终端机和SNMP
3. 勾选"启动SSH功能"，端口保持22
4. 点击应用

**第二步：安装必要套件**
```
套件中心搜索并安装：
- Docker（推荐方式1需要）
- Python 3.11（推荐方式2需要）  
- Git Server（可选，用于代码管理）
```

#### 方式1：Docker部署（推荐）

> 🎯 **适合**: 不想安装Python环境的用户  
> 🔧 **管理**: 图形界面管理，重启自启动  

**第一步：SSH连接群晖**
```bash
# 替换your-nas-ip为你的群晖IP地址
# 例如：ssh admin@192.168.1.100
ssh admin@your-nas-ip

# 输入管理员密码后进入命令行
```

**第二步：获取项目代码**
```bash
# 建议在homes目录下操作
cd /volume1/homes/admin

# 首次部署：下载项目代码
git clone https://github.com/cls3389/koukuanshibai-web.git
cd koukuanshibai-web

# 查看项目文件
ls -la
# 应该看到dsm文件夹和各种配置文件
```

**第三步：Docker一键部署**
```bash
# 运行部署脚本
./dsm/docker-start.sh

# 脚本会询问：是否拉取最新代码？(y/N，5秒后自动跳过)
# 新手建议：直接按回车跳过，使用当前代码

# 等待看到：✅ 容器启动成功
# 和显示的访问地址
```

**第四步：验证部署**
```bash
# 查看详细状态
./dsm/docker-status.sh

# 应该看到：
# ✅ Docker服务正常
# ✅ 应用响应正常
# 🌐 网络访问: http://your-nas-ip:4009
```

#### 方式2：Python直接部署

> 🎯 **适合**: 熟悉Python的用户  
> 🔧 **特点**: 直接运行，资源占用更少  

**准备：安装Python 3.11**
- 套件中心搜索"Python 3.11"安装
- 等待安装完成（约5-10分钟）

**部署步骤：**
```bash
# 连接SSH
ssh admin@your-nas-ip
cd /volume1/homes/admin

# 下载代码（如果没有的话）
git clone https://github.com/cls3389/koukuanshibai-web.git
cd koukuanshibai-web

# Python部署
./dsm/start.sh

# 等待看到：✅ 应用启动成功
# 查看状态
./dsm/status.sh

# 停止服务（需要时）
./dsm/stop.sh
```

#### 常见问题解决

**问题1：SSH连接失败**
```
解决方案：
1. 确认群晖IP地址正确
2. 确认SSH服务已开启
3. 检查防火墙设置
4. 尝试用admin用户名登录
```

**问题2：Docker服务未启动**
```
解决方案：
1. 群晖管理界面 → 套件中心
2. 找到Docker，点击运行
3. 等待启动完成再重试
```

**问题3：端口4009无法访问**
```
解决方案：
1. 群晖管理界面 → 控制面板 → 安全性
2. 防火墙 → 编辑规则
3. 添加4009端口允许访问
```

**问题4：Python版本不对**
```bash
# 检查Python版本
python3.11 --version
# 应该显示Python 3.11.x

# 如果没有，重新安装Python 3.11套件
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
docker pull ghcr.io/cls3389/koukuanshibai-web:latest

# 运行
docker run -d -p 4009:4009 ghcr.io/cls3389/koukuanshibai-web:latest

# 带数据卷运行（推荐）
docker run -d \
  --name excel-processor \
  -p 4009:4009 \
  -v ./uploads:/app/uploads \
  -v ./output:/app/output \
  -v ./logs:/app/logs \
  ghcr.io/cls3389/koukuanshibai-web:latest
```

## 项目说明

### 项目特点
- **Web版本**: 用于服务器部署，支持多用户在线使用，基于Flask + Docker

### 技术特点
- 基于Flask框架的现代Web应用
- Docker容器化部署，支持跨平台
- 自动化CI/CD流程，支持多CPU架构
- 智能文件清理，自动维护存储空间

## 许可证

MIT License

## 常见问题FAQ

### 部署相关

**Q1: 我是完全的小白，应该选择哪种部署方式？**
A: 推荐使用"方式1：使用预构建镜像"，只需要安装Docker Desktop，然后复制粘贴几行命令就能运行。

**Q2: Windows/Mac如何安装Docker？**
A: 
- 访问 https://www.docker.com/products/docker-desktop
- 下载Docker Desktop for Windows/Mac
- 双击安装，按提示完成
- 安装后重启电脑，看到Docker图标启动即可

**Q3: 如何知道部署成功了？**
A: 
- 在浏览器输入 http://localhost:4009
- 看到Excel上传界面就说明成功了
- 或者运行 `curl http://localhost:4009/health` 返回健康状态

**Q4: 端口4009被占用怎么办？**
A: 修改端口映射，例如改为4010：
```bash
# 将 -p 4009:4009 改为 -p 4010:4009
docker run -d -p 4010:4009 ...
# 然后访问 http://localhost:4010
```

### 功能使用

**Q5: 支持什么格式的Excel文件？**
A: 支持 .xlsx 和 .xls 格式，文件大小限制16MB。

**Q6: 必须包含哪些列？**
A: 必须包含：应还款金额、所属直营中心、所属团队、所属业务经理、客户姓名

**Q7: 处理后的文件在哪里？**
A: 
- Docker部署：在你创建的 `output` 文件夹内
- 网页界面：处理完成后点击下载链接

**Q8: 文件会被自动删除吗？**
A: 是的，超过1天的处理文件会自动清理，节省存储空间。

### 故障排除

**Q9: Docker容器启动失败怎么办？**
A:
```bash
# 查看错误日志
docker logs excel-processor

# 检查端口是否被占用
netstat -an | grep 4009

# 重新启动容器
docker restart excel-processor
```

**Q10: 群晖NAS无法访问4009端口？**
A: 检查群晖防火墙设置，添加4009端口到允许列表。

**Q11: 上传文件后没有反应？**
A: 
- 检查文件格式是否为 .xlsx 或 .xls
- 检查文件大小是否超过16MB
- 确认文件包含所有必需列

## 技术支持

遇到问题？可以通过以下方式获取帮助：

1. **查看日志**: `docker logs excel-processor`
2. **健康检查**: 访问 `http://localhost:4009/health`
3. **重启服务**: `docker restart excel-processor`
4. **GitHub Issues**: 在项目页面提交问题

## 贡献

欢迎提交Issues和Pull Requests！#   G i t H u b   A c t i o n s   T e s t   -   0 9 / 0 6 / 2 0 2 5   2 3 : 3 4 : 1 6 
 
 