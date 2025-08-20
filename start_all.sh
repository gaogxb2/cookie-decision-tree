#!/bin/bash

# 决策树编辑器启动脚本

echo "启动决策树编辑器..."

# 切换到py310环境
echo "切换到py310环境..."
source ~/.bash_profile
conda activate py310

echo "[OK] Python环境: $(python --version)"
echo "[OK] Conda环境: $CONDA_DEFAULT_ENV"

# 检查依赖
echo "[DEBUG] 检查依赖..."
python -c "import yaml, openai, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "安装依赖包..."
    pip install pyyaml openai requests
fi

echo "启动决策树编辑器..."
echo "后端将在 http://localhost:5000 启动"
echo "前端将在 http://localhost:3000 启动"
echo "按 Ctrl+C 停止所有服务"

# 安装前端依赖
echo "安装前端依赖..."
cd web_editor_vue
if [ ! -d "node_modules" ]; then
    echo "首次安装，正在安装 npm 依赖..."
    npm install
else
    echo "[OK] node_modules 已存在，跳过安装"
fi

# 启动前端服务器（后台运行）
echo "启动前端服务器..."
echo "前端将在 http://localhost:3000 启动"
npm run dev &
FRONTEND_PID=$!

# 返回根目录
cd ..

# 等待一下前端启动
echo "等待前端启动..."
sleep 3

# 启动后端服务器（前台运行，这样可以看到所有print输出）
echo "启动后端服务器..."
echo "后端将在 http://localhost:5000 启动"
echo "现在你可以看到所有的print输出了！"
echo "按 Ctrl+C 停止所有服务"

# 在前台启动后端，这样所有的print都会显示
python api_server.py

# 如果后端停止，清理前端进程
echo "正在停止前端服务..."
kill $FRONTEND_PID 2>/dev/null
echo "所有服务已停止" 