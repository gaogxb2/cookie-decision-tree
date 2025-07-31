// 简化测试用例
const TestCases = {
  // 测试删除解决方案节点
  testDeleteSolution() {
    console.log('=== 测试删除解决方案节点 ===');
    const data = {
      root_node: 'start',
      nodes: {
        'start': {
          question: '问题类型？',
          options: [
            { text: '硬件', next_node: 'hardware' },
            { text: '软件', next_node: 'software' }
          ]
        },
        'hardware': {
          question: '硬件问题？',
          options: [
            { text: '显示器', next_node: 'display' }
          ]
        },
        'software': {
          solution: '软件问题解决方案'
        },
        'display': {
          solution: '显示器问题解决方案'
        }
      }
    };
    
    // 删除 display 节点
    delete data.nodes['display'];
    
    // 更新引用
    Object.keys(data.nodes).forEach(id => {
      const node = data.nodes[id];
      if (node.options) {
        node.options = node.options.filter(option => 
          option.next_node !== 'display'
        );
      }
    });
    
    console.log('删除后:', data);
    return data;
  },

  // 测试删除决策节点
  testDeleteDecision() {
    console.log('=== 测试删除决策节点 ===');
    const data = {
      root_node: 'start',
      nodes: {
        'start': {
          question: '问题类型？',
          options: [
            { text: '硬件', next_node: 'hardware' },
            { text: '软件', next_node: 'software' }
          ]
        },
        'hardware': {
          question: '硬件问题？',
          options: [
            { text: '显示器', next_node: 'display' }
          ]
        },
        'software': {
          solution: '软件问题解决方案'
        },
        'display': {
          solution: '显示器问题解决方案'
        }
      }
    };
    
    // 删除 hardware 节点
    delete data.nodes['hardware'];
    
    // 更新引用
    Object.keys(data.nodes).forEach(id => {
      const node = data.nodes[id];
      if (node.options) {
        node.options = node.options.filter(option => 
          option.next_node !== 'hardware'
        );
      }
    });
    
    console.log('删除后:', data);
    return data;
  },

  // 测试添加节点
  testAddNode() {
    console.log('=== 测试添加节点 ===');
    const data = {
      root_node: 'start',
      nodes: {
        'start': {
          question: '问题类型？',
          options: [
            { text: '硬件', next_node: 'hardware' }
          ]
        },
        'hardware': {
          solution: '硬件问题解决方案'
        }
      }
    };
    
    // 添加新节点
    data.nodes['new_solution'] = {
      solution: '新的解决方案'
    };
    
    // 添加选项
    data.nodes['start'].options.push({
      text: '新问题',
      next_node: 'new_solution'
    });
    
    console.log('添加后:', data);
    return data;
  }
};

window.TestCases = TestCases;
console.log('测试用例已加载，使用 TestCases.testDeleteSolution() 等命令测试'); 