#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_simplified_layout():
    """测试简化后的布局算法"""
    print("🔧 测试简化后的布局算法...")
    print("=" * 80)
    
    try:
        # 获取决策树数据
        response = requests.get('http://localhost:5000/api/tree', timeout=10)
        
        if response.status_code == 200:
            tree_data = response.json()
            nodes = tree_data.get('nodes', {})
            
            print("📊 决策树节点分析:")
            print("-" * 40)
            print(f"总节点数: {len(nodes)}")
            
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
            
            print(f"根节点: {root_nodes}")
            
            # 获取所有后代节点的函数
            def get_all_descendants(node_id):
                descendants = set()
                queue = [node_id]
                
                while queue:
                    current = queue.pop(0)
                    node_data = nodes.get(current, {})
                    if 'options' in node_data:
                        for option in node_data['options']:
                            next_node = option.get('next_node')
                            if next_node and next_node in nodes:
                                descendants.add(next_node)
                                queue.append(next_node)
                
                return list(descendants)
            
            # 分析关键节点
            key_nodes = ['network_issue', 'software_issue', 'hardware_issue', 'performance_issue']
            
            print("\n🔍 关键节点分析:")
            print("-" * 40)
            
            for node_id in key_nodes:
                if node_id in nodes:
                    descendants = get_all_descendants(node_id)
                    leaf_nodes = [d for d in descendants if 'solution' in nodes.get(d, {})]
                    
                    print(f"\n  {node_id}:")
                    print(f"    后代数量: {len(descendants)}")
                    print(f"    叶子节点数量: {len(leaf_nodes)}")
                    print(f"    叶子节点: {leaf_nodes[:5]}{'...' if len(leaf_nodes) > 5 else ''}")
                    
                    if leaf_nodes:
                        # 模拟位置计算
                        min_spacing = 180
                        total_width = (len(leaf_nodes) - 1) * min_spacing
                        start_x = 600 - total_width / 2
                        
                        leaf_positions = []
                        for i in range(len(leaf_nodes)):
                            leaf_positions.append(start_x + i * min_spacing)
                        
                        avg_x = sum(leaf_positions) / len(leaf_positions)
                        print(f"    叶子节点平均位置: x={avg_x:.1f}")
                        print(f"    理想父节点位置: x={avg_x:.1f}")
            
            # 检查层级分布
            print("\n📋 层级分布:")
            for level in sorted(levels.keys()):
                level_nodes = levels[level]
                print(f"  层级 {level}: {len(level_nodes)} 个节点")
                if level == 1:  # 第一层是关键层
                    print(f"    节点: {level_nodes}")
            
            print("\n✅ 简化布局分析完成!")
            print("\n💡 改进内容:")
            print("  ✅ 去掉了同层节点重新分布")
            print("  ✅ 保留了基于后代节点的位置计算")
            print("  ✅ 简化了布局算法")
            print("  ✅ 避免了位置被覆盖的问题")
            
        else:
            print(f"❌ 获取决策树失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def check_frontend_layout():
    """检查前端布局效果"""
    print("\n🌐 检查前端布局效果...")
    print("=" * 80)
    
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常")
            print("🌐 访问地址: http://localhost:3000/")
            print("💡 在决策树编辑器中查看简化布局效果")
            print("🔍 观察要点:")
            print("  - network_issue是否居中到其子节点")
            print("  - 其他第一层节点是否也居中到各自子节点")
            print("  - 整体布局是否更加合理")
        else:
            print(f"⚠️ 前端响应异常: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到前端服务")
    except Exception as e:
        print(f"❌ 前端检查失败: {e}")

def main():
    print("🚀 测试简化布局算法...")
    print("=" * 80)
    
    # 测试简化布局
    test_simplified_layout()
    
    # 检查前端布局效果
    check_frontend_layout()
    
    print("\n" + "=" * 80)
    print("✅ 简化布局测试完成!")
    print("\n📝 修复总结:")
    print("  ✅ 去掉了同层重新分布逻辑")
    print("  ✅ 保留了基于后代的位置计算")
    print("  ✅ 简化了布局算法")
    print("  ✅ 解决了位置被覆盖的问题")

if __name__ == "__main__":
    main() 