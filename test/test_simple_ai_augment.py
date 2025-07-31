#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_simple_ai_augment():
    """测试简化后的AI增强功能"""
    print("🧪 测试简化后的AI增强功能...")
    
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
        
        if response.status_code != 200:
            print(f"❌ AI处理失败: {response.status_code}")
            return False
        
        result = response.json()
        if not result.get('success'):
            print(f"❌ AI处理失败: {result.get('error')}")
            return False
        
        print(f"✅ AI处理成功，耗时: {processing_time:.2f}秒")
        
        # 检查新节点结构
        new_nodes = result.get('new_nodes', {})
        if 'nodes' in new_nodes and 'root_node' in new_nodes:
            print(f"✅ 新节点有根节点: {new_nodes['root_node']}")
            print(f"✅ 新节点数量: {len(new_nodes['nodes'])}")
        else:
            print("❌ 新节点结构不完整")
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
            print(f"❌ 确认变更失败: {confirm_response.status_code}")
            return False
        
        confirm_result = confirm_response.json()
        if not confirm_result.get('success'):
            print(f"❌ 确认变更失败: {confirm_result.get('error')}")
            return False
        
        print("✅ 确认变更成功")
        
        # 3. 验证决策树更新
        print("📡 步骤3: 验证决策树更新...")
        time.sleep(2)  # 等待文件写入
        
        tree_response = requests.get('http://localhost:5000/api/tree')
        if tree_response.status_code == 200:
            tree_data = tree_response.json()
            root_node = tree_data.get('root_node', '')
            nodes = tree_data.get('nodes', {})
            
            print(f"✅ 决策树根节点: {root_node}")
            print(f"✅ 节点总数: {len(nodes)}")
            
            # 检查根节点是否有新选项
            if root_node and root_node in nodes:
                root_options = nodes[root_node].get('options', [])
                print(f"✅ 根节点选项数: {len(root_options)}")
                
                # 显示最新的选项
                if root_options:
                    print("📋 根节点选项:")
                    for i, opt in enumerate(root_options[-3:], 1):  # 显示最后3个选项
                        print(f"  {i}. {opt['text']} -> {opt.get('next_node', 'N/A')}")
            else:
                print("❌ 根节点不存在或无效")
                return False
        else:
            print("❌ 无法获取决策树数据")
            return False
        
        print("🎉 简化AI增强功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始简化AI增强功能测试...")
    
    success = test_simple_ai_augment()
    
    if success:
        print("\n✅ 测试通过！")
        print("📱 请在浏览器中访问: http://localhost:3001")
        print("🤖 在编辑器中切换到'AI增强'标签页进行测试")
        print("💡 提示: AI解析速度应该更快了，新路径会直接挂到根节点")
    else:
        print("\n❌ 测试失败")

if __name__ == "__main__":
    main() 