#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_ai_workflow():
    """测试AI增强完整工作流程"""
    print("🧪 测试AI增强完整工作流程...")
    
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
        print(f" 生成变更: {len(result.get('changes', []))}")
        
        # 2. 测试确认变更
        print("📡 步骤2: 测试确认变更...")
        new_nodes = result.get('new_nodes', {})
        if not new_nodes:
            print("[ERROR] 没有生成新节点")
            return False
        
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
        
        # 3. 验证决策树已更新
        print("📡 步骤3: 验证决策树更新...")
        time.sleep(2)  # 等待文件写入
        
        tree_response = requests.get('http://localhost:5000/api/tree')
        if tree_response.status_code == 200:
            tree_data = tree_response.json()
            node_count = len(tree_data.get('nodes', {}))
            print(f"[OK] 决策树已更新，当前节点数: {node_count}")
        else:
            print("[ERROR] 无法获取决策树数据")
            return False
        
        print(" AI增强工作流程测试通过！")
        return True
        
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        return False

def test_web_editor():
    """测试Web编辑器是否可访问"""
    try:
        print("🌐 测试Web编辑器...")
        response = requests.get('http://localhost:3001')  # 注意端口是3001
        if response.status_code == 200:
            print("[OK] Web编辑器可访问")
            return True
        else:
            print(f"[ERROR] Web编辑器不可访问: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Web编辑器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print(" 开始AI增强工作流程测试...")
    
    # 测试Web编辑器
    web_ok = test_web_editor()
    
    # 测试AI工作流程
    ai_ok = test_ai_workflow()
    
    print("\n 测试结果:")
    print(f"  Web编辑器: {'[OK] 正常' if web_ok else '[ERROR] 异常'}")
    print(f"  AI增强工作流程: {'[OK] 正常' if ai_ok else '[ERROR] 异常'}")
    
    if web_ok and ai_ok:
        print("\n 所有测试通过！")
        print("📱 请在浏览器中访问: http://localhost:3001")
        print("[AI] 在编辑器中切换到'AI增强'标签页进行测试")
        print("💡 提示: 新增的节点应该会在树状图中显示")
    else:
        print("\n[WARNING] 部分测试失败，请检查服务状态")

if __name__ == "__main__":
    main() 