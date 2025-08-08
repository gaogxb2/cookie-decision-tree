#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def debug_ai_response():
    """调试AI响应"""
    print("调试AI响应...")
    
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
        response = requests.post(
            'http://localhost:5000/api/ai/process-chat',
            json={
                'chat_history': chat_history,
                'auto_merge': False
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                new_nodes = result.get('new_nodes', {})
                print("AI响应结构:")
                print(json.dumps(new_nodes, ensure_ascii=False, indent=2))
                
                # 检查关键字段
                print("\n字段检查:")
                print(f"  entry_node: {'[OK]' if 'entry_node' in new_nodes else '[FAIL]'}")
                print(f"  nodes: {'[OK]' if 'nodes' in new_nodes else '[FAIL]'}")
                print(f"  root_node: {'[OK]' if 'root_node' in new_nodes else '[FAIL]'}")
                
                if 'nodes' in new_nodes:
                    nodes = new_nodes['nodes']
                    print(f"  节点数量: {len(nodes)}")
                    print("  节点列表:")
                    for node_id in list(nodes.keys())[:5]:  # 显示前5个节点
                        node_data = nodes[node_id]
                        node_type = "决策节点" if 'question' in node_data else "解决方案节点"
                        print(f"    - {node_id}: {node_type}")
            else:
                print(f"[ERROR] AI处理失败: {result.get('error')}")
        else:
            print(f"[ERROR] 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] 调试失败: {e}")

if __name__ == "__main__":
    debug_ai_response() 