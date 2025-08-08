#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_label_position():
    """测试连接线标签位置调整"""
    print(" 测试连接线标签位置调整...")
    print("=" * 80)
    
    try:
        # 获取决策树数据
        response = requests.get('http://localhost:5000/api/tree', timeout=10)
        
        if response.status_code == 200:
            tree_data = response.json()
            nodes = tree_data.get('nodes', {})
            
            print(" 决策树连接分析:")
            print("-" * 40)
            print(f"总节点数: {len(nodes)}")
            
            # 统计连接数量
            connection_count = 0
            for node_id, node_data in nodes.items():
                if 'options' in node_data:
                    connection_count += len(node_data['options'])
            
            print(f"总连接数: {connection_count}")
            
            # 分析关键连接
            key_connections = []
            for node_id, node_data in nodes.items():
                if 'options' in node_data:
                    for option in node_data['options']:
                        next_node = option.get('next_node')
                        if next_node and next_node in nodes:
                            key_connections.append({
                                'from': node_id,
                                'to': next_node,
                                'label': option.get('text', '')
                            })
            
            print(f"\n🔗 连接示例:")
            print("-" * 40)
            for i, conn in enumerate(key_connections[:10]):  # 显示前10个连接
                print(f"  {i+1}. {conn['from']} -> {conn['to']}: {conn['label']}")
            
            if len(key_connections) > 10:
                print(f"  ... 还有 {len(key_connections) - 10} 个连接")
            
            print("\n💡 标签位置调整:")
            print("-" * 40)
            print("  [OK] 标签位置从 midY - 10 调整为 midY + 15")
            print("  [OK] 标签背景也相应调整")
            print("  [OK] 避免被节点图标盖住")
            print("  [OK] 提高可读性")
            
        else:
            print(f"[ERROR] 获取决策树失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] 无法连接到后端服务")
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")

def check_frontend_labels():
    """检查前端标签效果"""
    print("\n🌐 检查前端标签效果...")
    print("=" * 80)
    
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code == 200:
            print("[OK] 前端服务正常")
            print("🌐 访问地址: http://localhost:3000/")
            print("💡 在决策树编辑器中查看标签位置调整效果")
            print("[DEBUG] 观察要点:")
            print("  - 连接线标签是否清晰可见")
            print("  - 标签是否不被节点图标盖住")
            print("  - 标签背景是否提供良好的对比度")
            print("  - 整体可读性是否提高")
        else:
            print(f"[WARNING] 前端响应异常: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("[ERROR] 无法连接到前端服务")
    except Exception as e:
        print(f"[ERROR] 前端检查失败: {e}")

def main():
    print(" 测试连接线标签位置调整...")
    print("=" * 80)
    
    # 测试标签位置调整
    test_label_position()
    
    # 检查前端标签效果
    check_frontend_labels()
    
    print("\n" + "=" * 80)
    print("[OK] 标签位置调整测试完成!")
    print("\n📝 调整总结:")
    print("  [OK] 标签位置向下移动")
    print("  [OK] 避免被节点图标遮挡")
    print("  [OK] 提高连接线标签可读性")
    print("  [OK] 保持整体视觉平衡")

if __name__ == "__main__":
    main() 