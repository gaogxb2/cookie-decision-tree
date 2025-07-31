#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import re
from typing import Dict, List, Optional, Tuple

class ProblemLocator:
    def __init__(self, config_file: str = "config/decision_tree.yaml"):
        """初始化问题定位器"""
        self.config_file = config_file
        self.config = self._load_config()
        self.current_node = self.config['decision_tree']['root_node']
        self.diagnostic_path = []
        
    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
            sys.exit(1)
    
    def _fuzzy_match(self, user_input: str, option_text: str) -> float:
        """模糊匹配用户输入和选项文本"""
        # 转换为小写进行比较
        user_lower = user_input.lower().strip()
        option_lower = option_text.lower().strip()
        
        # 完全匹配
        if user_lower == option_lower:
            return 1.0
        
        # 包含匹配
        if user_lower in option_lower or option_lower in user_lower:
            return 0.8
        
        # 关键词匹配
        user_words = set(re.findall(r'\w+', user_lower))
        option_words = set(re.findall(r'\w+', option_lower))
        
        if user_words and option_words:
            intersection = user_words & option_words
            union = user_words | option_words
            if union:
                return len(intersection) / len(union)
        
        return 0.0
    
    def _find_best_match(self, user_input: str, options: List[Dict]) -> Optional[Tuple[int, Dict]]:
        """找到最佳匹配的选项"""
        best_match = None
        best_score = 0.0
        
        for i, option in enumerate(options):
            score = self._fuzzy_match(user_input, option['text'])
            if score > best_score:
                best_score = score
                best_match = (i, option)
        
        # 设置匹配阈值
        if best_score >= 0.3:  # 30%的匹配度
            return best_match
        return None
    
    def _get_node_info(self, node_id: str) -> Optional[Dict]:
        """获取节点信息"""
        nodes = self.config['decision_tree']['nodes']
        return nodes.get(node_id)
    
    def _display_current_question(self):
        """显示当前问题"""
        node_data = self._get_node_info(self.current_node)
        if not node_data:
            print(f"❌ 错误: 找不到节点 '{self.current_node}'")
            return False
        
        if 'solution' in node_data:
            # 这是一个解决方案节点
            print("\n" + "=" * 60)
            print("✅ 问题定位完成！")
            print("=" * 60)
            print(f"💡 解决方案:")
            print("-" * 40)
            print(node_data['solution'])
            print("-" * 40)
            return True
        elif 'question' in node_data:
            # 这是一个决策节点
            print(f"\n❓ {node_data['question']}")
            print("\n选项:")
            for i, option in enumerate(node_data['options'], 1):
                print(f"  {i}. {option['text']}")
            return False
        else:
            print(f"❌ 错误: 节点 '{self.current_node}' 格式不正确")
            return False
    
    def _process_user_input(self, user_input: str) -> bool:
        """处理用户输入"""
        node_data = self._get_node_info(self.current_node)
        if not node_data or 'options' not in node_data:
            print("❌ 当前节点没有选项")
            return False
        
        # 尝试数字匹配
        try:
            choice_num = int(user_input.strip())
            if 1 <= choice_num <= len(node_data['options']):
                selected_option = node_data['options'][choice_num - 1]
                self._move_to_next_node(selected_option)
                return True
        except ValueError:
            pass
        
        # 尝试文本匹配
        best_match = self._find_best_match(user_input, node_data['options'])
        if best_match:
            index, selected_option = best_match
            print(f"✅ 匹配到选项: {selected_option['text']}")
            self._move_to_next_node(selected_option)
            return True
        else:
            print("❌ 无法匹配您的输入，请重新选择")
            return False
    
    def _move_to_next_node(self, selected_option: Dict):
        """移动到下一个节点"""
        next_node = selected_option.get('next_node')
        if not next_node:
            print("❌ 选项没有指向下一个节点")
            return
        
        # 记录诊断路径
        self.diagnostic_path.append({
            'node': self.current_node,
            'choice': selected_option['text'],
            'next_node': next_node
        })
        
        # 更新当前节点
        self.current_node = next_node
    
    def _display_diagnostic_path(self):
        """显示诊断路径"""
        if not self.diagnostic_path:
            return
        
        print(f"\n📋 诊断路径:")
        print("-" * 40)
        for i, step in enumerate(self.diagnostic_path, 1):
            print(f"{i}. {step['choice']}")
        print("-" * 40)
    
    def start_diagnostic(self):
        """开始问题诊断"""
        print("=" * 60)
        print("🔍 AI问题定位系统")
        print("=" * 60)
        print("欢迎使用AI问题定位系统！")
        print("系统将根据您的回答，逐步定位问题并提供解决方案。")
        print("输入 'quit' 或 'exit' 退出系统")
        print("输入 'restart' 重新开始诊断")
        print("输入 'path' 查看当前诊断路径")
        print("输入 'back' 返回上一步")
        print("-" * 60)
        
        # 诊断历史记录
        self.diagnostic_history = []
        
        while True:
            try:
                # 显示当前问题
                if self._display_current_question():
                    # 已到达解决方案
                    self._display_diagnostic_path()
                    break
                
                # 获取用户输入
                user_input = input("\n请输入您的选择: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n感谢使用AI问题定位系统！再见！")
                    break
                elif user_input.lower() in ['restart', 'r']:
                    print("\n重新开始诊断...")
                    self.current_node = self.config['decision_tree']['root_node']
                    self.diagnostic_path = []
                    self.diagnostic_history = []
                    continue
                elif user_input.lower() in ['path', 'p']:
                    self._display_diagnostic_path()
                    continue
                elif user_input.lower() in ['back', 'b']:
                    if self.diagnostic_path:
                        # 返回上一步
                        last_step = self.diagnostic_path.pop()
                        self.current_node = self._find_previous_node(last_step['node'])
                        print(f"↩️ 已返回上一步: {last_step['choice']}")
                    else:
                        print("❌ 没有可返回的步骤")
                    continue
                
                # 处理用户输入
                if not self._process_user_input(user_input):
                    continue
                    
            except KeyboardInterrupt:
                print("\n\n程序被中断。再见！")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                continue
    
    def _find_previous_node(self, current_node: str) -> str:
        """找到上一个节点"""
        # 遍历所有节点，找到指向当前节点的选项
        nodes = self.config['decision_tree']['nodes']
        for node_id, node_data in nodes.items():
            if 'options' in node_data:
                for option in node_data['options']:
                    if option.get('next_node') == current_node:
                        return node_id
        
        # 如果找不到，返回根节点
        return self.config['decision_tree']['root_node']

def main():
    """主函数"""
    try:
        # 检查配置文件是否存在
        config_file = "config/decision_tree.yaml"
        if not os.path.exists(config_file):
            print(f"❌ 错误: 配置文件 {config_file} 不存在")
            print("请确保配置文件存在并且格式正确。")
            return
        
        # 创建并启动问题定位系统
        locator = ProblemLocator(config_file)
        locator.start_diagnostic()
        
    except Exception as e:
        print(f"❌ 系统启动失败: {e}")
        print("请检查配置文件格式是否正确。")

if __name__ == "__main__":
    main() 