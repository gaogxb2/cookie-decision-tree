#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def test_windows_compatibility():
    """测试 Windows 兼容性"""
    
    print(" 测试 Windows 兼容性...")
    print("=" * 50)
    
    # 测试安全字符
    try:
        from ai_chat_parser import get_safe_chars
        safe_chars = get_safe_chars()
        print(f"[OK] 安全字符测试通过")
        print(f"   错误字符: {safe_chars['error']}")
        print(f"   成功字符: {safe_chars['success']}")
        print(f"   信息字符: {safe_chars['info']}")
    except Exception as e:
        print(f"[ERROR] 安全字符测试失败: {e}")
    
    # 测试 API 服务器
    try:
        from api_server import get_safe_chars as api_safe_chars
        api_chars = api_safe_chars()
        print(f"[OK] API 服务器安全字符测试通过")
        print(f"   错误字符: {api_chars['error']}")
        print(f"   成功字符: {api_chars['success']}")
    except Exception as e:
        print(f"[ERROR] API 服务器安全字符测试失败: {e}")
    
    # 测试编码
    try:
        test_message = "测试中文编码和特殊字符"
        encoded = test_message.encode('utf-8')
        decoded = encoded.decode('utf-8')
        print(f"[OK] UTF-8 编码测试通过")
        print(f"   原始: {test_message}")
        print(f"   编码后: {encoded}")
        print(f"   解码后: {decoded}")
    except Exception as e:
        print(f"[ERROR] UTF-8 编码测试失败: {e}")
    
    # 测试 GBK 编码（Windows 默认）
    try:
        test_message = "测试中文编码"
        # 尝试 GBK 编码（如果系统支持）
        try:
            gbk_encoded = test_message.encode('gbk')
            gbk_decoded = gbk_encoded.decode('gbk')
            print(f"[OK] GBK 编码测试通过")
            print(f"   原始: {test_message}")
            print(f"   GBK编码后: {gbk_encoded}")
            print(f"   GBK解码后: {gbk_decoded}")
        except LookupError:
            print(f"[INFO] GBK 编码不可用（非 Windows 系统）")
    except Exception as e:
        print(f"[ERROR] GBK 编码测试失败: {e}")
    
    print("=" * 50)
    print(" Windows 兼容性测试完成！")
    print("\n📝 如果所有测试都通过，说明系统在 Windows 上应该可以正常工作")
    print("📝 如果出现编码错误，请检查系统编码设置")

if __name__ == '__main__':
    test_windows_compatibility() 