#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import subprocess
import threading
import zipfile
import shutil
import json
from pathlib import Path

class DecisionTreeInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("决策树系统安装程序")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # 设置图标（如果有的话）
        try:
            self.root.iconbitmap("installer/icon.ico")
        except:
            pass
        
        # 安装状态
        self.install_status = {
            "python": False,
            "nodejs": False,
            "conda": False,
            "dependencies": False,
            "frontend": False
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主标题
        title_frame = tk.Frame(self.root)
        title_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = tk.Label(title_frame, text="🤖 决策树可视化编辑器", 
                              font=("Arial", 16, "bold"))
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="一键安装程序", 
                                 font=("Arial", 12))
        subtitle_label.pack()
        
        # 安装路径选择
        path_frame = tk.Frame(self.root)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(path_frame, text="安装路径:").pack(anchor="w")
        
        path_var = tk.StringVar(value="C:\\DecisionTreeSystem")
        path_entry = tk.Entry(path_frame, textvariable=path_var, width=50)
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(path_frame, text="浏览", 
                              command=lambda: self.browse_path(path_var))
        browse_btn.pack(side="right")
        
        # 安装选项
        options_frame = tk.Frame(self.root)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(options_frame, text="安装选项:").pack(anchor="w")
        
        self.python_var = tk.BooleanVar(value=True)
        self.nodejs_var = tk.BooleanVar(value=True)
        self.conda_var = tk.BooleanVar(value=True)
        self.desktop_shortcut_var = tk.BooleanVar(value=True)
        self.start_menu_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(options_frame, text="安装 Python 3.10", 
                      variable=self.python_var).pack(anchor="w")
        tk.Checkbutton(options_frame, text="安装 Node.js", 
                      variable=self.nodejs_var).pack(anchor="w")
        tk.Checkbutton(options_frame, text="安装 Miniconda", 
                      variable=self.conda_var).pack(anchor="w")
        tk.Checkbutton(options_frame, text="创建桌面快捷方式", 
                      variable=self.desktop_shortcut_var).pack(anchor="w")
        tk.Checkbutton(options_frame, text="添加到开始菜单", 
                      variable=self.start_menu_var).pack(anchor="w")
        
        # 进度条
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill="x", padx=20, pady=10)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill="x")
        
        # 状态显示
        status_frame = tk.Frame(self.root)
        status_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.status_text = tk.Text(status_frame, height=10, wrap="word")
        status_scrollbar = tk.Scrollbar(status_frame, orient="vertical", 
                                       command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.pack(side="left", fill="both", expand=True)
        status_scrollbar.pack(side="right", fill="y")
        
        # 按钮
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        self.install_btn = tk.Button(button_frame, text="开始安装", 
                                    command=self.start_installation,
                                    bg="#4CAF50", fg="white", 
                                    font=("Arial", 12, "bold"))
        self.install_btn.pack(side="left", padx=(0, 10))
        
        self.cancel_btn = tk.Button(button_frame, text="取消", 
                                   command=self.root.quit)
        self.cancel_btn.pack(side="left")
        
        # 保存路径变量
        self.install_path = path_var
        
    def browse_path(self, path_var):
        """浏览安装路径"""
        path = filedialog.askdirectory(title="选择安装路径")
        if path:
            path_var.set(path)
    
    def log_message(self, message):
        """添加日志消息"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def check_system_requirements(self):
        """检查系统要求"""
        self.log_message("🔍 检查系统要求...")
        
        # 检查Windows版本
        import platform
        if platform.system() != "Windows":
            messagebox.showerror("错误", "此安装程序仅支持Windows系统")
            return False
        
        # 检查磁盘空间
        try:
            free_space = shutil.disk_usage(self.install_path.get()).free
            required_space = 2 * 1024 * 1024 * 1024  # 2GB
            if free_space < required_space:
                messagebox.showerror("错误", "磁盘空间不足，需要至少2GB可用空间")
                return False
        except:
            pass
        
        self.log_message("✅ 系统要求检查通过")
        return True
    
    def extract_installer_files(self):
        """解压安装文件"""
        self.log_message("📦 解压安装文件...")
        
        try:
            # 创建安装目录
            install_dir = Path(self.install_path.get())
            install_dir.mkdir(parents=True, exist_ok=True)
            
            # 解压内置的安装包
            installer_zip = Path("installer/installer_package.zip")
            if installer_zip.exists():
                with zipfile.ZipFile(installer_zip, 'r') as zip_ref:
                    zip_ref.extractall(install_dir)
                self.log_message("✅ 安装文件解压完成")
            else:
                self.log_message("⚠️ 未找到安装包，将使用在线下载")
                
        except Exception as e:
            self.log_message(f"❌ 解压失败: {e}")
            return False
        
        return True
    
    def install_python(self):
        """安装Python"""
        if not self.python_var.get():
            return True
            
        self.log_message("🐍 安装Python 3.10...")
        
        try:
            # 检查是否已安装
            result = subprocess.run(["python", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.log_message("✅ Python已安装")
                return True
            
            # 使用内置的Python安装包
            python_installer = Path("installer/python-3.10.0-amd64.exe")
            if python_installer.exists():
                subprocess.run([str(python_installer), "/quiet", "/InstallAllUsers=1"])
                self.log_message("✅ Python安装完成")
                return True
            else:
                self.log_message("⚠️ 未找到Python安装包，请手动安装")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Python安装失败: {e}")
            return False
    
    def install_nodejs(self):
        """安装Node.js"""
        if not self.nodejs_var.get():
            return True
            
        self.log_message("📦 安装Node.js...")
        
        try:
            # 检查是否已安装
            result = subprocess.run(["node", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.log_message("✅ Node.js已安装")
                return True
            
            # 使用内置的Node.js安装包
            nodejs_installer = Path("installer/node-v18.17.0-x64.msi")
            if nodejs_installer.exists():
                subprocess.run(["msiexec", "/i", str(nodejs_installer), "/quiet"])
                self.log_message("✅ Node.js安装完成")
                return True
            else:
                self.log_message("⚠️ 未找到Node.js安装包，请手动安装")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Node.js安装失败: {e}")
            return False
    
    def install_conda(self):
        """安装Miniconda"""
        if not self.conda_var.get():
            return True
            
        self.log_message("🐍 安装Miniconda...")
        
        try:
            # 检查是否已安装
            result = subprocess.run(["conda", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.log_message("✅ Miniconda已安装")
                return True
            
            # 使用内置的Miniconda安装包
            conda_installer = Path("installer/Miniconda3-latest-Windows-x86_64.exe")
            if conda_installer.exists():
                subprocess.run([str(conda_installer), "/S", "/D=%USERPROFILE%\\miniconda3"])
                self.log_message("✅ Miniconda安装完成")
                return True
            else:
                self.log_message("⚠️ 未找到Miniconda安装包，请手动安装")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Miniconda安装失败: {e}")
            return False
    
    def setup_environment(self):
        """设置环境"""
        self.log_message("🔧 设置Python环境...")
        
        try:
            install_dir = Path(self.install_path.get())
            
            # 创建conda环境
            conda_path = Path.home() / "miniconda3" / "Scripts" / "conda.exe"
            if conda_path.exists():
                subprocess.run([str(conda_path), "create", "-n", "py310", 
                              "python=3.10", "-y"])
                self.log_message("✅ Python环境创建完成")
            else:
                self.log_message("⚠️ 未找到conda，请先安装Miniconda")
                return False
            
            # 安装Python依赖
            requirements_file = install_dir / "requirements.txt"
            if requirements_file.exists():
                subprocess.run([str(conda_path), "run", "-n", "py310", 
                              "pip", "install", "-r", str(requirements_file)])
                self.log_message("✅ Python依赖安装完成")
            
            return True
            
        except Exception as e:
            self.log_message(f"❌ 环境设置失败: {e}")
            return False
    
    def setup_frontend(self):
        """设置前端"""
        self.log_message("🌐 设置前端环境...")
        
        try:
            install_dir = Path(self.install_path.get())
            frontend_dir = install_dir / "web_editor_vue"
            
            if frontend_dir.exists():
                # 安装Node.js依赖
                subprocess.run(["npm", "install"], cwd=frontend_dir)
                self.log_message("✅ 前端依赖安装完成")
                return True
            else:
                self.log_message("⚠️ 未找到前端目录")
                return False
                
        except Exception as e:
            self.log_message(f"❌ 前端设置失败: {e}")
            return False
    
    def create_shortcuts(self):
        """创建快捷方式"""
        self.log_message("🔗 创建快捷方式...")
        
        try:
            install_dir = Path(self.install_path.get())
            
            # 创建桌面快捷方式
            if self.desktop_shortcut_var.get():
                desktop = Path.home() / "Desktop"
                shortcut_path = desktop / "决策树系统.lnk"
                
                # 创建启动脚本
                start_script = install_dir / "start_system.bat"
                with open(start_script, "w", encoding="utf-8") as f:
                    f.write("""@echo off
chcp 65001 >nul
echo 启动决策树系统...
cd /d "%~dp0"
call conda activate py310
start python api_server.py
timeout /t 3 /nobreak >nul
cd web_editor_vue
start npm run dev
echo 系统启动完成！
echo 请访问: http://localhost:3000
pause
""")
                
                # 创建快捷方式
                import winshell
                from win32com.client import Dispatch
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(str(shortcut_path))
                shortcut.Targetpath = str(start_script)
                shortcut.WorkingDirectory = str(install_dir)
                shortcut.IconLocation = str(install_dir / "icon.ico")
                shortcut.save()
                
                self.log_message("✅ 桌面快捷方式创建完成")
            
            # 添加到开始菜单
            if self.start_menu_var.get():
                start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
                start_menu.mkdir(parents=True, exist_ok=True)
                
                shortcut_path = start_menu / "决策树系统.lnk"
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(str(shortcut_path))
                shortcut.Targetpath = str(start_script)
                shortcut.WorkingDirectory = str(install_dir)
                shortcut.IconLocation = str(install_dir / "icon.ico")
                shortcut.save()
                
                self.log_message("✅ 开始菜单快捷方式创建完成")
            
            return True
            
        except Exception as e:
            self.log_message(f"❌ 快捷方式创建失败: {e}")
            return False
    
    def start_installation(self):
        """开始安装"""
        # 禁用安装按钮
        self.install_btn.config(state="disabled")
        
        # 在新线程中运行安装
        install_thread = threading.Thread(target=self.run_installation)
        install_thread.daemon = True
        install_thread.start()
    
    def run_installation(self):
        """运行安装过程"""
        try:
            # 检查系统要求
            if not self.check_system_requirements():
                return
            
            # 解压安装文件
            if not self.extract_installer_files():
                return
            
            # 安装组件
            steps = [
                ("安装Python", self.install_python),
                ("安装Node.js", self.install_nodejs),
                ("安装Miniconda", self.install_conda),
                ("设置环境", self.setup_environment),
                ("设置前端", self.setup_frontend),
                ("创建快捷方式", self.create_shortcuts)
            ]
            
            for i, (step_name, step_func) in enumerate(steps):
                self.progress["value"] = (i + 1) * 100 // len(steps)
                
                if not step_func():
                    messagebox.showerror("安装失败", f"{step_name}失败，请查看日志")
                    return
                
                self.log_message(f"✅ {step_name}完成")
            
            # 安装完成
            self.progress["value"] = 100
            self.log_message("🎉 安装完成！")
            
            messagebox.showinfo("安装完成", 
                              "决策树系统安装完成！\n\n"
                              "您可以通过以下方式启动系统：\n"
                              "1. 双击桌面快捷方式\n"
                              "2. 从开始菜单启动\n"
                              "3. 运行 start_system.bat")
            
            # 重新启用安装按钮
            self.install_btn.config(state="normal")
            
        except Exception as e:
            self.log_message(f"❌ 安装过程出错: {e}")
            messagebox.showerror("安装失败", f"安装过程出错：{e}")
            self.install_btn.config(state="normal")
    
    def run(self):
        """运行安装程序"""
        self.root.mainloop()

if __name__ == "__main__":
    installer = DecisionTreeInstaller()
    installer.run() 