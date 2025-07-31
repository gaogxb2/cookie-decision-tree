#!/bin/bash

# 决策树可视化编辑器 - 一键安装脚本
# 适用于 macOS 和 Linux 系统

# Set UTF-8 encoding for proper Chinese character display
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8

set -e  # 遇到错误时退出

echo "=========================================="
echo "🤖 决策树可视化编辑器 - 一键安装脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 未安装，请先安装 $1"
        return 1
    fi
    return 0
}

# 检查系统类型
check_system() {
    print_info "检查系统环境..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        SYSTEM="macos"
        print_info "检测到 macOS 系统"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        SYSTEM="linux"
        print_info "检测到 Linux 系统"
    else
        print_error "不支持的操作系统: $OSTYPE"
        exit 1
    fi
}

# 安装 Homebrew (macOS)
install_homebrew() {
    if [[ "$SYSTEM" == "macos" ]]; then
        if ! command -v brew &> /dev/null; then
            print_info "安装 Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            print_success "Homebrew 安装完成"
        else
            print_info "Homebrew 已安装"
        fi
    fi
}

# 安装 Python 3.10+
install_python() {
    print_info "检查 Python 环境..."
    
    if check_command python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
        if [[ "$PYTHON_VERSION" > "3.9" ]]; then
            print_success "Python $PYTHON_VERSION 已安装"
            PYTHON_CMD="python3"
        else
            print_warning "Python 版本过低 ($PYTHON_VERSION)，需要 3.10+"
            install_python_new
        fi
    else
        print_info "Python 未安装，正在安装..."
        install_python_new
    fi
}

install_python_new() {
    if [[ "$SYSTEM" == "macos" ]]; then
        print_info "使用 Homebrew 安装 Python 3.10..."
        brew install python@3.10
        PYTHON_CMD="python3.10"
    else
        print_error "请手动安装 Python 3.10+"
        exit 1
    fi
}

# 安装 Conda
install_conda() {
    print_info "检查 Conda 环境..."
    
    if ! command -v conda &> /dev/null; then
        print_info "安装 Miniconda..."
        
        if [[ "$SYSTEM" == "macos" ]]; then
            curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
            bash Miniconda3-latest-MacOSX-x86_64.sh -b -p $HOME/miniconda3
            rm Miniconda3-latest-MacOSX-x86_64.sh
        else
            curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
            bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
            rm Miniconda3-latest-Linux-x86_64.sh
        fi
        
        # 初始化 conda
        $HOME/miniconda3/bin/conda init bash
        source ~/.bashrc
        
        print_success "Miniconda 安装完成"
    else
        print_info "Conda 已安装"
    fi
}

# 安装 Node.js
install_nodejs() {
    print_info "检查 Node.js 环境..."
    
    if ! check_command node; then
        print_info "安装 Node.js..."
        
        if [[ "$SYSTEM" == "macos" ]]; then
            brew install node
        else
            # Linux 安装 Node.js
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
        fi
        
        print_success "Node.js 安装完成"
    else
        NODE_VERSION=$(node --version)
        print_success "Node.js $NODE_VERSION 已安装"
    fi
    
    # 检查 npm
    if ! check_command npm; then
        print_error "npm 未安装"
        exit 1
    fi
}

# 创建 Python 环境
setup_python_env() {
    print_info "设置 Python 环境..."
    
    # 创建 conda 环境
    if conda env list | grep -q "py310"; then
        print_info "py310 环境已存在"
    else
        print_info "创建 py310 环境..."
        conda create -n py310 python=3.10 -y
    fi
    
    # 激活环境
    print_info "激活 py310 环境..."
    eval "$(conda shell.bash hook)"
    conda activate py310
    
    # 安装 Python 依赖
    print_info "安装 Python 依赖..."
    pip install -r requirements.txt
    
    print_success "Python 环境设置完成"
}

# 设置前端环境
setup_frontend() {
    print_info "设置前端环境..."
    
    cd web_editor_vue
    
    # 安装 npm 依赖
    print_info "安装 Node.js 依赖..."
    npm install
    
    print_success "前端环境设置完成"
    cd ..
}

# 创建启动脚本
create_startup_scripts() {
    print_info "创建启动脚本..."
    
    # 创建后端启动脚本
    cat > start_backend.sh << 'EOF'
#!/bin/bash
echo "启动后端服务器..."
eval "$(conda shell.bash hook)"
conda activate py310
cd "$(dirname "$0")"
python web_editor/app.py
EOF
    chmod +x start_backend.sh
    
    # 创建前端启动脚本
    cat > start_frontend.sh << 'EOF'
#!/bin/bash
echo "启动前端服务器..."
cd "$(dirname "$0")/web_editor_vue"
npm run dev
EOF
    chmod +x start_frontend.sh
    
    # 创建一键启动脚本
    cat > start_all.sh << 'EOF'
#!/bin/bash
echo "启动决策树编辑器..."
echo "后端将在 http://localhost:5000 启动"
echo "前端将在 http://localhost:3001 启动"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 启动后端
./start_backend.sh &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
./start_frontend.sh &
FRONTEND_PID=$!

# 等待用户中断
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
EOF
    chmod +x start_all.sh
    
    print_success "启动脚本创建完成"
}

# 显示使用说明
show_usage() {
    echo ""
    echo "=========================================="
    echo "🎉 安装完成！"
    echo "=========================================="
    echo ""
    echo "启动方式："
    echo "1. 一键启动（推荐）："
    echo "   ./start_all.sh"
    echo ""
    echo "2. 分别启动："
    echo "   后端：./start_backend.sh"
    echo "   前端：./start_frontend.sh"
    echo ""
    echo "访问地址："
    echo "前端界面：http://localhost:3001"
    echo "后端API：http://localhost:5000"
    echo ""
    echo "注意事项："
    echo "- 确保端口 3001 和 5000 未被占用"
    echo "- 首次启动可能需要较长时间"
    echo "- 如遇问题，请查看控制台错误信息"
    echo ""
}

# 主函数
main() {
    check_system
    install_homebrew
    install_python
    install_conda
    install_nodejs
    setup_python_env
    setup_frontend
    create_startup_scripts
    show_usage
}

# 运行主函数
main "$@" 