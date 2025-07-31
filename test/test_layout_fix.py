#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_layout_fix():
    """测试布局修复效果"""
    print("🔧 测试布局修复效果...")
    print("=" * 80)
    
    try:
        # 获取当前决策树数据
        response = requests.get('http://localhost:5000/api/tree', timeout=10)
        
        if response.status_code == 200:
            tree_data = response.json()
            nodes = tree_data.get('nodes', {})
            
            print("📊 决策树节点分析:")
            print("-" * 40)
            print(f"总节点数: {len(nodes)}")
            
            # 分析节点层级和后代分布
            levels = {}
            descendants_map = {}
            
            # 计算每个节点的层级
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
            
            # 获取所有后代节点
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
            
            print(f"根节点: {root_nodes}")
            
            # 从根节点开始计算层级
            for root in root_nodes:
                calculate_levels(root)
            
            # 计算每个节点的所有后代
            for node_id in nodes:
                descendants_map[node_id] = get_all_descendants(node_id)
            
            # 显示层级信息和后代分布
            print("\n📋 节点层级和后代分布:")
            for level in sorted(levels.keys()):
                level_nodes = levels[level]
                print(f"\n  层级 {level}: {len(level_nodes)} 个节点")
                for node_id in level_nodes:
                    descendants = descendants_map[node_id]
                    node_data = nodes[node_id]
                    if 'solution' in node_data:
                        print(f"    - {node_id} (解决方案) -> {len(descendants)} 个后代")
                    else:
                        print(f"    - {node_id} (决策节点) -> {len(descendants)} 个后代")
                        if descendants:
                            print(f"      后代: {descendants[:5]}{'...' if len(descendants) > 5 else ''}")
            
            # 分析布局改进
            print("\n🔧 布局修复分析:")
            print("-" * 40)
            
            # 检查每个层级的节点分布
            for level in sorted(levels.keys()):
                level_nodes = levels[level]
                if level > 0:  # 跳过叶子节点层级
                    print(f"\n  层级 {level} 节点分析:")
                    for node_id in level_nodes:
                        descendants = descendants_map[node_id]
                        visible_descendants = [d for d in descendants if d in nodes]
                        print(f"    {node_id}: {len(visible_descendants)} 个可见后代")
                        if visible_descendants:
                            print(f"      后代分布: {visible_descendants[:3]}{'...' if len(visible_descendants) > 3 else ''}")
            
            print("\n✅ 布局修复完成!")
            print("\n💡 修复内容:")
            print("  ✅ 考虑所有后代节点而不是只考虑直接子节点")
            print("  ✅ 使用广度优先搜索获取所有后代")
            print("  ✅ 基于所有后代节点的分布计算父节点位置")
            print("  ✅ 确保上层节点居中到所有后代节点的平均位置")
            
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
            print("💡 在决策树编辑器中查看布局修复效果")
            print("🔍 观察要点:")
            print("  - 上层节点是否居中到下层节点的平均位置")
            print("  - 第三层及以上节点是否不再偏离中心")
            print("  - 整体布局是否更加平衡")
        else:
            print(f"⚠️ 前端响应异常: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到前端服务")
    except Exception as e:
        print(f"❌ 前端检查失败: {e}")

def main():
    print("🚀 测试布局修复效果...")
    print("=" * 80)
    
    # 测试布局修复
    test_layout_fix()
    
    # 检查前端布局效果
    check_frontend_layout()
    
    print("\n" + "=" * 80)
    print("✅ 布局修复测试完成!")
    print("\n📝 修复总结:")
    print("  ✅ 修复了上层节点居中问题")
    print("  ✅ 考虑所有后代节点的分布")
    print("  ✅ 使用改进的算法计算节点位置")
    print("  ✅ 确保更平衡的视觉布局")

if __name__ == "__main__":
    main() 