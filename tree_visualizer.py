#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import json
from typing import Dict, List, Optional, Set
from datetime import datetime

class TreeVisualizer:
    def __init__(self, config_file: str = "config/ai_config.yaml"):
        """初始化决策树可视化器"""
        self.config = self._load_config(config_file)
        self.styles = self.config['tree_augment']
        
    def _load_config(self, config_file: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[ERROR] 加载配置文件失败: {e}")
            sys.exit(1)
    
    def _get_node_style(self, node_id: str, node_type: str, is_new: bool = False, is_modified: bool = False) -> Dict:
        """获取节点样式"""
        if is_new:
            return {
                "background_color": self.styles['new_node_style']['background_color'],
                "border_color": self.styles['new_node_style']['border_color'],
                "text_color": self.styles['new_node_style']['text_color'],
                "border_width": 2,
                "border_style": "solid"
            }
        elif is_modified:
            return {
                "background_color": self.styles['modified_node_style']['background_color'],
                "border_color": self.styles['modified_node_style']['border_color'],
                "text_color": self.styles['modified_node_style']['text_color'],
                "border_width": 2,
                "border_style": "dashed"
            }
        else:
            return {
                "background_color": "#ffffff",
                "border_color": "#cccccc",
                "text_color": "#000000",
                "border_width": 1,
                "border_style": "solid"
            }
    
    def _get_relation_style(self, is_new: bool = False) -> Dict:
        """获取关系样式"""
        if is_new:
            return {
                "stroke_color": self.styles['new_relation_style']['stroke_color'],
                "stroke_width": self.styles['new_relation_style']['stroke_width'],
                "stroke_dasharray": self.styles['new_relation_style']['stroke_dasharray']
            }
        else:
            return {
                "stroke_color": "#666666",
                "stroke_width": 1,
                "stroke_dasharray": "none"
            }
    
    def generate_visualization_data(self, original_tree: Dict, new_nodes: Dict, 
                                  modified_nodes: Set = None) -> Dict:
        """生成可视化数据"""
        print("生成可视化数据...")
        
        # 合并原始树和新节点
        merged_tree = self._merge_trees(original_tree, new_nodes)
        
        # 识别新增和修改的节点
        new_node_ids = set(new_nodes.get('nodes', {}).keys())
        modified_node_ids = modified_nodes or set()
        
        # 生成可视化数据
        visualization_data = {
            "nodes": {},
            "relations": [],
            "metadata": {
                "original_node_count": len(original_tree.get('nodes', {})),
                "new_node_count": len(new_node_ids),
                "modified_node_count": len(modified_node_ids),
                "total_node_count": len(merged_tree.get('nodes', {})),
                "generated_at": datetime.now().isoformat()
            }
        }
        
        # 处理节点
        for node_id, node_data in merged_tree.get('nodes', {}).items():
            is_new = node_id in new_node_ids
            is_modified = node_id in modified_node_ids
            
            visualization_data["nodes"][node_id] = {
                "id": node_id,
                "data": node_data,
                "style": self._get_node_style(node_id, node_data.get('type', 'decision'), 
                                            is_new, is_modified),
                "status": self._get_node_status(is_new, is_modified)
            }
        
        # 处理关系
        relations = self._extract_relations(merged_tree)
        for relation in relations:
            is_new = relation['from'] in new_node_ids or relation['to'] in new_node_ids
            visualization_data["relations"].append({
                **relation,
                "style": self._get_relation_style(is_new)
            })
        
        return visualization_data
    
    def _merge_trees(self, original_tree: Dict, new_nodes: Dict) -> Dict:
        """合并决策树"""
        merged = original_tree.copy()
        
        # 合并节点
        if 'nodes' in new_nodes:
            merged['nodes'] = merged.get('nodes', {}).copy()
            merged['nodes'].update(new_nodes['nodes'])
        
        # 合并根节点（如果新树有根节点）
        if 'root_node' in new_nodes:
            merged['root_node'] = new_nodes['root_node']
        
        return merged
    
    def _extract_relations(self, tree: Dict) -> List[Dict]:
        """提取节点关系"""
        relations = []
        nodes = tree.get('nodes', {})
        
        for node_id, node_data in nodes.items():
            if 'options' in node_data:
                for option in node_data['options']:
                    if 'next_node' in option:
                        relations.append({
                            'from': node_id,
                            'to': option['next_node'],
                            'label': option.get('text', ''),
                            'condition': option.get('condition', '')
                        })
        
        return relations
    
    def _get_node_status(self, is_new: bool, is_modified: bool) -> str:
        """获取节点状态"""
        if is_new:
            return "new"
        elif is_modified:
            return "modified"
        else:
            return "original"
    
    def generate_diff_report(self, original_tree: Dict, new_nodes: Dict) -> Dict:
        """生成差异报告"""
        print(" 生成差异报告...")
        
        original_nodes = set(original_tree.get('nodes', {}).keys())
        new_node_ids = set(new_nodes.get('nodes', {}).keys())
        
        # 新增的节点
        added_nodes = new_node_ids - original_nodes
        
        # 修改的节点（在原始树中也存在的节点）
        modified_nodes = new_node_ids & original_nodes
        
        # 删除的节点（在原始树中存在但新树中不存在的节点）
        deleted_nodes = original_nodes - new_node_ids
        
        return {
            "summary": {
                "added": len(added_nodes),
                "modified": len(modified_nodes),
                "deleted": len(deleted_nodes),
                "total_changes": len(added_nodes) + len(modified_nodes) + len(deleted_nodes)
            },
            "details": {
                "added_nodes": list(added_nodes),
                "modified_nodes": list(modified_nodes),
                "deleted_nodes": list(deleted_nodes)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_html_visualization(self, visualization_data: Dict) -> str:
        """生成HTML可视化"""
        print("🌐 生成HTML可视化...")
        
        html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>决策树可视化</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        .node {
            cursor: pointer;
        }
        .node circle {
            stroke-width: 2px;
        }
        .node text {
            font: 12px sans-serif;
        }
        .link {
            fill: none;
            stroke-width: 2px;
        }
        .legend {
            font: 12px sans-serif;
        }
        .legend-item {
            display: inline-block;
            margin-right: 20px;
        }
        .legend-color {
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 5px;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <div id="visualization">
        <div class="legend">
            <div class="legend-item">
                <span class="legend-color" style="background-color: #ffffff; border-color: #cccccc;"></span>
                原始节点
            </div>
            <div class="legend-item">
                <span class="legend-color" style="background-color: #e3f2fd; border-color: #2196f3;"></span>
                新增节点
            </div>
            <div class="legend-item">
                <span class="legend-color" style="background-color: #fff3e0; border-color: #ff9800;"></span>
                修改节点
            </div>
        </div>
        <div id="tree-container"></div>
    </div>
    
    <script>
        const data = {visualization_data};
        
        // 设置画布
        const width = 1200;
        const height = 800;
        const margin = {top: 20, right: 90, bottom: 30, left: 90};
        
        const svg = d3.select("#tree-container")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
        
        const g = svg.append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);
        
        // 创建层次结构
        const nodes = Object.values(data.nodes);
        const links = data.relations;
        
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
                .y(d => d.x));
        
        // 应用连接线样式
        link.each(function(d) {
            const linkData = links.find(l => l.from === d.source.id && l.to === d.target.id);
            if (linkData) {
                d3.select(this)
                    .style("stroke", linkData.style.stroke_color)
                    .style("stroke-width", linkData.style.stroke_width)
                    .style("stroke-dasharray", linkData.style.stroke_dasharray);
            }
        });
        
        // 绘制节点
        const node = g.selectAll(".node")
            .data(treeData.descendants())
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${d.y},${d.x})`);
        
        // 绘制节点圆圈
        node.append("circle")
            .attr("r", 10)
            .style("fill", d => {
                const nodeData = data.nodes[d.data.id];
                return nodeData.style.background_color;
            })
            .style("stroke", d => {
                const nodeData = data.nodes[d.data.id];
                return nodeData.style.border_color;
            })
            .style("stroke-width", d => {
                const nodeData = data.nodes[d.data.id];
                return nodeData.style.border_width;
            });
        
        // 绘制节点文本
        node.append("text")
            .attr("dy", ".35em")
            .attr("x", d => d.children ? -13 : 13)
            .style("text-anchor", d => d.children ? "end" : "start")
            .style("fill", d => {
                const nodeData = data.nodes[d.data.id];
                return nodeData.style.text_color;
            })
            .text(d => {
                const nodeData = data.nodes[d.data.id];
                return nodeData.data.question || nodeData.data.solution || d.data.id;
            });
    </script>
</body>
</html>
        """
        
        return html_template.format(visualization_data=json.dumps(visualization_data, ensure_ascii=False))
    
    def save_visualization(self, visualization_data: Dict, output_file: str = "tree_visualization.html"):
        """保存可视化文件"""
        html_content = self.generate_html_visualization(visualization_data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[OK] 可视化文件已保存: {output_file}")
        return output_file

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
            },
            "network_issue": {
                "question": "网络问题具体是什么？",
                "options": [
                    {"text": "无法连接", "next_node": "network_no_connection"},
                    {"text": "速度很慢", "next_node": "network_slow"}
                ]
            }
        }
    }
    
    new_nodes = {
        "nodes": {
            "network_no_connection": {
                "question": "无法连接网络，请选择连接方式",
                "options": [
                    {"text": "WiFi连接", "next_node": "wifi_issue"},
                    {"text": "有线连接", "next_node": "ethernet_issue"}
                ]
            },
            "wifi_issue": {
                "solution": "请检查WiFi开关，重启路由器，更新网络驱动"
            },
            "ethernet_issue": {
                "solution": "请检查网线连接，更换网线或端口"
            }
        }
    }
    
    visualizer = TreeVisualizer()
    
    # 生成可视化数据
    viz_data = visualizer.generate_visualization_data(original_tree, new_nodes)
    
    # 生成差异报告
    diff_report = visualizer.generate_diff_report(original_tree, new_nodes)
    
    # 保存可视化文件
    output_file = visualizer.save_visualization(viz_data)
    
    print("可视化数据:")
    print(json.dumps(viz_data, ensure_ascii=False, indent=2))
    print("\n差异报告:")
    print(json.dumps(diff_report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 