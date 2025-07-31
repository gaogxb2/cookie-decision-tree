#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
启动脚本 - 确保在py310环境中运行
"""

import sys
import subprocess
import os

def check_python_environment():
    """检查Python环境"""
    print(f"🐍 Python版本: {sys.version}")
    print(f"📁 Python路径: {sys.executable}")
    
    # 检查是否在py310环境中
    if 'py310' in sys.executable:
        print("✅ 当前在py310环境中")
        return True
    else:
        print("⚠️ 当前不在py310环境中")
        return False

def run_script(script_name):
    """在py310环境中运行脚本"""
    if not check_python_environment():
        print("🔧 尝试激活py310环境...")
        
        # 获取conda路径
        conda_path = "/opt/anaconda3/bin/conda"
        if not os.path.exists(conda_path):
            print("❌ 找不到conda，请确保已安装Anaconda")
            return
        
        # 使用conda运行脚本
        cmd = [conda_path, "run", "-n", "py310", "python", script_name]
        print(f"🚀 执行命令: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("错误:", result.stderr)
        except Exception as e:
            print(f"❌ 运行失败: {e}")
    else:
        print(f"✅ 直接运行 {script_name}")
        try:
            with open(script_name, 'r', encoding='utf-8') as f:
                exec(f.read())
        except Exception as e:
            print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    # 默认运行log_ai_conversation.py
    script_to_run = "log_ai_conversation.py"
    
    if len(sys.argv) > 1:
        script_to_run = sys.argv[1]
    
    print(f"🎯 准备运行: {script_to_run}")
    run_script(script_to_run) 