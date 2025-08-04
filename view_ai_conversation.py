#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import yaml
from datetime import datetime

def load_prompts():
    """加载prompts配置"""
    try:
        with open('config/prompts.yaml', 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
        return prompts
    except Exception as e:
        print(f"❌ 加载prompts失败: {e}")
        return None

def load_ai_config():
    """加载AI配置"""
    try:
        with open('config/ai_config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"❌ 加载AI配置失败: {e}")
        return None

def view_ai_conversation():
    """查看AI对话详情"""
    print("🔍 查看AI对话详情...")
    print("=" * 80)
    
    # 加载配置
    prompts = load_prompts()
    ai_config = load_ai_config()
    
    if not prompts or not ai_config:
        print("❌ 配置加载失败")
        return
    
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
    
    print("ℹ️ 发送给AI的消息:")
    print("-" * 40)
    
    # 显示当前使用的prompt
    current_api = ai_config['ai']['current_api']
    api_config = ai_config['ai']['api'][current_api]
    
    print(f"🔧 当前AI服务: {current_api}")
    print(f"🔧 模型: {api_config.get('model', 'N/A')}")
    print(f"🔧 温度: {api_config.get('temperature', 'N/A')}")
    print(f"🔧 最大token: {api_config.get('max_tokens', 'N/A')}")
    print()
    
    # 显示System Prompt
    system_prompt = prompts['chat_analysis']['system']
    print("🔧 System Prompt:")
    print(system_prompt)
    print()
    
    # 显示User Prompt
    user_prompt = prompts['chat_analysis']['user'].format(chat_history=chat_history)
    print("👤 User Prompt:")
    print(user_prompt)
    print()
    
    print("📡 发送API请求...")
    print("-" * 40)
    
    # 发送请求
    try:
        response = requests.post(
            'http://localhost:5000/api/ai/direct-process',
            json={
                'chat_history': chat_history,
                'auto_merge': False
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"ℹ️ 响应状态码: {response.status_code}")
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
    
    print("=" * 80)
    print("✅ 对话详情查看完成")

def view_direct_ai_call():
    """查看直接AI调用的详细信息"""
    print("\n🔍 查看直接AI调用详情...")
    print("=" * 80)
    
    # 导入直接AI调用器
    try:
        from direct_ai_call import DirectAICaller
    except ImportError:
        print("❌ 无法导入DirectAICaller")
        return
    
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
    
    print("ℹ️ 直接AI调用详情:")
    print("-" * 40)
    
    try:
        caller = DirectAICaller()
        
        # 显示AI配置
        print(f"🔧 AI配置:")
        print(f"  当前API: {caller.ai_config['ai']['current_api']}")
        api_type = caller.ai_config['ai']['current_api']
        api_config = caller.ai_config['ai']['api'][api_type]
        print(f"  模型: {api_config.get('model', 'N/A')}")
        print(f"  温度: {api_config.get('temperature', 'N/A')}")
        print(f"  最大token: {api_config.get('max_tokens', 'N/A')}")
        print()
        
        # 显示prompt
        system_prompt = caller.prompts['chat_analysis']['system']
        user_prompt = caller.prompts['chat_analysis']['user'].format(chat_history=chat_history)
        
        print("🔧 System Prompt:")
        print(system_prompt)
        print()
        
        print("👤 User Prompt:")
        print(user_prompt)
        print()
        
        print("📡 直接调用AI API...")
        print("-" * 40)
        
        # 直接调用AI
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        ai_response = caller._call_ai_api(messages)
        
        print("ℹ️ AI原始回复:")
        print("-" * 40)
        print(ai_response)
        print()
        
        # 解析AI回复
        from ai_chat_parser import AIChatParser
        parser = AIChatParser()
        
        # 提取JSON
        ai_data = parser._extract_json_from_response(ai_response)
        if ai_data:
            print("🔍 解析后的JSON数据:")
            print(json.dumps(ai_data, ensure_ascii=False, indent=2))
            print()
            
            # 转换为路径
            if 'steps' in ai_data:
                print("✅ AI返回了路径格式")
                path_data = ai_data
            else:
                print("⚠️ AI返回了决策树格式，尝试提取路径")
                path_data = parser.extract_path_from_tree(ai_data)
            
            if path_data:
                print("📋 提取的路径数据:")
                print(json.dumps(path_data, ensure_ascii=False, indent=2))
                print()
                
                # 转换为节点
                tree_data = parser.convert_path_to_tree(path_data)
                print("🔍 转换后的节点数据:")
                print(json.dumps(tree_data, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ 直接AI调用失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("🚀 查看AI对话详情...")
    print("=" * 80)
    
    # 查看通过API的对话
    view_ai_conversation()
    
    # 查看直接AI调用
    view_direct_ai_call()
    
    print("\n" + "=" * 80)
    print("✅ 所有对话详情查看完成!")

if __name__ == "__main__":
    main() 