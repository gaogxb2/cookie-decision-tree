@echo off
REM 决策树编辑器启动脚本 (Windows PyCharm版本)
REM 这个脚本可以在PyCharm的终端中运行，使用PyCharm的Python环境

echo 启动决策树编辑器 (PyCharm版本)...

REM 检查是否在PyCharm环境中
echo [INFO] 检测Python环境...
python --version
echo [INFO] Python路径: %PYTHONPATH%
echo [INFO] 当前工作目录: %CD%

REM 检查依赖（使用PyCharm的Python环境）
echo [DEBUG] 检查依赖...
python -c "import yaml, openai, requests" 2>nul
if errorlevel 1 (
    echo [WARNING] 缺少依赖包，请在PyCharm中安装：
    echo   pip install pyyaml openai requests
    echo.
    echo 或者使用PyCharm的Package Manager安装依赖
    echo.
    pause
    exit /b 1
) else (
    echo [OK] 依赖检查通过
)

echo.
echo 启动决策树编辑器...
echo 后端将在 http://localhost:5000 启动
echo 前端将在 http://localhost:3000 启动
echo 按 Ctrl+C 停止所有服务

REM 检查前端依赖
echo.
echo 检查前端依赖...
if not exist "web_editor_vue\node_modules" (
    echo [WARNING] 前端依赖未安装
    echo 请在PyCharm终端中运行：
    echo   cd web_editor_vue
    echo   npm install
    echo.
    pause
    exit /b 1
) else (
    echo [OK] 前端依赖已安装
)

REM 启动前端服务器（新窗口）
echo.
echo 启动前端服务器...
echo 前端将在 http://localhost:3000 启动
start "Frontend" cmd /c "cd /d %CD%\web_editor_vue && npm run dev"

REM 等待前端启动
echo 等待前端启动...
timeout /t 3 /nobreak >nul

REM 启动后端服务器（当前窗口，这样可以看到所有print输出）
echo.
echo 启动后端服务器...
echo 后端将在 http://localhost:5000 启动
echo 现在你可以看到所有的print输出了！
echo 按 Ctrl+C 停止后端服务
echo.

REM 在前台启动后端，这样所有的print都会显示
python api_server.py

REM 如果后端停止，显示提示
echo.
echo 后端服务已停止
echo 前端服务仍在后台运行
echo 如需停止前端，请运行 stop_services.bat
echo.
pause 