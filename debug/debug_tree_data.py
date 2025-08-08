#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import yaml

def debug_tree_data():
    """调试决策树数据"""
    print("[DEBUG] 调试决策树数据...")
    
    try:
        # 1. 检查API返回的数据
        print("📡 检查API数据...")
        response = requests.get('http://localhost:5000/api/tree')
        if response.status_code == 200:
            api_data = response.json()
            print(f"[OK] API节点数: {len(api_data.get('nodes', {}))}")
            print(f"[OK] API根节点: {api_data.get('root_node', 'N/A')}")
            
            # 显示前几个节点
            nodes = api_data.get('nodes', {})
            print("\n前5个节点:")
            for i, (node_id, node_data) in enumerate(list(nodes.items())[:5]):
                print(f"  {i+1}. {node_id}: {node_data.get('question', node_data.get('solution', 'N/A'))[:50]}")
        else:
            print(f"[ERROR] API请求失败: {response.status_code}")
            return False
        
        # 2. 检查文件数据
        print("\n检查文件数据...")
        try:
            with open('config/decision_tree.yaml', 'r', encoding='utf-8') as f:
                file_data = yaml.safe_load(f)
                tree_data = file_data.get('decision_tree', {})
                print(f"[OK] 文件节点数: {len(tree_data.get('nodes', {}))}")
                print(f"[OK] 文件根节点: {tree_data.get('root_node', 'N/A')}")
                
                # 显示新增的节点（如果有）
                nodes = tree_data.get('nodes', {})
                new_nodes = [node_id for node_id in nodes.keys() if 'wifi' in node_id.lower() or 'restart' in node_id.lower()]
                if new_nodes:
                    print(f"\n🆕 可能的AI新增节点:")
                    for node_id in new_nodes:
                        node_data = nodes[node_id]
                        print(f"  - {node_id}: {node_data.get('question', node_data.get('solution', 'N/A'))[:50]}")
                else:
                    print("\n未发现明显的AI新增节点")
        except Exception as e:
            print(f"[ERROR] 文件读取失败: {e}")
            return False
        
        # 3. 比较API和文件数据
        print("\n[DEBUG] 数据一致性检查...")
        api_nodes = set(api_data.get('nodes', {}).keys())
        file_nodes = set(tree_data.get('nodes', {}).keys())
        
        if api_nodes == file_nodes:
            print("[OK] API和文件数据一致")
        else:
            print("[ERROR] API和文件数据不一致")
            print(f"  API独有节点: {api_nodes - file_nodes}")
            print(f"  文件独有节点: {file_nodes - api_nodes}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 调试失败: {e}")
        return False

def main():
    """主函数"""
    print("开始调试决策树数据...")
    
    success = debug_tree_data()
    
    if success:
        print("\n[OK] 调试完成")
        print("💡 如果数据正常但界面不显示，可能是浏览器缓存问题")
        print("🔄 建议: 刷新浏览器页面 (Ctrl+F5)")
    else:
        print("\n[ERROR] 调试失败")

if __name__ == "__main__":
    main() 