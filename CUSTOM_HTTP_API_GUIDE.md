# 自定义HTTP API使用指南

## 概述

本系统支持通过自定义HTTP POST请求访问任意AI服务，无需修改代码即可适配不同的API格式。

## 配置方法

### 1. 修改配置文件

编辑 `config/ai_config.yaml`，将 `current_api` 设置为 `custom_http`：

```yaml
ai:
  current_api: "custom_http"  # 改为 custom_http
```

### 2. 配置自定义API

在 `config/ai_config.yaml` 中配置 `custom_http` 部分：

```yaml
custom_http:
  url: "https://your-ai-service.com/api/chat"
  method: "POST"
  headers:
    "Content-Type": "application/json"
    "Authorization": "Bearer ${CUSTOM_API_KEY}"
    "X-Custom-Header": "your-value"
  body_template: |
    {
      "messages": {messages},
      "model": "your-model-name",
      "temperature": 0.1,
      "max_tokens": 2000
    }
  response_parser:
    content_field: "choices.0.message.content"
    error_field: "error.message"
```

### 3. 设置环境变量

```bash
export CUSTOM_API_KEY="your-api-key"
```

## 配置参数说明

### URL
- **说明**: AI服务的API端点地址
- **示例**: `https://api.openai.com/v1/chat/completions`

### Headers
- **说明**: HTTP请求头
- **支持环境变量**: 使用 `${ENV_VAR}` 格式
- **示例**:
  ```yaml
  headers:
    "Content-Type": "application/json"
    "Authorization": "Bearer ${CUSTOM_API_KEY}"
    "X-API-Version": "v1"
  ```

### Body Template
- **说明**: 请求体模板
- **占位符**: `{messages}` 会被替换为实际的消息数组
- **示例**:
  ```yaml
  body_template: |
    {
      "messages": {messages},
      "model": "gpt-3.5-turbo",
      "temperature": 0.1,
      "max_tokens": 2000
    }
  ```

### Response Parser
- **说明**: 响应解析配置
- **content_field**: AI回复内容的字段路径
- **error_field**: 错误信息的字段路径

## 常见API格式示例

### OpenAI兼容格式

```yaml
custom_http:
  url: "https://your-openai-compatible-api.com/v1/chat/completions"
  headers:
    "Content-Type": "application/json"
    "Authorization": "Bearer ${CUSTOM_API_KEY}"
  body_template: |
    {
      "messages": {messages},
      "model": "gpt-3.5-turbo",
      "temperature": 0.1,
      "max_tokens": 2000
    }
  response_parser:
    content_field: "choices.0.message.content"
    error_field: "error.message"
```

### Claude API格式

```yaml
custom_http:
  url: "https://api.anthropic.com/v1/messages"
  headers:
    "Content-Type": "application/json"
    "x-api-key": "${CUSTOM_API_KEY}"
    "anthropic-version": "2023-06-01"
  body_template: |
    {
      "messages": {messages},
      "model": "claude-3-sonnet-20240229",
      "max_tokens": 2000
    }
  response_parser:
    content_field: "content.0.text"
    error_field: "error.message"
```

### 简单格式

```yaml
custom_http:
  url: "https://your-simple-api.com/chat"
  headers:
    "Content-Type": "application/json"
    "Authorization": "Bearer ${CUSTOM_API_KEY}"
  body_template: |
    {
      "messages": {messages}
    }
  response_parser:
    content_field: "response"
    error_field: "error"
```

### 嵌套格式

```yaml
custom_http:
  url: "https://your-nested-api.com/chat"
  headers:
    "Content-Type": "application/json"
    "Authorization": "Bearer ${CUSTOM_API_KEY}"
  body_template: |
    {
      "messages": {messages},
      "model": "your-model"
    }
  response_parser:
    content_field: "data.result.content"
    error_field: "error.message"
```

## 字段路径语法

### 基本语法
- 使用点号 `.` 分隔字段层级
- 使用数字索引访问数组元素
- 支持任意深度的嵌套

### 示例
```yaml
# 访问 choices 数组的第一个元素的 message 对象的 content 字段
content_field: "choices.0.message.content"

# 访问 content 数组的第一个元素的 text 字段
content_field: "content.0.text"

# 访问嵌套对象
content_field: "data.result.content"

# 访问简单字段
content_field: "response"
```

## 测试方法

### 1. 运行测试脚本

```bash
python test_custom_http_api.py
```

### 2. 检查测试结果

测试脚本会验证：
- ✅ 请求格式正确
- ✅ 响应解析正确
- ✅ 错误处理正确
- ✅ 环境变量替换正确

### 3. 手动测试

```python
from ai_chat_parser import AIChatParser

# 创建解析器
parser = AIChatParser()

# 测试消息
messages = [
    {"role": "system", "content": "你是一个助手"},
    {"role": "user", "content": "你好"}
]

# 调用API
response = parser._call_ai_api(messages)
print(response)
```

## 错误排查

### 常见问题

1. **HTTP错误**
   - 检查URL是否正确
   - 检查API密钥是否有效
   - 检查网络连接

2. **解析错误**
   - 检查 `content_field` 路径是否正确
   - 检查响应格式是否匹配
   - 查看响应数据确认字段结构

3. **环境变量错误**
   - 确认环境变量已设置
   - 检查变量名是否正确
   - 确认变量值有效

### 调试方法

1. **查看日志**
   - 检查控制台输出
   - 查看错误信息

2. **测试响应格式**
   - 使用测试脚本验证
   - 手动调用API确认响应格式

3. **验证配置**
   - 检查YAML语法
   - 确认字段路径正确

## 最佳实践

### 1. 配置管理
- 使用环境变量管理敏感信息
- 为不同环境准备不同配置
- 定期更新API密钥

### 2. 错误处理
- 配置合适的超时时间
- 设置重试机制
- 记录详细的错误日志

### 3. 性能优化
- 选择合适的模型参数
- 优化请求频率
- 监控API使用情况

## 示例配置

### 完整配置示例

```yaml
ai:
  current_api: "custom_http"
  api:
    custom_http:
      url: "https://your-ai-service.com/api/chat"
      method: "POST"
      headers:
        "Content-Type": "application/json"
        "Authorization": "Bearer ${CUSTOM_API_KEY}"
        "X-API-Version": "v1"
      body_template: |
        {
          "messages": {messages},
          "model": "your-model",
          "temperature": 0.1,
          "max_tokens": 2000,
          "stream": false
        }
      response_parser:
        content_field: "choices.0.message.content"
        error_field: "error.message"
  api_keys:
    custom_http: "${CUSTOM_API_KEY}"
```

### 环境变量设置

```bash
# 设置API密钥
export CUSTOM_API_KEY="your-api-key-here"

# 验证设置
echo $CUSTOM_API_KEY
```

## 总结

自定义HTTP API功能提供了极大的灵活性，可以适配各种AI服务：

- ✅ **无需修改代码**：通过配置文件即可适配
- ✅ **支持任意格式**：可配置请求和响应格式
- ✅ **环境变量支持**：安全管理敏感信息
- ✅ **错误处理完善**：提供详细的错误信息
- ✅ **测试验证**：提供完整的测试工具

通过合理配置，可以轻松集成各种AI服务，为决策树系统提供强大的AI增强功能。 