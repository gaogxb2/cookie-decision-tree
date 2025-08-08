#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def debug_ai_path_response():
    """调试AI的路径响应"""
    print("[DEBUG] 调试AI路径响应...")
    
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
            print("AI原始响应:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            if result.get('success'):
                new_nodes = result.get('new_nodes', {})
                print("\n[DEBUG] 响应结构分析:")
                print(f"  problem: {'[OK]' if 'problem' in new_nodes else '[ERROR]'}")
                print(f"  steps: {'[OK]' if 'steps' in new_nodes else '[ERROR]'}")
                print(f"  solution: {'[OK]' if 'solution' in new_nodes else '[ERROR]'}")
                print(f"  nodes: {'[OK]' if 'nodes' in new_nodes else '[ERROR]'}")
                print(f"  entry_node: {'[OK]' if 'entry_node' in new_nodes else '[ERROR]'}")
                
                if 'steps' in new_nodes:
                    steps = new_nodes['steps']
                    print(f"\n路径步骤 ({len(steps)} 步):")
                    for step in steps:
                        print(f"  步骤 {step.get('step', 'N/A')}: {step.get('question', 'N/A')} -> {step.get('answer', 'N/A')}")
                elif 'nodes' in new_nodes:
                    print(f"\nAI返回了决策树结构而不是路径")
                    nodes = new_nodes['nodes']
                    print(f"  节点数量: {len(nodes)}")
                    
                    # 检查是否有路径相关的节点
                    path_nodes = [k for k in nodes.keys() if 'step_' in k or 'solution' in k]
                    if path_nodes:
                        print(f"  发现路径节点: {path_nodes}")
                    else:
                        print("  没有发现路径节点")
            else:
                print(f"[ERROR] AI处理失败: {result.get('error')}")
        else:
            print(f"[ERROR] 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] 调试失败: {e}")

if __name__ == "__main__":
    debug_ai_path_response() 