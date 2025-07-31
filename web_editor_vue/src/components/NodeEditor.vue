<template>
  <div class="node-editor">
    <el-form :model="form" label-width="80px">
      <!-- 节点ID -->
      <el-form-item label="节点ID">
        <el-input 
          v-model="form.nodeId" 
          :readonly="form.nodeId === 'start'"
          :placeholder="form.nodeId === 'start' ? '根节点ID不可修改' : '请输入节点ID'"
        />
      </el-form-item>
      
      <!-- 节点类型 -->
      <el-form-item label="节点类型">
        <el-radio-group v-model="form.nodeType" @change="handleTypeChange">
          <el-radio value="decision">决策节点</el-radio>
          <el-radio value="solution">解决方案节点</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <!-- 决策节点内容 -->
      <template v-if="form.nodeType === 'decision'">
        <el-form-item label="问题">
          <el-input 
            v-model="form.question" 
            type="textarea" 
            :rows="3"
            placeholder="请输入问题内容"
          />
        </el-form-item>
        
        <el-form-item label="选项">
          <div class="options-container">
            <div 
              v-for="(option, index) in form.options" 
              :key="index"
              class="option-item"
            >
              <div class="option-header">
                <span>选项 {{ index + 1 }}</span>
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="removeOption(index)"
                  :disabled="form.options.length <= 1"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
              <div class="option-content">
                <el-input 
                  v-model="option.text" 
                  placeholder="选项文本"
                  class="option-text"
                />
                <el-input 
                  v-model="option.next_node" 
                  placeholder="下一节点ID"
                  class="option-next"
                />
              </div>
            </div>
            <el-button @click="addOption" type="primary" size="small">
              <el-icon><Plus /></el-icon>
              添加选项
            </el-button>
          </div>
        </el-form-item>
      </template>
      
      <!-- 解决方案节点内容 -->
      <template v-if="form.nodeType === 'solution'">
        <el-form-item label="解决方案">
          <el-input 
            v-model="form.solution" 
            type="textarea" 
            :rows="6"
            placeholder="请输入解决方案内容"
          />
        </el-form-item>
      </template>
      
      <!-- 操作按钮 -->
      <el-form-item>
        <el-button @click="saveNode" type="primary">
          <el-icon><Check /></el-icon>
          保存
        </el-button>
        <el-button @click="addChildNode" type="success">
          <el-icon><Plus /></el-icon>
          添加子节点
        </el-button>
        <el-button @click="deleteNode" type="danger">
          <el-icon><Delete /></el-icon>
          删除节点
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ref, reactive, watch, computed } from 'vue'

export default {
  name: 'NodeEditor',
  props: {
    nodeId: {
      type: String,
      required: true
    },
    nodeData: {
      type: Object,
      required: true
    }
  },
  emits: ['update', 'delete', 'add-child', 'change-id'],
  setup(props, { emit }) {
    const form = reactive({
      nodeId: '',
      nodeType: 'decision',
      question: '',
      options: [],
      solution: ''
    })
    
    const initForm = () => {
      if (!props.nodeData) {
        return
      }
      
      form.nodeId = props.nodeId
      
      if (props.nodeData.solution) {
        form.nodeType = 'solution'
        form.solution = props.nodeData.solution
        form.question = ''
        form.options = []
      } else {
        form.nodeType = 'decision'
        form.question = props.nodeData.question || ''
        form.options = props.nodeData.options ? [...props.nodeData.options] : []
        form.solution = ''
      }
    }
    
    // 处理节点类型变化
    const handleTypeChange = () => {
      if (form.nodeType === 'solution') {
        form.question = ''
        form.options = []
      } else {
        form.solution = ''
        if (form.options.length === 0) {
          form.options = [{ text: '', next_node: '' }]
        }
      }
    }
    
    // 添加选项
    const addOption = () => {
      form.options.push({ text: '', next_node: '' })
    }
    
    // 删除选项
    const removeOption = (index) => {
      form.options.splice(index, 1)
    }
    
    // 保存节点
    const saveNode = () => {
      // 检查ID是否变更
      if (form.nodeId !== props.nodeId && form.nodeId.trim()) {
        emit('change-id', props.nodeId, form.nodeId.trim())
        return // ID变更后，等待父组件处理完成再保存
      }
      
      const nodeData = {}
      
      if (form.nodeType === 'solution') {
        nodeData.solution = form.solution
      } else {
        nodeData.question = form.question
        nodeData.options = form.options.filter(option => 
          option.text.trim() && option.next_node.trim()
        )
      }
      
      emit('update', props.nodeId, nodeData)
    }
    
    // 删除节点
    const deleteNode = () => {
      emit('delete', props.nodeId)
    }

    // 添加子节点
    const addChildNode = () => {
      emit('add-child', props.nodeId)
    }
    
    // 处理ID变更
    const handleIdChange = () => {
      if (form.nodeId !== props.nodeId && form.nodeId.trim()) {
        emit('change-id', props.nodeId, form.nodeId.trim())
      }
    }
    
    // 监听节点数据变化
    watch(() => props.nodeData, () => {
      initForm()
    }, { immediate: true })
    
    return {
      form,
      handleTypeChange,
      addOption,
      removeOption,
      saveNode,
      deleteNode,
      addChildNode
    }
  }
}
</script>

<style scoped>
.node-editor {
  padding: 20px;
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.option-item {
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 15px;
  background: #f8f9fa;
}

.option-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-weight: 500;
  color: #495057;
}

.option-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-text {
  margin-bottom: 10px;
}

.option-next {
  margin-bottom: 0;
}
</style> 