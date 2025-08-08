#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import yaml
from datetime import datetime

def load_prompts():
    """加载prompts配置"""
    try:
        with open('config/prompts.yaml', 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
        return prompts
    except Exception as e:
        print(f"[ERROR] 加载prompts失败: {e}")
        return None

def log_ai_conversation():
    """记录AI对话"""
    print("📝 开始记录AI对话...")
    
    # 加载prompts配置
    prompts = load_prompts()
    if not prompts:
        print("[ERROR] 无法加载prompts配置")
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
    
    # 构建日志内容
    log_content = []
    log_content.append("=" * 80)
    log_content.append("[AI] AI对话记录")
    log_content.append("=" * 80)
    log_content.append(f"[TIME] 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_content.append("")
    
    log_content.append("[INFO] 发送给AI的消息:")
    log_content.append("-" * 40)
    
    # 使用config/prompts.yaml中的prompt
    system_prompt = prompts['chat_analysis']['system']
    user_prompt = prompts['chat_analysis']['user'].format(chat_history=chat_history)
    
    log_content.append("[SYSTEM] System Prompt:")
    log_content.append(system_prompt)
    log_content.append("")
    log_content.append("[USER] User Prompt:")
    log_content.append(user_prompt)
    log_content.append("")
    
    # 发送请求并记录响应
    log_content.append("📡 发送API请求...")
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
    
    log_content.append(f"[TIME] 处理时间: {processing_time:.2f}秒")
    log_content.append("")
    
    if response.status_code == 200:
        result = response.json()
        
        log_content.append("[INFO] AI回复内容:")
        log_content.append("-" * 40)
        
        if result.get('success'):
            new_nodes = result.get('new_nodes', {})
            
            # 记录AI生成的节点结构
            log_content.append("AI生成的决策树节点:")
            log_content.append(json.dumps(new_nodes, ensure_ascii=False, indent=2))
            
            # 记录变更信息
            changes = result.get('changes', [])
            if changes:
                log_content.append("")
                log_content.append("变更列表:")
                for change in changes:
                    log_content.append(f"  - {change['text']} ({change['type']})")
            
            # 记录消息
            message = result.get('message', '')
            if message:
                log_content.append("")
                log_content.append(f"💬 消息: {message}")
        else:
            log_content.append(f"[ERROR] AI处理失败: {result.get('error')}")
    else:
        log_content.append(f"[ERROR] 请求失败: {response.status_code}")
    
    log_content.append("")
    log_content.append("=" * 80)
    log_content.append("[OK] 对话记录完成")
    log_content.append("=" * 80)
    
    # 保存到文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"ai_conversation_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_content))
    
    print(f"[SAVE] 对话记录已保存到: {filename}")
    
    # 同时在控制台显示
    print('\n'.join(log_content))

if __name__ == "__main__":
    log_ai_conversation() 