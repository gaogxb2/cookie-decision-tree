#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import json
import openai
import os
import requests
from datetime import datetime

class DirectAICaller:
    def __init__(self, ai_config_file: str = "config/ai_config.yaml", 
                 prompts_file: str = "config/prompts.yaml"):
        """初始化直接AI调用器"""
        self.ai_config = self._load_config(ai_config_file)
        self.prompts = self._load_config(prompts_file)
        self.client = self._init_ai_client()
    
    def _load_config(self, config_file: str) -> dict:
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[ERROR] 加载配置文件失败: {e}")
            return {}
    
    def _init_ai_client(self):
        """初始化AI客户端"""
        try:
            api_type = self.ai_config['ai']['current_api']
            api_config = self.ai_config['ai']['api'][api_type]
            
            if api_type == "custom_http":
                # 自定义HTTP请求不需要初始化客户端
                return None
            elif api_type == "dashscope":
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
            else:
                raise ValueError(f"不支持的API类型: {api_type}")
                
        except Exception as e:
            print(f"[ERROR] 初始化AI客户端失败: {e}")
            return None
    
    def _call_ai_api(self, messages: list, model: str = None) -> str:
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
            print(f"[ERROR] AI API调用失败: {e}")
            return None
    
    def _call_custom_http_api(self, messages: list) -> str:
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
            
            # 构建请求体
            body = {
                "inputs": prompt_text,
                "parameters": {
                    "detail": True,
                    "temperature": 0.1
                }
            }
            
            # 发送请求 - 使用requests.post(url, headers=headers, json=body)的方式
            response = requests.post(
                api_config['url'],
                headers=headers,
                json=body,
                timeout=30
            )
            
            if response.status_code != 200:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"[ERROR] 自定义HTTP API调用失败: {error_msg}")
                return None
            
            # 直接返回响应文本
            return response.text
            
        except Exception as e:
            print(f"[ERROR] 自定义HTTP API调用失败: {e}")
            return None
    
    def _messages_to_prompt(self, messages: list) -> str:
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
    
    def parse_chat_to_path(self, chat_history: str) -> dict:
        """直接解析聊天记录为路径"""
        print("[DEBUG] 直接解析聊天记录为路径...")
        
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
            # 解析AI响应
            path_data = self._extract_json_from_response(response)
            if not path_data:
                print("[ERROR] 无法解析AI响应")
                return None
            
            return path_data
            
        except Exception as e:
            print(f"[ERROR] 解析失败: {e}")
            return None
    
    def _extract_json_from_response(self, response: str) -> dict:
        """从AI响应中提取JSON内容"""
        try:
            # 方法1: 尝试直接解析整个响应
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        try:
            # 方法2: 查找JSON代码块
            import re
            json_block_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_block_match:
                return json.loads(json_block_match.group(1))
        except json.JSONDecodeError:
            pass
        
        try:
            # 方法3: 查找任何JSON对象
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        
        return None
    
    def convert_path_to_nodes(self, path_data: dict) -> dict:
        """将路径转换为节点结构"""
        print("🔄 将路径转换为节点结构...")
        
        if not path_data or 'steps' not in path_data:
            return None
        
        problem = path_data.get('problem', '问题定位')
        steps = path_data.get('steps', [])
        solution = path_data.get('solution', '')
        
        # 生成节点ID
        entry_node_id = f"{problem.replace(' ', '_').lower()}_issue"
        
        # 构建节点
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
    
    def merge_to_existing_tree(self, new_nodes: dict, existing_tree: dict) -> dict:
        """将新节点合并到现有决策树"""
        print("🔗 合并到现有决策树...")
        
        if not existing_tree or 'nodes' not in existing_tree:
            return new_nodes
        
        existing_nodes = existing_tree.get('nodes', {})
        new_nodes_dict = new_nodes.get('nodes', {})
        entry_node = new_nodes.get('entry_node', '')
        
        # 获取现有根节点
        existing_root = existing_tree.get('root_node', 'start')
        
        # 在现有根节点添加新路径的入口
        if existing_root in existing_nodes and entry_node in new_nodes_dict:
            entry_node_data = new_nodes_dict[entry_node]
            entry_question = entry_node_data.get('question', '新问题')
            
            new_option = {
                "text": entry_question,
                "next_node": entry_node
            }
            
            if 'options' not in existing_nodes[existing_root]:
                existing_nodes[existing_root]['options'] = []
            
            # 检查是否已存在相同选项
            existing_options = [opt['text'] for opt in existing_nodes[existing_root]['options']]
            if new_option['text'] not in existing_options:
                existing_nodes[existing_root]['options'].append(new_option)
                print(f"[OK] 已添加新选项: {new_option['text']} -> {entry_node}")
            else:
                print(f"[WARNING] 选项已存在: {new_option['text']}")
        
        # 合并所有新节点
        existing_nodes.update(new_nodes_dict)
        
        return {
            "root_node": existing_root,
            "nodes": existing_nodes
        }

def main():
    """测试直接AI调用"""
    print(" 测试直接AI调用...")
    
    # 测试聊天记录
    chat_history = """
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
    
    # 创建直接AI调用器
    caller = DirectAICaller()
    
    # 1. 直接解析聊天记录为路径
    print("\n 步骤1: 解析聊天记录为路径")
    path_data = caller.parse_chat_to_path(chat_history)
    
    if path_data:
        print("[OK] 路径解析成功:")
        print(json.dumps(path_data, ensure_ascii=False, indent=2))
        
        # 2. 转换为节点结构
        print("\n 步骤2: 转换为节点结构")
        nodes = caller.convert_path_to_nodes(path_data)
        
        if nodes:
            print("[OK] 节点转换成功:")
            print(json.dumps(nodes, ensure_ascii=False, indent=2))
            
            # 3. 合并到现有决策树
            print("\n 步骤3: 合并到现有决策树")
            
            # 加载现有决策树
            try:
                with open('config/decision_tree.yaml', 'r', encoding='utf-8') as f:
                    tree_data = yaml.safe_load(f)
                    existing_tree = tree_data.get('decision_tree', {})
                
                merged_tree = caller.merge_to_existing_tree(nodes, existing_tree)
                
                print("[OK] 合并成功:")
                print(f"  新节点数量: {len(nodes['nodes'])}")
                print(f"  总节点数量: {len(merged_tree['nodes'])}")
                
                # 保存合并后的决策树
                with open('config/decision_tree.yaml', 'w', encoding='utf-8') as f:
                    yaml.dump({'decision_tree': merged_tree}, f, default_flow_style=False, allow_unicode=True, indent=2)
                
                print("[SAVE] 已保存到 config/decision_tree.yaml")
                
            except Exception as e:
                print(f"[ERROR] 合并失败: {e}")
        else:
            print("[ERROR] 节点转换失败")
    else:
        print("[ERROR] 路径解析失败")

if __name__ == "__main__":
    main() 