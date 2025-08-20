#!/bin/bash

# 停止决策树编辑器服务 (Windows Git Bash/WSL版本)

echo "正在停止决策树编辑器服务 (Windows版本)..."

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

echo ""
echo "查找并停止Python后端进程..."

# 查找Python进程
PYTHON_PIDS=$(pgrep -f "python.*api_server.py" 2>/dev/null || echo "")
if [[ -n "$PYTHON_PIDS" ]]; then
    echo "找到Python后端进程，正在停止..."
    for pid in $PYTHON_PIDS; do
        echo "  停止进程 PID: $pid"
        kill -TERM $pid 2>/dev/null
        sleep 1
        if kill -0 $pid 2>/dev/null; then
            echo "  强制停止进程 PID: $pid"
            kill -KILL $pid 2>/dev/null
        fi
    done
    echo "[OK] Python后端进程已停止"
else
    echo "[INFO] 未找到运行中的Python后端进程"
fi

echo ""
echo "查找并停止Node前端进程..."

# 查找Node进程
NODE_PIDS=$(pgrep -f "npm.*run.*dev\|vite.*dev" 2>/dev/null || echo "")
if [[ -n "$NODE_PIDS" ]]; then
    echo "找到Node前端进程，正在停止..."
    for pid in $NODE_PIDS; do
        echo "  停止进程 PID: $pid"
        kill -TERM $pid 2>/dev/null
        sleep 1
        if kill -0 $pid 2>/dev/null; then
            echo "  强制停止进程 PID: $pid"
            kill -KILL $pid 2>/dev/null
        fi
    done
    echo "[OK] Node前端进程已停止"
else
    echo "[INFO] 未找到运行中的Node前端进程"
fi

echo ""
echo "检查端口占用情况..."

# 检查端口5000
if command -v netstat &> /dev/null; then
    if netstat -tuln 2>/dev/null | grep ":5000 " > /dev/null; then
        echo "[WARNING] 端口5000仍被占用"
    else
        echo "[OK] 端口5000已释放"
    fi
    
    if netstat -tuln 2>/dev/null | grep ":3000 " > /dev/null; then
        echo "[WARNING] 端口3000仍被占用"
    else
        echo "[OK] 端口3000已释放"
    fi
else
    echo "[INFO] 无法检查端口占用情况（netstat不可用）"
fi

echo ""
echo "清理日志文件..."
if [[ -f "frontend.log" ]]; then
    rm -f frontend.log
    echo "[OK] 已删除前端日志文件"
fi

echo ""
echo "服务停止完成！"
echo ""
echo "提示：如果使用PyCharm，建议在PyCharm终端中运行此脚本"
echo "这样可以确保使用正确的Python环境"
echo "" 