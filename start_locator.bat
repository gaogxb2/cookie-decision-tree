@echo off
REM 问题定位器启动脚本 (Windows)

echo 🔍 启动问题定位器...

REM 切换到py310环境
echo 🔄 切换到py310环境...
call conda activate py310

echo ✅ Python环境: 
python --version
echo ✅ Conda环境: %CONDA_DEFAULT_ENV%

REM 检查依赖
echo 🔍 检查依赖...
python -c "import yaml" 2>nul
if errorlevel 1 (
    echo 📦 安装依赖包...
    pip install pyyaml
)

echo 启动问题定位器...
echo 在py310环境中运行problem_locator.py
python problem_locator.py

pause 