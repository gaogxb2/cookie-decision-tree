#!/bin/bash

# 决策树编辑器启动脚本

echo "启动决策树编辑器..."

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

echo "启动决策树编辑器..."
echo "后端将在 http://localhost:5000 启动"
echo "前端将在 http://localhost:3000 启动"
echo "按 Ctrl+C 停止所有服务"

# 启动后端服务器
echo "启动后端服务器..."
echo "后端将在 http://localhost:5000 启动"
python api_server.py &
BACKEND_PID=$!

# 安装前端依赖并启动前端服务器
echo " 安装前端依赖..."
cd web_editor_vue
if [ ! -d "node_modules" ]; then
    echo "首次安装，正在安装 npm 依赖..."
    npm install
else
    echo "[OK] node_modules 已存在，跳过安装"
fi

echo "启动前端服务器..."
echo "前端将在 http://localhost:3000 启动"
npm run dev &
FRONTEND_PID=$!

# 等待用户中断
echo "启动决策树API服务器..."
echo "API服务器将在 http://localhost:5000 启动"
wait

# 清理进程
echo "正在停止服务..."
kill $BACKEND_PID 2>/dev/null
kill $FRONTEND_PID 2>/dev/null
echo "服务已停止" 