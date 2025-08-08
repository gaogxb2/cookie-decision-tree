<template>
  <div class="decision-tree-editor">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-content">
        <div class="logo">
          <el-icon><Connection /></el-icon>
          <span>决策树可视化编辑器</span>
        </div>
        <div class="toolbar">
          <el-button @click="loadTree" :loading="loading">
            <el-icon><Refresh /></el-icon>
            重新加载
          </el-button>
          <el-button type="primary" @click="saveTree" :loading="saving">
            <el-icon><Download /></el-icon>
            保存
          </el-button>
          <el-button type="success" @click="validateTree">
            <el-icon><Check /></el-icon>
            验证
          </el-button>
          <el-button type="warning" @click="testTree">
            <el-icon><VideoPlay /></el-icon>
            测试
          </el-button>
        </div>
      </div>
    </el-header>

    <!-- 主要内容区域 -->
    <el-container class="main-container">
      <!-- 左侧：树形视图 -->
      <el-aside width="70%" class="tree-panel">
        <div class="panel-header">
          <h3>决策树结构</h3>
        </div>
        <div class="tree-container" ref="treeContainer">
          <TreeVisualization 
            :tree-data="treeData" 
            :selected-node="selectedNode"
            @node-click="handleNodeClick"
          />
        </div>
      </el-aside>

      <!-- 右侧：编辑面板 -->
      <el-aside width="30%" class="editor-panel">
        <!-- 标签页切换 -->
        <el-tabs v-model="activeTab" type="border-card">
          <el-tab-pane label="节点编辑" name="editor">
            <div class="editor-content">
              <NodeEditor 
                v-if="selectedNode"
                :node-id="selectedNode"
                :node-data="currentNodeData"
                @update="handleNodeUpdate"
                @delete="handleNodeDelete"
                @add-child="handleAddChildNode"
                @change-id="handleNodeIdChange"
              />
              <div v-else class="no-selection">
                <el-icon><ArrowLeft /></el-icon>
                <p>选择左侧节点进行编辑</p>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="[AI] AI增强" name="ai">
            <AIAugmentPanel 
              @changes-confirmed="handleAIChangesConfirmed"
              @changes-discarded="handleAIChangesDiscarded"
            />
          </el-tab-pane>
        </el-tabs>
      </el-aside>
    </el-container>

    <!-- 状态栏 -->
    <el-footer class="status-bar">
      <el-alert 
        :title="statusMessage" 
        :type="statusType" 
        :show-icon="true"
        :closable="false"
      />
    </el-footer>

    <!-- 测试结果对话框 -->
    <el-dialog 
      v-model="testDialogVisible" 
      title="测试结果" 
      width="600px"
    >
      <TestResult :result="testResult" />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import TreeVisualization from '../components/TreeVisualization.vue'
import NodeEditor from '../components/NodeEditor.vue'
import TestResult from '../components/TestResult.vue'
import AIAugmentPanel from '../components/AIAugmentPanel.vue'
import { useTreeStore } from '../stores/treeStore'

