# PyCharm 使用指南

## 概述

这个指南说明如何在PyCharm中使用决策树编辑器，避免在系统Python中安装额外的包。

## 文件说明

### 启动脚本
- `start_all_windows.sh` - **Windows Git Bash/WSL版本启动脚本（推荐）**
- `start_all_pycharm.bat` - Windows CMD版本启动脚本
- `start_all.sh` - Linux/macOS启动脚本

### 停止脚本
- `stop_services_windows.sh` - **Windows Git Bash/WSL版本停止脚本（推荐）**
- `stop_services_pycharm.bat` - Windows CMD版本停止脚本
- `stop_services.bat` - 通用停止脚本

## 在PyCharm中使用（推荐方式）

### 1. 准备工作

#### 安装Python依赖
在PyCharm的终端中运行：
```bash
pip install pyyaml openai requests flask flask-cors
```

或者使用PyCharm的Package Manager：
1. 打开 `File` → `Settings` → `Project: cookie2` → `Python Interpreter`
2. 点击 `+` 号添加包
3. 搜索并安装：`pyyaml`, `openai`, `requests`, `flask`, `flask-cors`

#### 安装Node.js依赖
在PyCharm的终端中运行：
```bash
cd web_editor_vue
npm install
```

### 2. 启动服务（推荐使用sh脚本）

#### 方法1：使用sh脚本（推荐）
1. 在PyCharm中打开终端
2. 确保终端在项目根目录
3. 给脚本添加执行权限：
   ```bash
   chmod +x start_all_windows.sh
   ```
4. 运行启动脚本：
   ```bash
   ./start_all_windows.sh
   ```

#### 方法2：使用bat脚本
```cmd
start_all_pycharm.bat
```

#### 方法3：手动启动
1. 启动前端（新终端）：
   ```bash
   cd web_editor_vue
   npm run dev
   ```

2. 启动后端（当前终端）：
   ```bash
   python api_server.py
   ```

### 3. 停止服务

#### 使用sh脚本（推荐）
```bash
./stop_services_windows.sh
```

#### 使用bat脚本
```cmd
stop_services_pycharm.bat
```

#### 手动停止
- 后端：按 `Ctrl+C`
- 前端：在运行前端的终端中按 `Ctrl+C`

## 为什么推荐sh脚本？

### 1. **跨平台兼容性**
- 在Windows Git Bash中运行
- 在WSL中运行
- 在Linux/macOS中运行
- 在PyCharm终端中运行

### 2. **更好的进程管理**
- 使用Unix风格的进程控制
- 更精确的进程查找和停止
- 支持信号处理

### 3. **日志管理**
- 前端日志保存到 `frontend.log`
- 后端print输出实时显示
- 自动清理日志文件

## 优势

### 1. **环境隔离**
- 使用PyCharm的虚拟环境
- 不会影响系统Python
- 依赖管理更清晰

### 2. **调试友好**
- 可以在PyCharm中设置断点
- 使用PyCharm的调试器
- 变量查看更方便

### 3. **代码提示**
- 完整的代码补全
- 类型提示支持
- 错误检查

## 注意事项

### 1. **端口冲突**
如果遇到端口被占用：
```bash
# 查看端口占用
netstat -tuln | grep :5000
netstat -tuln | grep :3000

# 停止占用进程
./stop_services_windows.sh
```

### 2. **环境变量**
确保PyCharm使用正确的Python解释器：
1. 检查 `File` → `Settings` → `Project: cookie2` → `Python Interpreter`
2. 选择正确的虚拟环境

### 3. **工作目录**
确保PyCharm终端在项目根目录：
```bash
# 检查当前目录
pwd
# 应该显示项目根目录路径
```

## 故障排除

### 常见问题

#### Q: 依赖包找不到
A: 在PyCharm中安装包，或检查Python解释器设置

#### Q: 端口被占用
A: 使用 `./stop_services_windows.sh` 停止服务

#### Q: 前端无法启动
A: 检查Node.js是否安装，运行 `npm install`

#### Q: 后端无法启动
A: 检查Python环境和依赖包

#### Q: 脚本权限问题
A: 运行 `chmod +x start_all_windows.sh`

## 推荐工作流程

1. **开发时**：在PyCharm中运行 `./start_all_windows.sh`
2. **调试时**：使用PyCharm的调试器运行 `api_server.py`
3. **测试时**：在PyCharm终端中测试API接口
4. **停止时**：运行 `./stop_services_windows.sh`

## 环境要求

### Windows用户
- **Git Bash**（推荐）
- **WSL**（Windows Subsystem for Linux）
- **PowerShell**（需要安装Git Bash工具）

### 依赖要求
- Python 3.7+
- Node.js 14+
- npm 或 yarn

这样你就可以充分利用PyCharm的功能，同时避免污染系统Python环境！🚀 