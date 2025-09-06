#!/bin/sh
# 群晖DSM Docker停止脚本

echo "========================================="
echo "  扣款失败信息处理工具 - 停止Docker容器"
echo "========================================="

# 检查容器是否存在并运行
if docker ps --format '{{.Names}}' | grep -q "excel-processor-dsm"; then
    echo "🛑 正在停止Docker容器..."
    
    # 优雅停止容器
    docker stop excel-processor-dsm
    
    echo "✅ 容器已停止"
    
    # 询问是否删除容器
    echo ""
    echo "是否删除容器？(y/N)"
    read -r response
    
    case "$response" in
        [yY]|[yY][eE][sS])
            docker rm excel-processor-dsm
            echo "✅ 容器已删除"
            ;;
        *)
            echo "ℹ️  容器已保留，可使用 docker start excel-processor-dsm 重新启动"
            ;;
    esac
    
elif docker ps -a --format '{{.Names}}' | grep -q "excel-processor-dsm"; then
    echo "ℹ️  容器已停止"
    
    # 询问是否删除容器
    echo "是否删除已停止的容器？(y/N)"
    read -r response
    
    case "$response" in
        [yY]|[yY][eE][sS])
            docker rm excel-processor-dsm
            echo "✅ 容器已删除"
            ;;
        *)
            echo "ℹ️  容器已保留"
            ;;
    esac
else
    echo "ℹ️  未找到Excel处理器容器"
fi

echo "🏁 操作完成"
