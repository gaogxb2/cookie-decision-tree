# Debug 文件夹

这个文件夹包含了各种调试脚本，用于排查和诊断系统问题。

## 文件说明

### debug_ai_response.py
- **用途**: 调试AI响应解析问题
- **功能**: 分析AI返回的原始响应，检查JSON解析是否正确
- **使用**: `python debug_ai_response.py`

### debug_ai_path_response.py
- **用途**: 调试AI路径响应解析
- **功能**: 专门用于调试AI返回路径格式的响应
- **使用**: `python debug_ai_path_response.py`

### debug_api_response.py
- **用途**: 调试API响应问题
- **功能**: 检查后端API的响应格式和内容
- **使用**: `python debug_api_response.py`

### debug_network_issue_position.py
- **用途**: 调试网络问题节点位置计算
- **功能**: 分析决策树中network_issue节点的位置计算过程
- **使用**: `python debug_network_issue_position.py`

### debug_tree_data.py
- **用途**: 调试决策树数据结构
- **功能**: 检查决策树的节点和连接关系
- **使用**: `python debug_tree_data.py`

## 使用建议

1. **问题排查**: 当遇到AI响应解析问题时，使用相应的debug脚本
2. **数据验证**: 使用debug脚本验证数据格式和内容
3. **性能分析**: 通过debug脚本分析系统性能瓶颈

## 注意事项

- 这些脚本主要用于开发和调试阶段
- 在生产环境中请谨慎使用
- 某些脚本可能需要特定的环境变量或配置 