# 自定义 HTTP API 使用指南

## 概述

本系统支持自定义 HTTP API 调用，可以连接到任何符合格式要求的 AI 服务。

## 请求格式

### 请求体格式
```json
{
  "inputs": "prompt message...",
  "parameters": {
    "detail": true,
    "temperature": 0.1
  }
}
```

### 请求方式
```python
import requests
import json

url = "https://your-ai-service.com/api/chat"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your-api-key"
}
body = {
    "inputs": "prompt message...",
    "parameters": {
        "detail": True,
        "temperature": 0.1
    }
}

response = requests.post(url, headers=headers, data=json.dumps(body))
result = response.text
```

## 配置步骤

### 1. 修改配置文件

编辑 `config/ai_config.yaml`：

```yaml
ai:
  api:
    custom_http:
      url: "https://your-ai-service.com/api/chat"
      headers:
        "Content-Type": "application/json"
        "Authorization": "Bearer ${CUSTOM_API_KEY}"
  
  current_api: "custom_http"  # 设置为使用自定义 HTTP API
  
  api_keys:
    custom_http: "${CUSTOM_API_KEY}"
```

### 2. 设置环境变量

```bash
# Linux/Mac
export CUSTOM_API_KEY="your-api-key"

# Windows
set CUSTOM_API_KEY=your-api-key
```

### 3. 测试配置

运行测试脚本：
```bash
python test_simple_custom_api.py
```

## 功能特性

### [OK] 已支持的功能

1. **简单 HTTP POST 请求** - 使用 `requests.post()` 发送请求
2. **自定义请求头** - 支持 Authorization 等自定义头部
3. **环境变量支持** - 通过环境变量配置 API 密钥
4. **消息转换** - 自动将对话消息转换为单个提示文本
5. **错误处理** - 完整的错误处理和日志记录
6. **Windows 兼容** - 修复了 Windows 系统的编码问题

###  消息转换逻辑

系统会自动将对话消息转换为单个提示文本：

```
原始消息:
- system: "你是一个决策树分析助手..."
- user: "我的电脑无法开机，应该怎么办？"

转换后:
"系统指令: 你是一个决策树分析助手...\n\n用户: 我的电脑无法开机，应该怎么办？"
```

## 使用示例

### 基本使用

1. **启动系统**：
   ```bash
   ./start_all.sh
   ```

2. **在前端界面使用 AI 分析**：
   - 打开 http://localhost:3000
   - 输入问题描述
   - 点击 AI 分析按钮

3. **查看日志**：
   - 系统会自动记录 AI 对话日志
   - 日志文件保存在项目根目录

### 高级配置

#### 自定义参数

您可以在 `ai_chat_parser.py` 中修改默认参数：

```python
body = {
    "inputs": prompt_text,
    "parameters": {
        "detail": True,        # 可以修改为 False
        "temperature": 0.1     # 可以调整温度参数
    }
}
```

#### 自定义请求头

在配置文件中添加更多请求头：

```yaml
custom_http:
  url: "https://your-ai-service.com/api/chat"
  headers:
    "Content-Type": "application/json"
    "Authorization": "Bearer ${CUSTOM_API_KEY}"
    "X-Custom-Header": "custom-value"
    "User-Agent": "DecisionTree-Editor/1.0"
```

## 故障排除

### 常见问题

1. **编码错误**：
   - 已修复 Windows 系统的 Unicode 编码问题
   - 使用安全的字符替代表情符号

2. **连接失败**：
   - 检查 URL 是否正确
   - 检查网络连接
   - 检查 API 密钥是否有效

3. **响应解析错误**：
   - 系统直接返回 `response.text`
   - 不需要复杂的 JSON 解析

### 调试方法

1. **查看日志**：
   ```bash
   tail -f ai_conversation_*.txt
   ```

2. **测试 API**：
   ```bash
   python test_simple_custom_api.py
   ```

3. **检查配置**：
   ```bash
   python -c "import yaml; print(yaml.safe_load(open('config/ai_config.yaml')))"
   ```

## 更新日志

- [OK] 支持自定义 HTTP API 格式
- [OK] 修复 Windows 编码问题
- [OK] 简化配置项
- [OK] 添加测试脚本
- [OK] 完善错误处理 