# 决策树可视化编辑器

一个基于Vue.js和LangGraph的决策树可视化编辑器，支持图形化编辑和AI驱动的决策流程。

## 功能特性

### 🎯 核心功能
- **可视化编辑**：直观的树形图界面，支持拖拽和点击操作
- **节点管理**：添加、删除、修改决策树节点
- **聚焦模式**：选中节点时只显示相关路径，提高编辑效率
- **实时预览**：修改后立即在树形图中看到效果

### 🔧 编辑功能
- **节点类型**：支持决策节点和解决方案节点
- **选项管理**：为决策节点添加多个选项和下一节点
- **ID管理**：支持修改节点ID，自动更新所有引用关系
- **数据验证**：确保决策树的完整性和正确性

### 🎨 界面特性
- **响应式设计**：适配不同屏幕尺寸
- **缩放控制**：支持放大、缩小、重置视图
- **聚焦模式**：选中节点时显示完整路径和同级节点
- **状态管理**：实时显示操作状态和错误信息

## 技术栈

### 后端
- **Python 3.10+**：核心编程语言
- **LangGraph**：AI决策流程引擎
- **Flask**：Web API服务器
- **PyYAML**：配置文件解析
- **Pydantic**：数据验证

### 前端
- **Vue.js 3**：响应式前端框架
- **Element Plus**：UI组件库
- **D3.js**：数据可视化
- **Vite**：构建工具
- **Axios**：HTTP客户端

## 快速开始

### 1. 环境准备

确保系统已安装：
- Python 3.10+
- Node.js 18+
- npm 或 yarn

### 2. 克隆项目

```bash
git clone <repository-url>
cd cookie2
```

### 3. 后端设置

```bash
# 创建并激活conda环境
conda create -n py310 python=3.10
conda activate py310

# 安装Python依赖
pip install -r requirements.txt

# 启动Flask后端服务器
python web_editor/app.py
```

后端服务器将在 `http://localhost:5000` 启动。

### 4. 前端设置

```bash
# 进入前端目录
cd web_editor_vue

# 安装Node.js依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 `http://localhost:3001` 启动。

## 使用指南

### 基本操作

1. **查看决策树**：打开应用后，树形图会自动加载并显示
2. **选择节点**：点击任意节点进行编辑
3. **编辑节点**：在右侧面板修改节点属性
4. **保存更改**：点击"保存"按钮应用修改

### 节点编辑

#### 决策节点
- **问题**：输入决策问题
- **选项**：添加多个选项，每个选项指向下一节点
- **ID**：修改节点标识符（根节点除外）

#### 解决方案节点
- **解决方案**：输入具体的解决方案内容
- **ID**：修改节点标识符

### 高级功能

#### 聚焦模式
1. 点击工具栏中的"聚焦模式"按钮
2. 选择要聚焦的节点
3. 界面将只显示相关路径和同级节点
4. 再次点击按钮退出聚焦模式

#### 节点管理
- **添加子节点**：点击"添加子节点"按钮
- **删除节点**：点击"删除节点"按钮
- **修改ID**：在ID输入框中输入新ID并保存

#### 视图控制
- **缩放**：使用鼠标滚轮或工具栏按钮
- **平移**：拖拽视图区域
- **重置**：点击重置按钮恢复默认视图

## 项目结构

```
cookie2/
├── README.md                 # 项目说明
├── requirements.txt          # Python依赖
├── install.sh               # 一键安装脚本
├── src/                     # 后端核心代码
│   ├── decision_tree_engine.py
│   └── main.py
├── config/                  # 配置文件
│   └── decision_tree.yaml
├── web_editor/             # Flask后端
│   └── app.py
└── web_editor_vue/         # Vue.js前端
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── components/
        ├── views/
        ├── stores/
        └── main.js
```

## 配置说明

### 决策树配置 (config/decision_tree.yaml)

```yaml
root_node: start
nodes:
  start:
    question: "您遇到了什么类型的问题？"
    options:
      - text: "硬件问题"
        next_node: hardware_issue
      - text: "软件问题"
        next_node: software_issue
  hardware_issue:
    question: "硬件问题具体是什么？"
    options:
      - text: "显示器问题"
        next_node: display_issue
  display_issue:
    solution: "检查显示器连接线，尝试重新插拔。"
```

### 环境变量

- `FLASK_ENV`：Flask环境（development/production）
- `FLASK_PORT`：后端服务器端口（默认5000）
- `VITE_API_BASE_URL`：API基础URL（默认http://localhost:5000）

## 开发指南

### 添加新功能

1. **后端功能**：在 `web_editor/app.py` 中添加新的API端点
2. **前端组件**：在 `web_editor_vue/src/components/` 中创建新组件
3. **状态管理**：在 `web_editor_vue/src/stores/` 中修改状态逻辑

### 调试技巧

1. **后端调试**：查看Flask控制台输出
2. **前端调试**：使用浏览器开发者工具
3. **数据调试**：检查浏览器Network标签页的API请求

## 常见问题

### Q: 节点删除后树形图显示异常
A: 刷新页面或重新加载决策树数据

### Q: 聚焦模式下节点位置不正确
A: 退出聚焦模式后重新进入

### Q: 保存失败
A: 检查后端服务器是否正常运行，查看控制台错误信息

### Q: 前端无法连接后端
A: 确认后端服务器在5000端口运行，检查CORS设置

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系开发团队。 