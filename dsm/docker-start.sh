#!/bin/sh
# 群晖DSM Docker部署脚本 - 一键构建和运行Docker容器

echo "========================================="
echo "  扣款失败信息处理工具 - 群晖Docker部署"
echo "========================================="

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIR="$(dirname "$SCRIPT_DIR")"  # 项目根目录

echo "项目目录: $DIR"

# 检查是否在git仓库中
if [ -d "$DIR/.git" ]; then
    echo "📥 检测到Git仓库"
    
    # 询问是否更新代码
    echo "是否拉取最新代码？(y/N，5秒后自动跳过)"
    read -r -t 5 update_code || update_code="n"
    
    case "$update_code" in
        [yY]|[yY][eE][sS])
            echo "正在拉取最新代码..."
            cd "$DIR" || {
                echo "❌ 无法进入项目目录: $DIR"
                exit 1
            }
            
            # 保存当前更改（如果有）
            if ! git diff-index --quiet HEAD -- 2>/dev/null; then
                echo "⚠️  检测到本地更改，自动保存..."
                git stash push -m "Auto stash before docker deployment $(date)"
            fi
            
            # 拉取最新代码
            if git pull --rebase; then
                echo "✅ 代码更新成功"
            else
                echo "❌ 代码拉取失败"
                echo "请手动更新代码或检查网络连接"
                echo "继续使用当前版本部署？(y/N)"
                read -r continue_deploy
                case "$continue_deploy" in
                    [yY]|[yY][eE][sS])
                        echo "继续使用当前版本..."
                        ;;
                    *)
                        echo "部署已取消"
                        exit 1
                        ;;
                esac
            fi
            ;;
        *)
            echo "⏭️  跳过代码更新，使用当前版本"
            ;;
    esac
fi

cd "$DIR" || {
    echo "❌ 无法进入项目目录: $DIR"
    exit 1
}

# 检查Docker是否可用
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ Docker未安装或不可用"
    echo "请在群晖套件中心安装Docker"
    exit 1
fi

echo "✅ Docker已安装"

# 检查Docker服务状态
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker服务未启动"
    echo "请启动Docker服务"
    exit 1
fi

echo "✅ Docker服务正常"

# 停止现有容器（如果存在）
if docker ps -a --format '{{.Names}}' | grep -q "excel-processor-dsm"; then
    echo "🛑 停止现有容器..."
    docker stop excel-processor-dsm >/dev/null 2>&1
    docker rm excel-processor-dsm >/dev/null 2>&1
fi

# 创建必要目录
echo "📁 创建数据目录..."
mkdir -p uploads output logs
chmod 755 uploads output logs

# 构建Docker镜像
echo "🔨 构建Docker镜像..."
if docker build -t excel-processor:dsm . >/dev/null 2>&1; then
    echo "✅ 镜像构建成功"
else
    echo "❌ 镜像构建失败，尝试详细输出..."
    docker build -t excel-processor:dsm .
    exit 1
fi

# 运行Docker容器
echo "🚀 启动Docker容器..."
docker run -d \
    --name excel-processor-dsm \
    --restart unless-stopped \
    -p 4009:4009 \
    -v "$DIR/uploads":/app/uploads \
    -v "$DIR/output":/app/output \
    -v "$DIR/logs":/app/logs \
    -e FLASK_ENV=production \
    excel-processor:dsm

# 检查容器启动状态
sleep 5
if docker ps --format '{{.Names}}' | grep -q "excel-processor-dsm"; then
    echo "✅ 容器启动成功"
    
    # 显示访问信息
    echo ""
    echo "📍 访问地址:"
    echo "   本机: http://$(hostname):4009"
    
    # 获取群晖内网IP
    INTERNAL_IP=$(ip route get 1 | awk '{print $NF;exit}' 2>/dev/null)
    if [ -n "$INTERNAL_IP" ]; then
        echo "   内网: http://$INTERNAL_IP:4009"
    fi
    
    echo ""
    echo "🔧 管理命令:"
    echo "   查看状态: docker ps | grep excel-processor"
    echo "   查看日志: docker logs excel-processor-dsm"
    echo "   停止服务: $SCRIPT_DIR/docker-stop.sh"
    echo "   重启服务: docker restart excel-processor-dsm"
    
    # 健康检查
    echo ""
    echo "🩺 健康检查..."
    sleep 10
    if curl -f "http://localhost:4009/health" >/dev/null 2>&1; then
        echo "✅ 应用健康检查通过"
    else
        echo "⚠️  健康检查失败，请查看日志: docker logs excel-processor-dsm"
    fi
    
else
    echo "❌ 容器启动失败"
    echo "检查日志: docker logs excel-processor-dsm"
    exit 1
fi

echo "🎉 Docker部署完成！"
