#!/bin/bash

# 问题定位器启动脚本

echo "[DEBUG] 启动问题定位器..."

# 切换到py310环境
echo "🔄 切换到py310环境..."
source ~/.bash_profile
conda activate py310

echo "[OK] Python环境: $(python --version)"
echo "[OK] Conda环境: $CONDA_DEFAULT_ENV"

# 检查依赖
echo "[DEBUG] 检查依赖..."
python -c "import yaml" 2>/dev/null
if [ $? -ne 0 ]; then
    echo " 安装依赖包..."
    pip install pyyaml
fi

echo "启动问题定位器..."
echo "在py310环境中运行problem_locator.py"
python problem_locator.py 