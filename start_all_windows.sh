#!/bin/bash

# 决策树编辑器启动脚本 (Windows Git Bash/WSL版本)
# 这个脚本可以在Windows的Git Bash、WSL或PowerShell中运行

echo "启动决策树编辑器 (Windows版本)..."

# 检测操作系统
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "[INFO] 检测到Windows环境 (Git Bash/Cygwin)"
    IS_WINDOWS=true
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    echo "[INFO] 检测到Linux环境 (WSL)"
    IS_WINDOWS=true
else
    echo "[INFO] 检测到其他环境"
    IS_WINDOWS=false
fi

# 检查Python环境
echo "[INFO] 检测Python环境..."
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "[ERROR] 未找到Python，请先安装Python"
    exit 1
fi

echo "[OK] Python版本: $($PYTHON_CMD --version)"
echo "[OK] Python路径: $(which $PYTHON_CMD)"

# 检查conda环境（如果存在）
if command -v conda &> /dev/null; then
    echo "[INFO] 检测到Conda环境"
    if [[ -n "$CONDA_DEFAULT_ENV" ]]; then
        echo "[OK] 当前Conda环境: $CONDA_DEFAULT_ENV"
    else
        echo "[INFO] 未激活Conda环境"
    fi
else
    echo "[INFO] 未检测到Conda，使用系统Python"
fi

# 检查依赖
echo "[DEBUG] 检查依赖..."
$PYTHON_CMD -c "import yaml, openai, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] 缺少依赖包，请安装："
    echo "  pip install pyyaml openai requests flask flask-cors"
    echo ""
    echo "或者使用conda安装："
    echo "  conda install pyyaml requests flask flask-cors"
    echo "  pip install openai"
    echo ""
    read -p "是否现在安装依赖？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在安装依赖..."
        if command -v conda &> /dev/null; then
            conda install -y pyyaml requests flask flask-cors
            pip install openai
        else
            pip install pyyaml openai requests flask flask-cors
        fi
    else
        echo "[ERROR] 依赖包未安装，无法继续"
        exit 1
    fi
else
    echo "[OK] 依赖检查通过"
fi

echo ""
echo "启动决策树编辑器..."
echo "后端将在 http://localhost:5000 启动"
echo "前端将在 http://localhost:3000 启动"
echo "按 Ctrl+C 停止所有服务"

# 检查前端依赖
echo ""
echo "检查前端依赖..."
if [ ! -d "web_editor_vue/node_modules" ]; then
    echo "[WARNING] 前端依赖未安装"
    echo "请在终端中运行："
    echo "  cd web_editor_vue"
    echo "  npm install"
    echo ""
    read -p "是否现在安装前端依赖？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在安装前端依赖..."
        cd web_editor_vue
        npm install
        cd ..
    else
        echo "[ERROR] 前端依赖未安装，无法继续"
        exit 1
    fi
else
    echo "[OK] 前端依赖已安装"
fi

# 启动前端服务器（后台运行）
echo ""
echo "启动前端服务器..."
echo "前端将在 http://localhost:3000 启动"

# 在Windows环境下使用不同的启动方式
if [[ "$IS_WINDOWS" == "true" ]]; then
    # Windows Git Bash/WSL环境
    cd web_editor_vue
    nohup npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    echo "[OK] 前端启动成功，PID: $FRONTEND_PID"
    echo "[INFO] 前端日志保存在: frontend.log"
else
    # 其他环境
    cd web_editor_vue
    npm run dev &
    FRONTEND_PID=$!
    cd ..
fi

# 等待前端启动
echo "等待前端启动..."
sleep 3

# 检查前端是否启动成功
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "[ERROR] 前端启动失败！"
    echo "请检查前端日志: frontend.log"
    exit 1
fi

echo "[OK] 前端启动成功，PID: $FRONTEND_PID"

# 启动后端服务器（前台运行，这样可以看到所有print输出）
echo ""
echo "启动后端服务器..."
echo "后端将在 http://localhost:5000 启动"
echo "现在你可以看到所有的print输出了！"
echo "按 Ctrl+C 停止后端服务"
echo ""

# 在前台启动后端，这样所有的print都会显示
$PYTHON_CMD api_server.py

# 如果后端停止，清理前端进程
echo ""
echo "正在停止前端服务..."
kill $FRONTEND_PID 2>/dev/null
echo "所有服务已停止" 