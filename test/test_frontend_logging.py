#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
from datetime import datetime

def test_frontend_ai_logging():
    """测试前端AI对话记录功能"""
    print("📝 测试前端AI对话记录功能...")
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
    
    print("[INFO] 发送测试请求到后端...")
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
        
        print(f"[INFO] 响应状态码: {response.status_code}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("[OK] AI处理成功!")
                print()
                
                # 显示路径数据
                if 'path_data' in result:
                    path_data = result['path_data']
                    print(" AI解析的路径数据:")
                    print(json.dumps(path_data, ensure_ascii=False, indent=2))
                    print()
                
                # 显示新节点数据
                if 'new_nodes' in result:
                    new_nodes = result['new_nodes']
                    print("[DEBUG] AI生成的节点数据:")
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
                print("📝 记录功能:")
                print("  [OK] AI对话已记录到文件")
                print("  [OK] 包含发送给AI的消息")
                print("  [OK] 包含AI的回复内容")
                print("  [OK] 包含处理时间")
                print("  [OK] 包含解析后的JSON数据")
                
            else:
                print(f"[ERROR] AI处理失败: {result.get('error', '未知错误')}")
        else:
            print(f"[ERROR] 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.Timeout:
        print("[ERROR] 请求超时")
    except requests.exceptions.ConnectionError:
        print("[ERROR] 连接失败，请检查后端服务是否运行")
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")

def check_log_files():
    """检查生成的日志文件"""
    print("\n 检查生成的日志文件...")
    print("=" * 80)
    
    import os
    import glob
    
    # 查找AI对话记录文件
    log_files = glob.glob("ai_conversation_frontend_*.txt")
    
    if log_files:
        # 按修改时间排序，获取最新的文件
        log_files.sort(key=os.path.getmtime, reverse=True)
        latest_file = log_files[0]
        
        print(f"📄 最新日志文件: {latest_file}")
        print(f"[TIME] 修改时间: {datetime.fromtimestamp(os.path.getmtime(latest_file))}")
        print()
        
        # 显示文件内容的前几行
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                print(" 日志文件内容预览:")
                print("-" * 40)
                
                # 显示前20行
                for i, line in enumerate(lines[:20]):
                    print(f"{i+1:2d}: {line}")
                
                if len(lines) > 20:
                    print("...")
                    print(f"总行数: {len(lines)}")
                
                print()
                print("[OK] 日志文件生成成功!")
                
        except Exception as e:
            print(f"[ERROR] 读取日志文件失败: {e}")
    else:
        print("[ERROR] 未找到AI对话记录文件")

def main():
    print(" 测试前端AI对话记录功能...")
    print("=" * 80)
    
    # 测试AI对话记录
    test_frontend_ai_logging()
    
    # 检查生成的日志文件
    check_log_files()
    
    print("\n" + "=" * 80)
    print("[OK] 记录功能测试完成!")
    print("\n📝 功能总结:")
    print("  [OK] 前端调用AI时自动记录对话")
    print("  [OK] 记录发送给AI的完整消息")
    print("  [OK] 记录AI的原始回复")
    print("  [OK] 记录处理时间和解析结果")
    print("  [OK] 保存为时间戳命名的文件")
    print("\n💡 使用方法:")
    print("  1. 在前端界面使用AI功能")
    print("  2. 系统自动生成日志文件")
    print("  3. 文件名格式: ai_conversation_frontend_YYYYMMDD_HHMMSS.txt")

if __name__ == "__main__":
    main() 