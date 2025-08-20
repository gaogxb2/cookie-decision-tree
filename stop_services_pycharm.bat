@echo off
REM 停止决策树编辑器服务 (Windows PyCharm版本)

echo 正在停止决策树编辑器服务 (PyCharm版本)...

echo.
echo 查找并停止Python后端进程...
tasklist | findstr python.exe >nul
if %errorlevel% equ 0 (
    echo 找到Python进程，正在停止...
    taskkill /f /im python.exe
    echo [OK] Python后端进程已停止
) else (
    echo [INFO] 未找到运行中的Python进程
)

echo.
echo 查找并停止Node前端进程...
tasklist | findstr node.exe >nul
if %errorlevel% equ 0 (
    echo 找到Node进程，正在停止...
    taskkill /f /im node.exe
    echo [OK] Node前端进程已停止
) else (
    echo [INFO] 未找到运行中的Node进程
)

echo.
echo 检查端口占用情况...
netstat -ano | findstr :5000 >nul
if %errorlevel% equ 0 (
    echo [WARNING] 端口5000仍被占用
) else (
    echo [OK] 端口5000已释放
)

netstat -ano | findstr :3000 >nul
if %errorlevel% equ 0 (
    echo [WARNING] 端口3000仍被占用
) else (
    echo [OK] 端口3000已释放
)

echo.
echo 服务停止完成！
echo.
echo 提示：如果使用PyCharm，建议在PyCharm终端中运行此脚本
echo 这样可以确保使用正确的Python环境
echo.
pause 