#!/bin/sh  
# 群晖DSM Docker状态检查脚本

echo "========================================="
echo "  扣款失败信息处理工具 - Docker状态检查"
echo "========================================="

# 检查Docker服务
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ Docker未安装"
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker服务未启动"
    exit 1
fi

echo "✅ Docker服务正常"
echo ""

# 检查镜像
echo "🐳 Docker镜像:"
if docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}" | grep -E "(REPOSITORY|excel-processor)"; then
    echo ""
else
    echo "   未找到excel-processor镜像"
    echo ""
fi

# 检查容器状态
echo "📦 容器状态:"
if docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(NAMES|excel-processor)"; then
    
    # 详细容器信息
    if docker ps --format '{{.Names}}' | grep -q "excel-processor-dsm"; then
        CONTAINER_ID=$(docker ps --format '{{.ID}}' --filter name=excel-processor-dsm)
        
        echo ""
        echo "📊 容器详细信息:"
        echo "   容器ID: $CONTAINER_ID"
        
        # CPU和内存使用
        docker stats --no-stream --format "   CPU使用: {{.CPUPerc}}, 内存使用: {{.MemUsage}}" excel-processor-dsm 2>/dev/null
        
        # 启动时间
        START_TIME=$(docker inspect -f '{{.State.StartedAt}}' excel-processor-dsm 2>/dev/null)
        echo "   启动时间: $START_TIME"
        
        # 健康检查
        echo ""
        echo "🩺 健康检查:"
        if curl -f "http://localhost:4009/health" >/dev/null 2>&1; then
            echo "   ✅ 应用响应正常"
            # 获取健康状态详情
            HEALTH_INFO=$(curl -s "http://localhost:4009/health" 2>/dev/null)
            if [ -n "$HEALTH_INFO" ]; then
                echo "   📋 健康状态: $HEALTH_INFO"
            fi
        else
            echo "   ❌ 应用无响应"
        fi
        
        # 网络信息
        echo ""
        echo "🌐 网络访问:"
        echo "   本地: http://localhost:4009"
        
        # 获取群晖内网IP
        INTERNAL_IP=$(ip route get 1 | awk '{print $NF;exit}' 2>/dev/null)
        if [ -n "$INTERNAL_IP" ]; then
            echo "   内网: http://$INTERNAL_IP:4009"
        fi
        
        # 端口检查
        if netstat -ln 2>/dev/null | grep -q ":4009 "; then
            echo "   ✅ 端口4009已监听"
        else
            echo "   ⚠️  端口4009可能未正确映射"
        fi
    fi
else
    echo "   未找到excel-processor容器"
fi

echo ""
echo "📁 数据目录状态:"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"  
DIR="$(dirname "$SCRIPT_DIR")"

for dir_name in uploads output logs; do
    dir_path="$DIR/$dir_name"
    if [ -d "$dir_path" ]; then
        file_count=$(find "$dir_path" -type f | wc -l)
        dir_size=$(du -sh "$dir_path" 2>/dev/null | awk '{print $1}')
        echo "   $dir_name/: $file_count 个文件, $dir_size"
    else
        echo "   $dir_name/: 目录不存在"
    fi
done

echo ""
echo "🔧 管理命令:"
echo "   启动Docker: $SCRIPT_DIR/docker-start.sh"
echo "   停止Docker: $SCRIPT_DIR/docker-stop.sh" 
echo "   Python版本: $SCRIPT_DIR/start.sh"
echo "   查看日志: docker logs excel-processor-dsm"
