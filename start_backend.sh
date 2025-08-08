#!/bin/bash

# 后端启动脚本

echo " 启动后端服务器..."

# 切换到py310环境
echo "🔄 切换到py310环境..."
source ~/.bash_profile
conda activate py310

echo "[OK] Python环境: $(python --version)"
echo "[OK] Conda环境: $CONDA_DEFAULT_ENV"

# 检查依赖
echo "[DEBUG] 检查依赖..."
python -c "import yaml, openai, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo " 安装依赖包..."
    pip install pyyaml openai requests
fi

echo "启动决策树API服务器..."
echo "API服务器将在 http://localhost:5000 启动"
python api_server.py 