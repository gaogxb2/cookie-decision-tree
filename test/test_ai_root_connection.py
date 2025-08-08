#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_ai_root_connection():
    """测试AI增强的根节点连接功能"""
    print("🧪 测试AI增强根节点连接...")
    
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
        # 1. 测试AI处理
        print("📡 步骤1: 测试AI处理...")
        response = requests.post(
            'http://localhost:5000/api/ai/process-chat',
            json={
                'chat_history': chat_history,
                'auto_merge': False
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            print(f"[ERROR] AI处理失败: {response.status_code}")
            return False
        
        result = response.json()
        if not result.get('success'):
            print(f"[ERROR] AI处理失败: {result.get('error')}")
            return False
        
        print("[OK] AI处理成功")
        
        # 检查新节点是否有根节点
        new_nodes = result.get('new_nodes', {})
        if 'root_node' in new_nodes:
            print(f"[OK] 新节点有根节点: {new_nodes['root_node']}")
        else:
            print("[ERROR] 新节点没有根节点")
            return False
        
        # 2. 测试确认变更
        print("📡 步骤2: 测试确认变更...")
        confirm_response = requests.post(
            'http://localhost:5000/api/ai/confirm-changes',
            json={
                'new_nodes': new_nodes
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if confirm_response.status_code != 200:
            print(f"[ERROR] 确认变更失败: {confirm_response.status_code}")
            return False
        
        confirm_result = confirm_response.json()
        if not confirm_result.get('success'):
            print(f"[ERROR] 确认变更失败: {confirm_result.get('error')}")
            return False
        
        print("[OK] 确认变更成功")
        
        # 3. 验证决策树根节点连接
        print("📡 步骤3: 验证根节点连接...")
        time.sleep(2)  # 等待文件写入
        
        tree_response = requests.get('http://localhost:5000/api/tree')
        if tree_response.status_code == 200:
            tree_data = tree_response.json()
            root_node = tree_data.get('root_node', '')
            nodes = tree_data.get('nodes', {})
            
            print(f"[OK] 决策树根节点: {root_node}")
            print(f"[OK] 节点总数: {len(nodes)}")
            
            # 检查根节点是否有选项
            if root_node and root_node in nodes:
                root_options = nodes[root_node].get('options', [])
                print(f"[OK] 根节点选项数: {len(root_options)}")
                
                # 检查是否有网络相关选项
                network_options = [opt for opt in root_options if 'wifi' in opt.get('text', '').lower() or 'network' in opt.get('text', '').lower()]
                if network_options:
                    print(f"[OK] 发现网络相关选项: {len(network_options)}")
                    for opt in network_options:
                        print(f"  - {opt['text']} -> {opt.get('next_node', 'N/A')}")
                else:
                    print("[WARNING] 未发现网络相关选项")
            else:
                print("[ERROR] 根节点不存在或无效")
                return False
        else:
            print("[ERROR] 无法获取决策树数据")
            return False
        
        print(" AI增强根节点连接测试通过！")
        return True
        
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print(" 开始AI增强根节点连接测试...")
    
    success = test_ai_root_connection()
    
    if success:
        print("\n[OK] 测试通过！")
        print("📱 请在浏览器中访问: http://localhost:3001")
        print("[AI] 在编辑器中切换到'AI增强'标签页进行测试")
        print("💡 提示: 新增的节点现在应该连接到根节点了")
    else:
        print("\n[ERROR] 测试失败")

if __name__ == "__main__":
    main() 