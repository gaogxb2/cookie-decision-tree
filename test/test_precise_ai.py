#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
from datetime import datetime

def test_precise_ai():
    """测试AI是否严格按照聊天记录生成决策树"""
    print("🧪 测试AI精确生成决策树...")
    
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
        
        print(f"[TIME] 处理时间: {processing_time:.2f}秒")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                new_nodes = result.get('new_nodes', {})
                
                print("\n AI生成的节点分析:")
                print("-" * 50)
                
                # 分析节点数量
                if 'nodes' in new_nodes:
                    nodes = new_nodes['nodes']
                    print(f"[OK] 节点总数: {len(nodes)}")
                    
                    # 检查是否只包含聊天记录中的内容
                    expected_nodes = [
                        'network_connection_issue', 'wifi_connection', 'check_wifi_switch',
                        'restart_router', 'check_network_adapter', 'update_driver'
                    ]
                    
                    print("\n[DEBUG] 节点内容分析:")
                    for node_id, node_data in nodes.items():
                        if 'question' in node_data:
                            question = node_data['question']
                            print(f"  📝 {node_id}: {question}")
                        elif 'solution' in node_data:
                            solution = node_data['solution']
                            print(f"  💡 {node_id}: {solution}")
                    
                    # 检查是否有聊天记录中没有的内容
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
                        print(f"\n[WARNING] 发现可能超出聊天记录的内容:")
                        for node in unexpected_nodes[:5]:  # 只显示前5个
                            print(f"  - {node}")
                        print(f"  ... 还有 {len(unexpected_nodes)-5} 个节点")
                    else:
                        print("\n[OK] 所有节点都基于聊天记录内容")
                        
                else:
                    print("[ERROR] 没有找到nodes字段")
                    
            else:
                print(f"[ERROR] AI处理失败: {result.get('error')}")
        else:
            print(f"[ERROR] 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")

def main():
    """主函数"""
    print(" 开始测试AI精确生成决策树...")
    
    test_precise_ai()
    
    print("\n📝 测试完成")
    print("💡 如果AI仍然添加了额外内容，可能需要进一步调整prompt")

if __name__ == "__main__":
    main() 