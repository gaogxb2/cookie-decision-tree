@echo off
chcp 65001 >nul
title 决策树系统安装程序

echo ==========================================
echo 🤖 决策树系统安装程序
echo ==========================================
echo.

:: 检查Python是否可用
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查必要文件
if not exist "installer\installer.py" (
    echo ❌ 未找到安装程序文件
    pause
    exit /b 1
)

:: 安装必要的Python包
echo 📦 检查Python依赖...
pip install tkinter requests >nul 2>&1

:: 运行安装程序
echo 🚀 启动安装程序...
python installer\installer.py

echo.
echo 安装程序已退出
pause 