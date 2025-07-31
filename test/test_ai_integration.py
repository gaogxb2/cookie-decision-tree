#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_ai_integration():
    """测试AI增强功能集成"""
    print("🧪 测试AI增强功能集成...")
    
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
    
    # 测试API接口
    try:
        print("📡 测试AI处理接口...")
        response = requests.post(
            'http://localhost:5000/api/ai/process-chat',
            json={
                'chat_history': chat_history,
                'auto_merge': False
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ AI处理接口正常")
                print(f"📊 生成变更: {len(result.get('changes', []))}")
                return True
            else:
                print(f"❌ AI处理失败: {result.get('error')}")
                return False
        else:
            print(f"❌ API请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_web_editor():
    """测试Web编辑器是否可访问"""
    try:
        print("🌐 测试Web编辑器...")
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            print("✅ Web编辑器可访问")
            return True
        else:
            print(f"❌ Web编辑器不可访问: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Web编辑器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始AI增强功能集成测试...")
    
    # 测试Web编辑器
    web_ok = test_web_editor()
    
    # 测试AI接口
    ai_ok = test_ai_integration()
    
    print("\n📋 测试结果:")
    print(f"  Web编辑器: {'✅ 正常' if web_ok else '❌ 异常'}")
    print(f"  AI增强接口: {'✅ 正常' if ai_ok else '❌ 异常'}")
    
    if web_ok and ai_ok:
        print("\n🎉 所有测试通过！")
        print("📱 请在浏览器中访问: http://localhost:3000")
        print("🤖 在编辑器中切换到'AI增强'标签页进行测试")
    else:
        print("\n⚠️ 部分测试失败，请检查服务状态")

if __name__ == "__main__":
    main() 