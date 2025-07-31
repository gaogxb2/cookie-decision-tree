<template>
  <div class="tree-visualization">
    <!-- 工具栏 -->
    <div class="toolbar">
      <el-button-group>
        <el-button @click="zoomIn" size="small">
          <el-icon><ZoomIn /></el-icon>
          放大
        </el-button>
        <el-button @click="zoomOut" size="small">
          <el-icon><ZoomOut /></el-icon>
          缩小
        </el-button>
        <el-button @click="resetZoom" size="small">
          <el-icon><Refresh /></el-icon>
          重置
        </el-button>
      </el-button-group>
      
      <el-divider direction="vertical" />
      
      <el-button 
        @click="toggleFocusMode" 
        size="small"
        :type="focusMode ? 'primary' : 'default'"
      >
        <el-icon><View /></el-icon>
        {{ focusMode ? '退出聚焦' : '聚焦模式' }}
      </el-button>
    </div>
    
    <!-- SVG容器 -->
    <div ref="svgContainer" class="svg-container"></div>
  </div>
</template>

<script>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as d3 from 'd3'

export default {
  name: 'TreeVisualization',
  props: {
    treeData: {
      type: Object,
      required: true
    },
    selectedNode: {
      type: String,
      default: null
    }
  },
  emits: ['node-click'],
  setup(props, { emit }) {
    const svgContainer = ref(null)
    let svg = null
    let g = null
    let zoom = null
    const focusMode = ref(false)
    
    // 切换聚焦模式
    const toggleFocusMode = () => {
      focusMode.value = !focusMode.value
      renderTree()
    }
    
    // 初始化SVG
    const initSvg = () => {
      if (svg) {
        svg.remove()
      }
      
      svg = d3.select(svgContainer.value)
        .append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('viewBox', '0 0 1200 800')
      
      // 添加箭头标记
      svg.append('defs').append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 8)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
        .append('path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('fill', '#6c757d')
      
      g = svg.append('g')
        .attr('transform', 'translate(100, 100) scale(0.6)')
      
      // 添加缩放功能
      zoom = d3.zoom()
        .scaleExtent([0.1, 3])
        .on('zoom', (event) => {
          g.attr('transform', event.transform)
        })
      
      svg.call(zoom)
    }
    
    // 检查节点是否在到目标节点的路径上
    const isNodeInPath = (currentNodeId, targetNodeId, nodes) => {
      if (currentNodeId === targetNodeId) {
        return true
      }
      
      const nodeData = nodes[currentNodeId]
      if (!nodeData || !nodeData.options) {
        return false
      }
      
      return nodeData.options.some(option => {
        if (option.next_node && nodes[option.next_node]) {
          return isNodeInPath(option.next_node, targetNodeId, nodes)
        }
        return false
      })
    }
    
    // 计算节点位置
    const calculatePositions = (data) => {
      const positions = {}
      const levels = {}
      const children = {}
      
      // 计算每个节点的层级
      const calculateLevels = (nodeId, level = 0, visited = new Set()) => {
        if (visited.has(nodeId)) return
        visited.add(nodeId)
        
        if (!levels[level]) levels[level] = []
        levels[level].push(nodeId)
        
        const nodeData = data.nodes[nodeId]
        if (nodeData && nodeData.options) {
          nodeData.options.forEach(option => {
            if (option.next_node && data.nodes[option.next_node]) {
              if (!children[nodeId]) children[nodeId] = []
              children[nodeId].push(option.next_node)
              calculateLevels(option.next_node, level + 1, visited)
            }
          })
        }
      }
      
      // 从根节点开始计算层级
      Object.keys(data.nodes).forEach(nodeId => {
        const nodeData = data.nodes[nodeId]
        // 检查是否是根节点（没有其他节点指向它）
        let isRoot = true
        Object.keys(data.nodes).forEach(otherId => {
          const otherNode = data.nodes[otherId]
          if (otherNode && otherNode.options) {
            otherNode.options.forEach(option => {
              if (option.next_node === nodeId) {
                isRoot = false
              }
            })
          }
        })
        
        if (isRoot) {
          calculateLevels(nodeId)
        }
      })
      
      // 确定要显示的节点
      const nodesToShow = new Set()
      
      if (focusMode.value && props.selectedNode) {
        const focusNodeId = props.selectedNode
        
        // 添加聚焦节点
        nodesToShow.add(focusNodeId)
        
        // 添加聚焦节点的父节点
        const addParentNodes = (nodeId) => {
          Object.keys(data.nodes).forEach(id => {
            const node = data.nodes[id]
            if (node.options) {
              node.options.forEach(option => {
                if (option.next_node === nodeId) {
                  nodesToShow.add(id)
                  addParentNodes(id)
                }
              })
            }
          })
        }
        addParentNodes(focusNodeId)
        
        // 添加聚焦节点的同级节点
        const addSiblingNodes = (nodeId) => {
          // 找到父节点
          let parentNode = null
          Object.keys(data.nodes).forEach(id => {
            const node = data.nodes[id]
            if (node.options) {
              node.options.forEach(option => {
                if (option.next_node === nodeId) {
                  parentNode = id
                }
              })
            }
          })
          
          // 如果找到父节点，添加所有同级节点
          if (parentNode) {
            const parentData = data.nodes[parentNode]
            if (parentData && parentData.options) {
              parentData.options.forEach(option => {
                if (option.next_node && data.nodes[option.next_node]) {
                  nodesToShow.add(option.next_node)
                }
              })
            }
          }
        }
        
        // 添加聚焦节点的同级节点
        addSiblingNodes(focusNodeId)
        
        // 添加聚焦节点及其所有子节点
        const addNodeAndChildren = (nodeId) => {
          nodesToShow.add(nodeId)
          const nodeData = data.nodes[nodeId]
          if (nodeData && nodeData.options) {
            nodeData.options.forEach(option => {
              if (option.next_node && data.nodes[option.next_node]) {
                addNodeAndChildren(option.next_node)
              }
            })
          }
        }
        addNodeAndChildren(focusNodeId)
      } else {
        // 非聚焦模式：显示所有节点
        Object.keys(data.nodes).forEach(nodeId => {
          nodesToShow.add(nodeId)
        })
      }
      
      // 获取所有后代节点的函数
      const getAllDescendants = (nodeId) => {
        const descendants = new Set()
        const queue = [nodeId]
        
        while (queue.length > 0) {
          const current = queue.shift()
          const nodeData = data.nodes[current]
          if (nodeData && nodeData.options) {
            nodeData.options.forEach(option => {
              if (option.next_node && data.nodes[option.next_node]) {
                descendants.add(option.next_node)
                queue.push(option.next_node)
              }
            })
          }
        }
        return Array.from(descendants)
      }
      
      // 改进的布局算法：自底向上计算位置
      const maxLevel = Math.max(...Object.keys(levels).map(Number))
      const levelHeight = 150
      const minNodeSpacing = 180 // 增加最小节点间距
      
      // 从最底层开始，计算每个节点的位置
      for (let level = maxLevel; level >= 0; level--) {
        const nodes = levels[level] || []
        const visibleNodes = nodes.filter(node => nodesToShow.has(node))
        
        if (visibleNodes.length === 0) continue // 跳过空层级
        
        if (level === maxLevel) {
          // 叶子节点：均匀分布
          const totalWidth = (visibleNodes.length - 1) * minNodeSpacing
          const startX = 600 - totalWidth / 2
          
          visibleNodes.forEach((node, index) => {
            positions[node] = {
              x: startX + index * minNodeSpacing,
              y: 100 + level * levelHeight
            }
          })
        } else {
          // 非叶子节点：基于所有后代节点的位置计算
          visibleNodes.forEach(node => {
            const allDescendants = getAllDescendants(node)
            const visibleDescendants = allDescendants.filter(desc => nodesToShow.has(desc) && positions[desc])
            
            if (visibleDescendants.length === 0) {
              // 没有可见后代节点的节点，放在中间
              positions[node] = {
                x: 600,
                y: 100 + level * levelHeight
              }
            } else {
              // 有可见后代节点的节点，放在所有后代节点的中心位置
              const descendantPositions = visibleDescendants.map(desc => positions[desc])
              const avgX = descendantPositions.reduce((sum, pos) => sum + pos.x, 0) / descendantPositions.length
              positions[node] = {
                x: avgX,
                y: 100 + level * levelHeight
              }
            }
          })
        }
      }
      
      // 只保留根节点的居中处理
      if (levels[0] && levels[0].length === 1) {
        const rootNode = levels[0][0]
        if (nodesToShow.has(rootNode) && positions[rootNode]) {
          positions[rootNode] = {
            x: 600,
            y: positions[rootNode].y
          }
        }
      }
      
      return positions
    }
    
    // 绘制连接线
    const drawConnections = (positions, data) => {
      const connections = []
      
      Object.keys(data.nodes).forEach(nodeId => {
        // 只绘制有位置的节点（可见节点）的连接线
        if (!positions[nodeId]) return
        
        const nodeData = data.nodes[nodeId]
        if (nodeData && nodeData.options) {
          nodeData.options.forEach(option => {
            // 只绘制指向可见节点的连接线
            if (option.next_node && positions[option.next_node]) {
              connections.push({
                from: nodeId,
                to: option.next_node,
                label: option.text
              })
            }
          })
        }
      })
      
      g.selectAll('.connection')
        .data(connections)
        .enter()
        .append('g')
        .attr('class', 'connection')
        .each(function(d) {
          const g = d3.select(this)
          const fromPos = positions[d.from]
          const toPos = positions[d.to]
          
          if (!fromPos || !toPos) return
          
          const fromNode = data.nodes[d.from]
          const toNode = data.nodes[d.to]
          const isFromSolution = fromNode.solution
          const isToSolution = toNode.solution
          
          // 计算连接线的起点和终点
          const fromX = fromPos.x + 60 // 节点中心X
          const fromY = fromPos.y + (isFromSolution ? 40 : 50) // 节点底部Y
          const toX = toPos.x + 60 // 节点中心X
          const toY = toPos.y + 20 // 节点顶部Y
          
          // 计算控制点，创建更平滑的曲线
          const midY = (fromY + toY) / 2
          const controlPoint1X = fromX
          const controlPoint1Y = fromY + (toY - fromY) * 0.3
          const controlPoint2X = toX
          const controlPoint2Y = toY - (toY - fromY) * 0.3
          
          // 绘制平滑的连接线
          const pathData = `M ${fromX} ${fromY} C ${controlPoint1X} ${controlPoint1Y} ${controlPoint2X} ${controlPoint2Y} ${toX} ${toY}`
          
          g.append('path')
            .attr('d', pathData)
            .attr('class', 'connection-line')
            .style('stroke', '#6c757d')
            .style('stroke-width', '2')
            .style('fill', 'none')
            .style('marker-end', 'url(#arrowhead)')
          
          // 绘制标签
          const labelX = (fromX + toX) / 2
          const labelY = midY + 15
          
          // 添加标签背景
          g.append('rect')
            .attr('x', labelX - 30)
            .attr('y', labelY - 8)
            .attr('width', 60)
            .attr('height', 16)
            .attr('rx', 3)
            .style('fill', '#ffffff')
            .style('stroke', '#e4e7ed')
            .style('stroke-width', '1')
          
          g.append('text')
            .attr('x', labelX)
            .attr('y', labelY)
            .attr('text-anchor', 'middle')
            .attr('font-size', '10px')
            .attr('fill', '#6c757d')
            .text(d.label)
        })
    }
    
    // 绘制节点
    const drawNodes = (positions, data) => {
      const nodes = Object.keys(data.nodes)
        .map(nodeId => ({
          id: nodeId,
          data: data.nodes[nodeId],
          position: positions[nodeId]
        }))
        .filter(node => node.position) // 只绘制有位置的节点（可见节点）
      
      g.selectAll('.node')
        .data(nodes)
        .enter()
        .append('g')
        .attr('class', 'node')
        .attr('transform', d => `translate(${d.position.x}, ${d.position.y})`)
        .each(function(d) {
          const g = d3.select(this)
          const isSolution = d.data.solution
          const isSelected = d.id === props.selectedNode
          
          // 绘制节点背景
          g.append('rect')
            .attr('width', 120)
            .attr('height', isSolution ? 80 : 100)
            .attr('rx', 8)
            .attr('fill', isSolution ? '#fff3cd' : '#ffffff')
            .attr('stroke', isSelected ? '#28a745' : '#dee2e6')
            .attr('stroke-width', isSelected ? 3 : 2)
            .attr('class', 'node-background')
            .style('cursor', 'pointer')
          
          // 添加节点ID
          g.append('text')
            .attr('x', 60)
            .attr('y', 15)
            .attr('text-anchor', 'middle')
            .attr('font-size', '10px')
            .attr('font-weight', 'bold')
            .attr('fill', '#495057')
            .text(d.id)
          
          if (isSolution) {
            // 解决方案节点
            g.append('text')
              .attr('x', 60)
              .attr('y', 35)
              .attr('text-anchor', 'middle')
              .attr('font-size', '9px')
              .attr('fill', '#6c757d')
              .text('解决方案')
            
            g.append('text')
              .attr('x', 60)
              .attr('y', 55)
              .attr('text-anchor', 'middle')
              .attr('font-size', '8px')
              .attr('fill', '#6c757d')
              .text(d.data.solution.substring(0, 20) + '...')
          } else {
            // 决策节点
            g.append('text')
              .attr('x', 60)
              .attr('y', 35)
              .attr('text-anchor', 'middle')
              .attr('font-size', '9px')
              .attr('fill', '#495057')
              .text('决策节点')
            
            g.append('text')
              .attr('x', 60)
              .attr('y', 55)
              .attr('text-anchor', 'middle')
              .attr('font-size', '8px')
              .attr('fill', '#6c757d')
              .text(d.data.question.substring(0, 20) + '...')
            
            g.append('text')
              .attr('x', 60)
              .attr('y', 75)
              .attr('text-anchor', 'middle')
              .attr('font-size', '8px')
              .attr('fill', '#28a745')
              .text(`${d.data.options.length} 个选项`)
          }
          
          // 添加点击事件
          g.on('click', function() {
            emit('node-click', d.id)
          })
        })
    }
    
    // 渲染树
    const renderTree = () => {
      // 确保获取响应式数据的实际值
      const treeDataValue = props.treeData?.value || props.treeData
      
      if (!treeDataValue?.nodes || Object.keys(treeDataValue.nodes).length === 0) {
        return
      }
      
      // 保存当前的缩放状态
      let currentTransform = null
      if (svg && zoom) {
        currentTransform = d3.zoomTransform(svg.node())
      }
      
      // 清除之前的SVG内容
      if (svg) {
        svg.selectAll('*').remove()
      }
      
      initSvg()
      
      // 根据聚焦模式决定是否使用聚焦功能
      const focusNodeId = focusMode.value ? props.selectedNode : null
      const positions = calculatePositions(treeDataValue)
      drawConnections(positions, treeDataValue)
      drawNodes(positions, treeDataValue)
      
      // 恢复缩放状态
      if (currentTransform && svg && zoom) {
        svg.call(zoom.transform, currentTransform)
      }
    }
    
    // 缩放方法
    const zoomIn = () => {
      if (svg && zoom) {
        svg.transition().call(zoom.scaleBy, 1.2)
      }
    }
    
    const zoomOut = () => {
      if (svg && zoom) {
        svg.transition().call(zoom.scaleBy, 0.8)
      }
    }
    
    const resetZoom = () => {
      if (svg && zoom) {
        svg.transition().call(zoom.transform, d3.zoomIdentity)
      }
    }
    
    // 监听数据变化
    watch(() => props.treeData, () => {
      nextTick(() => {
        renderTree()
      })
    }, { deep: true, immediate: true })
    
    watch(() => props.selectedNode, () => {
      // 在聚焦模式下，需要重新渲染以更新显示的节点
      if (focusMode.value) {
        nextTick(() => {
          renderTree()
        })
      } else {
        // 非聚焦模式下，只更新节点的选中状态
        nextTick(() => {
          updateNodeSelection()
        })
      }
    })
    
    // 更新节点选中状态
    const updateNodeSelection = () => {
      if (!svg) return
      
      // 更新所有节点的选中状态
      svg.selectAll('.node-background')
        .attr('stroke', function(d) {
          const nodeId = d3.select(this.parentNode).datum().id
          return nodeId === props.selectedNode ? '#28a745' : '#dee2e6'
        })
        .attr('stroke-width', function(d) {
          const nodeId = d3.select(this.parentNode).datum().id
          return nodeId === props.selectedNode ? 3 : 2
        })
    }
    
    onMounted(() => {
      renderTree()
    })
    
    return {
      svgContainer,
      zoomIn,
      zoomOut,
      resetZoom,
      focusMode,
      toggleFocusMode
    }
  }
}
</script>

<style scoped>
.tree-visualization {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.toolbar {
  padding: 10px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  gap: 10px;
}

.svg-container {
  flex: 1;
  overflow: hidden;
  position: relative;
  min-height: 600px;
  width: 100%;
}

.connection-line {
  stroke: #6c757d;
  stroke-width: 2;
  fill: none;
  marker-end: url(#arrowhead);
}

.node-background:hover {
  stroke: #007bff !important;
  stroke-width: 3 !important;
}
</style>
