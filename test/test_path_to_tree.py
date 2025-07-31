#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_path_to_tree():
    """测试路径转决策树的方法"""
    print("🧪 测试路径转决策树方法...")
    
    # 测试聊天记录
    chat_history = """
用户: 我的电脑无法连接网络了
客服: 请问是WiFi还是有线连接？
用户: WiFi连接
客服: 请检查WiFi开关是否打开
用户: 开关是打开的
客服: 请尝试重启路由器
用户: 重启后还是不行
客服: 请检查网络适配器驱动是否正常
用户: 怎么检查？
客服: 在设备管理器中查看网络适配器是否有感叹号
用户: 有感叹号，显示驱动有问题
客服: 请更新或重新安装网络适配器驱动
用户: 更新后可以连接了，谢谢
    """
    
    try:
        print("📡 发送API请求...")
        start_time = time.time()
        
        response = requests.post(
            'http://localhost:5000/api/ai/process-chat',
            json={
                'chat_history': chat_history,
                'auto_merge': False
            },
            headers={'Content-Type': 'application/json'}
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"⏱️ 处理时间: {processing_time:.2f}秒")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                new_nodes = result.get('new_nodes', {})
                
                print("\n📋 生成的决策树分析:")
                print("-" * 50)
                
                # 分析节点数量
                if 'nodes' in new_nodes:
                    nodes = new_nodes['nodes']
                    print(f"✅ 节点总数: {len(nodes)}")
                    
                    # 显示节点内容
                    print("\n🔍 节点内容:")
                    for node_id, node_data in nodes.items():
                        if 'question' in node_data:
                            question = node_data['question']
                            options = node_data.get('options', [])
                            print(f"  📝 {node_id}: {question}")
                            for opt in options:
                                print(f"    - {opt['text']} -> {opt.get('next_node', 'N/A')}")
                        elif 'solution' in node_data:
                            solution = node_data['solution']
                            print(f"  💡 {node_id}: {solution}")
                    
                    # 检查是否只包含聊天记录中的内容
                    chat_keywords = ['网络', 'WiFi', '开关', '路由器', '网络适配器', '驱动', '感叹号', '更新']
                    unexpected_nodes = []
                    
                    for node_id, node_data in nodes.items():
                        node_text = ""
                        if 'question' in node_data:
                            node_text = node_data['question']
                        elif 'solution' in node_data:
                            node_text = node_data['solution']
                        
                        # 检查是否包含聊天记录中没有的关键词
                        has_unexpected_content = True
                        for keyword in chat_keywords:
                            if keyword in node_text:
                                has_unexpected_content = False
                                break
                        
                        if has_unexpected_content and len(node_text) > 10:
                            unexpected_nodes.append(f"{node_id}: {node_text}")
                    
                    if unexpected_nodes:
                        print(f"\n⚠️ 发现可能超出聊天记录的内容:")
                        for node in unexpected_nodes:
                            print(f"  - {node}")
                    else:
                        print("\n✅ 所有节点都基于聊天记录内容")
                        
                else:
                    print("❌ 没有找到nodes字段")
                    
            else:
                print(f"❌ AI处理失败: {result.get('error')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def main():
    """主函数"""
    print("🚀 开始测试路径转决策树方法...")
    
    test_path_to_tree()
    
    print("\n📝 测试完成")
    print("💡 如果节点数量大幅减少且都基于聊天记录，说明方法有效")

if __name__ == "__main__":
    main() 