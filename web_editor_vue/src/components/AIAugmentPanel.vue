<template>
  <div class="ai-augment-panel">
    <h3>🤖 AI增强决策树</h3>
    
    <!-- 聊天记录输入 -->
    <div class="input-section">
      <label>聊天记录：</label>
      <textarea 
        v-model="chatHistory" 
        placeholder="请输入聊天记录..."
        rows="8"
        class="chat-input"
      ></textarea>
    </div>
    
    <!-- 操作按钮 -->
    <div class="button-section">
      <el-button 
        type="primary" 
        @click="processChatDirect"
        :loading="processingDirect"
        :disabled="!chatHistory.trim()"
      >
        {{ processingDirect ? 'AI分析中...' : 'AI分析' }}
      </el-button>
    </div>
    
    <!-- 处理结果 -->
    <div v-if="aiResult" class="result-section">
      <h4>📋 AI分析结果</h4>
      
      <!-- 路径数据 -->
      <div v-if="aiResult.path_data" class="path-data">
        <h5>🔍 解析的路径：</h5>
        <div class="path-steps">
          <div v-for="step in aiResult.path_data.steps" :key="step.step" class="step">
            <span class="step-number">步骤 {{ step.step }}:</span>
            <span class="question">{{ step.question }}</span>
            <span class="answer">→ {{ step.answer }}</span>
          </div>
          <div class="solution">
            <strong>解决方案:</strong> {{ aiResult.path_data.solution }}
          </div>
        </div>
      </div>
      
      <!-- 变更列表 -->
      <div v-if="aiResult.changes && aiResult.changes.length > 0" class="changes-list">
        <h5>📝 变更列表：</h5>
        <ul>
          <li v-for="change in aiResult.changes" :key="change.id" :class="change.type">
            {{ change.text }}
          </li>
        </ul>
      </div>
      
      <!-- 新节点预览 -->
      <div v-if="aiResult.new_nodes" class="nodes-preview">
        <h5>🔍 新节点预览：</h5>
        <div class="nodes-list">
          <div v-for="(node, nodeId) in aiResult.new_nodes.nodes" :key="nodeId" class="node-item">
            <div class="node-id">{{ nodeId }}</div>
            <div v-if="node.question" class="node-question">
              问题: {{ node.question }}
            </div>
            <div v-if="node.options" class="node-options">
              选项:
              <ul>
                <li v-for="option in node.options" :key="option.text">
                  {{ option.text }} → {{ option.next_node }}
                </li>
              </ul>
            </div>
            <div v-if="node.solution" class="node-solution">
              解决方案: {{ node.solution }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button 
          type="success" 
          @click="confirmChanges"
          :loading="confirming"
          :disabled="!aiResult.new_nodes"
        >
          {{ confirming ? '确认中...' : '确认并合并' }}
        </el-button>
        
        <el-button 
          type="warning" 
          @click="discardChanges"
        >
          丢弃变更
        </el-button>
      </div>
    </div>
    
    <!-- 错误信息 -->
    <div v-if="error" class="error-message">
      <el-alert 
        :title="error" 
        type="error" 
        show-icon
        @close="error = ''"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

// 响应式数据
const chatHistory = ref('')
const processingDirect = ref(false)
const confirming = ref(false)
const aiResult = ref(null)
const error = ref('')

// 事件
const emit = defineEmits(['changes-confirmed', 'changes-discarded'])

// 处理聊天记录
const processChatDirect = async () => {
  if (!chatHistory.value.trim()) {
    ElMessage.warning('请输入聊天记录')
    return
  }
  
  processingDirect.value = true
  error.value = ''
  
  try {
    const response = await fetch('/api/ai/direct-process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        chat_history: chatHistory.value,
        auto_merge: false
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      aiResult.value = result
      ElMessage.success('AI分析完成')
    } else {
      error.value = result.error || 'AI分析失败'
      ElMessage.error(error.value)
    }
  } catch (err) {
    error.value = '网络请求失败'
    ElMessage.error(error.value)
  } finally {
    processingDirect.value = false
  }
}

// 确认变更
const confirmChanges = async () => {
  if (!aiResult.value || !aiResult.value.new_nodes) {
    ElMessage.warning('没有可确认的变更')
    return
  }
  
  confirming.value = true
  
  try {
    const response = await fetch('/api/ai/direct-process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        chat_history: chatHistory.value,
        auto_merge: true
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      emit('changes-confirmed', result.data)
      ElMessage.success('变更已确认并合并')
      aiResult.value = null
      chatHistory.value = ''
    } else {
      error.value = result.error || '确认失败'
      ElMessage.error(error.value)
    }
  } catch (err) {
    error.value = '网络请求失败'
    ElMessage.error(error.value)
  } finally {
    confirming.value = false
  }
}

// 丢弃变更
const discardChanges = () => {
  aiResult.value = null
  chatHistory.value = ''
  emit('changes-discarded')
  ElMessage.info('已丢弃变更')
}
</script>

<style scoped>
.ai-augment-panel {
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background: #fff;
}

.input-section {
  margin-bottom: 20px;
}

.input-section label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.chat-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-family: monospace;
  font-size: 14px;
  resize: vertical;
}

.button-section {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.result-section {
  margin-top: 20px;
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  background: #f8f9fa;
}

.path-data {
  margin-bottom: 20px;
}

.path-steps {
  margin-top: 10px;
}

.step {
  margin-bottom: 8px;
  padding: 8px;
  background: #fff;
  border-radius: 4px;
  border-left: 3px solid #409eff;
}

.step-number {
  font-weight: bold;
  color: #409eff;
  margin-right: 8px;
}

.question {
  color: #606266;
}

.answer {
  color: #67c23a;
  font-weight: bold;
}

.solution {
  margin-top: 12px;
  padding: 8px;
  background: #f0f9ff;
  border-radius: 4px;
  border-left: 3px solid #67c23a;
}

.changes-list {
  margin-bottom: 20px;
}

.changes-list ul {
  list-style: none;
  padding: 0;
}

.changes-list li {
  padding: 6px 12px;
  margin-bottom: 4px;
  border-radius: 4px;
  font-size: 14px;
}

.changes-list li.new {
  background: #f0f9ff;
  color: #409eff;
  border-left: 3px solid #409eff;
}

.changes-list li.modified {
  background: #fff7e6;
  color: #e6a23c;
  border-left: 3px solid #e6a23c;
}

.nodes-preview {
  margin-bottom: 20px;
}

.nodes-list {
  max-height: 300px;
  overflow-y: auto;
}

.node-item {
  margin-bottom: 12px;
  padding: 12px;
  background: #fff;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
}

.node-id {
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.node-question {
  margin-bottom: 8px;
  color: #606266;
}

.node-options ul {
  margin: 4px 0;
  padding-left: 20px;
}

.node-options li {
  margin-bottom: 2px;
  color: #67c23a;
}

.node-solution {
  margin-top: 8px;
  padding: 6px 10px;
  background: #f0f9ff;
  border-radius: 4px;
  color: #67c23a;
  font-weight: bold;
}

.action-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.error-message {
  margin-top: 16px;
}

h3, h4, h5 {
  margin: 0 0 12px 0;
  color: #303133;
}

h3 {
  color: #409eff;
  border-bottom: 2px solid #409eff;
  padding-bottom: 8px;
}
</style> 