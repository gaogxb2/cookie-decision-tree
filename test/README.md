# Test 文件夹

这个文件夹包含了各种测试脚本，用于验证系统功能和性能。

## 文件说明

### AI功能测试

#### test_ai_workflow.py
- **用途**: 测试AI工作流程
- **功能**: 验证AI聊天记录解析和决策树增补的完整流程
- **使用**: `python test_ai_workflow.py`

#### test_ai_root_connection.py
- **用途**: 测试AI节点根连接
- **功能**: 验证AI生成的节点是否正确连接到根节点
- **使用**: `python test_ai_root_connection.py`

#### test_simple_ai_augment.py
- **用途**: 测试简单AI增补功能
- **功能**: 验证基本的AI决策树增补功能
- **使用**: `python test_simple_ai_augment.py`

#### test_precise_ai.py
- **用途**: 测试精确AI解析
- **功能**: 验证AI严格按照聊天记录内容进行解析
- **使用**: `python test_precise_ai.py`

#### test_path_to_tree.py
- **用途**: 测试路径转树结构
- **功能**: 验证将AI返回的路径转换为决策树结构
- **使用**: `python test_path_to_tree.py`

#### test_ai_integration.py
- **用途**: 测试AI集成功能
- **功能**: 验证AI功能与现有系统的集成
- **使用**: `python test_ai_integration.py`

### 安全测试

#### test_secure_ai.py
- **用途**: 测试AI安全性
- **功能**: 验证AI调用不会泄露决策树敏感信息
- **使用**: `python test_secure_ai.py`

#### test_simplified_ai.py
- **用途**: 测试简化AI功能
- **功能**: 验证移除冗余AI功能后的系统稳定性
- **使用**: `python test_simplified_ai.py`

### 前端测试

#### test_frontend_ai.py
- **用途**: 测试前端AI功能
- **功能**: 验证前端AI分析功能的正确性
- **使用**: `python test_frontend_ai.py`

#### test_frontend_logging.py
- **用途**: 测试前端日志记录
- **功能**: 验证前端AI对话日志记录功能
- **使用**: `python test_frontend_logging.py`

#### test_old_ai_api.py
- **用途**: 测试旧版AI API
- **功能**: 验证旧版AI API的兼容性
- **使用**: `python test_old_ai_api.py`

### 布局测试

#### test_layout_fix.py
- **用途**: 测试布局修复
- **功能**: 验证决策树布局算法的修复效果
- **使用**: `python test_layout_fix.py`

#### test_layout_simplified.py
- **用途**: 测试简化布局
- **功能**: 验证简化后的布局算法
- **使用**: `python test_layout_simplified.py`

#### test_tree_layout.py
- **用途**: 测试树布局
- **功能**: 验证决策树可视化布局
- **使用**: `python test_tree_layout.py`

#### test_label_position.py
- **用途**: 测试标签位置
- **功能**: 验证连接线标签位置调整
- **使用**: `python test_label_position.py`

### 自定义HTTP API测试

#### test_custom_http_api.py
- **用途**: 测试自定义HTTP API
- **功能**: 验证自定义HTTP API的配置和调用
- **使用**: `python test_custom_http_api.py`

### 问题定位测试

#### test_locator.py
- **用途**: 测试问题定位功能
- **功能**: 验证问题定位脚本的功能
- **使用**: `python test_locator.py`

## 测试分类

### 功能测试
- AI功能测试
- 前端功能测试
- 布局功能测试

### 安全测试
- 数据安全验证
- API安全测试

### 性能测试
- 布局算法性能
- AI响应性能

### 集成测试
- 系统集成验证
- 组件间协作测试

## 运行建议

1. **完整测试**: 运行所有测试脚本验证系统功能
2. **分类测试**: 根据需求运行特定类别的测试
3. **问题排查**: 遇到问题时运行相关的测试脚本

## 注意事项

- 运行测试前确保环境配置正确
- 某些测试需要特定的环境变量
- 测试结果会输出到控制台
- 建议在开发环境中运行测试 