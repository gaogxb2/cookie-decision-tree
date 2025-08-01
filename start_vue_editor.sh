#!/bin/bash

# Vue编辑器启动脚本

echo "🚀 启动Vue编辑器..."

# 切换到py310环境
echo "🔄 切换到py310环境..."
source ~/.bash_profile
conda activate py310

echo "✅ Python环境: $(python --version)"
echo "✅ Conda环境: $CONDA_DEFAULT_ENV"

# 检查依赖
echo "🔍 检查依赖..."
python -c "import yaml, openai, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装依赖包..."
    pip install pyyaml openai requests
fi

echo "启动Vue编辑器..."
echo "编辑器将在 http://localhost:3000 启动"
echo "API服务器将在 http://localhost:5000 启动"

# 启动后端
echo "启动后端服务器..."
python api_server.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
echo "启动前端服务器..."
cd web_editor_vue && npm run dev &
FRONTEND_PID=$!

# 等待用户中断
echo "按 Ctrl+C 停止所有服务"
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait 