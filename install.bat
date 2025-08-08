@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==========================================
echo [AI] 决策树可视化编辑器 - Windows安装脚本
echo ==========================================

:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] 检测到管理员权限
) else (
    echo [WARNING] 建议以管理员身份运行此脚本
    pause
)

:: 检查系统要求
echo [INFO] 检查系统环境...

:: 检查是否安装了 Chocolatey
where choco >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] 安装 Chocolatey 包管理器...
    powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    if %errorLevel% neq 0 (
        echo [ERROR] Chocolatey 安装失败
        pause
        exit /b 1
    )
)

:: 安装 Python
echo [INFO] 检查 Python 环境...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] 安装 Python 3.10...
    choco install python --version=3.10.0 -y
    if %errorLevel% neq 0 (
        echo [ERROR] Python 安装失败
        pause
        exit /b 1
    )
    :: 刷新环境变量
    call refreshenv
) else (
    echo [SUCCESS] Python 已安装
)

:: 安装 Node.js
echo [INFO] 检查 Node.js 环境...
node --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] 安装 Node.js...
    choco install nodejs -y
    if %errorLevel% neq 0 (
        echo [ERROR] Node.js 安装失败
        pause
        exit /b 1
    )
    :: 刷新环境变量
    call refreshenv
) else (
    echo [SUCCESS] Node.js 已安装
)

:: 安装 Git
echo [INFO] 检查 Git 环境...
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] 安装 Git...
    choco install git -y
    if %errorLevel% neq 0 (
        echo [ERROR] Git 安装失败
        pause
        exit /b 1
    )
    :: 刷新环境变量
    call refreshenv
) else (
    echo [SUCCESS] Git 已安装
)

:: 安装 Miniconda
echo [INFO] 检查 Conda 环境...
conda --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] 安装 Miniconda...
    choco install miniconda3 -y
    if %errorLevel% neq 0 (
        echo [ERROR] Miniconda 安装失败
        pause
        exit /b 1
    )
    :: 刷新环境变量
    call refreshenv
) else (
    echo [SUCCESS] Conda 已安装
)

:: 设置 Python 环境
echo [INFO] 设置 Python 环境...

:: 创建 conda 环境
conda env list | findstr "py310" >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] 创建 py310 环境...
    conda create -n py310 python=3.10 -y
) else (
    echo [INFO] py310 环境已存在
)

:: 激活环境并安装依赖
echo [INFO] 安装 Python 依赖...
call conda activate py310
pip install -r requirements.txt

:: 设置前端环境
echo [INFO] 设置前端环境...
cd web_editor_vue
call npm install
cd ..

:: 创建启动脚本
echo [INFO] 创建启动脚本...

:: 后端启动脚本
echo @echo off > start_backend.bat
echo echo 启动后端服务器... >> start_backend.bat
echo call conda activate py310 >> start_backend.bat
echo cd /d "%%~dp0" >> start_backend.bat
echo python web_editor/app.py >> start_backend.bat
echo pause >> start_backend.bat

:: 前端启动脚本
echo @echo off > start_frontend.bat
echo echo 启动前端服务器... >> start_frontend.bat
echo cd /d "%%~dp0\web_editor_vue" >> start_frontend.bat
echo call npm run dev >> start_frontend.bat
echo pause >> start_frontend.bat

:: 一键启动脚本
echo @echo off > start_all.bat
echo echo 启动决策树编辑器... >> start_all.bat
echo echo 后端将在 http://localhost:5000 启动 >> start_all.bat
echo echo 前端将在 http://localhost:3001 启动 >> start_all.bat
echo echo. >> start_all.bat
echo echo 按 Ctrl+C 停止所有服务 >> start_all.bat
echo echo. >> start_all.bat
echo start /B start_backend.bat >> start_all.bat
echo timeout /t 3 /nobreak ^>nul >> start_all.bat
echo start /B start_frontend.bat >> start_all.bat
echo pause >> start_all.bat

echo [SUCCESS] 启动脚本创建完成

:: 显示使用说明
echo.
echo ==========================================
echo  安装完成！
echo ==========================================
echo.
echo 启动方式：
echo 1. 一键启动（推荐）：
echo    start_all.bat
echo.
echo 2. 分别启动：
echo    后端：start_backend.bat
echo    前端：start_frontend.bat
echo.
echo 访问地址：
echo 前端界面：http://localhost:3001
echo 后端API：http://localhost:5000
echo.
echo 注意事项：
echo - 确保端口 3001 和 5000 未被占用
echo - 首次启动可能需要较长时间
echo - 如遇问题，请查看控制台错误信息
echo.

pause 