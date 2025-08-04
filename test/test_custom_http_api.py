#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml
import json
import requests
from unittest.mock import patch, Mock
from ai_chat_parser import AIChatParser

def create_mock_response(content_field_path, response_data):
    """创建模拟的HTTP响应"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = response_data
    mock_response.text = json.dumps(response_data, ensure_ascii=False)
    return mock_response

def test_custom_http_api_with_mock():
    """使用打桩测试自定义HTTP API功能"""
    print("🔧 测试自定义HTTP API功能（打桩模式）...")
    print("=" * 80)
    
    # 测试配置
    test_config = {
        'ai': {
            'current_api': 'custom_http',
            'api': {
                'custom_http': {
                    'url': 'https://example.com/api/chat',
                    'method': 'POST',
                    'headers': {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ${CUSTOM_API_KEY}',
                        'X-Custom-Header': 'test-value'
                    },
                    'body_template': '''
                    {
                        "messages": {messages},
                        "model": "test-model",
                        "temperature": 0.1,
                        "max_tokens": 2000
                    }
                    ''',
                    'response_parser': {
                        'content_field': 'choices.0.message.content',
                        'error_field': 'error.message'
                    }
                }
            },
            'api_keys': {
                'custom_http': '${CUSTOM_API_KEY}'
            }
        }
    }
    
    # 保存测试配置
    with open('test_ai_config.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(test_config, f, default_flow_style=False, allow_unicode=True)
    
    try:
        # 设置测试环境变量
        os.environ['CUSTOM_API_KEY'] = 'test-key-12345'
        
        # 创建AI解析器
        parser = AIChatParser(ai_config_file='test_ai_config.yaml')
        
        # 测试消息
        test_messages = [
            {"role": "system", "content": "你是一个专业的IT问题诊断专家"},
            {"role": "user", "content": "我的电脑无法连接网络，请帮我分析一下"}
        ]
        
        print("ℹ️ 准备测试请求...")
        print(f"URL: {test_config['ai']['api']['custom_http']['url']}")
        print(f"Headers: {json.dumps(test_config['ai']['api']['custom_http']['headers'], indent=2, ensure_ascii=False)}")
        print(f"Messages: {json.dumps(test_messages, ensure_ascii=False, indent=2)}")
        
        # 模拟不同的响应格式
        test_cases = [
            {
                "name": "OpenAI兼容格式",
                "response_data": {
                    "choices": [
                        {
                            "message": {
                                "content": "根据您的描述，这是一个网络连接问题。建议按以下步骤排查：1. 检查网络线缆连接 2. 重启路由器 3. 检查网络适配器设置"
                            }
                        }
                    ]
                }
            },
            {
                "name": "Claude格式",
                "response_data": {
                    "content": [
                        {
                            "text": "这是一个网络连接问题。建议检查：1. 网络线缆 2. 路由器状态 3. 网络适配器"
                        }
                    ]
                }
            },
            {
                "name": "简单格式",
                "response_data": {
                    "response": "网络连接问题，请检查网络设置和硬件连接"
                }
            },
            {
                "name": "嵌套格式",
                "response_data": {
                    "data": {
                        "result": {
                            "content": "网络连接问题，建议重启路由器"
                        }
                    }
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 测试用例 {i}: {test_case['name']}")
            print("-" * 50)
            
            # 根据测试用例调整响应解析配置
            if test_case['name'] == "OpenAI兼容格式":
                content_field = "choices.0.message.content"
            elif test_case['name'] == "Claude格式":
                content_field = "content.0.text"
            elif test_case['name'] == "简单格式":
                content_field = "response"
            elif test_case['name'] == "嵌套格式":
                content_field = "data.result.content"
            
            # 更新配置
            test_config['ai']['api']['custom_http']['response_parser']['content_field'] = content_field
            
            # 重新保存配置
            with open('test_ai_config.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(test_config, f, default_flow_style=False, allow_unicode=True)
            
            # 重新创建解析器
            parser = AIChatParser(ai_config_file='test_ai_config.yaml')
            
            # 创建模拟响应
            mock_response = create_mock_response(content_field, test_case['response_data'])
            
            # 使用patch模拟requests.post
            with patch('requests.post', return_value=mock_response) as mock_post:
                print(f"模拟响应: {json.dumps(test_case['response_data'], ensure_ascii=False, indent=2)}")
                print(f"内容字段路径: {content_field}")
                
                # 调用API
                response = parser._call_ai_api(test_messages)
                
                if response:
                    print("✅ 测试成功!")
                    print(f"提取的内容: {response}")
                    
                    # 验证请求参数
                    mock_post.assert_called_once()
                    call_args = mock_post.call_args
                    print(f"请求URL: {call_args[0][0]}")
                    print(f"请求头: {json.dumps(call_args[1]['headers'], indent=2, ensure_ascii=False)}")
                    print(f"请求体: {json.dumps(call_args[1]['json'], indent=2, ensure_ascii=False)}")
                else:
                    print("❌ 测试失败")
                
                print()
        
        # 测试错误情况
        print("🧪 测试错误情况")
        print("-" * 50)
        
        # 测试HTTP错误
        error_response = Mock()
        error_response.status_code = 500
        error_response.text = "Internal Server Error"
        
        with patch('requests.post', return_value=error_response) as mock_post:
            response = parser._call_ai_api(test_messages)
            if response is None:
                print("✅ HTTP错误处理正确")
            else:
                print("❌ HTTP错误处理失败")
        
        # 测试解析错误
        invalid_response = Mock()
        invalid_response.status_code = 200
        invalid_response.json.return_value = {"invalid": "response"}
        
        with patch('requests.post', return_value=invalid_response) as mock_post:
            response = parser._call_ai_api(test_messages)
            if response is None:
                print("✅ 解析错误处理正确")
            else:
                print("❌ 解析错误处理失败")
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        # 清理测试文件
        if os.path.exists('test_ai_config.yaml'):
            os.remove('test_ai_config.yaml')

def test_config_examples():
    """显示配置示例"""
    print("\n📋 配置示例:")
    print("=" * 80)
    
    examples = {
        "OpenAI兼容API": {
            "url": "https://your-openai-compatible-api.com/v1/chat/completions",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer ${CUSTOM_API_KEY}"
            },
            "body_template": '''
            {
                "messages": {messages},
                "model": "gpt-3.5-turbo",
                "temperature": 0.1,
                "max_tokens": 2000
            }
            ''',
            "response_parser": {
                "content_field": "choices.0.message.content",
                "error_field": "error.message"
            }
        },
        "Claude API": {
            "url": "https://api.anthropic.com/v1/messages",
            "headers": {
                "Content-Type": "application/json",
                "x-api-key": "${CUSTOM_API_KEY}",
                "anthropic-version": "2023-06-01"
            },
            "body_template": '''
            {
                "messages": {messages},
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 2000
            }
            ''',
            "response_parser": {
                "content_field": "content.0.text",
                "error_field": "error.message"
            }
        },
        "本地部署模型": {
            "url": "http://localhost:8000/v1/chat/completions",
            "headers": {
                "Content-Type": "application/json"
            },
            "body_template": '''
            {
                "messages": {messages},
                "model": "local-model",
                "temperature": 0.1,
                "max_tokens": 2000
            }
            ''',
            "response_parser": {
                "content_field": "choices.0.message.content",
                "error_field": "error.message"
            }
        }
    }
    
    for name, config in examples.items():
        print(f"\n🔧 {name}:")
        print("-" * 40)
        print(f"URL: {config['url']}")
        print(f"Headers: {json.dumps(config['headers'], indent=2, ensure_ascii=False)}")
        print(f"Body Template: {config['body_template'].strip()}")
        print(f"Response Parser: {json.dumps(config['response_parser'], indent=2, ensure_ascii=False)}")

def show_usage_guide():
    """显示使用指南"""
    print("\n📖 使用指南:")
    print("=" * 80)
    
    print("1. 配置自定义HTTP API:")
    print("   - 编辑 config/ai_config.yaml")
    print("   - 设置 current_api: 'custom_http'")
    print("   - 配置 custom_http 部分")
    
    print("\n2. 设置环境变量:")
    print("   - 设置 CUSTOM_API_KEY 环境变量")
    print("   - 或在配置中使用其他环境变量")
    
    print("\n3. 配置说明:")
    print("   - url: API端点地址")
    print("   - headers: 请求头（支持环境变量）")
    print("   - body_template: 请求体模板（{messages}为占位符）")
    print("   - response_parser: 响应解析配置")
    
    print("\n4. 响应解析字段路径:")
    print("   - 使用点号分隔访问嵌套字段")
    print("   - 使用数字索引访问数组元素")
    print("   - 例如: 'choices.0.message.content'")
    
    print("\n5. 测试配置:")
    print("   - 使用 test_custom_http_api.py 测试")
    print("   - 检查日志输出确认配置正确")

def main():
    print("🚀 测试自定义HTTP API功能（打桩模式）...")
    print("=" * 80)
    
    # 测试自定义HTTP API
    test_custom_http_api_with_mock()
    
    # 显示配置示例
    test_config_examples()
    
    # 显示使用指南
    show_usage_guide()
    
    print("\n" + "=" * 80)
    print("✅ 自定义HTTP API功能测试完成!")
    print("\n💡 功能特点:")
    print("  ✅ 支持任意HTTP POST API")
    print("  ✅ 灵活的请求头和请求体配置")
    print("  ✅ 支持环境变量替换")
    print("  ✅ 可配置的响应解析")
    print("  ✅ 错误处理和日志记录")
    print("  ✅ 打桩测试验证功能")

if __name__ == "__main__":
    main() 