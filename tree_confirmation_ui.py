#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import json
from typing import Dict, List, Optional, Set
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser

class TreeConfirmationUI:
    def __init__(self, config_file: str = "config/ai_config.yaml"):
        """初始化确认界面"""
        self.config = self._load_config(config_file)
        self.ui_config = self.config['ui']
        self.original_tree = None
        self.new_nodes = None
        self.modified_tree = None
        self.visualization_file = None
        
    def _load_config(self, config_file: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[ERROR] 加载配置文件失败: {e}")
            sys.exit(1)
    
    def show_confirmation_dialog(self, original_tree: Dict, new_nodes: Dict, 
                                confirmation_message: str = None) -> Dict:
        """显示确认对话框"""
        self.original_tree = original_tree
        self.new_nodes = new_nodes
        
        # 创建主窗口
        root = tk.Tk()
        root.title("决策树变更确认")
        root.geometry("1000x700")
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="决策树变更确认", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # 确认信息
        if confirmation_message:
            info_label = ttk.Label(main_frame, text=confirmation_message, 
                                  wraplength=800, justify="left")
            info_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # 创建选项卡
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 变更摘要选项卡
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="变更摘要")
        self._create_summary_tab(summary_frame)
        
        # 节点编辑选项卡
        edit_frame = ttk.Frame(notebook)
        notebook.add(edit_frame, text="节点编辑")
        self._create_edit_tab(edit_frame)
        
        # 可视化预览选项卡
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="可视化预览")
        self._create_preview_tab(preview_frame)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # 按钮
        ttk.Button(button_frame, text="预览可视化", 
                  command=self._preview_visualization).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="保存备份", 
                  command=self._save_backup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="确认合并", 
                  command=lambda: self._confirm_merge(root)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", 
                  command=root.destroy).pack(side=tk.LEFT, padx=5)
        
        # 启动界面
        root.mainloop()
        
        return self.modified_tree if self.modified_tree else None
    
    def _create_summary_tab(self, parent):
        """创建变更摘要选项卡"""
        # 创建树形视图
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建树形控件
        self.summary_tree = ttk.Treeview(tree_frame, columns=("type", "status", "description"), 
                                        show="tree headings")
        self.summary_tree.heading("#0", text="节点ID")
        self.summary_tree.heading("type", text="类型")
        self.summary_tree.heading("status", text="状态")
        self.summary_tree.heading("description", text="描述")
        
        # 设置列宽
        self.summary_tree.column("#0", width=150)
        self.summary_tree.column("type", width=100)
        self.summary_tree.column("status", width=100)
        self.summary_tree.column("description", width=300)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=scrollbar.set)
        
        self.summary_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 填充数据
        self._populate_summary_tree()
    
    def _populate_summary_tree(self):
        """填充摘要树形视图"""
        # 清空现有数据
        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)
        
        # 添加原始节点
        original_nodes = set(self.original_tree.get('nodes', {}).keys())
        new_node_ids = set(self.new_nodes.get('nodes', {}).keys())
        
        # 新增节点
        for node_id in new_node_ids - original_nodes:
            node_data = self.new_nodes['nodes'][node_id]
            node_type = "决策节点" if 'question' in node_data else "解决方案节点"
            description = node_data.get('question', node_data.get('solution', ''))[:50]
            
            self.summary_tree.insert("", "end", text=node_id, 
                                   values=(node_type, "新增", description),
                                   tags=("new",))
        
        # 修改的节点
        for node_id in new_node_ids & original_nodes:
            node_data = self.new_nodes['nodes'][node_id]
            node_type = "决策节点" if 'question' in node_data else "解决方案节点"
            description = node_data.get('question', node_data.get('solution', ''))[:50]
            
            self.summary_tree.insert("", "end", text=node_id, 
                                   values=(node_type, "修改", description),
                                   tags=("modified",))
        
        # 设置标签颜色
        self.summary_tree.tag_configure("new", background="#e3f2fd")
        self.summary_tree.tag_configure("modified", background="#fff3e0")
    
    def _create_edit_tab(self, parent):
        """创建节点编辑选项卡"""
        # 创建编辑框架
        edit_frame = ttk.Frame(parent)
        edit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 节点选择
        select_frame = ttk.LabelFrame(edit_frame, text="选择节点", padding="5")
        select_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.node_var = tk.StringVar()
        node_combo = ttk.Combobox(select_frame, textvariable=self.node_var, 
                                  state="readonly", width=30)
        node_combo.pack(side=tk.LEFT, padx=(0, 10))
        node_combo.bind("<<ComboboxSelected>>", self._on_node_selected)
        
        # 填充节点列表
        new_node_ids = list(self.new_nodes.get('nodes', {}).keys())
        node_combo['values'] = new_node_ids
        if new_node_ids:
            node_combo.set(new_node_ids[0])
        
        # 编辑框架
        self.edit_frame = ttk.LabelFrame(edit_frame, text="编辑节点", padding="5")
        self.edit_frame.pack(fill=tk.BOTH, expand=True)
        
        # 节点ID
        ttk.Label(self.edit_frame, text="节点ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.node_id_var = tk.StringVar()
        self.node_id_entry = ttk.Entry(self.edit_frame, textvariable=self.node_id_var, width=30)
        self.node_id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # 节点类型
        ttk.Label(self.edit_frame, text="节点类型:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.node_type_var = tk.StringVar()
        self.node_type_combo = ttk.Combobox(self.edit_frame, textvariable=self.node_type_var, 
                                           values=["决策节点", "解决方案节点"], state="readonly", width=30)
        self.node_type_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        self.node_type_combo.bind("<<ComboboxSelected>>", self._on_type_changed)
        
        # 问题/解决方案
        ttk.Label(self.edit_frame, text="内容:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.content_text = tk.Text(self.edit_frame, height=4, width=50)
        self.content_text.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # 选项框架
        self.options_frame = ttk.LabelFrame(self.edit_frame, text="选项", padding="5")
        self.options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 选项列表
        self.options_listbox = tk.Listbox(self.options_frame, height=4)
        self.options_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 选项按钮
        options_button_frame = ttk.Frame(self.options_frame)
        options_button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        ttk.Button(options_button_frame, text="添加", command=self._add_option).pack(pady=2)
        ttk.Button(options_button_frame, text="编辑", command=self._edit_option).pack(pady=2)
        ttk.Button(options_button_frame, text="删除", command=self._delete_option).pack(pady=2)
        
        # 保存按钮
        ttk.Button(self.edit_frame, text="保存修改", 
                  command=self._save_node_changes).grid(row=4, column=0, columnspan=2, pady=10)
        
        # 配置网格权重
        self.edit_frame.columnconfigure(1, weight=1)
    
    def _create_preview_tab(self, parent):
        """创建可视化预览选项卡"""
        preview_frame = ttk.Frame(parent)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 预览按钮
        ttk.Button(preview_frame, text="生成可视化预览", 
                  command=self._generate_preview).pack(pady=10)
        
        # 预览信息
        self.preview_info = tk.Text(preview_frame, height=10, width=80)
        self.preview_info.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def _on_node_selected(self, event):
        """节点选择事件"""
        selected_node = self.node_var.get()
        if selected_node and selected_node in self.new_nodes.get('nodes', {}):
            self._load_node_data(selected_node)
    
    def _load_node_data(self, node_id):
        """加载节点数据"""
        node_data = self.new_nodes['nodes'][node_id]
        
        self.node_id_var.set(node_id)
        
        if 'question' in node_data:
            self.node_type_var.set("决策节点")
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, node_data['question'])
        else:
            self.node_type_var.set("解决方案节点")
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, node_data.get('solution', ''))
        
        # 加载选项
        self._load_options(node_data.get('options', []))
    
    def _load_options(self, options):
        """加载选项"""
        self.options_listbox.delete(0, tk.END)
        for option in options:
            self.options_listbox.insert(tk.END, f"{option['text']} -> {option.get('next_node', '')}")
    
    def _on_type_changed(self, event):
        """节点类型改变事件"""
        node_type = self.node_type_var.get()
        if node_type == "决策节点":
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, "请输入问题...")
        else:
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, "请输入解决方案...")
    
    def _add_option(self):
        """添加选项"""
        # 这里可以创建一个对话框来添加选项
        messagebox.showinfo("添加选项", "添加选项功能待实现")
    
    def _edit_option(self):
        """编辑选项"""
        selection = self.options_listbox.curselection()
        if selection:
            messagebox.showinfo("编辑选项", "编辑选项功能待实现")
    
    def _delete_option(self):
        """删除选项"""
        selection = self.options_listbox.curselection()
        if selection:
            self.options_listbox.delete(selection)
    
    def _save_node_changes(self):
        """保存节点修改"""
        node_id = self.node_id_var.get()
        node_type = self.node_type_var.get()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not node_id or not content:
            messagebox.showerror("错误", "请填写完整的节点信息")
            return
        
        # 更新节点数据
        if node_id in self.new_nodes.get('nodes', {}):
            if node_type == "决策节点":
                self.new_nodes['nodes'][node_id] = {
                    'question': content,
                    'options': self.new_nodes['nodes'][node_id].get('options', [])
                }
            else:
                self.new_nodes['nodes'][node_id] = {
                    'solution': content
                }
            
            messagebox.showinfo("成功", "节点修改已保存")
            self._populate_summary_tree()
    
    def _preview_visualization(self):
        """预览可视化"""
        try:
            from tree_visualizer import TreeVisualizer
            
            visualizer = TreeVisualizer()
            viz_data = visualizer.generate_visualization_data(self.original_tree, self.new_nodes)
            self.visualization_file = visualizer.save_visualization(viz_data)
            
            # 在浏览器中打开
            webbrowser.open(f"file://{os.path.abspath(self.visualization_file)}")
            
            messagebox.showinfo("成功", f"可视化文件已生成: {self.visualization_file}")
        except Exception as e:
            messagebox.showerror("错误", f"生成可视化失败: {e}")
    
    def _generate_preview(self):
        """生成预览信息"""
        try:
            from tree_visualizer import TreeVisualizer
            
            visualizer = TreeVisualizer()
            viz_data = visualizer.generate_visualization_data(self.original_tree, self.new_nodes)
            diff_report = visualizer.generate_diff_report(self.original_tree, self.new_nodes)
            
            preview_text = f"""
可视化预览信息:

节点统计:
- 原始节点: {diff_report['summary']['added'] + diff_report['summary']['modified']}
- 新增节点: {diff_report['summary']['added']}
- 修改节点: {diff_report['summary']['modified']}
- 删除节点: {diff_report['summary']['deleted']}

新增节点:
{chr(10).join(f"- {node_id}" for node_id in diff_report['details']['added_nodes'])}

修改节点:
{chr(10).join(f"- {node_id}" for node_id in diff_report['details']['modified_nodes'])}

生成时间: {viz_data['metadata']['generated_at']}
            """
            
            self.preview_info.delete(1.0, tk.END)
            self.preview_info.insert(1.0, preview_text)
            
        except Exception as e:
            self.preview_info.delete(1.0, tk.END)
            self.preview_info.insert(1.0, f"生成预览失败: {e}")
    
    def _save_backup(self):
        """保存备份"""
        try:
            backup_data = {
                "original_tree": self.original_tree,
                "new_nodes": self.new_nodes,
                "timestamp": datetime.now().isoformat()
            }
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("成功", f"备份已保存: {filename}")
        except Exception as e:
            messagebox.showerror("错误", f"保存备份失败: {e}")
    
    def _confirm_merge(self, root):
        """确认合并"""
        if messagebox.askyesno("确认", "确定要合并这些变更到决策树吗？"):
            # 合并决策树
            self.modified_tree = self._merge_trees()
            root.destroy()
    
    def _merge_trees(self) -> Dict:
        """合并决策树"""
        merged = self.original_tree.copy()
        
        # 合并节点
        if 'nodes' in self.new_nodes:
            merged['nodes'] = merged.get('nodes', {}).copy()
            merged['nodes'].update(self.new_nodes['nodes'])
        
        # 合并根节点（如果新树有根节点）
        if 'root_node' in self.new_nodes:
            merged['root_node'] = self.new_nodes['root_node']
        
        return merged

def main():
    """测试函数"""
    # 示例数据
    original_tree = {
        "root_node": "start",
        "nodes": {
            "start": {
                "question": "您遇到了什么类型的问题？",
                "options": [
                    {"text": "网络问题", "next_node": "network_issue"},
                    {"text": "硬件问题", "next_node": "hardware_issue"}
                ]
            }
        }
    }
    
    new_nodes = {
        "nodes": {
            "network_issue": {
                "question": "网络问题具体是什么？",
                "options": [
                    {"text": "无法连接", "next_node": "network_no_connection"},
                    {"text": "速度很慢", "next_node": "network_slow"}
                ]
            },
            "network_no_connection": {
                "solution": "请检查网络设置，重启路由器"
            }
        }
    }
    
    ui = TreeConfirmationUI()
    result = ui.show_confirmation_dialog(original_tree, new_nodes, "发现新的网络问题处理流程")
    
    if result:
        print("合并结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 