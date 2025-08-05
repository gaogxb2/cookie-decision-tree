import os
import yaml
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from decision_tree_engine import DecisionTreeEngine
import platform

app = Flask(__name__)
CORS(app)

# 检测操作系统，在 Windows 下使用安全的字符
def get_safe_chars():
    """根据操作系统返回安全的字符"""
    # 为了兼容性，在所有系统下都使用安全字符
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

# 获取安全字符
safe_chars = get_safe_chars()

class DecisionTreeAPI:
    def __init__(self, config_file: str = None):
        if config_file is None:
            # 使用绝对路径
            config_file = os.path.join(os.path.dirname(__file__), 'config', 'decision_tree.yaml')
        self.config_file = config_file
        self.engine = DecisionTreeEngine(config_file)
    
    def load_tree(self):
        """加载决策树数据"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return data['decision_tree']
        except Exception as e:
            return {"error": str(e)}
    
    def save_tree(self, tree_data):
        """保存决策树数据"""
        try:
            data = {"decision_tree": tree_data}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            # 重新加载引擎
            self.engine.reload_config()
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}
    
    def validate_tree(self, tree_data):
        """验证决策树结构"""
        errors = []
        
        # 检查根节点
        if 'root_node' not in tree_data:
            errors.append("缺少根节点定义")
            return errors
        
        root_node = tree_data['root_node']
        nodes = tree_data.get('nodes', {})
        
        # 检查根节点是否存在
        if root_node not in nodes:
            errors.append(f"根节点 '{root_node}' 不存在")
        
        # 检查所有节点引用
        for node_id, node_data in nodes.items():
            if 'options' in node_data:
                for i, option in enumerate(node_data['options']):
                    if 'next_node' not in option:
                        errors.append(f"节点 '{node_id}' 的选项 {i+1} 缺少 next_node")
                    elif option['next_node'] not in nodes:
                        errors.append(f"节点 '{node_id}' 引用了不存在的节点 '{option['next_node']}'")
        
        return errors

api = DecisionTreeAPI()

@app.route('/api/tree', methods=['GET'])
def get_tree():
    """获取决策树数据"""
    tree_data = api.load_tree()
    return jsonify(tree_data)

@app.route('/api/tree', methods=['POST'])
def save_tree():
    """保存决策树数据"""
    tree_data = request.json
    
    # 验证数据
    errors = api.validate_tree(tree_data)
    if errors:
        return jsonify({"error": "验证失败", "details": errors}), 400
    
    # 保存数据
    result = api.save_tree(tree_data)
    if "error" in result:
        return jsonify(result), 500
    
    return jsonify(result)

@app.route('/api/validate', methods=['POST'])
def validate_tree():
    """验证决策树结构"""
    tree_data = request.json
    errors = api.validate_tree(tree_data)
    return jsonify({"errors": errors, "valid": len(errors) == 0})

@app.route('/api/test', methods=['POST'])
def test_tree():
    """测试决策树流程"""
    try:
        tree_data = request.json
        test_path = request.json.get('test_path', [])
        
        # 创建临时引擎进行测试
        temp_engine = DecisionTreeEngine()
        temp_engine.config = type('Config', (), {
            'decision_tree': tree_data
        })()
        
        # 执行测试路径
        result = temp_engine.process_path(test_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# AI增强相关接口
@app.route('/api/ai/direct-process', methods=['POST'])
def direct_process_chat():
    """直接调用AI API处理聊天记录"""
    try:
        data = request.get_json()
        chat_history = data.get('chat_history', '')
        auto_merge = data.get('auto_merge', False)
        
        if not chat_history:
            return jsonify({'success': False, 'error': '聊天记录不能为空'})
        
        # 导入直接AI调用器
        from direct_ai_call import DirectAICaller
        
        # 创建AI调用器
        caller = DirectAICaller()
        
        # 记录AI对话
        log_ai_conversation(caller, chat_history)
        
        # 1. 直接解析聊天记录为路径（不传递决策树）
        path_data = caller.parse_chat_to_path(chat_history)
        if not path_data:
            return jsonify({'success': False, 'error': 'AI解析失败'})
        
        # 2. 转换为节点结构
        nodes = caller.convert_path_to_nodes(path_data)
        if not nodes:
            return jsonify({'success': False, 'error': '节点转换失败'})
        
        # 3. 合并到现有决策树
        try:
            with open('config/decision_tree.yaml', 'r', encoding='utf-8') as f:
                tree_data = yaml.safe_load(f)
                existing_tree = tree_data.get('decision_tree', {})
            
            merged_tree = caller.merge_to_existing_tree(nodes, existing_tree)
            
            if auto_merge:
                # 自动保存
                with open('config/decision_tree.yaml', 'w', encoding='utf-8') as f:
                    yaml.dump({'decision_tree': merged_tree}, f, default_flow_style=False, allow_unicode=True, indent=2)
                
                return jsonify({
                    'success': True,
                    'data': merged_tree,
                    'message': 'AI增强已自动合并',
                    'path_data': path_data,
                    'new_nodes': nodes
                })
            else:
                # 返回预览
                changes = []
                original_node_ids = set(existing_tree.get('nodes', {}).keys())
                new_node_ids = set(nodes.get('nodes', {}).keys())
                
                for node_id in new_node_ids:
                    if node_id not in original_node_ids:
                        changes.append({
                            'id': node_id,
                            'type': 'new',
                            'text': f'新增节点: {node_id}'
                        })
                    else:
                        changes.append({
                            'id': node_id,
                            'type': 'modified',
                            'text': f'修改节点: {node_id}'
                        })
                
                return jsonify({
                    'success': True,
                    'changes': changes,
                    'new_nodes': nodes,
                    'path_data': path_data,
                    'message': 'AI解析完成，请确认变更'
                })
                
        except Exception as e:
            return jsonify({'success': False, 'error': f'合并失败: {str(e)}'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def log_ai_conversation(caller, chat_history):
    """记录AI对话"""
    try:
        from datetime import datetime
        import json
        
        # 获取当前时间戳
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 构建发送给AI的消息
        system_prompt = caller.prompts['chat_analysis']['system']
        user_prompt = caller.prompts['chat_analysis']['user'].format(chat_history=chat_history)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # 记录开始时间
        start_time = datetime.now()
        
        # 调用AI API
        ai_response = caller._call_ai_api(messages)
        
        # 记录结束时间
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # 构建日志内容
        log_content = []
        log_content.append(safe_chars['separator'])
        log_content.append(f"{safe_chars['ai']} AI对话记录 (前端调用)")
        log_content.append(safe_chars['separator'])
        log_content.append(f"{safe_chars['time']} 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_content.append(f"{safe_chars['time']} 处理时间: {processing_time:.2f}秒")
        log_content.append("")
        
        log_content.append(f"{safe_chars['info']} 发送给AI的消息:")
        log_content.append(safe_chars['sub_separator'])
        log_content.append(f"{safe_chars['system']} System Prompt:")
        log_content.append(system_prompt)
        log_content.append("")
        log_content.append(f"{safe_chars['user']} User Prompt:")
        log_content.append(user_prompt)
        log_content.append("")
        
        log_content.append(f"{safe_chars['info']} AI回复内容:")
        log_content.append(safe_chars['sub_separator'])
        log_content.append(ai_response)
        log_content.append("")
        
        # 解析AI响应
        if ai_response:
            try:
                parsed_data = caller._extract_json_from_response(ai_response)
                if parsed_data:
                    log_content.append(f"{safe_chars['parse']} 解析后的JSON数据:")
                    log_content.append(safe_chars['sub_separator'])
                    log_content.append(json.dumps(parsed_data, ensure_ascii=False, indent=2))
                    log_content.append("")
            except Exception as e:
                log_content.append(f"{safe_chars['error']} JSON解析失败: {e}")
                log_content.append("")
        
        log_content.append(safe_chars['separator'])
        log_content.append(f"{safe_chars['success']} 对话记录完成")
        log_content.append(safe_chars['separator'])
        
        # 保存到文件
        filename = f"ai_conversation_frontend_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(log_content))
        
        print(f"{safe_chars['save']} AI对话记录已保存到: {filename}")
        
    except Exception as e:
        print(f"{safe_chars['error']} 记录AI对话失败: {e}")

@app.route('/api/ai/confirm-changes', methods=['POST'])
def confirm_changes():
    """确认AI增强变更"""
    try:
        # 从请求中获取要合并的节点数据
        data = request.get_json()
        new_nodes = data.get('new_nodes', {})
        
        if not new_nodes:
            return jsonify({'success': False, 'error': '没有要合并的节点数据'})
        
        # 加载现有决策树
        with open('config/decision_tree.yaml', 'r', encoding='utf-8') as f:
            tree_data = yaml.safe_load(f)
            existing_tree = tree_data.get('decision_tree', {})
        
        # 合并决策树
        merged_tree = existing_tree.copy()
        if 'nodes' in new_nodes:
            merged_tree['nodes'] = merged_tree.get('nodes', {}).copy()
            merged_tree['nodes'].update(new_nodes['nodes'])
        
        # 合并根节点（如果新树有根节点）
        if 'root_node' in new_nodes:
            merged_tree['root_node'] = new_nodes['root_node']
        
        # 保存合并后的决策树
        with open('config/decision_tree.yaml', 'w', encoding='utf-8') as f:
            yaml.dump({'decision_tree': merged_tree}, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        return jsonify({
            'success': True,
            'data': merged_tree,
            'message': '变更已确认并合并'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("启动决策树API服务器...")
    print("API服务器将在 http://localhost:5000 启动")
    app.run(host='0.0.0.0', port=5000, debug=True) 