#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import os
import sys

def setup_custom_http():
    """快速设置自定义HTTP API配置"""
    print("🚀 自定义HTTP API快速配置工具")
    print("=" * 80)
    
    # 读取当前配置
    try:
        with open('config/ai_config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return
    
    print("📋 请选择API类型:")
    print("1. OpenAI兼容API")
    print("2. Claude API")
    print("3. 简单格式API")
    print("4. 自定义格式")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    # 获取基本信息
    print("\n📝 请输入基本信息:")
    url = input("API URL: ").strip()
    api_key = input("API密钥: ").strip()
    
    # 根据选择设置配置
    if choice == "1":
        # OpenAI兼容格式
        custom_config = {
            "url": url,
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer ${CUSTOM_API_KEY}"
            },
            "body_template": '''{
                "messages": {messages},
                "model": "gpt-3.5-turbo",
                "temperature": 0.1,
                "max_tokens": 2000
            }''',
            "response_parser": {
                "content_field": "choices.0.message.content",
                "error_field": "error.message"
            }
        }
        print("✅ 已配置为OpenAI兼容格式")
        
    elif choice == "2":
        # Claude格式
        custom_config = {
            "url": url,
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "x-api-key": "${CUSTOM_API_KEY}",
                "anthropic-version": "2023-06-01"
            },
            "body_template": '''{
                "messages": {messages},
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 2000
            }''',
            "response_parser": {
                "content_field": "content.0.text",
                "error_field": "error.message"
            }
        }
        print("✅ 已配置为Claude格式")
        
    elif choice == "3":
        # 简单格式
        custom_config = {
            "url": url,
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer ${CUSTOM_API_KEY}"
            },
            "body_template": '''{
                "messages": {messages}
            }''',
            "response_parser": {
                "content_field": "response",
                "error_field": "error"
            }
        }
        print("✅ 已配置为简单格式")
        
    elif choice == "4":
        # 自定义格式
        print("\n🔧 自定义配置:")
        content_field = input("响应内容字段路径 (如: choices.0.message.content): ").strip()
        error_field = input("错误信息字段路径 (如: error.message): ").strip()
        
        # 获取请求体模板
        print("\n📝 请求体模板 (使用 {messages} 作为消息占位符):")
        print("示例: {\"messages\": {messages}, \"model\": \"your-model\"}")
        body_template = input("请求体模板: ").strip()
        
        custom_config = {
            "url": url,
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer ${CUSTOM_API_KEY}"
            },
            "body_template": body_template,
            "response_parser": {
                "content_field": content_field,
                "error_field": error_field
            }
        }
        print("✅ 已配置为自定义格式")
        
    else:
        print("❌ 无效选择")
        return
    
    # 更新配置
    config['ai']['api']['custom_http'] = custom_config
    config['ai']['current_api'] = 'custom_http'
    config['ai']['api_keys']['custom_http'] = '${CUSTOM_API_KEY}'
    
    # 保存配置
    try:
        with open('config/ai_config.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        print("✅ 配置文件已更新")
    except Exception as e:
        print(f"❌ 保存配置文件失败: {e}")
        return
    
    # 设置环境变量
    print(f"\n🔑 设置环境变量:")
    print(f"export CUSTOM_API_KEY=\"{api_key}\"")
    
    # 询问是否自动设置环境变量
    auto_set = input("\n是否自动设置环境变量? (y/n): ").strip().lower()
    if auto_set == 'y':
        os.environ['CUSTOM_API_KEY'] = api_key
        print("✅ 环境变量已设置")
    
    # 显示配置摘要
    print("\n📊 配置摘要:")
    print("-" * 40)
    print(f"API URL: {url}")
    print(f"API类型: {['OpenAI兼容', 'Claude', '简单格式', '自定义格式'][int(choice)-1]}")
    print(f"内容字段: {custom_config['response_parser']['content_field']}")
    print(f"错误字段: {custom_config['response_parser']['error_field']}")
    
    # 测试配置
    print("\n🧪 是否运行测试? (y/n): ", end="")
    test_choice = input().strip().lower()
    if test_choice == 'y':
        print("\n🚀 运行测试...")
        try:
            from test_custom_http_api import test_custom_http_api_with_mock
            test_custom_http_api_with_mock()
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    
    print("\n✅ 配置完成!")
    print("\n💡 使用提示:")
    print("1. 确保环境变量 CUSTOM_API_KEY 已设置")
    print("2. 运行 python test_custom_http_api.py 测试配置")
    print("3. 启动服务后即可使用自定义HTTP API")

def show_current_config():
    """显示当前配置"""
    try:
        with open('config/ai_config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        current_api = config['ai']['current_api']
        print(f"📋 当前API类型: {current_api}")
        
        if current_api == 'custom_http':
            custom_config = config['ai']['api']['custom_http']
            print(f"API URL: {custom_config['url']}")
            print(f"内容字段: {custom_config['response_parser']['content_field']}")
        else:
            api_config = config['ai']['api'][current_api]
            print(f"Base URL: {api_config['base_url']}")
            print(f"Model: {api_config['model']}")
            
    except Exception as e:
        print(f"❌ 读取配置失败: {e}")

def main():
    print("🔧 自定义HTTP API配置工具")
    print("=" * 80)
    
    print("请选择操作:")
    print("1. 设置自定义HTTP API")
    print("2. 查看当前配置")
    print("3. 退出")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        setup_custom_http()
    elif choice == "2":
        show_current_config()
    elif choice == "3":
        print("👋 再见!")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 