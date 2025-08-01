#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import zipfile
import requests
from pathlib import Path

class InstallerBuilder:
    def __init__(self):
        self.installer_dir = Path("installer")
        self.installer_dir.mkdir(exist_ok=True)
        
        # 需要下载的文件
        self.downloads = {
            "python": {
                "url": "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe",
                "filename": "python-3.10.0-amd64.exe"
            },
            "nodejs": {
                "url": "https://nodejs.org/dist/v18.17.0/node-v18.17.0-x64.msi",
                "filename": "node-v18.17.0-x64.msi"
            },
            "miniconda": {
                "url": "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe",
                "filename": "Miniconda3-latest-Windows-x86_64.exe"
            }
        }
    
    def download_file(self, url, filename):
        """下载文件"""
        filepath = self.installer_dir / filename
        
        if filepath.exists():
            print(f"✅ {filename} 已存在")
            return True
        
        print(f"📥 下载 {filename}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ {filename} 下载完成")
            return True
            
        except Exception as e:
            print(f"❌ {filename} 下载失败: {e}")
            return False
    
    def download_all_files(self):
        """下载所有必要文件"""
        print("🚀 开始下载安装文件...")
        
        for name, info in self.downloads.items():
            if not self.download_file(info["url"], info["filename"]):
                return False
        
        return True
    
    def create_installer_package(self):
        """创建安装包"""
        print("📦 创建安装包...")
        
        # 创建临时目录
        temp_dir = Path("temp_installer")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()
        
        # 复制项目文件
        project_files = [
            "api_server.py",
            "ai_chat_parser.py",
            "problem_locator.py",
            "direct_ai_call.py",
            "requirements.txt",
            "README.md"
        ]
        
        for file in project_files:
            if Path(file).exists():
                shutil.copy2(file, temp_dir)
        
        # 复制配置目录
        if Path("config").exists():
            shutil.copytree("config", temp_dir / "config")
        
        # 复制前端目录
        if Path("web_editor_vue").exists():
            shutil.copytree("web_editor_vue", temp_dir / "web_editor_vue")
        
        # 复制调试和测试目录
        for dir_name in ["debug", "test"]:
            if Path(dir_name).exists():
                shutil.copytree(dir_name, temp_dir / dir_name)
        
        # 创建启动脚本
        start_script = temp_dir / "start_system.bat"
        with open(start_script, "w", encoding="utf-8") as f:
            f.write("""@echo off
chcp 65001 >nul
echo ==========================================
echo 🤖 决策树可视化编辑器
echo ==========================================
echo.
echo 启动服务中，请稍候...
echo.

cd /d "%~dp0"

:: 激活conda环境
call conda activate py310

:: 启动后端
echo 启动后端服务器...
start /B python api_server.py

:: 等待后端启动
timeout /t 5 /nobreak >nul

:: 启动前端
echo 启动前端服务器...
cd web_editor_vue
start /B npm run dev
cd ..

echo.
echo ==========================================
echo 🎉 系统启动完成！
echo ==========================================
echo 前端地址: http://localhost:3000
echo 后端地址: http://localhost:5000
echo.
echo 按任意键退出...
pause >nul
""")
        
        # 创建图标文件（如果有的话）
        icon_file = Path("icon.ico")
        if icon_file.exists():
            shutil.copy2(icon_file, temp_dir)
        
        # 创建安装包
        package_file = self.installer_dir / "installer_package.zip"
        with zipfile.ZipFile(package_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arc_name)
        
        # 清理临时目录
        shutil.rmtree(temp_dir)
        
        print(f"✅ 安装包创建完成: {package_file}")
        return True
    
    def create_standalone_installer(self):
        """创建独立安装程序"""
        print("🔧 创建独立安装程序...")
        
        # 创建主安装程序
        main_installer = self.installer_dir / "DecisionTreeInstaller.exe"
        
        # 使用PyInstaller打包（如果可用）
        try:
            import PyInstaller.__main__
            
            PyInstaller.__main__.run([
                'installer/installer.py',
                '--onefile',
                '--windowed',
                '--name=DecisionTreeInstaller',
                '--distpath=installer',
                '--workpath=build',
                '--specpath=build'
            ])
            
            print(f"✅ 独立安装程序创建完成: {main_installer}")
            return True
            
        except ImportError:
            print("⚠️ PyInstaller未安装，跳过独立安装程序创建")
            return False
    
    def create_readme(self):
        """创建安装说明"""
        readme_content = """# 决策树系统安装程序

## 文件说明

- `DecisionTreeInstaller.exe` - 图形界面安装程序
- `installer.py` - 安装程序源码
- `installer_package.zip` - 项目文件包
- `python-3.10.0-amd64.exe` - Python 3.10安装包
- `node-v18.17.0-x64.msi` - Node.js安装包
- `Miniconda3-latest-Windows-x86_64.exe` - Miniconda安装包

## 使用方法

1. 双击运行 `DecisionTreeInstaller.exe`
2. 选择安装路径
3. 选择需要安装的组件
4. 点击"开始安装"
5. 等待安装完成

## 系统要求

- Windows 10 或更高版本
- 至少 2GB 可用磁盘空间
- 管理员权限（推荐）

## 安装后使用

安装完成后，您可以通过以下方式启动系统：

1. 桌面快捷方式
2. 开始菜单
3. 运行 `start_system.bat`

## 技术支持

如遇问题，请查看安装日志或联系技术支持。
"""
        
        readme_file = self.installer_dir / "README.txt"
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print("✅ 安装说明创建完成")
    
    def build(self):
        """构建完整安装程序"""
        print("🚀 开始构建安装程序...")
        
        # 下载必要文件
        if not self.download_all_files():
            print("❌ 文件下载失败")
            return False
        
        # 创建安装包
        if not self.create_installer_package():
            print("❌ 安装包创建失败")
            return False
        
        # 创建独立安装程序
        self.create_standalone_installer()
        
        # 创建说明文件
        self.create_readme()
        
        print("\n🎉 安装程序构建完成！")
        print(f"📁 安装程序位于: {self.installer_dir.absolute()}")
        print("\n📋 包含文件:")
        for file in self.installer_dir.iterdir():
            print(f"  - {file.name}")
        
        return True

def main():
    builder = InstallerBuilder()
    builder.build()

if __name__ == "__main__":
    main() 