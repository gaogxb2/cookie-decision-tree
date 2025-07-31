#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_ai_direct_process():
    """测试直接AI处理功能"""
    print("🧪 测试前端AI功能...")
    
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
    
    print("📤 发送测试请求到后端...")
    
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
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("✅ AI处理成功!")
                
                # 显示路径数据
                if 'path_data' in result:
                    path_data = result['path_data']
                    print(f"\n🔍 解析的路径:")
                    print(f"   问题: {path_data.get('problem', 'N/A')}")
                    print(f"   步骤数: {len(path_data.get('steps', []))}")
                    print(f"   解决方案: {path_data.get('solution', 'N/A')}")
                    
                    for step in path_data.get('steps', []):
                        print(f"   步骤{step['step']}: {step['question']} → {step['answer']}")
                
                # 显示变更信息
                if 'changes' in result:
                    changes = result['changes']
                    print(f"\n📝 变更列表 ({len(changes)} 项):")
                    for change in changes:
                        print(f"   - {change['text']} ({change['type']})")
                
                # 显示新节点信息
                if 'new_nodes' in result:
                    new_nodes = result['new_nodes']
                    node_count = len(new_nodes.get('nodes', {}))
                    print(f"\n🔍 新节点信息:")
                    print(f"   节点数量: {node_count}")
                    print(f"   入口节点: {new_nodes.get('entry_node', 'N/A')}")
                    
                    # 显示前几个节点
                    nodes = new_nodes.get('nodes', {})
                    for i, (node_id, node_data) in enumerate(list(nodes.items())[:3]):
                        print(f"   节点{i+1}: {node_id}")
                        if 'question' in node_data:
                            print(f"     问题: {node_data['question']}")
                        if 'solution' in node_data:
                            print(f"     解决方案: {node_data['solution']}")
                
                print(f"\n💬 消息: {result.get('message', 'N/A')}")
                
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

def test_frontend_access():
    """测试前端访问"""
    print("\n🌐 测试前端访问...")
    
    try:
        response = requests.get('http://localhost:3003/', timeout=10)
        print(f"📥 前端响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 前端服务正常")
        else:
            print(f"⚠️ 前端响应异常: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到前端服务")
    except Exception as e:
        print(f"❌ 前端访问异常: {e}")

def main():
    print("🚀 开始测试决策树AI功能...")
    print("=" * 50)
    
    # 测试前端访问
    test_frontend_access()
    
    print("\n" + "=" * 50)
    
    # 测试AI功能
    test_ai_direct_process()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成!")
    print("\n📋 访问地址:")
    print("   前端界面: http://localhost:3003/")
    print("   后端API: http://localhost:5000/")
    print("\n💡 使用说明:")
    print("   1. 打开前端界面")
    print("   2. 切换到 '🤖 AI增强' 标签页")
    print("   3. 输入聊天记录")
    print("   4. 点击 '直接AI分析' 按钮")
    print("   5. 查看分析结果并确认合并")

if __name__ == "__main__":
    main() 