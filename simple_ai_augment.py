#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import json
from typing import Dict, Optional

# 导入AI处理模块
from ai_chat_parser import AIChatParser
from tree_visualizer import TreeVisualizer

class SimpleAIAugment:
    def __init__(self):
        """初始化简化的AI增强器"""
        self.parser = AIChatParser()
        self.visualizer = TreeVisualizer()
        self.tree_file = "config/decision_tree.yaml"
        
    def load_existing_tree(self) -> Dict:
        """加载现有决策树"""
        try:
            with open(self.tree_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data.get('decision_tree', {})
        except Exception as e:
            print(f"[ERROR] 加载决策树失败: {e}")
            return {"root_node": "start", "nodes": {}}
    
    def save_tree(self, tree_data: Dict):
        """保存决策树"""
        try:
            data = {"decision_tree": tree_data}
            with open(self.tree_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)
            print(f"[OK] 决策树已保存: {self.tree_file}")
        except Exception as e:
            print(f"[ERROR] 保存决策树失败: {e}")
    
    def process_chat_and_merge(self, chat_history: str, auto_confirm: bool = False) -> bool:
        """处理聊天记录并合并到决策树"""
        print("开始AI决策树增强...")
        
        # 1. 加载现有决策树
        existing_tree = self.load_existing_tree()
        print(f"现有节点数: {len(existing_tree.get('nodes', {}))}")
        
        # 2. AI解析聊天记录
        print("[DEBUG] AI解析聊天记录...")
        result = self.parser.process_chat_and_generate_tree(chat_history, existing_tree)
        
        if not result.get('success', False):
            print(f"[ERROR] AI解析失败: {result.get('error', '未知错误')}")
            return False
        
        new_nodes = result['new_nodes']
        print(f"[OK] AI解析完成，生成 {len(new_nodes.get('nodes', {}))} 个新节点")
        
        # 3. 生成可视化预览
        print("生成可视化预览...")
        viz_data = self.visualizer.generate_visualization_data(existing_tree, new_nodes)
        diff_report = self.visualizer.generate_diff_report(existing_tree, new_nodes)
        
        # 4. 显示变更摘要
        self._show_changes_summary(diff_report)
        
        # 5. 用户确认
        if not auto_confirm:
            confirm = input("\n是否确认合并这些变更？(y/n): ").strip().lower()
            if confirm not in ['y', 'yes', '是']:
                print("[ERROR] 用户取消操作")
                return False
        
        # 6. 合并决策树
        print("🔗 合并决策树...")
        merged_tree = self._merge_trees(existing_tree, new_nodes)
        
        # 7. 保存决策树
        print("[SAVE] 保存决策树...")
        self.save_tree(merged_tree)
        
        # 8. 生成可视化文件
        print("生成可视化文件...")
        viz_file = self.visualizer.save_visualization(viz_data)
        print(f"[OK] 可视化文件已生成: {viz_file}")
        
        print(" AI决策树增强完成！")
        return True
    
    def _show_changes_summary(self, diff_report: Dict):
        """显示变更摘要"""
        print("\n变更摘要:")
        print(f"  - 新增节点: {diff_report['summary']['added']}")
        print(f"  - 修改节点: {diff_report['summary']['modified']}")
        print(f"  - 删除节点: {diff_report['summary']['deleted']}")
        
        if diff_report['details']['added_nodes']:
            print("\n🆕 新增节点:")
            for node_id in diff_report['details']['added_nodes']:
                print(f"    - {node_id}")
        
        if diff_report['details']['modified_nodes']:
            print("\n修改节点:")
            for node_id in diff_report['details']['modified_nodes']:
                print(f"    - {node_id}")
    
    def _merge_trees(self, original_tree: Dict, new_nodes: Dict) -> Dict:
        """合并决策树"""
        merged = original_tree.copy()
        
        # 合并节点
        if 'nodes' in new_nodes:
            merged['nodes'] = merged.get('nodes', {}).copy()
            merged['nodes'].update(new_nodes['nodes'])
        
        # 合并根节点（如果新树有根节点）
        if 'root_node' in new_nodes:
            merged['root_node'] = new_nodes['root_node']
        
        return merged
    
    def interactive_mode(self):
        """交互模式"""
        print("🎮 进入AI决策树增强交互模式")
        print("输入聊天记录，输入 'quit' 退出，输入 'auto' 启用自动确认模式")
        
        auto_confirm = False
        
        while True:
            print("\n" + "="*50)
            chat_history = input("请输入聊天记录 (或输入 'quit'/'auto'): ").strip()
            
            if chat_history.lower() == 'quit':
                break
            elif chat_history.lower() == 'auto':
                auto_confirm = not auto_confirm
                print(f"自动确认模式: {'开启' if auto_confirm else '关闭'}")
                continue
            elif not chat_history:
                continue
            
            # 处理聊天记录
            success = self.process_chat_and_merge(chat_history, auto_confirm)
            
            if success:
                print("[OK] 处理成功!")
            else:
                print("[ERROR] 处理失败")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="简化AI决策树增强器")
    parser.add_argument("--input", help="输入聊天记录文件")
    parser.add_argument("--auto", action="store_true", help="自动确认模式")
    parser.add_argument("--interactive", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    augmentor = SimpleAIAugment()
    
    if args.interactive:
        augmentor.interactive_mode()
    elif args.input:
        if not os.path.exists(args.input):
            print(f"[ERROR] 文件不存在: {args.input}")
            return
        
        with open(args.input, 'r', encoding='utf-8') as f:
            chat_history = f.read()
        
        success = augmentor.process_chat_and_merge(chat_history, args.auto)
        
        if success:
            print("[OK] 处理成功!")
        else:
            print("[ERROR] 处理失败")
    else:
        print("请指定输入文件或使用交互模式")
        print("用法:")
        print("  python simple_ai_augment.py --input chat.txt")
        print("  python simple_ai_augment.py --interactive")

if __name__ == "__main__":
    main() 