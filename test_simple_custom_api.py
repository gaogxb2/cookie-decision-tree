#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

def test_simple_custom_api():
    """测试简单的自定义 API 格式"""
    
    # 您的 API 配置
    url = "https://your-ai-service.com/api/chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your-api-key"
    }
    
    # 构建请求体 - 按照您的格式
    body = {
        "inputs": "你是一个决策树分析助手，请帮助分析用户的问题并提供解决方案。\n\n用户: 我的电脑无法开机，应该怎么办？",
        "parameters": {
            "detail": True,
            "temperature": 0.1
        }
    }
    
    print(" 测试简单自定义 API 格式")
    print("=" * 50)
    print(f" 请求 URL: {url}")
    print(f" 请求头: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    print(f" 请求体: {json.dumps(body, indent=2, ensure_ascii=False)}")
    print("=" * 50)
    
    # 模拟请求（实际使用时取消注释）
    # response = requests.post(url, headers=headers, data=json.dumps(body))
    # print(f" 响应状态码: {response.status_code}")
    # print(f" 响应内容: {response.text}")
    
    # 模拟响应
    mock_response_text = "根据您的描述，电脑无法开机可能有以下几个原因：\n\n1. 电源问题：检查电源线是否连接正常\n2. 硬件问题：可能是内存条松动或硬盘故障\n3. 系统问题：可能是系统文件损坏\n\n建议按以下步骤排查：\n1. 检查电源连接\n2. 尝试重新插拔内存条\n3. 如果问题持续，建议联系专业维修人员"
    
    print(f" 模拟响应: {mock_response_text}")
    print("=" * 50)
    print("[OK] 简单自定义 API 格式测试完成！")
    print("\n📝 使用说明：")
    print("1. 将 url 替换为您的实际 API 地址")
    print("2. 将 'your-api-key' 替换为您的实际 API 密钥")
    print("3. 取消注释 response = requests.post(...) 行来测试真实 API")
    print("4. 在 config/ai_config.yaml 中设置 current_api: 'custom_http'")
    print("5. 设置环境变量 CUSTOM_API_KEY=your-api-key")

if __name__ == '__main__':
    test_simple_custom_api() 