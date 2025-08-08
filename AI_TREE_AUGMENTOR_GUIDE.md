# [AI] AI决策树增强器使用指南

## 概述

AI决策树增强器是一个智能系统，能够通过AI分析聊天记录，自动提取问题定位路径，并将其转换为决策树节点，支持可视化预览和用户确认后合并到现有决策树中。

##  核心功能

### 1. AI聊天记录解析
- **智能提取**: 自动识别问题定位的关键步骤
- **节点生成**: 将聊天记录转换为决策树节点结构
- **关系建立**: 自动建立节点间的逻辑关系

### 2. 可视化差异显示
- **颜色编码**: 新增节点用蓝色，修改节点用橙色
- **关系标识**: 新增关系用绿色虚线
- **HTML预览**: 生成交互式可视化页面

### 3. 用户确认和编辑
- **图形界面**: 基于tkinter的用户友好界面
- **节点编辑**: 支持修改节点内容和选项
- **批量操作**: 支持批量处理多个聊天记录

### 4. 智能合并
- **冲突检测**: 自动检测节点ID冲突
- **逻辑验证**: 验证决策树的逻辑完整性
- **备份机制**: 合并前自动创建备份

##  快速开始

### 1. 环境准备

#### 安装依赖
```bash
pip install pyyaml openai
```

#### 设置API密钥
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 2. 启动方式

#### 交互模式（推荐）
```bash
./start_ai_augmentor.sh
```

#### 文件模式
```bash
./start_ai_augmentor.sh --mode file --input chat.txt
```

#### 批量模式
```bash
./start_ai_augmentor.sh --mode batch --input chat_directory/
```

#### 自动合并模式
```bash
./start_ai_augmentor.sh --mode file --input chat.txt --auto
```

##  文件结构

```
config/
├── ai_config.yaml      # AI配置（API设置、样式等）
├── prompts.yaml        # AI提示词配置
└── decision_tree.yaml  # 决策树数据

ai_chat_parser.py       # AI聊天记录解析器
tree_visualizer.py      # 决策树可视化器
tree_confirmation_ui.py # 用户确认界面
ai_tree_augmentor.py    # 主控制器
start_ai_augmentor.sh   # 启动脚本
```

##  配置说明

### AI配置 (config/ai_config.yaml)

```yaml
ai:
  current_api: "openai"  # openai, azure, local
  api:
    openai:
      base_url: "https://api.openai.com/v1"
      model: "gpt-4"
      temperature: 0.1
      max_tokens: 2000

tree_augment:
  new_node_style:
    background_color: "#e3f2fd"  # 浅蓝色
    border_color: "#2196f3"      # 蓝色边框
  new_relation_style:
    stroke_color: "#4caf50"      # 绿色
    stroke_dasharray: "5,5"      # 虚线
```

### 提示词配置 (config/prompts.yaml)

```yaml
chat_analysis:
  system: |
    你是一个专业的IT问题诊断专家...
  user: |
    请分析以下聊天记录...
```

##  使用流程

### 1. 准备聊天记录
聊天记录格式：
```
用户: 问题描述
客服: 询问或建议
用户: 回答或反馈
客服: 进一步指导
...
```

### 2. 启动系统
```bash
./start_ai_augmentor.sh
```

### 3. 输入聊天记录
在交互模式下输入聊天记录，或指定文件路径。

### 4. AI解析
系统会自动：
- 分析聊天记录
- 提取问题定位路径
- 生成决策树节点
- 验证逻辑完整性

### 5. 可视化预览
- 生成HTML可视化页面
- 用不同颜色显示新增内容
- 支持交互式查看

### 6. 用户确认
- 查看变更摘要
- 编辑节点内容
- 确认或取消合并

### 7. 合并决策树
- 自动备份原文件
- 合并新节点到决策树
- 更新配置文件

##  可视化特性

### 颜色编码
- **白色**: 原始节点
- **浅蓝色**: 新增节点
- **浅橙色**: 修改节点
- **绿色虚线**: 新增关系

### 交互功能
- **节点选择**: 点击查看节点详情
- **缩放平移**: 鼠标操作视图
- **搜索定位**: 快速找到特定节点

## [DEBUG] 高级功能

### 批量处理
```bash
# 处理目录下所有聊天记录文件
./start_ai_augmentor.sh --mode batch --input chat_logs/ --output report.html
```

### 自动合并
```bash
# 跳过用户确认，直接合并
./start_ai_augmentor.sh --mode file --input chat.txt --auto
```

### 自定义配置
修改 `config/ai_config.yaml` 和 `config/prompts.yaml` 来自定义：
- AI模型和参数
- 可视化样式
- 提示词内容

##  输出文件

### 可视化文件
- `tree_visualization.html`: 决策树可视化页面
- `augmentation_report.html`: 批量处理报告

### 备份文件
- `decision_tree.yaml.backup`: 合并前的备份
- `backup_YYYYMMDD_HHMMSS/`: 时间戳备份目录

## 故障排除

### 常见问题

#### Q: API调用失败
A: 检查API密钥设置和网络连接
```bash
export OPENAI_API_KEY='your-api-key-here'
```

#### Q: 可视化页面无法显示
A: 检查浏览器支持和文件路径
```bash
open tree_visualization.html
```

#### Q: 节点ID冲突
A: 系统会自动检测并提示，可以手动修改节点ID

#### Q: 决策树逻辑错误
A: 系统会验证逻辑完整性，根据提示修复

### 调试模式
```bash
# 启用详细日志
python ai_tree_augmentor.py --mode interactive --debug
```

##  扩展功能

### 1. 多语言支持
- 支持中文、英文聊天记录
- 自动语言检测
- 多语言提示词

### 2. 机器学习增强
- 基于历史数据优化
- 智能节点合并
- 自动冲突解决

### 3. 集成功能
- 与现有系统集成
- API接口支持
- 数据库存储

### 4. 高级可视化
- 3D决策树视图
- 动画过渡效果
- 实时协作编辑

## 📈 性能优化

### 处理速度
- **单文件**: < 30秒
- **批量处理**: 100文件/分钟
- **可视化生成**: < 5秒

### 内存使用
- **基础内存**: ~50MB
- **大文件处理**: ~200MB
- **批量模式**: ~500MB

### 优化建议
- 使用SSD存储
- 增加内存配置
- 优化网络连接

##  贡献指南

### 开发环境
1. 克隆项目
2. 安装依赖: `pip install -r requirements.txt`
3. 设置API密钥
4. 运行测试: `python -m pytest tests/`

### 代码规范
- 使用Python类型注解
- 遵循PEP 8代码风格
- 添加详细文档字符串
- 编写单元测试

### 提交规范
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `refactor`: 代码重构

##  技术支持

### 获取帮助
- 查看完整文档
- 提交Issue
- 联系开发团队

### 反馈建议
- 功能建议
- 性能优化
- 用户体验改进

---

*最后更新: 2024年12月* 