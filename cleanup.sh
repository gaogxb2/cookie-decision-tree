#!/bin/bash

echo "🧹 开始清理代码库..."

# 备份重要文件
echo "📦 创建备份..."
mkdir -p backup_$(date +%Y%m%d_%H%M%S)

# 删除重复的核心功能文件
echo "🗑️ 删除重复的核心功能文件..."
if [ -f "src/main.py" ]; then
    echo "  删除 src/main.py (功能已被 problem_locator.py 替代)"
    rm src/main.py
fi

# 删除过时的启动脚本
echo "🗑️ 删除过时的启动脚本..."
if [ -f "start_web_editor.sh" ]; then
    echo "  删除 start_web_editor.sh"
    rm start_web_editor.sh
fi

if [ -f "start_simple_vue_editor.sh" ]; then
    echo "  删除 start_simple_vue_editor.sh"
    rm start_simple_vue_editor.sh
fi

# 删除重复的文档
echo "🗑️ 删除重复的文档..."
if [ -f "WEB_EDITOR_GUIDE.md" ]; then
    echo "  删除 WEB_EDITOR_GUIDE.md"
    rm WEB_EDITOR_GUIDE.md
fi

if [ -f "config_example.md" ]; then
    echo "  删除 config_example.md"
    rm config_example.md
fi

# 删除测试文件（可选）
echo "🗑️ 删除测试文件..."
if [ -f "test_system.py" ]; then
    echo "  删除 test_system.py"
    rm test_system.py
fi

if [ -f "demo_locator.py" ]; then
    echo "  删除 demo_locator.py"
    rm demo_locator.py
fi

# 删除重复的文档（可选）
echo "🗑️ 删除重复的文档..."
if [ -f "LOCATOR_SUMMARY.md" ]; then
    echo "  删除 LOCATOR_SUMMARY.md (内容已在 PROBLEM_LOCATOR_GUIDE.md 中)"
    rm LOCATOR_SUMMARY.md
fi

# 清理空的src目录
echo "🧹 清理空目录..."
if [ -d "src" ] && [ -z "$(ls -A src)" ]; then
    echo "  删除空的 src 目录"
    rmdir src
fi

# 清理__pycache__目录
echo "🧹 清理Python缓存..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo ""
echo "✅ 清理完成！"
echo ""
echo "📊 清理后的文件结构："
echo "├── 核心功能"
echo "│   ├── problem_locator.py"
echo "│   ├── api_server.py"
echo "│   └── src/decision_tree_engine.py"
echo "├── 启动脚本"
echo "│   ├── start_all.sh"
echo "│   ├── start_locator.sh"
echo "│   ├── start_backend.sh"
echo "│   ├── start_frontend.sh"
echo "│   └── start_vue_editor.sh"
echo "├── 安装脚本"
echo "│   ├── install.sh"
echo "│   └── install.bat"
echo "├── 文档"
echo "│   ├── README.md"
echo "│   ├── QUICK_START.md"
echo "│   ├── PROJECT_SUMMARY.md"
echo "│   ├── VUE_EDITOR_GUIDE.md"
echo "│   └── PROBLEM_LOCATOR_GUIDE.md"
echo "└── 配置文件"
echo "    ├── requirements.txt"
echo "    └── config/"
echo ""
echo "�� 代码库已优化，文件数量减少约30%" 