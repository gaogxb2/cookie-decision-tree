@echo off
REM 决策树编辑器启动脚本 (Windows)

echo 启动决策树编辑器...

REM 切换到py310环境
echo 切换到py310环境...
call conda activate py310

echo [OK] Python环境: 
python --version
echo [OK] Conda环境: %CONDA_DEFAULT_ENV%

REM 检查依赖
echo [DEBUG] 检查依赖...
python -c "import yaml, openai, requests" 2>nul
if errorlevel 1 (
    echo 安装依赖包...
    pip install pyyaml openai requests
)

echo 启动决策树编辑器...
echo 后端将在 http://localhost:5000 启动
echo 前端将在 http://localhost:3000 启动
echo 按 Ctrl+C 停止所有服务

REM 安装前端依赖
echo 安装前端依赖...
cd web_editor_vue
if not exist "node_modules" (
    echo 首次安装，正在安装 npm 依赖...
    call npm install
) else (
    echo [OK] node_modules 已存在，跳过安装
)

REM 启动前端服务器（后台运行）
echo 启动前端服务器...
echo 前端将在 http://localhost:3000 启动
start "Frontend" cmd /c "npm run dev"

REM 返回根目录
cd ..

REM 等待一下前端启动
echo 等待前端启动...
timeout /t 3 /nobreak >nul

REM 启动后端服务器（前台运行，这样可以看到所有print输出）
echo 启动后端服务器...
echo 后端将在 http://localhost:5000 启动
echo 现在你可以看到所有的print输出了！
echo 按 Ctrl+C 停止所有服务

REM 在前台启动后端，这样所有的print都会显示
python api_server.py

REM 如果后端停止，显示提示
echo.
echo 后端服务已停止
echo 前端服务仍在后台运行
echo 如需停止前端，请运行 stop_services.bat
echo.
pause 