export default {
  name: 'DecisionTreeEditor',
  components: {
    TreeVisualization,
    NodeEditor,
    TestResult,
    AIAugmentPanel
  },
  setup() {
    const treeStore = useTreeStore()
    
    // 响应式数据
    const loading = ref(false)
    const saving = ref(false)
    const selectedNode = ref(null)
    const testDialogVisible = ref(false)
    const testResult = ref({})
    const activeTab = ref('editor')
    
    // 状态管理
    const statusMessage = ref('准备就绪')
    const statusType = ref('info')
    
    // 计算属性
    const treeData = computed(() => treeStore.treeData.value)
    const currentNodeData = computed(() => {
      
      if (!selectedNode.value || !treeData.value?.nodes) {
        return null
      }
      
      const nodeData = treeData.value.nodes[selectedNode.value]
      return nodeData
    })
    
    // AI增强相关方法
    const handleAIChangesConfirmed = (changes) => {
      // 重新加载决策树以显示AI增强的结果
      loadTree()
      ElMessage.success('AI增强已成功合并到决策树')
    }
    
    const handleAIChangesDiscarded = () => {
      ElMessage.info('AI增强变更已丢弃')
    }
    
    // 方法
    const loadTree = async () => {
      loading.value = true
      statusMessage.value = '正在加载决策树...'
      statusType.value = 'info'
      
      try {
        await treeStore.loadTree()
        statusMessage.value = '决策树加载成功'
        statusType.value = 'success'
        ElMessage.success('决策树加载成功')
      } catch (error) {
        statusMessage.value = `加载失败: ${error.message}`
        statusType.value = 'error'
        ElMessage.error(`加载失败: ${error.message}`)
      } finally {
        loading.value = false
      }
    }
    
    const saveTree = async () => {
      saving.value = true
      statusMessage.value = '正在保存...'
      statusType.value = 'info'
      
      try {
        await treeStore.saveTree()
        statusMessage.value = '保存成功'
        statusType.value = 'success'
        ElMessage.success('保存成功')
      } catch (error) {
        statusMessage.value = `保存失败: ${error.message}`
        statusType.value = 'error'
        ElMessage.error(`保存失败: ${error.message}`)
      } finally {
        saving.value = false
      }
    }
    
    const validateTree = async () => {
      statusMessage.value = '正在验证...'
      statusType.value = 'info'
      
      try {
        const result = await treeStore.validateTree()
        if (result.valid) {
          statusMessage.value = '验证通过'
          statusType.value = 'success'
          ElMessage.success('验证通过')
        } else {
          statusMessage.value = `验证失败: ${result.errors.join(', ')}`
          statusType.value = 'error'
          ElMessage.error(`验证失败: ${result.errors.join(', ')}`)
        }
      } catch (error) {
        statusMessage.value = `验证失败: ${error.message}`
        statusType.value = 'error'
        ElMessage.error(`验证失败: ${error.message}`)
      }
    }
    
    const testTree = async () => {
      try {
        const result = await treeStore.testTree()
        testResult.value = result
        testDialogVisible.value = true
        ElMessage.success('测试完成')
      } catch (error) {
        ElMessage.error(`测试失败: ${error.message}`)
      }
    }
    
    const handleNodeClick = (nodeId) => {
      selectedNode.value = nodeId
    }
    
    const handleNodeUpdate = (nodeId, nodeData) => {
      treeStore.updateNode(nodeId, nodeData)
      ElMessage.success('节点更新成功')
    }
    
    const handleNodeDelete = (nodeId) => {
      treeStore.deleteNode(nodeId)
      if (selectedNode.value === nodeId) {
        selectedNode.value = null
      }
      ElMessage.success('节点删除成功')
    }

    const handleAddChildNode = (nodeId) => {
      const newNodeId = treeStore.addNode(nodeId)
      selectedNode.value = newNodeId // 自动选中新创建的节点
      ElMessage.success('子节点添加成功')
    }

    const handleNodeIdChange = (oldId, newId) => {
      try {
        treeStore.changeNodeId(oldId, newId)
        // 更新选中的节点ID
        if (selectedNode.value === oldId) {
          selectedNode.value = newId
        }
        ElMessage.success('节点ID已更新')
      } catch (error) {
        ElMessage.error(error.message)
      }
    }
    
    // 生命周期
    onMounted(() => {
      loadTree()
    })
    
    return {
      loading,
      saving,
      selectedNode,
      testDialogVisible,
      testResult,
      statusMessage,
      statusType,
      treeData,
      currentNodeData,
      loadTree,
      saveTree,
      validateTree,
      testTree,
      handleNodeClick,
      handleNodeUpdate,
      handleNodeDelete,
      handleAddChildNode,
      handleNodeIdChange,
      activeTab,
      handleAIChangesConfirmed,
      handleAIChangesDiscarded
    }
  }
}
</script>

<style scoped>
.decision-tree-editor {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.logo .el-icon {
  margin-right: 8px;
  font-size: 24px;
}

.toolbar {
  display: flex;
  gap: 10px;
}

.main-container {
  flex: 1;
  background: #f5f5f5;
}

.tree-panel, .editor-panel {
  background: white;
  margin: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.panel-header {
  background: #f8f9fa;
  padding: 15px 20px;
  border-bottom: 1px solid #e9ecef;
}

.panel-header h3 {
  margin: 0;
  color: #495057;
  font-size: 16px;
}

.tree-container {
  height: calc(100vh - 200px);
  overflow: auto;
  padding: 20px;
  min-height: 600px;
}

.editor-content {
  height: calc(100vh - 200px);
  overflow: auto;
  padding: 20px;
}

.no-selection {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6c757d;
}

.no-selection .el-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.status-bar {
  background: white;
  padding: 10px 20px;
  border-top: 1px solid #e9ecef;
}

.status-bar .el-alert {
  margin: 0;
}
</style> 