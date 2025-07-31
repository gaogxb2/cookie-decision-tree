#!/bin/bash

# Decision Tree Visual Editor - Linux Installation Script
# 决策树可视化编辑器 - Linux 安装脚本

# Set UTF-8 encoding
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

set -e  # Exit on error

echo "=========================================="
echo "Decision Tree Visual Editor - Linux Install"
echo "=========================================="

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
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

# Check if command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 is not installed, please install $1 first"
        return 1
    fi
    return 0
}

# Check system type
check_system() {
    print_info "Checking system environment..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        SYSTEM="linux"
        print_info "Detected Linux system"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

# Install Python 3.10+
install_python() {
    print_info "Checking Python environment..."
    
    if check_command python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
        if [[ "$PYTHON_VERSION" > "3.9" ]]; then
            print_success "Python $PYTHON_VERSION is installed"
            PYTHON_CMD="python3"
        else
            print_warning "Python version is too low ($PYTHON_VERSION), need 3.10+"
            install_python_new
        fi
    else
        print_info "Python is not installed, installing..."
        install_python_new
    fi
}

install_python_new() {
    print_info "Installing Python 3.10+..."
    
    # Check distribution
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        print_info "Using apt to install Python 3.10..."
        sudo apt-get update
        sudo apt-get install -y python3.10 python3.10-venv python3.10-dev
        PYTHON_CMD="python3.10"
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        print_info "Using yum to install Python 3.10..."
        sudo yum update -y
        sudo yum install -y python3.10 python3.10-devel
        PYTHON_CMD="python3.10"
    elif command -v dnf &> /dev/null; then
        # Fedora
        print_info "Using dnf to install Python 3.10..."
        sudo dnf update -y
        sudo dnf install -y python3.10 python3.10-devel
        PYTHON_CMD="python3.10"
    else
        print_error "Please manually install Python 3.10+"
        print_info "You can download from: https://www.python.org/downloads/"
        exit 1
    fi
}

# Install Node.js
install_nodejs() {
    print_info "Checking Node.js environment..."
    
    if check_command node; then
        NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d. -f1)
        if [[ "$NODE_VERSION" -ge 16 ]]; then
            print_success "Node.js $(node --version) is installed"
        else
            print_warning "Node.js version is too low, need 16+"
            install_nodejs_new
        fi
    else
        print_info "Node.js is not installed, installing..."
        install_nodejs_new
    fi
}

install_nodejs_new() {
    print_info "Installing Node.js 16+..."
    
    # Install Node.js using NodeSource repository
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    
    print_success "Node.js $(node --version) installed"
}

# Install Miniconda
install_miniconda() {
    print_info "Checking Conda environment..."
    
    if check_command conda; then
        print_success "Conda is already installed"
    else
        print_info "Installing Miniconda..."
        
        # Download Miniconda
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        MINICONDA_SCRIPT="miniconda_install.sh"
        
        curl -fsSL $MINICONDA_URL -o $MINICONDA_SCRIPT
        bash $MINICONDA_SCRIPT -b -p $HOME/miniconda3
        
        # Initialize conda
        $HOME/miniconda3/bin/conda init bash
        
        # Clean up
        rm $MINICONDA_SCRIPT
        
        print_success "Miniconda installed"
        
        # Reload shell environment
        source ~/.bashrc
    fi
}

# Create Python environment
create_python_env() {
    print_info "Creating Python environment..."
    
    # Create py310 environment
    conda create -n py310 python=3.10 -y
    print_success "Python environment 'py310' created"
}

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."
    
    # Activate environment and install packages
    conda activate py310
    pip install -r requirements.txt
    
    print_success "Python dependencies installed"
}

# Install Node.js dependencies
install_nodejs_deps() {
    print_info "Installing Node.js dependencies..."
    
    cd web_editor_vue
    npm install
    cd ..
    
    print_success "Node.js dependencies installed"
}

# Create startup scripts
create_startup_scripts() {
    print_info "Creating startup scripts..."
    
    # Create start_all.sh with proper encoding
    cat > start_all_linux.sh << 'EOF'
#!/bin/bash

# Decision Tree System - Start All Services (Linux)
# 决策树系统 - 启动所有服务 (Linux)

# Set UTF-8 encoding
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

echo "=========================================="
echo "Starting Decision Tree System..."
echo "=========================================="

# Activate conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate py310

# Start backend
echo "Starting backend server..."
python api_server.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd web_editor_vue
npm run dev &
FRONTEND_PID=$!
cd ..

echo "=========================================="
echo "Services started successfully!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo "=========================================="
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF

    chmod +x start_all_linux.sh
    
    print_success "Startup scripts created"
}

# Main installation function
main() {
    print_info "Starting installation..."
    
    check_system
    install_python
    install_nodejs
    install_miniconda
    create_python_env
    install_python_deps
    install_nodejs_deps
    create_startup_scripts
    
    print_success "Installation completed successfully!"
    echo ""
    echo "=========================================="
    echo "Installation Summary:"
    echo "=========================================="
    echo "Python Environment: py310"
    echo "Backend Server: http://localhost:5000"
    echo "Frontend Server: http://localhost:3000"
    echo ""
    echo "To start the system:"
    echo "  ./start_all_linux.sh"
    echo ""
    echo "To activate Python environment:"
    echo "  conda activate py310"
    echo "=========================================="
}

# Run main function
main "$@" 