#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
from datetime import datetime

def test_custom_format():
    """测试自定义格式的 HTTP API 调用"""
    
    # 模拟您的 API 配置
    api_config = {
        "url": "https://your-ai-service.com/api/chat",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer your-api-key"
        },
        "body_template": '''{
          "inputs": "{prompt}",
          "parameters": {
            "detail": true,
            "temperature": 0.1
          }
        }'''
    }
    
    # 模拟消息列表
    messages = [
        {"role": "system", "content": "你是一个决策树分析助手，请帮助分析用户的问题并提供解决方案。"},
        {"role": "user", "content": "我的电脑无法开机，应该怎么办？"}
    ]
    
    # 将消息转换为提示文本
    def messages_to_prompt(messages):
        prompt_parts = []
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            if role == 'system':
                prompt_parts.append(f"系统指令: {content}")
            elif role == 'user':
                prompt_parts.append(f"用户: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"助手: {content}")
        
        return '\n\n'.join(prompt_parts)
    
    # 生成请求体
    prompt_text = messages_to_prompt(messages)
    body_json = api_config['body_template'].replace('{prompt}', json.dumps(prompt_text))
    body = json.loads(body_json)
    
    print("测试自定义 HTTP API 格式")
    print("=" * 50)
    print(f" 请求 URL: {api_config['url']}")
    print(f" 请求头: {json.dumps(api_config['headers'], indent=2, ensure_ascii=False)}")
    print(f" 请求体: {json.dumps(body, indent=2, ensure_ascii=False)}")
    print("=" * 50)
    
    # 模拟响应（实际使用时会被真实 API 调用替换）
    mock_response = {
        "output": "根据您的描述，电脑无法开机可能有以下几个原因：\n\n1. 电源问题：检查电源线是否连接正常\n2. 硬件问题：可能是内存条松动或硬盘故障\n3. 系统问题：可能是系统文件损坏\n\n建议按以下步骤排查：\n1. 检查电源连接\n2. 尝试重新插拔内存条\n3. 如果问题持续，建议联系专业维修人员"
    }
    
    print(f" 模拟响应: {json.dumps(mock_response, indent=2, ensure_ascii=False)}")
    print("=" * 50)
    print("[OK] 自定义格式测试完成！")
    print("\n📝 使用说明：")
    print("1. 将 api_config['url'] 替换为您的实际 API 地址")
    print("2. 将 'your-api-key' 替换为您的实际 API 密钥")
    print("3. 根据您的 API 响应格式调整 content_field 配置")
    print("4. 在 config/ai_config.yaml 中设置 current_api: 'custom_http'")

if __name__ == '__main__':
    test_custom_format() 