#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import json
from typing import Dict, List, Optional
from datetime import datetime

# 导入自定义模块
from ai_chat_parser import AIChatParser
from tree_visualizer import TreeVisualizer
from web_confirmation_ui import WebConfirmationUI

class AITreeAugmentor:
    def __init__(self, config_dir: str = "config"):
        """初始化AI决策树增强器"""
        self.config_dir = config_dir
        self.parser = AIChatParser()
        self.visualizer = TreeVisualizer()
        self.ui = WebConfirmationUI()
        
        # 加载现有决策树
        self.tree_file = os.path.join(config_dir, "decision_tree.yaml")
        self.existing_tree = self._load_existing_tree()
        
    def _load_existing_tree(self) -> Dict:
        """加载现有决策树"""
        try:
            with open(self.tree_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data.get('decision_tree', {})
        except Exception as e:
            print(f"[ERROR] 加载决策树失败: {e}")
            return {"root_node": "start", "nodes": {}}
    
    def _save_tree(self, tree_data: Dict):
        """保存决策树"""
        try:
            data = {"decision_tree": tree_data}
            with open(self.tree_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)
            print(f"[OK] 决策树已保存: {self.tree_file}")
        except Exception as e:
            print(f"[ERROR] 保存决策树失败: {e}")
    
    def process_chat_and_augment(self, chat_history: str, auto_merge: bool = False) -> Dict:
        """处理聊天记录并增强决策树"""
        print("开始AI决策树增强流程...")
        
        # 1. AI解析聊天记录
        print("📝 步骤1: AI解析聊天记录...")
        parse_result = self.parser.process_chat_and_generate_tree(chat_history, self.existing_tree)
        
        if not parse_result.get('success', False):
            return {"success": False, "error": parse_result.get('error', '解析失败')}
        
        new_nodes = parse_result['new_nodes']
        confirmation_message = parse_result.get('confirmation_message', '发现新的问题定位路径')
        
        # 2. 生成可视化数据
        print("步骤2: 生成可视化数据...")
        viz_data = self.visualizer.generate_visualization_data(self.existing_tree, new_nodes)
        diff_report = self.visualizer.generate_diff_report(self.existing_tree, new_nodes)
        
        # 3. 用户确认和编辑
        if not auto_merge:
            print("[USER] 步骤3: 用户确认和编辑...")
            modified_tree = self.ui.show_confirmation_dialog(
                self.existing_tree, 
                new_nodes, 
                confirmation_message
            )
            
            if modified_tree is None:
                return {"success": False, "error": "用户取消操作"}
            
            # 4. 保存修改后的决策树
            print("[SAVE] 步骤4: 保存决策树...")
            self._save_tree(modified_tree)
            
            return {
                "success": True,
                "original_tree": self.existing_tree,
                "new_nodes": new_nodes,
                "modified_tree": modified_tree,
                "visualization_data": viz_data,
                "diff_report": diff_report,
                "timestamp": datetime.now().isoformat()
            }
        else:
            # 自动合并模式
            print("[AI] 自动合并模式...")
            merged_tree = self._merge_trees_auto(self.existing_tree, new_nodes)
            self._save_tree(merged_tree)
            
            return {
                "success": True,
                "original_tree": self.existing_tree,
                "new_nodes": new_nodes,
                "merged_tree": merged_tree,
                "visualization_data": viz_data,
                "diff_report": diff_report,
                "timestamp": datetime.now().isoformat()
            }
    
    def _merge_trees_auto(self, original_tree: Dict, new_nodes: Dict) -> Dict:
        """自动合并决策树"""
        merged = original_tree.copy()
        
        # 合并节点
        if 'nodes' in new_nodes:
            merged['nodes'] = merged.get('nodes', {}).copy()
            merged['nodes'].update(new_nodes['nodes'])
        
        # 合并根节点（如果新树有根节点）
        if 'root_node' in new_nodes:
            merged['root_node'] = new_nodes['root_node']
        
        return merged
    
    def batch_process_chats(self, chat_files: List[str], auto_merge: bool = False) -> List[Dict]:
        """批量处理聊天记录文件"""
        print(f"开始批量处理 {len(chat_files)} 个聊天记录文件...")
        
        results = []
        for i, chat_file in enumerate(chat_files, 1):
            print(f"\n📄 处理文件 {i}/{len(chat_files)}: {chat_file}")
            
            try:
                with open(chat_file, 'r', encoding='utf-8') as f:
                    chat_history = f.read()
                
                result = self.process_chat_and_augment(chat_history, auto_merge)
                result['source_file'] = chat_file
                results.append(result)
                
                if result['success']:
                    print(f"[OK] 文件 {chat_file} 处理成功")
                else:
                    print(f"[ERROR] 文件 {chat_file} 处理失败: {result.get('error', '未知错误')}")
                    
            except Exception as e:
                print(f"[ERROR] 处理文件 {chat_file} 时发生错误: {e}")
                results.append({
                    "success": False,
                    "source_file": chat_file,
                    "error": str(e)
                })
        
        return results
    
    def generate_report(self, results: List[Dict], output_file: str = "augmentation_report.html"):
        """生成处理报告"""
        print("生成处理报告...")
        
        html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI决策树增强报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
        .summary { background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .error { background-color: #ffebee; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .file-result { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .success { border-left: 5px solid #4caf50; }
        .failure { border-left: 5px solid #f44336; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI决策树增强报告</h1>
        <p>生成时间: {timestamp}</p>
        <p>处理文件数: {total_files}</p>
    </div>
    
    <div class="summary">
        <h2>处理摘要</h2>
        <table>
            <tr>
                <th>指标</th>
                <th>数量</th>
            </tr>
            <tr>
                <td>总文件数</td>
                <td>{total_files}</td>
            </tr>
            <tr>
                <td>成功处理</td>
                <td>{success_count}</td>
            </tr>
            <tr>
                <td>处理失败</td>
                <td>{failure_count}</td>
            </tr>
            <tr>
                <td>新增节点总数</td>
                <td>{total_new_nodes}</td>
            </tr>
        </table>
    </div>
    
    <h2>详细结果</h2>
    {file_results}
</body>
</html>
        """
        
        # 统计数据
        total_files = len(results)
        success_count = sum(1 for r in results if r['success'])
        failure_count = total_files - success_count
        total_new_nodes = sum(
            len(r.get('new_nodes', {}).get('nodes', {})) 
            for r in results if r['success']
        )
        
        # 生成文件结果HTML
        file_results_html = ""
        for result in results:
            if result['success']:
                file_results_html += f"""
                <div class="file-result success">
                    <h3>[OK] {result['source_file']}</h3>
                    <p><strong>新增节点:</strong> {len(result['new_nodes'].get('nodes', {}))}</p>
                    <p><strong>修改节点:</strong> {len(result['diff_report']['details']['modified_nodes'])}</p>
                    <p><strong>处理时间:</strong> {result['timestamp']}</p>
                </div>
                """
            else:
                file_results_html += f"""
                <div class="file-result failure">
                    <h3>[ERROR] {result['source_file']}</h3>
                    <p><strong>错误:</strong> {result.get('error', '未知错误')}</p>
                </div>
                """
        
        # 生成完整HTML
        html_content = html_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_files=total_files,
            success_count=success_count,
            failure_count=failure_count,
            total_new_nodes=total_new_nodes,
            file_results=file_results_html
        )
        
        # 保存报告
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[OK] 报告已生成: {output_file}")
        return output_file
    
    def interactive_mode(self):
        """交互模式"""
        print("🎮 进入交互模式...")
        print("输入聊天记录，输入 'quit' 退出，输入 'auto' 启用自动合并模式")
        
        auto_merge = False
        
        while True:
            print("\n" + "="*50)
            chat_history = input("请输入聊天记录 (或输入 'quit'/'auto'): ").strip()
            
            if chat_history.lower() == 'quit':
                break
            elif chat_history.lower() == 'auto':
                auto_merge = not auto_merge
                print(f"自动合并模式: {'开启' if auto_merge else '关闭'}")
                continue
            elif not chat_history:
                continue
            
            # 处理聊天记录
            result = self.process_chat_and_augment(chat_history, auto_merge)
            
            if result['success']:
                print("[OK] 处理成功!")
                print(f"新增节点: {len(result['new_nodes'].get('nodes', {}))}")
                print(f"修改节点: {len(result['diff_report']['details']['modified_nodes'])}")
            else:
                print(f"[ERROR] 处理失败: {result.get('error', '未知错误')}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI决策树增强器")
    parser.add_argument("--mode", choices=["interactive", "file", "batch"], 
                       default="interactive", help="运行模式")
    parser.add_argument("--input", help="输入文件或聊天记录")
    parser.add_argument("--auto", action="store_true", help="启用自动合并模式")
    parser.add_argument("--output", help="输出报告文件")
    
    args = parser.parse_args()
    
    augmentor = AITreeAugmentor()
    
    if args.mode == "interactive":
        augmentor.interactive_mode()
    elif args.mode == "file":
        if not args.input:
            print("[ERROR] 请指定输入文件")
            return
        
        if not os.path.exists(args.input):
            print(f"[ERROR] 文件不存在: {args.input}")
            return
        
        with open(args.input, 'r', encoding='utf-8') as f:
            chat_history = f.read()
        
        result = augmentor.process_chat_and_augment(chat_history, args.auto)
        
        if result['success']:
            print("[OK] 处理成功!")
            print(f"新增节点: {len(result['new_nodes'].get('nodes', {}))}")
        else:
            print(f"[ERROR] 处理失败: {result.get('error', '未知错误')}")
    
    elif args.mode == "batch":
        if not args.input:
            print("[ERROR] 请指定输入目录")
            return
        
        if not os.path.isdir(args.input):
            print(f"[ERROR] 目录不存在: {args.input}")
            return
        
        # 查找所有聊天记录文件
        chat_files = []
        for root, dirs, files in os.walk(args.input):
            for file in files:
                if file.endswith(('.txt', '.log', '.chat')):
                    chat_files.append(os.path.join(root, file))
        
        if not chat_files:
            print(f"[ERROR] 在目录 {args.input} 中未找到聊天记录文件")
            return
        
        results = augmentor.batch_process_chats(chat_files, args.auto)
        
        # 生成报告
        if args.output:
            augmentor.generate_report(results, args.output)
        else:
            augmentor.generate_report(results)

if __name__ == "__main__":
    main() 