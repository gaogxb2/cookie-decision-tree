#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
from problem_locator import ProblemLocator

def test_config_loading():
    """测试配置文件加载"""
    print("🧪 测试配置文件加载...")
    
    try:
        locator = ProblemLocator("config/decision_tree.yaml")
        print("✅ 配置文件加载成功")
        print(f"   根节点: {locator.current_node}")
        print(f"   节点数量: {len(locator.config['decision_tree']['nodes'])}")
        return True
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        return False

def test_fuzzy_matching():
    """测试模糊匹配功能"""
    print("\n🧪 测试模糊匹配功能...")
    
    locator = ProblemLocator("config/decision_tree.yaml")
    
    # 测试用例
    test_cases = [
        ("硬件问题", "硬件问题", 1.0),
        ("硬件", "硬件问题", 0.8),
        ("显示器", "显示器问题", 0.8),
        ("键盘", "键盘问题", 0.8),
        ("软件", "软件问题", 0.8),
        ("网络", "网络问题", 0.8),
        ("声音", "声音问题", 0.8),
        ("启动", "启动问题", 0.8),
        ("安装", "安装问题", 0.8),
        ("性能", "性能问题", 0.8),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for user_input, option_text, expected_score in test_cases:
        score = locator._fuzzy_match(user_input, option_text)
        if score >= expected_score * 0.8:  # 允许20%的误差
            print(f"✅ '{user_input}' 匹配 '{option_text}': {score:.2f}")
            passed += 1
        else:
            print(f"❌ '{user_input}' 匹配 '{option_text}': {score:.2f} (期望: {expected_score})")
    
    print(f"\n📊 匹配测试结果: {passed}/{total} 通过")
    return passed == total

def test_node_traversal():
    """测试节点遍历"""
    print("\n🧪 测试节点遍历...")
    
    locator = ProblemLocator("config/decision_tree.yaml")
    
    # 测试从根节点开始
    root_node = locator.config['decision_tree']['root_node']
    print(f"根节点: {root_node}")
    
    # 获取根节点信息
    root_info = locator._get_node_info(root_node)
    if root_info and 'question' in root_info:
        print(f"根节点问题: {root_info['question']}")
        print(f"选项数量: {len(root_info['options'])}")
        
        # 测试第一个选项
        if root_info['options']:
            first_option = root_info['options'][0]
            print(f"第一个选项: {first_option['text']}")
            print(f"下一个节点: {first_option.get('next_node', 'N/A')}")
            return True
    
    print("❌ 节点遍历测试失败")
    return False

def test_diagnostic_path():
    """测试诊断路径记录"""
    print("\n🧪 测试诊断路径记录...")
    
    locator = ProblemLocator("config/decision_tree.yaml")
    
    # 模拟用户选择
    test_path = [
        ("硬件问题", "hardware_issue"),
        ("显示器问题", "display_issue"),
    ]
    
    for choice, expected_next in test_path:
        # 找到匹配的选项
        node_info = locator._get_node_info(locator.current_node)
        if node_info and 'options' in node_info:
            for option in node_info['options']:
                if option['text'] == choice:
                    locator._move_to_next_node(option)
                    print(f"✅ 选择 '{choice}' -> 节点 '{locator.current_node}'")
                    break
            else:
                print(f"❌ 找不到选项 '{choice}'")
                return False
    
    print(f"📋 诊断路径: {len(locator.diagnostic_path)} 步")
    for i, step in enumerate(locator.diagnostic_path, 1):
        print(f"  {i}. {step['choice']} -> {step['next_node']}")
    
    return True

def main():
    """主测试函数"""
    print("🔍 问题定位器功能测试")
    print("=" * 50)
    
    tests = [
        ("配置文件加载", test_config_loading),
        ("模糊匹配", test_fuzzy_matching),
        ("节点遍历", test_node_traversal),
        ("诊断路径", test_diagnostic_path),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！问题定位器可以正常使用。")
        print("\n🚀 启动命令:")
        print("  macOS/Linux: ./start_locator.sh")
        print("  Windows: start_locator.bat")
        print("  直接运行: python problem_locator.py")
    else:
        print("⚠️ 部分测试失败，请检查配置和代码。")

if __name__ == "__main__":
    main() 