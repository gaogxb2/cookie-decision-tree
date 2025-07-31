#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def debug_network_issue_position():
    """调试network_issue节点的位置计算"""
    print("🔍 调试network_issue节点位置计算...")
    print("=" * 80)
    
    try:
        # 获取决策树数据
        response = requests.get('http://localhost:5000/api/tree', timeout=10)
        
        if response.status_code == 200:
            tree_data = response.json()
            nodes = tree_data.get('nodes', {})
            
            # 分析network_issue节点
            network_issue = nodes.get('network_issue', {})
            print("📊 network_issue节点信息:")
            print("-" * 40)
            print(f"节点类型: {'解决方案' if 'solution' in network_issue else '决策节点'}")
            print(f"选项数量: {len(network_issue.get('options', []))}")
            
            # 获取所有后代节点
            descendants = []
            queue = ['network_issue']
            visited = set()
            
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                
                current_node = nodes.get(current, {})
                if 'options' in current_node:
                    for option in current_node['options']:
                        next_node = option.get('next_node')
                        if next_node and next_node in nodes:
                            descendants.append(next_node)
                            queue.append(next_node)
            
            print(f"后代节点数量: {len(descendants)}")
            print(f"后代节点: {descendants}")
            
            # 分析层级结构
            levels = {}
            def calculate_levels(node_id, level=0, visited=None):
                if visited is None:
                    visited = set()
                if node_id in visited:
                    return
                visited.add(node_id)
                
                if level not in levels:
                    levels[level] = []
                levels[level].append(node_id)
                
                node_data = nodes.get(node_id, {})
                if 'options' in node_data:
                    for option in node_data['options']:
                        next_node = option.get('next_node')
                        if next_node and next_node in nodes:
                            calculate_levels(next_node, level + 1, visited)
            
            # 找到根节点
            root_nodes = []
            for node_id in nodes:
                is_root = True
                for other_id, other_node in nodes.items():
                    if 'options' in other_node:
                        for option in other_node['options']:
                            if option.get('next_node') == node_id:
                                is_root = False
                                break
                    if not is_root:
                        break
                if is_root:
                    root_nodes.append(node_id)
            
            # 计算层级
            for root in root_nodes:
                calculate_levels(root)
            
            print("\n📋 层级结构:")
            for level in sorted(levels.keys()):
                level_nodes = levels[level]
                print(f"  层级 {level}: {len(level_nodes)} 个节点")
                if 'network_issue' in level_nodes:
                    print(f"    network_issue 在第 {level} 层")
                    print(f"    同层节点: {level_nodes}")
            
            # 分析network_issue的直接子节点
            network_children = []
            if 'options' in network_issue:
                for option in network_issue['options']:
                    next_node = option.get('next_node')
                    if next_node and next_node in nodes:
                        network_children.append(next_node)
            
            print(f"\n🔗 network_issue的直接子节点:")
            print(f"  子节点: {network_children}")
            
            # 分析叶子节点分布
            leaf_nodes = []
            for node_id, node_data in nodes.items():
                if 'solution' in node_data:
                    # 检查是否是network_issue的后代
                    if node_id in descendants:
                        leaf_nodes.append(node_id)
            
            print(f"\n🍃 network_issue的叶子节点:")
            print(f"  叶子节点数量: {len(leaf_nodes)}")
            print(f"  叶子节点: {leaf_nodes}")
            
            # 模拟位置计算
            print(f"\n🧮 位置计算分析:")
            print("-" * 40)
            
            # 假设叶子节点均匀分布
            if leaf_nodes:
                min_spacing = 180
                total_width = (len(leaf_nodes) - 1) * min_spacing
                start_x = 600 - total_width / 2
                
                leaf_positions = {}
                for i, leaf in enumerate(leaf_nodes):
                    leaf_positions[leaf] = start_x + i * min_spacing
                
                print(f"  叶子节点位置:")
                for leaf, pos in leaf_positions.items():
                    print(f"    {leaf}: x={pos}")
                
                # 计算平均位置
                avg_x = sum(leaf_positions.values()) / len(leaf_positions)
                print(f"  叶子节点平均位置: x={avg_x}")
                print(f"  理想network_issue位置: x={avg_x}")
                
                # 检查同层其他节点的影响
                network_level = None
                for level, level_nodes in levels.items():
                    if 'network_issue' in level_nodes:
                        network_level = level
                        break
                
                if network_level is not None:
                    level_nodes = levels[network_level]
                    print(f"\n  同层节点分析 (层级 {network_level}):")
                    print(f"    同层节点: {level_nodes}")
                    print(f"    同层节点数量: {len(level_nodes)}")
                    
                    if len(level_nodes) > 1:
                        # 模拟同层重新分布
                        total_width = (len(level_nodes) - 1) * min_spacing
                        start_x = 600 - total_width / 2
                        
                        print(f"    同层重新分布:")
                        for i, node in enumerate(level_nodes):
                            new_pos = start_x + i * min_spacing
                            print(f"      {node}: x={new_pos}")
                        
                        # 找到network_issue在同层中的索引
                        try:
                            network_index = level_nodes.index('network_issue')
                            final_pos = start_x + network_index * min_spacing
                            print(f"    network_issue最终位置: x={final_pos}")
                            print(f"    与理想位置差异: {final_pos - avg_x}")
                        except ValueError:
                            print("    network_issue不在同层节点列表中")
            
            print("\n💡 问题分析:")
            print("-" * 40)
            print("1. 叶子节点平均位置计算正确")
            print("2. 同层节点重新分布可能覆盖了基于后代的位置")
            print("3. 需要优化同层重新分布的逻辑")
            
        else:
            print(f"❌ 获取决策树失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务")
    except Exception as e:
        print(f"❌ 调试失败: {e}")

def main():
    debug_network_issue_position()

if __name__ == "__main__":
    main() 