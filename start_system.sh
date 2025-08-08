#!/bin/bash
echo "启动决策树系统..."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate py310
python api_server.py &
sleep 3
cd web_editor_vue

# 安装前端依赖
echo " 安装前端依赖..."
if [ ! -d "node_modules" ]; then
    echo " 首次安装，正在安装 npm 依赖..."
    npm install
else
    echo "[OK] node_modules 已存在，跳过安装"
fi

npm run dev &
echo "系统启动完成！"
echo "请访问: http://localhost:3000"
wait
