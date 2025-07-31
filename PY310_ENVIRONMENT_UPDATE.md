# 🔄 py310环境更新说明

## 更新内容

所有启动脚本已更新，确保在启动前自动切换到py310环境。

## 📝 修改的脚本

### 1. `start_all.sh` - 主启动脚本
- ✅ 添加py310环境切换
- ✅ 添加依赖检查
- ✅ 优化启动流程

### 2. `start_backend.sh` - 后端启动脚本
- ✅ 添加py310环境切换
- ✅ 添加依赖检查
- ✅ 简化启动命令

### 3. `start_frontend.sh` - 前端启动脚本
- ✅ 添加py310环境切换
- ✅ 保持环境一致性

### 4. `start_vue_editor.sh` - Vue编辑器启动脚本
- ✅ 添加py310环境切换
- ✅ 添加依赖检查
- ✅ 优化进程管理

### 5. `start_locator.sh` - 问题定位器启动脚本
- ✅ 添加py310环境切换
- ✅ 添加依赖检查

### 6. `start_locator.bat` - Windows问题定位器启动脚本
- ✅ 添加py310环境切换
- ✅ 添加依赖检查

### 7. `start_ai_augmentor.sh` - AI增强器启动脚本
- ✅ 优化py310环境切换
- ✅ 添加依赖检查
- ✅ 保持API密钥检查

## 🚀 使用方法

### 启动完整系统
```bash
./start_all.sh
```

### 启动后端API
```bash
./start_backend.sh
```

### 启动前端编辑器
```bash
./start_frontend.sh
```

### 启动Vue编辑器
```bash
./start_vue_editor.sh
```

### 启动问题定位器
```bash
./start_locator.sh
```

### 启动AI增强器
```bash
./start_ai_augmentor.sh
```

## 🔧 环境要求

### 必需的环境变量
```bash
export DASHSCOPE_API_KEY='your-api-key-here'
```

### 必需的依赖包
```bash
pip install pyyaml openai requests
```

## 📊 验证步骤

1. **检查环境**
   ```bash
   conda info --envs
   ```

2. **验证Python版本**
   ```bash
   python --version
   # 应该显示: Python 3.10.x
   ```

3. **检查依赖**
   ```bash
   python -c "import yaml, openai, requests; print('✅ 依赖正常')"
   ```

4. **测试启动**
   ```bash
   ./start_all.sh
   ```

## 🎯 AI增强功能

### 在Web编辑器中使用AI增强

1. **启动编辑器**
   ```bash
   ./start_all.sh
   ```

2. **访问编辑器**
   - 打开浏览器访问: http://localhost:3000

3. **使用AI增强**
   - 在编辑器中切换到"🤖 AI增强"标签页
   - 点击"添加聊天记录"按钮
   - 输入聊天记录
   - 点击"开始处理"
   - 确认变更后合并到决策树

### 命令行AI增强

```bash
# 交互模式
./start_ai_augmentor.sh

# 文件模式
./start_ai_augmentor.sh --mode file --input chat.txt

# 自动合并模式
./start_ai_augmentor.sh --mode file --input chat.txt --auto
```

## 🔍 故障排除

### 问题1: conda activate失败
```bash
# 解决方案
source ~/.bash_profile
conda activate py310
```

### 问题2: 依赖包缺失
```bash
# 解决方案
pip install pyyaml openai requests
```

### 问题3: API密钥未设置
```bash
# 解决方案
export DASHSCOPE_API_KEY='your-api-key-here'
```

### 问题4: 端口被占用
```bash
# 解决方案
lsof -ti:3000 | xargs kill -9
lsof -ti:5000 | xargs kill -9
```

## 📈 性能优化

### 启动时间优化
- 所有脚本现在都会检查并安装缺失的依赖
- 环境切换已优化，减少启动时间

### 内存使用优化
- 使用py310环境，确保最佳性能
- 依赖包版本已固定，避免兼容性问题

## 🔮 未来改进

1. **自动化环境检查**
   - 自动检测并修复环境问题
   - 智能依赖管理

2. **一键部署**
   - 创建完整的部署脚本
   - 支持Docker容器化

3. **监控和日志**
   - 添加服务监控
   - 详细的日志记录

---

*最后更新: 2024年12月* 