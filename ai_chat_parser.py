#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import openai
import requests
import platform

# 检测操作系统，在 Windows 下使用安全的字符
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

# 获取安全字符
safe_chars = get_safe_chars()

class AIChatParser:
    def __init__(self, ai_config_file: str = "config/ai_config.yaml", 
                 prompts_file: str = "config/prompts.yaml"):
        """初始化AI聊天记录解析器"""
        self.ai_config = self._load_config(ai_config_file)
        self.prompts = self._load_config(prompts_file)
        self.client = self._init_ai_client()
        
    def _load_config(self, config_file: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"{safe_chars['error']} 加载配置文件失败: {e}")
            sys.exit(1)
    
    def _init_ai_client(self):
        """初始化AI客户端"""
        api_type = self.ai_config['ai']['current_api']
        api_config = self.ai_config['ai']['api'][api_type]
        
        if api_type == "dashscope":
            api_key = os.getenv('DASHSCOPE_API_KEY')
            if not api_key:
                raise ValueError("请设置DASHSCOPE_API_KEY环境变量")
            
            return openai.OpenAI(
                api_key=api_key,
                base_url=api_config['base_url']
            )
        elif api_type == "openai":
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("请设置OPENAI_API_KEY环境变量")
            
            return openai.OpenAI(
                api_key=api_key,
                base_url=api_config['base_url']
            )
        elif api_type == "azure":
            api_key = os.getenv('AZURE_OPENAI_API_KEY')
            if not api_key:
                raise ValueError("请设置AZURE_OPENAI_API_KEY环境变量")
            
            return openai.AzureOpenAI(
                api_key=api_key,
                azure_endpoint=api_config['base_url'],
                api_version=api_config['api_version']
            )
        elif api_type == "local":
            return openai.OpenAI(
                api_key="not-needed",
                base_url=api_config['base_url']
            )
        elif api_type == "custom_http":
            # 自定义HTTP请求不需要初始化客户端
            return None
        else:
            raise ValueError(f"不支持的API类型: {api_type}")
    
    def _call_ai_api(self, messages: List[Dict], model: str = None) -> str:
        """调用AI API"""
        try:
            api_type = self.ai_config['ai']['current_api']
            
            if api_type == "custom_http":
                return self._call_custom_http_api(messages)
            else:
                if model is None:
                    model = self.ai_config['ai']['api'][api_type]['model']
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=self.ai_config['ai']['api'][api_type]['temperature'],
                    max_tokens=self.ai_config['ai']['api'][api_type]['max_tokens']
                )
                
                return response.choices[0].message.content
        except Exception as e:
            print(f"{safe_chars['error']} AI API调用失败: {e}")
            return None
    
    def _messages_to_prompt(self, messages: List[Dict]) -> str:
        """将消息列表转换为单个提示文本"""
        prompt_parts = []
        
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            if role == 'system':
                prompt_parts.append(f"系统指令: {content}")
            elif role == 'user':
                prompt_parts.append(f"用户: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"助手: {content}")
        
        return '\n\n'.join(prompt_parts)
    
    def _call_custom_http_api(self, messages: List[Dict]) -> str:
        """调用自定义HTTP API"""
        try:
            api_config = self.ai_config['ai']['api']['custom_http']
            
            # 获取API密钥
            api_key_env = self.ai_config['ai']['api_keys']['custom_http']
            api_key = os.getenv(api_key_env.replace('${', '').replace('}', ''))
            if not api_key:
                raise ValueError(f"请设置{api_key_env}环境变量")
            
            # 准备请求头
            headers = {}
            for key, value in api_config['headers'].items():
                if value.startswith('${') and value.endswith('}'):
                    # 替换环境变量
                    env_var = value[2:-1]
                    headers[key] = os.getenv(env_var, value)
                else:
                    headers[key] = value
            
            # 将消息列表转换为单个提示文本
            prompt_text = self._messages_to_prompt(messages)
            
            # 构建请求体 - 使用您指定的格式
            body = {
                "inputs": prompt_text,
                "parameters": {
                    "detail": True,
                    "temperature": 0.1
                }
            }
            
            # 发送请求 - 使用您指定的方式
            response = requests.post(
                api_config['url'],
                headers=headers,
                data=json.dumps(body),
                timeout=30
            )
            
            if response.status_code != 200:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"{safe_chars['error']} 自定义HTTP API调用失败: {error_msg}")
                return None
            
            # 直接返回响应文本
            return response.text
            
        except Exception as e:
            print(f"{safe_chars['error']} 自定义HTTP API调用失败: {e}")
            return None
    
    def _extract_json_from_response(self, response: str) -> Dict:
        """从AI响应中提取JSON内容"""
        try:
            # 方法1: 尝试直接解析整个响应
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        try:
            # 方法2: 查找JSON代码块
            json_block_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_block_match:
                return json.loads(json_block_match.group(1))
        except json.JSONDecodeError:
            pass
        
        try:
            # 方法3: 查找任何JSON对象
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        
        try:
            # 方法4: 手动构建JSON结构
            # 查找nodes部分
            nodes_match = re.search(r'"nodes":\s*\{[^}]+\}', response, re.DOTALL)
            if nodes_match:
                # 构建基本的JSON结构
                json_str = "{" + nodes_match.group() + "}"
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # 如果所有方法都失败，返回None
        return None
    
    def parse_chat_history(self, chat_history: str, existing_tree: Dict = None) -> Dict:
        """解析聊天记录并生成决策树节点"""
        print("🔍 开始解析聊天记录...")
        
        system_prompt = self.prompts['chat_analysis']['system']
        user_prompt = self.prompts['chat_analysis']['user'].format(
            chat_history=chat_history
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._call_ai_api(messages)
        if not response:
            return None
        
        try:
            # 解析AI返回的路径数据
            path_data = self._extract_json_from_response(response)
            if not path_data:
                print("❌ 无法解析AI响应")
                return None
            
            # 将路径转换为决策树结构
            tree_data = self.convert_path_to_tree(path_data)
            if not tree_data:
                print("❌ 路径转换失败")
                return None
            
            return tree_data
            
        except Exception as e:
            print(f"❌ 解析失败: {e}")
            return None
    
    def validate_tree_nodes(self, new_nodes: Dict, existing_tree: Dict) -> Dict:
        """验证新生成的决策树节点"""
        print("✅ 验证决策树节点...")
        
        system_prompt = self.prompts['tree_validation']['system']
        user_prompt = self.prompts['tree_validation']['user'].format(
            existing_tree=json.dumps(existing_tree, ensure_ascii=False, indent=2),
            new_nodes=json.dumps(new_nodes, ensure_ascii=False, indent=2)
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._call_ai_api(messages)
        if not response:
            return {"valid": False, "errors": ["AI API调用失败"]}
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"valid": True, "message": response}
    
    def merge_nodes(self, existing_nodes: Dict, new_nodes: Dict) -> Dict:
        """将AI生成的路径挂到现有根节点"""
        print("🔗 合并决策树节点...")
        
        # 获取AI生成的入口节点和新节点
        entry_node = new_nodes.get('entry_node', '')
        new_nodes_dict = new_nodes.get('nodes', {})
        
        if not entry_node or not new_nodes_dict:
            print("❌ AI生成的节点数据不完整")
            return None
        
        # 获取现有决策树的根节点
        existing_root = existing_nodes.get('root_node', '')
        existing_nodes_dict = existing_nodes.get('nodes', {})
        
        if not existing_root or not existing_nodes_dict:
            print("❌ 现有决策树数据不完整")
            return None
        
        # 在现有根节点添加AI路径的入口选项
        if existing_root in existing_nodes_dict:
            # 获取入口节点的数据
            entry_node_data = new_nodes_dict.get(entry_node, {})
            entry_question = entry_node_data.get('question', '新问题')
            
            # 创建新的选项
            new_option = {
                "text": entry_question,
                "next_node": entry_node
            }
            
            # 添加到现有根节点的选项中
            if 'options' not in existing_nodes_dict[existing_root]:
                existing_nodes_dict[existing_root]['options'] = []
            
            # 检查是否已存在相同选项
            existing_options = [opt['text'] for opt in existing_nodes_dict[existing_root]['options']]
            if new_option['text'] not in existing_options:
                existing_nodes_dict[existing_root]['options'].append(new_option)
                print(f"✅ 已添加新选项: {new_option['text']} -> {entry_node}")
            else:
                print(f"⚠️ 选项已存在: {new_option['text']}")
        
        # 合并所有新节点到现有树
        existing_nodes_dict.update(new_nodes_dict)
        
        return {
            "merged_tree": {
                "root_node": existing_root,
                "nodes": existing_nodes_dict
            },
            "message": f"AI路径已挂接到根节点，入口节点: {entry_node}"
        }
    
    def classify_problem(self, problem_description: str, existing_categories: List[str]) -> Dict:
        """对问题进行分类"""
        print("🏷️ 对问题进行分类...")
        
        system_prompt = self.prompts['problem_classification']['system']
        user_prompt = self.prompts['problem_classification']['user'].format(
            problem_description=problem_description,
            existing_categories=json.dumps(existing_categories, ensure_ascii=False)
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._call_ai_api(messages)
        if not response:
            return None
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"category": "unknown", "reason": response}
    
    def optimize_solution(self, original_solution: str, problem_context: str) -> str:
        """优化解决方案"""
        print("✨ 优化解决方案...")
        
        system_prompt = self.prompts['solution_optimization']['system']
        user_prompt = self.prompts['solution_optimization']['user'].format(
            original_solution=original_solution,
            problem_context=problem_context
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._call_ai_api(messages)
        return response if response else original_solution
    
    def check_errors(self, tree_structure: Dict) -> Dict:
        """检查决策树错误"""
        print("🔍 检查决策树错误...")
        
        system_prompt = self.prompts['error_handling']['system']
        user_prompt = self.prompts['error_handling']['user'].format(
            tree_structure=json.dumps(tree_structure, ensure_ascii=False, indent=2)
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._call_ai_api(messages)
        if not response:
            return {"errors": [], "warnings": ["无法检查错误"]}
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"errors": [], "warnings": [response]}
    
    def generate_confirmation_message(self, changes: Dict) -> str:
        """生成用户确认信息"""
        print("📝 生成确认信息...")
        
        system_prompt = self.prompts['user_confirmation']['system']
        user_prompt = self.prompts['user_confirmation']['user'].format(
            changes=json.dumps(changes, ensure_ascii=False, indent=2)
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._call_ai_api(messages)
        return response if response else "请确认以下变更..."
    
    def process_chat_and_generate_tree(self, chat_history: str, existing_tree: Dict = None) -> Dict:
        """处理聊天记录并生成决策树节点"""
        print("🚀 开始处理聊天记录...")
        
        # 1. 解析聊天记录（不传递现有决策树）
        parsed_nodes = self.parse_chat_history(chat_history)
        if not parsed_nodes:
            return {"success": False, "error": "解析聊天记录失败"}
        
        # 2. 验证节点（不传递现有决策树，只验证新节点的内部结构）
        validation_result = self.validate_new_nodes_only(parsed_nodes)
        if not validation_result.get("valid", True):
            return {"success": False, "error": f"节点验证失败: {validation_result.get('errors', [])}"}
        
        # 3. 合并节点（如果有现有树）
        if existing_tree:
            merge_result = self.merge_nodes(existing_tree, parsed_nodes)
            if merge_result:
                parsed_nodes = merge_result.get("merged_tree", parsed_nodes)
        
        # 4. 检查错误
        error_result = self.check_errors(parsed_nodes)
        
        # 5. 生成确认信息
        confirmation_message = self.generate_confirmation_message({
            "new_nodes": parsed_nodes,
            "validation": validation_result,
            "errors": error_result
        })
        
        return {
            "success": True,
            "new_nodes": parsed_nodes,
            "validation": validation_result,
            "errors": error_result,
            "confirmation_message": confirmation_message,
            "timestamp": datetime.now().isoformat()
        }
    
    def validate_new_nodes_only(self, new_nodes: Dict) -> Dict:
        """只验证新节点的内部结构，不发送现有决策树"""
        print("✅ 验证新节点结构...")
        
        # 简单的结构验证，不调用AI
        errors = []
        
        if not new_nodes:
            errors.append("新节点数据为空")
            return {"valid": False, "errors": errors}
        
        nodes = new_nodes.get('nodes', {})
        if not nodes:
            errors.append("节点字典为空")
            return {"valid": False, "errors": errors}
        
        # 检查每个节点的基本结构
        for node_id, node_data in nodes.items():
            if not isinstance(node_data, dict):
                errors.append(f"节点 {node_id} 数据格式错误")
                continue
            
            # 检查节点是否有必要字段
            if 'question' in node_data:
                if not node_data['question']:
                    errors.append(f"节点 {node_id} 问题为空")
            elif 'solution' in node_data:
                if not node_data['solution']:
                    errors.append(f"节点 {node_id} 解决方案为空")
            else:
                errors.append(f"节点 {node_id} 缺少问题或解决方案")
            
            # 检查选项结构
            if 'options' in node_data:
                options = node_data['options']
                if not isinstance(options, list):
                    errors.append(f"节点 {node_id} 选项格式错误")
                else:
                    for i, option in enumerate(options):
                        if not isinstance(option, dict):
                            errors.append(f"节点 {node_id} 选项 {i} 格式错误")
                        elif 'text' not in option or 'next_node' not in option:
                            errors.append(f"节点 {node_id} 选项 {i} 缺少必要字段")
        
        if errors:
            return {"valid": False, "errors": errors}
        else:
            return {"valid": True, "message": "节点结构验证通过"}

    def convert_path_to_tree(self, path_data: Dict) -> Dict:
        """将问题定位路径转换为决策树结构"""
        print("🔄 将路径转换为决策树...")
        
        if not path_data or 'steps' not in path_data:
            return None
        
        problem = path_data.get('problem', '问题定位')
        steps = path_data.get('steps', [])
        solution = path_data.get('solution', '')
        
        # 生成节点ID
        entry_node_id = f"{problem.replace(' ', '_').lower()}_issue"
        
        # 构建决策树
        nodes = {}
        
        # 入口节点
        if steps:
            first_step = steps[0]
            nodes[entry_node_id] = {
                "question": first_step.get('question', problem),
                "options": [
                    {
                        "text": first_step.get('answer', ''),
                        "next_node": f"step_{first_step.get('step', 1)}"
                    }
                ]
            }
        
        # 中间步骤节点
        for i, step in enumerate(steps):
            step_id = f"step_{step.get('step', i+1)}"
            
            if i < len(steps) - 1:
                # 中间步骤
                next_step = steps[i + 1]
                nodes[step_id] = {
                    "question": next_step.get('question', ''),
                    "options": [
                        {
                            "text": next_step.get('answer', ''),
                            "next_node": f"step_{next_step.get('step', i+2)}"
                        }
                    ]
                }
            else:
                # 最后一步，连接到解决方案
                nodes[step_id] = {
                    "question": step.get('question', ''),
                    "options": [
                        {
                            "text": step.get('answer', ''),
                            "next_node": "solution"
                        }
                    ]
                }
        
        # 解决方案节点
        if solution:
            nodes["solution"] = {
                "solution": solution
            }
        
        return {
            "entry_node": entry_node_id,
            "nodes": nodes
        }

def main():
    """测试函数"""
    # 示例聊天记录
    sample_chat = """
    用户: 我的电脑无法连接网络了
    客服: 请问是WiFi还是有线连接？
    用户: WiFi连接
    客服: 请检查WiFi开关是否打开
    用户: 开关是打开的
    客服: 请尝试重启路由器
    用户: 重启后还是不行
    客服: 请检查网络适配器驱动是否正常
    用户: 怎么检查？
    客服: 在设备管理器中查看网络适配器是否有感叹号
    用户: 有感叹号，显示驱动有问题
    客服: 请更新或重新安装网络适配器驱动
    用户: 更新后可以连接了，谢谢
    """
    
    parser = AIChatParser()
    result = parser.process_chat_and_generate_tree(sample_chat)
    
    print("处理结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 