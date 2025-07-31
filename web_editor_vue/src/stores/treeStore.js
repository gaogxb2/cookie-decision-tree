import { reactive, ref } from 'vue'
import axios from 'axios'

// 创建API服务
const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export function useTreeStore() {
  // 状态
  const treeData = ref({
    root_node: '',
    nodes: {}
  })
  
  // 方法
  const loadTree = async () => {
    try {
      console.log('开始加载决策树数据...')
      const response = await api.get('/tree')
      console.log('API响应:', response.data)
      treeData.value = response.data
      console.log('树数据已更新:', treeData.value)
    } catch (error) {
      console.error('加载失败:', error)
      throw new Error(error.response?.data?.error || error.message)
    }
  }
  
  const saveTree = async () => {
    try {
      const response = await api.post('/tree', treeData.value)
      if (response.data.error) {
        throw new Error(response.data.error)
      }
    } catch (error) {
      throw new Error(error.response?.data?.error || error.message)
    }
  }
  
  const validateTree = async () => {
    try {
      const response = await api.post('/validate', treeData.value)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || error.message)
    }
  }
  
  const testTree = async (testPath = [1, 1, 1]) => {
    try {
      const response = await api.post('/test', {
        ...treeData.value,
        test_path: testPath
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || error.message)
    }
  }
  
  const updateNode = (nodeId, nodeData) => {
    if (!treeData.value.nodes) {
      treeData.value.nodes = {}
    }
    treeData.value.nodes[nodeId] = nodeData
  }
  
  const deleteNode = (nodeId) => {
    if (treeData.value.nodes && treeData.value.nodes[nodeId]) {
      delete treeData.value.nodes[nodeId]
      
      // 更新所有引用该节点的选项
      Object.keys(treeData.value.nodes).forEach(id => {
        const node = treeData.value.nodes[id]
        if (node.options) {
          node.options = node.options.filter(option => 
            option.next_node !== nodeId
          )
        }
      })
    }
  }
  
  const addNode = (parentNodeId) => {
    if (!treeData.value.nodes) {
      treeData.value.nodes = {}
    }
    
    // 生成新的节点ID
    const timestamp = Date.now()
    const newNodeId = `new_node_${timestamp}`
    
    // 创建新的决策节点
    const newNodeData = {
      question: '新问题',
      options: [
        { text: '选项1', next_node: '' },
        { text: '选项2', next_node: '' }
      ]
    }
    
    // 添加新节点
    treeData.value.nodes[newNodeId] = newNodeData
    
    // 为父节点添加指向新节点的选项
    const parentNode = treeData.value.nodes[parentNodeId]
    if (parentNode && parentNode.options) {
      parentNode.options.push({
        text: '新选项',
        next_node: newNodeId
      })
    }
    
    return newNodeId
  }
  
  const changeNodeId = (oldId, newId) => {
    if (!treeData.value.nodes || !treeData.value.nodes[oldId]) {
      return false
    }
    
    // 检查新ID是否已存在
    if (treeData.value.nodes[newId]) {
      throw new Error('节点ID已存在')
    }
    
    // 保存节点数据
    const nodeData = treeData.value.nodes[oldId]
    
    // 删除旧节点
    delete treeData.value.nodes[oldId]
    
    // 添加新节点
    treeData.value.nodes[newId] = nodeData
    
    // 更新根节点引用
    if (treeData.value.root_node === oldId) {
      treeData.value.root_node = newId
    }
    
    // 更新所有引用该节点的选项
    Object.keys(treeData.value.nodes).forEach(id => {
      const node = treeData.value.nodes[id]
      if (node.options) {
        node.options.forEach(option => {
          if (option.next_node === oldId) {
            option.next_node = newId
          }
        })
      }
    })
    
    return true
  }
  
  return {
    treeData,
    loadTree,
    saveTree,
    validateTree,
    testTree,
    updateNode,
    deleteNode,
    addNode,
    changeNodeId
  }
} 