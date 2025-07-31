# Linux 中文乱码问题解决指南

## 问题描述

在Linux服务器上运行 `install.sh` 脚本时，中文字符显示为乱码。

## 原因分析

1. **字符编码不匹配**: Linux服务器默认可能不是UTF-8编码
2. **终端设置问题**: 终端没有正确设置UTF-8编码
3. **系统语言环境**: 系统语言环境配置不正确

## 解决方案

### 方案1: 使用修复后的安装脚本

我们创建了专门针对Linux的安装脚本：

```bash
# 使用Linux专用安装脚本
./install_linux.sh
```

### 方案2: 手动设置环境变量

在运行安装脚本前，先设置环境变量：

```bash
# 设置UTF-8编码
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8

# 然后运行安装脚本
./install.sh
```

### 方案3: 永久设置系统编码

#### Ubuntu/Debian 系统

1. **编辑系统配置文件**:
```bash
sudo nano /etc/default/locale
```

2. **添加以下内容**:
```
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
LC_CTYPE=en_US.UTF-8
```

3. **重新生成locale**:
```bash
sudo locale-gen en_US.UTF-8
sudo update-locale
```

#### CentOS/RHEL 系统

1. **编辑系统配置文件**:
```bash
sudo nano /etc/environment
```

2. **添加以下内容**:
```
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
LC_CTYPE=en_US.UTF-8
```

3. **重启系统或重新登录**

### 方案4: 检查终端设置

确保终端支持UTF-8：

```bash
# 检查当前编码设置
locale

# 检查终端类型
echo $TERM

# 设置终端编码
export TERM=xterm-256color
```

### 方案5: 使用英文版本

如果中文显示仍有问题，可以使用英文版本的脚本：

```bash
# 创建英文版本的启动脚本
cat > start_all_en.sh << 'EOF'
#!/bin/bash

# Decision Tree System - Start All Services
# 决策树系统 - 启动所有服务

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

chmod +x start_all_en.sh
```

## 验证修复

运行以下命令验证编码设置：

```bash
# 检查编码设置
locale

# 测试中文显示
echo "测试中文显示: 决策树系统"

# 检查Python编码
python3 -c "import sys; print(sys.getdefaultencoding())"
```

## 常见问题

### Q1: 为什么会出现中文乱码？
A1: Linux服务器默认可能使用非UTF-8编码，导致中文字符无法正确显示。

### Q2: 如何永久解决这个问题？
A2: 可以通过设置系统环境变量或使用专门的Linux安装脚本。

### Q3: 是否影响系统功能？
A3: 乱码只是显示问题，不影响系统功能，但建议修复以获得更好的用户体验。

### Q4: 其他脚本也有类似问题吗？
A4: 是的，所有包含中文的脚本都可能遇到类似问题，建议统一设置UTF-8编码。

## 最佳实践

1. **使用UTF-8编码**: 所有脚本文件都使用UTF-8编码保存
2. **设置环境变量**: 在脚本开头设置UTF-8环境变量
3. **提供英文版本**: 为重要脚本提供英文版本作为备选
4. **测试验证**: 在不同Linux发行版上测试脚本兼容性

## 相关文件

- `install.sh` - 原始安装脚本（已修复）
- `install_linux.sh` - Linux专用安装脚本
- `start_all_linux.sh` - Linux专用启动脚本
- `start_all_en.sh` - 英文版启动脚本

## 总结

通过设置正确的UTF-8编码环境变量，可以解决Linux服务器上的中文乱码问题。建议使用提供的Linux专用脚本，或者手动设置环境变量后运行原始脚本。 