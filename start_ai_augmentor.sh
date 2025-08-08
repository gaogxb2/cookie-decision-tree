#!/bin/bash

# AI决策树增强器启动脚本

echo "[AI] 启动AI决策树增强器..."

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "[ERROR] 错误：未安装Python"
    exit 1
fi

# 切换到py310环境
echo "🔄 切换到py310环境..."
source ~/.bash_profile
conda activate py310

echo "[OK] Python环境: $(python --version)"
echo "[OK] Conda环境: $CONDA_DEFAULT_ENV"

# 检查依赖
echo "[DEBUG] 检查依赖..."
python -c "import yaml, openai, tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo " 安装依赖包..."
    pip install pyyaml openai
fi

# 检查配置文件
if [ ! -f "config/ai_config.yaml" ]; then
    echo "[ERROR] 错误：配置文件 config/ai_config.yaml 不存在"
    exit 1
fi

if [ ! -f "config/prompts.yaml" ]; then
    echo "[ERROR] 错误：配置文件 config/prompts.yaml 不存在"
    exit 1
fi

echo "[OK] 配置文件检查通过"

# 检查API密钥
if [ -z "$DASHSCOPE_API_KEY" ]; then
    echo "警告：未设置DASHSCOPE_API_KEY环境变量"
    echo "请设置您的阿里云百炼API密钥："
    echo "export DASHSCOPE_API_KEY='your-api-key-here'"
    echo ""
fi

# 启动AI决策树增强器
echo "启动AI决策树增强器..."
echo "使用说明："
echo "  - 交互模式：./start_ai_augmentor.sh"
echo "  - 文件模式：./start_ai_augmentor.sh --file --input chat.txt"
echo "  - 批量模式：./start_ai_augmentor.sh --batch --input chat_dir/"
echo "  - 自动合并：添加 --auto 参数"
echo ""

# 检查命令行参数
if [ $# -eq 0 ]; then
    # 交互模式
    python ai_tree_augmentor.py --mode interactive
else
    # 传递所有参数
    python ai_tree_augmentor.py "$@"
fi 