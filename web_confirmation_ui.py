#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import json
import webbrowser
from typing import Dict, List, Optional
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import time

class WebConfirmationUI:
    def __init__(self, config_file: str = "config/ai_config.yaml"):
        """初始化Web确认界面"""
        self.config = self._load_config(config_file)
        self.app = Flask(__name__)
        self.original_tree = None
        self.new_nodes = None
        self.modified_tree = None
        self.result = None
        
        # 设置模板和静态文件目录
        self.templates_dir = "templates"
        self.static_dir = "static"
        self._create_directories()
        self._create_templates()
        
        # 注册路由
        self._register_routes()
    
    def _load_config(self, config_file: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[ERROR] 加载配置文件失败: {e}")
            sys.exit(1)
    
    def _create_directories(self):
        """创建必要的目录"""
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.static_dir, exist_ok=True)
        os.makedirs(os.path.join(self.static_dir, "css"), exist_ok=True)
        os.makedirs(os.path.join(self.static_dir, "js"), exist_ok=True)
    
    def _create_templates(self):
        """创建HTML模板"""
        # 主页面模板
        main_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>决策树确认界面</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vue@3.2.31/dist/vue.global.js"></script>
</head>
<body>
    <div id="app">
        <header class="header">
            <h1>[AI] AI决策树增强确认</h1>
            <div class="status-bar">
                <span class="status-item">
                    <span class="status-label">原始节点:</span>
                    <span class="status-value">{{ originalNodeCount }}</span>
                </span>
                <span class="status-item">
                    <span class="status-label">新增节点:</span>
                    <span class="status-value new-count">{{ newNodeCount }}</span>
                </span>
                <span class="status-item">
                    <span class="status-label">修改节点:</span>
                    <span class="status-value modified-count">{{ modifiedNodeCount }}</span>
                </span>
            </div>
        </header>

        <main class="main-content">
            <div class="sidebar">
                <div class="panel">
                    <h3>变更摘要</h3>
                    <div class="changes-summary">
                        <div v-for="change in changes" :key="change.id" class="change-item" :class="change.type">
                            <span class="change-icon">{{ change.icon }}</span>
                            <span class="change-text">{{ change.text }}</span>
                        </div>
                    </div>
                </div>

                <div class="panel">
                    <h3>操作</h3>
                    <div class="actions">
                        <button @click="previewVisualization" class="btn btn-primary">
                            预览可视化
                        </button>
                        <button @click="saveBackup" class="btn btn-secondary">
                            [SAVE] 保存备份
                        </button>
                        <button @click="confirmMerge" class="btn btn-success">
                            [OK] 确认合并
                        </button>
                        <button @click="cancelOperation" class="btn btn-danger">
                            [ERROR] 取消
                        </button>
                    </div>
                </div>

                <div class="panel" v-if="selectedNode">
                    <h3>编辑节点</h3>
                    <div class="node-editor">
                        <div class="form-group">
                            <label>节点ID:</label>
                            <input v-model="selectedNode.id" type="text" class="form-control">
                        </div>
                        <div class="form-group">
                            <label>节点类型:</label>
                            <select v-model="selectedNode.type" class="form-control">
                                <option value="decision">决策节点</option>
                                <option value="solution">解决方案节点</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>内容:</label>
                            <textarea v-model="selectedNode.content" class="form-control" rows="3"></textarea>
                        </div>
                        <div class="form-group" v-if="selectedNode.type === 'decision'">
                            <label>选项:</label>
                            <div v-for="(option, index) in selectedNode.options" :key="index" class="option-item">
                                <input v-model="option.text" placeholder="选项文本" class="form-control">
                                <input v-model="option.nextNode" placeholder="下一节点" class="form-control">
                                <button @click="removeOption(index)" class="btn btn-sm btn-danger">删除</button>
                            </div>
                            <button @click="addOption" class="btn btn-sm btn-primary">添加选项</button>
                        </div>
                        <button @click="saveNodeChanges" class="btn btn-primary">保存修改</button>
                    </div>
                </div>
            </div>

            <div class="main-panel">
                <div class="visualization-container">
                    <div id="tree-visualization"></div>
                </div>
            </div>
        </main>
    </div>

    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
        """
        
        with open(os.path.join(self.templates_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(main_template)
        
        # CSS样式
        css_content = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    color: #333;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header h1 {
    margin-bottom: 15px;
    font-size: 24px;
}

.status-bar {
    display: flex;
    gap: 20px;
}

.status-item {
    display: flex;
    align-items: center;
    gap: 5px;
}

.status-label {
    font-weight: 500;
}

.status-value {
    background: rgba(255,255,255,0.2);
    padding: 2px 8px;
    border-radius: 12px;
    font-weight: bold;
}

.new-count {
    background: rgba(76, 175, 80, 0.3);
}

.modified-count {
    background: rgba(255, 152, 0, 0.3);
}

.main-content {
    display: flex;
    height: calc(100vh - 100px);
}

.sidebar {
    width: 350px;
    background: white;
    border-right: 1px solid #ddd;
    overflow-y: auto;
    padding: 20px;
}

.panel {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: #fafafa;
}

.panel h3 {
    margin-bottom: 15px;
    color: #555;
    font-size: 16px;
}

.changes-summary {
    max-height: 200px;
    overflow-y: auto;
}

.change-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px;
    margin-bottom: 5px;
    border-radius: 4px;
    background: #f0f0f0;
}

.change-item.new {
    background: #e8f5e8;
    border-left: 3px solid #4caf50;
}

.change-item.modified {
    background: #fff3e0;
    border-left: 3px solid #ff9800;
}

.change-icon {
    font-size: 16px;
}

.actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.btn {
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-primary {
    background: #2196f3;
    color: white;
}

.btn-primary:hover {
    background: #1976d2;
}

.btn-secondary {
    background: #757575;
    color: white;
}

.btn-secondary:hover {
    background: #616161;
}

.btn-success {
    background: #4caf50;
    color: white;
}

.btn-success:hover {
    background: #388e3c;
}

.btn-danger {
    background: #f44336;
    color: white;
}

.btn-danger:hover {
    background: #d32f2f;
}

.btn-sm {
    padding: 5px 10px;
    font-size: 12px;
}

.main-panel {
    flex: 1;
    padding: 20px;
    overflow: hidden;
}

.visualization-container {
    width: 100%;
    height: 100%;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    overflow: hidden;
}

#tree-visualization {
    width: 100%;
    height: 100%;
}

.node-editor {
    max-height: 400px;
    overflow-y: auto;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #555;
}

.form-control {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.form-control:focus {
    outline: none;
    border-color: #2196f3;
    box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
}

.option-item {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
    align-items: center;
}

.option-item .form-control {
    flex: 1;
}

.node {
    cursor: pointer;
    transition: all 0.3s ease;
}

.node:hover {
    opacity: 0.8;
}

.node circle {
    stroke-width: 2px;
}

.node text {
    font: 12px sans-serif;
    font-weight: 500;
}

.link {
    fill: none;
    stroke-width: 2px;
    transition: all 0.3s ease;
}

.link:hover {
    stroke-width: 3px;
}

.node.original circle {
    fill: #ffffff;
    stroke: #cccccc;
}

.node.new circle {
    fill: #e3f2fd;
    stroke: #2196f3;
}

.node.modified circle {
    fill: #fff3e0;
    stroke: #ff9800;
}

.node.selected circle {
    stroke: #f44336;
    stroke-width: 3px;
}
        """
        
        with open(os.path.join(self.static_dir, "css", "style.css"), "w", encoding="utf-8") as f:
            f.write(css_content)
        
        # JavaScript应用逻辑
        js_content = """
const { createApp } = Vue;

createApp({
    data() {
        return {
            originalTree: null,
            newNodes: null,
            visualizationData: null,
            selectedNode: null,
            changes: [],
            originalNodeCount: 0,
            newNodeCount: 0,
            modifiedNodeCount: 0
        }
    },
    
    async mounted() {
        await this.loadData();
        this.initializeVisualization();
        this.generateChanges();
    },
    
    methods: {
        async loadData() {
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                this.originalTree = data.originalTree;
                this.newNodes = data.newNodes;
                this.visualizationData = data.visualizationData;
                
                this.originalNodeCount = Object.keys(this.originalTree.nodes || {}).length;
                this.newNodeCount = Object.keys(this.newNodes.nodes || {}).length;
                this.modifiedNodeCount = this.calculateModifiedNodes();
            } catch (error) {
                console.error('加载数据失败:', error);
            }
        },
        
        calculateModifiedNodes() {
            const originalNodes = new Set(Object.keys(this.originalTree.nodes || {}));
            const newNodeIds = new Set(Object.keys(this.newNodes.nodes || {}));
            return [...originalNodes].filter(id => newNodeIds.has(id)).length;
        },
        
        generateChanges() {
            this.changes = [];
            
            // 新增节点
            const originalNodeIds = new Set(Object.keys(this.originalTree.nodes || {}));
            const newNodeIds = Object.keys(this.newNodes.nodes || {});
            
            newNodeIds.forEach(id => {
                if (!originalNodeIds.has(id)) {
                    this.changes.push({
                        id: id,
                        type: 'new',
                        icon: '🆕',
                        text: `新增节点: ${id}`
                    });
                } else {
                    this.changes.push({
                        id: id,
                        type: 'modified',
                        icon: '[EDIT]',
                        text: `修改节点: ${id}`
                    });
                }
            });
        },
        
        initializeVisualization() {
            if (!this.visualizationData) return;
            
            const width = document.getElementById('tree-visualization').offsetWidth;
            const height = document.getElementById('tree-visualization').offsetHeight;
            const margin = {top: 20, right: 90, bottom: 30, left: 90};
            
            const svg = d3.select("#tree-visualization")
                .append("svg")
                .attr("width", width)
                .attr("height", height);
            
            const g = svg.append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);
            
            // 创建层次结构
            const nodes = Object.values(this.visualizationData.nodes);
            const links = this.visualizationData.relations;
            
            // 创建树形布局
            const tree = d3.tree().size([height - margin.top - margin.bottom, width - margin.left - margin.right]);
            
            // 构建层次结构
            const root = d3.stratify()
                .id(d => d.id)
                .parentId(d => {
                    const link = links.find(l => l.to === d.id);
                    return link ? link.from : null;
                })(nodes);
            
            // 应用树形布局
            const treeData = tree(root);
            
            // 绘制连接线
            const link = g.selectAll(".link")
                .data(treeData.links())
                .enter().append("path")
                .attr("class", "link")
                .attr("d", d3.linkHorizontal()
                    .x(d => d.y)
                    .y(d => d.x))
                .style("stroke", d => {
                    const linkData = links.find(l => l.from === d.source.id && l.to === d.target.id);
                    return linkData ? linkData.style.stroke_color : "#666666";
                })
                .style("stroke-width", d => {
                    const linkData = links.find(l => l.from === d.source.id && l.to === d.target.id);
                    return linkData ? linkData.style.stroke_width : 1;
                })
                .style("stroke-dasharray", d => {
                    const linkData = links.find(l => l.from === d.source.id && l.to === d.target.id);
                    return linkData ? linkData.style.stroke_dasharray : "none";
                });
            
            // 绘制节点
            const node = g.selectAll(".node")
                .data(treeData.descendants())
                .enter().append("g")
                .attr("class", "node")
                .attr("transform", d => `translate(${d.y},${d.x})`)
                .on("click", (event, d) => this.selectNode(d.data.id));
            
            // 绘制节点圆圈
            node.append("circle")
                .attr("r", 10)
                .style("fill", d => {
                    const nodeData = this.visualizationData.nodes[d.data.id];
                    return nodeData.style.background_color;
                })
                .style("stroke", d => {
                    const nodeData = this.visualizationData.nodes[d.data.id];
                    return nodeData.style.border_color;
                })
                .style("stroke-width", d => {
                    const nodeData = this.visualizationData.nodes[d.data.id];
                    return nodeData.style.border_width;
                });
            
            // 绘制节点文本
            node.append("text")
                .attr("dy", ".35em")
                .attr("x", d => d.children ? -13 : 13)
                .style("text-anchor", d => d.children ? "end" : "start")
                .style("fill", d => {
                    const nodeData = this.visualizationData.nodes[d.data.id];
                    return nodeData.style.text_color;
                })
                .text(d => {
                    const nodeData = this.visualizationData.nodes[d.data.id];
                    return nodeData.data.question || nodeData.data.solution || d.data.id;
                });
        },
        
        selectNode(nodeId) {
            // 清除之前的选择
            d3.selectAll(".node").classed("selected", false);
            
            // 选择当前节点
            d3.selectAll(".node").filter(d => d.data.id === nodeId).classed("selected", true);
            
            // 加载节点数据到编辑器
            const nodeData = this.newNodes.nodes[nodeId];
            if (nodeData) {
                this.selectedNode = {
                    id: nodeId,
                    type: nodeData.question ? 'decision' : 'solution',
                    content: nodeData.question || nodeData.solution || '',
                    options: nodeData.options || []
                };
            }
        },
        
        addOption() {
            if (!this.selectedNode.options) {
                this.selectedNode.options = [];
            }
            this.selectedNode.options.push({
                text: '',
                nextNode: ''
            });
        },
        
        removeOption(index) {
            this.selectedNode.options.splice(index, 1);
        },
        
        async saveNodeChanges() {
            if (!this.selectedNode) return;
            
            const nodeData = {
                id: this.selectedNode.id,
                content: this.selectedNode.content
            };
            
            if (this.selectedNode.type === 'decision') {
                nodeData.question = this.selectedNode.content;
                nodeData.options = this.selectedNode.options;
            } else {
                nodeData.solution = this.selectedNode.content;
            }
            
            try {
                const response = await fetch('/api/update-node', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(nodeData)
                });
                
                if (response.ok) {
                    // 更新本地数据
                    this.newNodes.nodes[this.selectedNode.id] = nodeData;
                    this.generateChanges();
                    alert('节点修改已保存');
                }
            } catch (error) {
                console.error('保存失败:', error);
                alert('保存失败');
            }
        },
        
        async previewVisualization() {
            try {
                const response = await fetch('/api/preview');
                const data = await response.json();
                if (data.url) {
                    window.open(data.url, '_blank');
                }
            } catch (error) {
                console.error('预览失败:', error);
            }
        },
        
        async saveBackup() {
            try {
                const response = await fetch('/api/backup', {
                    method: 'POST'
                });
                const data = await response.json();
                if (data.success) {
                    alert('备份已保存');
                }
            } catch (error) {
                console.error('备份失败:', error);
            }
        },
        
        async confirmMerge() {
            if (confirm('确定要合并这些变更到决策树吗？')) {
                try {
                    const response = await fetch('/api/confirm-merge', {
                        method: 'POST'
                    });
                    const data = await response.json();
                    if (data.success) {
                        alert('合并成功！');
                        window.close();
                    }
                } catch (error) {
                    console.error('合并失败:', error);
                }
            }
        },
        
        cancelOperation() {
            if (confirm('确定要取消操作吗？')) {
                window.close();
            }
        }
    }
}).mount('#app');
        """
        
        with open(os.path.join(self.static_dir, "js", "app.js"), "w", encoding="utf-8") as f:
            f.write(js_content)
    
    def _register_routes(self):
        """注册Flask路由"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/api/data')
        def get_data():
            return jsonify({
                'originalTree': self.original_tree,
                'newNodes': self.new_nodes,
                'visualizationData': self._generate_visualization_data()
            })
        
        @self.app.route('/api/update-node', methods=['POST'])
        def update_node():
            data = request.json
            node_id = data['id']
            
            if node_id in self.new_nodes.get('nodes', {}):
                if data.get('question'):
                    self.new_nodes['nodes'][node_id] = {
                        'question': data['question'],
                        'options': data.get('options', [])
                    }
                else:
                    self.new_nodes['nodes'][node_id] = {
                        'solution': data['content']
                    }
            
            return jsonify({'success': True})
        
        @self.app.route('/api/preview')
        def preview():
            # 生成可视化文件
            from tree_visualizer import TreeVisualizer
            visualizer = TreeVisualizer()
            viz_data = visualizer.generate_visualization_data(self.original_tree, self.new_nodes)
            filename = visualizer.save_visualization(viz_data)
            
            return jsonify({'url': f'file://{os.path.abspath(filename)}'})
        
        @self.app.route('/api/backup', methods=['POST'])
        def backup():
            try:
                backup_data = {
                    'original_tree': self.original_tree,
                    'new_nodes': self.new_nodes,
                    'timestamp': datetime.now().isoformat()
                }
                
                backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                
                return jsonify({'success': True, 'file': backup_file})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/confirm-merge', methods=['POST'])
        def confirm_merge():
            try:
                # 合并决策树
                merged_tree = self._merge_trees()
                
                # 保存到文件
                from ai_tree_augmentor import AITreeAugmentor
                augmentor = AITreeAugmentor()
                augmentor._save_tree(merged_tree)
                
                self.result = {
                    'success': True,
                    'merged_tree': merged_tree
                }
                
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
    
    def _generate_visualization_data(self):
        """生成可视化数据"""
        from tree_visualizer import TreeVisualizer
        visualizer = TreeVisualizer()
        return visualizer.generate_visualization_data(self.original_tree, self.new_nodes)
    
    def _merge_trees(self):
        """合并决策树"""
        merged = self.original_tree.copy()
        
        # 合并节点
        if 'nodes' in self.new_nodes:
            merged['nodes'] = merged.get('nodes', {}).copy()
            merged['nodes'].update(self.new_nodes['nodes'])
        
        # 合并根节点（如果新树有根节点）
        if 'root_node' in self.new_nodes:
            merged['root_node'] = self.new_nodes['root_node']
        
        return merged
    
    def show_confirmation_dialog(self, original_tree: Dict, new_nodes: Dict, 
                                confirmation_message: str = None) -> Dict:
        """显示Web确认界面"""
        self.original_tree = original_tree
        self.new_nodes = new_nodes
        
        print("🌐 启动Web确认界面...")
        print("📱 界面将在浏览器中打开")
        
        # 启动Flask服务器
        def run_server():
            self.app.run(host='127.0.0.1', port=8080, debug=False)
        
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()
        
        # 等待服务器启动
        time.sleep(2)
        
        # 打开浏览器
        webbrowser.open('http://127.0.0.1:8080')
        
        # 等待用户操作完成
        print("⏳ 等待用户确认...")
        while self.result is None:
            time.sleep(1)
        
        return self.result

def main():
    """测试函数"""
    # 示例数据
    original_tree = {
        "root_node": "start",
        "nodes": {
            "start": {
                "question": "您遇到了什么类型的问题？",
                "options": [
                    {"text": "网络问题", "next_node": "network_issue"},
                    {"text": "硬件问题", "next_node": "hardware_issue"}
                ]
            }
        }
    }
    
    new_nodes = {
        "nodes": {
            "network_issue": {
                "question": "网络问题具体是什么？",
                "options": [
                    {"text": "无法连接", "next_node": "network_no_connection"},
                    {"text": "速度很慢", "next_node": "network_slow"}
                ]
            },
            "network_no_connection": {
                "solution": "请检查网络设置，重启路由器"
            }
        }
    }
    
    ui = WebConfirmationUI()
    result = ui.show_confirmation_dialog(original_tree, new_nodes, "发现新的网络问题处理流程")
    
    if result:
        print("合并结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 