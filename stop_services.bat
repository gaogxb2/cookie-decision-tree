@echo off
echo 正在停止决策树编辑器服务...

echo.
echo 查找并终止 Python 进程（后端）...
tasklist | findstr python >nul
if %errorlevel% equ 0 (
    echo 找到 Python 进程，正在终止...
    taskkill /f /im python.exe
    echo [OK] Python 进程已终止
) else (
    echo [INFO] 未找到运行中的 Python 进程
)

echo.
echo 查找并终止 Node.js 进程（前端）...
tasklist | findstr node >nul
if %errorlevel% equ 0 (
    echo 找到 Node.js 进程，正在终止...
    taskkill /f /im node.exe
    echo [OK] Node.js 进程已终止
) else (
    echo [INFO] 未找到运行中的 Node.js 进程
)

echo.
echo 检查端口占用情况：
echo 端口 5000（后端）：
netstat -ano | findstr :5000
echo.
echo 端口 3000（前端）：
netstat -ano | findstr :3000

echo.
echo  服务停止完成！
pause 