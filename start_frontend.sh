#!/bin/bash

# 前端启动脚本

echo "启动前端服务器..."

# 切换到py310环境（虽然前端不需要Python，但保持一致性）
echo "🔄 切换到py310环境..."
source ~/.bash_profile
conda activate py310

echo "[OK] Conda环境: $CONDA_DEFAULT_ENV"

echo "启动前端服务器..."
echo "前端将在 http://localhost:3000 启动"

# 安装前端依赖
echo " 安装前端依赖..."
cd web_editor_vue
if [ ! -d "node_modules" ]; then
    echo "首次安装，正在安装 npm 依赖..."
    npm install
else
    echo "[OK] node_modules 已存在，跳过安装"
fi

npm run dev 