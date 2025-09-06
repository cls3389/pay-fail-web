@echo off
chcp 65001 >nul
echo ==========================================================
echo   扣款失败信息处理工具 - Windows 本地版本
echo ==========================================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

echo 🐍 Python环境正常

REM 安装依赖（如果需要）
echo 📦 检查Python依赖...
python -c "import flask, pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  安装缺失的依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

echo ✅ 依赖包正常

REM 创建目录
if not exist "uploads" mkdir uploads
if not exist "output" mkdir output  
if not exist "logs" mkdir logs

echo 📁 目录结构正常
echo.
echo 🚀 启动应用...
echo 📍 访问地址: http://localhost:4009
echo ⏹️  按 Ctrl+C 停止应用
echo.

REM 启动应用
python start-local.py

pause
