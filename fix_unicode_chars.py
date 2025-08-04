#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import platform

def get_safe_chars():
    """根据操作系统返回安全的字符"""
    if platform.system() == 'Windows':
        return {
            'success': '[SUCCESS]',
            'error': '[ERROR]',
            'info': '[INFO]',
            'warning': '[WARNING]',
            'ai': '[AI]',
            'time': '[TIME]',
            'user': '[USER]',
            'system': '[SYSTEM]',
            'parse': '[PARSE]',
            'save': '[SAVE]',
            'separator': '=' * 80,
            'sub_separator': '-' * 40
        }
    else:
        return {
            'success': '✅',
            'error': '❌',
            'info': 'ℹ️',
            'warning': '⚠️',
            'ai': '🤖',
            'time': '⏱️',
            'user': '👤',
            'system': '🔧',
            'parse': '🔍',
            'save': '💾',
            'separator': '=' * 80,
            'sub_separator': '-' * 40
        }

def fix_unicode_chars_in_file(file_path):
    """修复单个文件中的 Unicode 字符"""
    safe_chars = get_safe_chars()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换 Unicode 表情符号
        replacements = [
            ('❌', safe_chars['error']),
            ('✅', safe_chars['success']),
            ('ℹ️', safe_chars['info']),
            ('⚠️', safe_chars['warning']),
            ('🤖', safe_chars['ai']),
            ('⏱️', safe_chars['time']),
            ('👤', safe_chars['user']),
            ('🔧', safe_chars['system']),
            ('🔍', safe_chars['parse']),
            ('💾', safe_chars['save']),
            ('⏱️', safe_chars['time']),
            ('ℹ️', safe_chars['info']),
            ('ℹ️', safe_chars['info']),
            ('ℹ️', safe_chars['info']),
            ('🔧', safe_chars['system']),
        ]
        
        modified = False
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已修复: {file_path}")
        else:
            print(f"无需修复: {file_path}")
            
    except Exception as e:
        print(f"处理文件失败 {file_path}: {e}")

def find_python_files(directory):
    """查找目录中的所有 Python 文件"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # 跳过 node_modules 和 dist 目录
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'dist', '__pycache__']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def main():
    """主函数"""
    print("🔧 开始修复 Unicode 字符编码问题...")
    
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"工作目录: {current_dir}")
    
    # 查找所有 Python 文件
    python_files = find_python_files(current_dir)
    print(f"找到 {len(python_files)} 个 Python 文件")
    
    # 修复每个文件
    for file_path in python_files:
        fix_unicode_chars_in_file(file_path)
    
    print("🎉 Unicode 字符修复完成！")
    print(f"在 {platform.system()} 系统上，已使用安全的字符替换 Unicode 表情符号")

if __name__ == '__main__':
    main() 