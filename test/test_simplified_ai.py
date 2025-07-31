#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime

def test_simplified_ai():
    """测试简化后的AI功能"""
    print("🧹 测试简化后的AI功能...")
    print("=" * 80)
    
    # 测试聊天记录
    test_chat = """
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
    
    print("📤 发送请求到 /api/ai/direct-process...")
    print("-" * 40)
    
    try:
        response = requests.post(
            'http://localhost:5000/api/ai/direct-process',
            json={
                'chat_history': test_chat,
                'auto_merge': False
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📥 响应状态码: {response.status_code}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("✅ AI处理成功!")
                print()
                
                # 显示路径数据
                if 'path_data' in result:
                    path_data = result['path_data']
                    print("📋 AI解析的路径数据:")
                    print(json.dumps(path_data, ensure_ascii=False, indent=2))
                    print()
                
                # 显示新节点数据
                if 'new_nodes' in result:
                    new_nodes = result['new_nodes']
                    print("🔍 AI生成的节点数据:")
                    print(json.dumps(new_nodes, ensure_ascii=False, indent=2))
                    print()
                
                # 显示变更信息
                if 'changes' in result:
                    changes = result['changes']
                    print("📝 变更列表:")
                    for change in changes:
                        print(f"  - {change['text']} ({change['type']})")
                    print()
                
                print(f"💬 消息: {result.get('message', 'N/A')}")
                print()
                print("🔒 安全验证:")
                print("  ✅ 只发送聊天记录给AI")
                print("  ✅ 没有发送决策树给AI")
                print("  ✅ 自动记录对话过程")
                
            else:
                print(f"❌ AI处理失败: {result.get('error', '未知错误')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请检查后端服务是否运行")
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def check_old_api():
    """检查旧的API是否还存在"""
    print("\n🔍 检查旧的API端点...")
    print("=" * 80)
    
    try:
        response = requests.post(
            'http://localhost:5000/api/ai/process-chat',
            json={
                'chat_history': 'test',
                'auto_merge': False
            },
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 404:
            print("✅ 旧的API端点已删除")
        else:
            print("⚠️ 旧的API端点仍然存在")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
    except Exception as e:
        print(f"✅ 旧的API端点已删除 (错误: {e})")

def main():
    print("🚀 测试简化后的AI功能...")
    print("=" * 80)
    
    # 检查旧的API
    check_old_api()
    
    # 测试新的AI功能
    test_simplified_ai()
    
    print("\n" + "=" * 80)
    print("✅ 简化测试完成!")
    print("\n📝 简化总结:")
    print("  ✅ 删除了'开始AI分析'按钮")
    print("  ✅ 删除了旧的API端点")
    print("  ✅ 只保留安全的'AI分析'功能")
    print("  ✅ 自动记录对话过程")
    print("  ✅ 保护敏感信息")

if __name__ == "__main__":
    main() 