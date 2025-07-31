import yaml
from typing import Dict, List, Optional, Any, TypedDict
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import json

class DecisionOption(BaseModel):
    text: str
    next_node: str

class DecisionNode(BaseModel):
    question: str
    options: List[DecisionOption]

class SolutionNode(BaseModel):
    solution: str

class DecisionTreeConfig(BaseModel):
    root_node: str
    nodes: Dict[str, Any]

class DecisionTreeEngine:
    def __init__(self, config_file: str = "config/decision_tree.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
        self.graph = self._build_graph()
    
    def _load_config(self) -> DecisionTreeConfig:
        """加载决策树配置文件"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return DecisionTreeConfig(**data['decision_tree'])
    
    def _build_graph(self) -> StateGraph:
        """构建决策图"""
        workflow = StateGraph(StateType)
        
        # 添加决策节点
        for node_id, node_data in self.config.nodes.items():
            if 'solution' in node_data:
                # 这是终端节点，提供解决方案
                workflow.add_node(node_id, self._create_solution_node(node_data['solution']))
                workflow.add_edge(node_id, END)
            else:
                # 这是决策节点，询问用户
                workflow.add_node(node_id, self._create_decision_node(node_id, node_data))
        
        # 设置根节点
        workflow.set_entry_point(self.config.root_node)
        
        return workflow.compile()
    
    def _create_decision_node(self, node_id: str, node_data: Dict) -> callable:
        """创建决策节点"""
        def decision_node(state: Dict) -> Dict:
            question = node_data['question']
            options = node_data['options']
            
            # 构建选项文本
            options_text = "\n".join([f"{i+1}. {opt['text']}" for i, opt in enumerate(options)])
            
            # 生成AI消息
            ai_message = f"问题：{question}\n\n请选择以下选项之一：\n{options_text}\n\n请输入选项编号（1-{len(options)}）："
            
            return {
                **state,
                "current_node": node_id,
                "question": question,
                "options": options,
                "messages": state.get("messages", []) + [AIMessage(content=ai_message)]
            }
        
        return decision_node
    
    def _create_solution_node(self, solution: str) -> callable:
        """创建解决方案节点"""
        def solution_node(state: Dict) -> Dict:
            ai_message = f"根据您的描述，建议的解决方案是：\n\n{solution}\n\n问题定位完成！"
            
            return {
                **state,
                "solution": solution,
                "messages": state.get("messages", []) + [AIMessage(content=ai_message)]
            }
        
        return solution_node
    
    def process_user_response(self, user_input: str, state: Optional[Dict] = None) -> Dict:
        """处理用户响应"""
        if state is None:
            state = {"messages": []}
        
        # 添加用户消息
        state["messages"] = state.get("messages", []) + [HumanMessage(content=user_input)]
        
        # 获取当前节点
        current_node = state.get("current_node", self.config.root_node)
        
        # 处理用户选择
        try:
            choice_index = int(user_input.strip()) - 1
            if current_node in self.config.nodes:
                node_data = self.config.nodes[current_node]
                if 'options' in node_data and 0 <= choice_index < len(node_data['options']):
                    selected_option = node_data['options'][choice_index]
                    next_node = selected_option['next_node']
                    
                    # 更新状态
                    state["current_node"] = next_node
                    state["selected_option"] = selected_option['text']
                    
                    # 检查下一节点是否为解决方案节点
                    if next_node in self.config.nodes:
                        next_node_data = self.config.nodes[next_node]
                        if 'solution' in next_node_data:
                            # 直接返回解决方案
                            return {
                                **state,
                                "solution": next_node_data['solution'],
                                "messages": state.get("messages", []) + [AIMessage(content=f"根据您的描述，建议的解决方案是：\n\n{next_node_data['solution']}\n\n问题定位完成！")]
                            }
                        else:
                            # 继续决策流程
                            return self._create_decision_node(next_node, next_node_data)(state)
                    else:
                        return {
                            **state,
                            "error": "引用的节点不存在。"
                        }
                else:
                    return {
                        **state,
                        "error": "无效的选项，请重新选择。"
                    }
            else:
                return {
                    **state,
                    "error": "当前节点不存在。"
                }
        except ValueError:
            return {
                **state,
                "error": "请输入有效的数字选项。"
            }
    
    def get_current_question(self, state: Dict) -> Optional[str]:
        """获取当前问题"""
        current_node = state.get("current_node", self.config.root_node)
        if current_node in self.config.nodes:
            node_data = self.config.nodes[current_node]
            if 'question' in node_data:
                return node_data['question']
        return None
    
    def reload_config(self):
        """重新加载配置文件"""
        self.config = self._load_config()
        self.graph = self._build_graph()

class StateType:
    """状态类型定义"""
    pass 