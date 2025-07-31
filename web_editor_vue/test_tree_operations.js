// 测试决策树编辑器的各种操作
// 在浏览器控制台中运行这些测试

// 测试数据
const testTreeData = {
  root_node: 'start',
  nodes: {
    'start': {
      question: '您遇到了什么类型的问题？',
      options: [
        { text: '硬件问题', next_node: 'hardware_issue' },
        { text: '软件问题', next_node: 'software_issue' },
        { text: '网络问题', next_node: 'network_issue' },
        { text: '性能问题', next_node: 'performance_issue' }
      ]
    },
    'hardware_issue': {
      question: '硬件问题具体是什么？',
      options: [
        { text: '显示器问题', next_node: 'display_issue' },
        { text: '输入设备问题', next_node: 'input_device_issue' },
        { text: '音频问题', next_node: 'audio_issue' }
      ]
    },
    'software_issue': {
      question: '软件问题具体是什么？',
      options: [
        { text: '程序崩溃', next_node: 'software_crash' },
        { text: '程序无法启动', next_node: 'software_wont_start' },
        { text: '程序无响应', next_node: 'software_no_response' }
      ]
    },
    'network_issue': {
      question: '网络问题具体是什么？',
      options: [
        { text: '无法连接网络', next_node: 'no_connection' },
        { text: '网络速度慢', next_node: 'slow_network' },
        { text: '网络不稳定', next_node: 'unstable_network' }
      ]
    },
    'performance_issue': {
      question: '性能问题具体是什么？',
      options: [
        { text: '系统运行慢', next_node: 'system_slow' },
        { text: '程序运行慢', next_node: 'app_slow' },
        { text: '启动慢', next_node: 'slow_boot' }
      ]
    },
    'display_issue': {
      solution: '检查显示器连接线，尝试重新插拔。如果问题持续，可能需要更换显示器。'
    },
    'input_device_issue': {
      solution: '检查键盘鼠标连接，尝试重新插拔USB接口。如果是无线设备，检查电池电量。'
    },
    'audio_issue': {
      solution: '检查音频设备连接，确认音量设置。尝试更新音频驱动程序。'
    },
    'software_crash': {
      solution: '尝试重新启动程序。如果问题持续，检查是否有更新版本，或重新安装程序。'
    },
    'software_wont_start': {
      solution: '检查程序文件是否完整，尝试以管理员身份运行。可能需要重新安装程序。'
    },
    'software_no_response': {
      solution: '强制关闭程序，检查任务管理器中的进程。重启计算机后再试。'
    },
    'no_connection': {
      solution: '检查网络线缆连接，重启路由器。确认网络设置是否正确。'
    },
    'slow_network': {
      solution: '检查网络使用情况，关闭不必要的网络应用。联系网络服务提供商。'
    },
    'unstable_network': {
      solution: '检查网络设备，尝试更换网络线缆。重启网络设备。'
    },
    'system_slow': {
      solution: '检查系统资源使用情况，关闭不必要的程序。考虑增加内存或清理磁盘。'
    },
    'app_slow': {
      solution: '检查程序设置，关闭不必要的功能。更新到最新版本。'
    },
    'slow_boot': {
      solution: '检查启动项，禁用不必要的自启动程序。考虑升级硬盘到SSD。'
    }
  }
};

// 测试函数
const TreeOperationsTest = {
  // 初始化测试
  init() {
    console.log('=== 决策树编辑器测试开始 ===');
    console.log('测试数据:', testTreeData);
    return testTreeData;
  },

  // 测试1: 删除解决方案节点
  testDeleteSolutionNode() {
    console.log('\n=== 测试1: 删除解决方案节点 ===');
    
    // 模拟删除 display_issue 节点
    const testData = JSON.parse(JSON.stringify(testTreeData));
    delete testData.nodes['display_issue'];
    
    // 更新引用该节点的选项
    Object.keys(testData.nodes).forEach(id => {
      const node = testData.nodes[id];
      if (node.options) {
        node.options = node.options.filter(option => 
          option.next_node !== 'display_issue'
        );
      }
    });
    
    console.log('删除 display_issue 节点后的数据:', testData);
    console.log('hardware_issue 节点的选项:', testData.nodes['hardware_issue'].options);
    
    return testData;
  },

  // 测试2: 删除决策节点
  testDeleteDecisionNode() {
    console.log('\n=== 测试2: 删除决策节点 ===');
    
    // 模拟删除 hardware_issue 节点
    const testData = JSON.parse(JSON.stringify(testTreeData));
    delete testData.nodes['hardware_issue'];
    
    // 更新引用该节点的选项
    Object.keys(testData.nodes).forEach(id => {
      const node = testData.nodes[id];
      if (node.options) {
        node.options = node.options.filter(option => 
          option.next_node !== 'hardware_issue'
        );
      }
    });
    
    console.log('删除 hardware_issue 节点后的数据:', testData);
    console.log('start 节点的选项:', testData.nodes['start'].options);
    
    return testData;
  },

  // 测试3: 添加新的解决方案节点
  testAddSolutionNode() {
    console.log('\n=== 测试3: 添加新的解决方案节点 ===');
    
    const testData = JSON.parse(JSON.stringify(testTreeData));
    
    // 添加新的解决方案节点
    testData.nodes['new_solution'] = {
      solution: '这是一个新的解决方案节点，用于测试节点添加功能。'
    };
    
    // 为某个决策节点添加指向新解决方案节点的选项
    testData.nodes['software_issue'].options.push({
      text: '新问题类型',
      next_node: 'new_solution'
    });
    
    console.log('添加 new_solution 节点后的数据:', testData);
    console.log('software_issue 节点的选项:', testData.nodes['software_issue'].options);
    
    return testData;
  },

  // 测试4: 添加新的决策节点
  testAddDecisionNode() {
    console.log('\n=== 测试4: 添加新的决策节点 ===');
    
    const testData = JSON.parse(JSON.stringify(testTreeData));
    
    // 添加新的决策节点
    testData.nodes['new_decision'] = {
      question: '这是一个新的决策节点，用于测试节点添加功能。',
      options: [
        { text: '选项1', next_node: 'display_issue' },
        { text: '选项2', next_node: 'input_device_issue' }
      ]
    };
    
    // 为某个决策节点添加指向新决策节点的选项
    testData.nodes['start'].options.push({
      text: '新问题类型',
      next_node: 'new_decision'
    });
    
    console.log('添加 new_decision 节点后的数据:', testData);
    console.log('start 节点的选项:', testData.nodes['start'].options);
    
    return testData;
  },

  // 测试5: 修改节点类型（决策节点改为解决方案节点）
  testChangeNodeType() {
    console.log('\n=== 测试5: 修改节点类型 ===');
    
    const testData = JSON.parse(JSON.stringify(testTreeData));
    
    // 将 performance_issue 从决策节点改为解决方案节点
    testData.nodes['performance_issue'] = {
      solution: '性能问题通常可以通过优化系统设置和清理垃圾文件来解决。'
    };
    
    console.log('修改 performance_issue 节点类型后的数据:', testData);
    
    return testData;
  },

  // 测试6: 孤立节点测试
  testIsolatedNode() {
    console.log('\n=== 测试6: 孤立节点测试 ===');
    
    const testData = JSON.parse(JSON.stringify(testTreeData));
    
    // 添加一个孤立的节点（没有父节点引用）
    testData.nodes['isolated_node'] = {
      solution: '这是一个孤立的解决方案节点，用于测试孤立节点处理。'
    };
    
    console.log('添加孤立节点后的数据:', testData);
    
    return testData;
  },

  // 运行所有测试
  runAllTests() {
    console.log('开始运行所有测试...');
    
    try {
      this.init();
      this.testDeleteSolutionNode();
      this.testDeleteDecisionNode();
      this.testAddSolutionNode();
      this.testAddDecisionNode();
      this.testChangeNodeType();
      this.testIsolatedNode();
      
      console.log('\n=== 所有测试完成 ===');
      console.log('请检查每个测试的输出，确保：');
      console.log('1. 删除节点后，引用该节点的选项被正确移除');
      console.log('2. 添加节点后，数据结构正确');
      console.log('3. 修改节点类型后，数据结构正确');
      console.log('4. 孤立节点被正确处理');
      
    } catch (error) {
      console.error('测试过程中出现错误:', error);
    }
  }
};

// 导出测试对象
window.TreeOperationsTest = TreeOperationsTest;

console.log('测试模块已加载，可以使用以下命令：');
console.log('TreeOperationsTest.runAllTests() - 运行所有测试');
console.log('TreeOperationsTest.testDeleteSolutionNode() - 测试删除解决方案节点');
console.log('TreeOperationsTest.testDeleteDecisionNode() - 测试删除决策节点');
console.log('TreeOperationsTest.testAddSolutionNode() - 测试添加解决方案节点');
console.log('TreeOperationsTest.testAddDecisionNode() - 测试添加决策节点');
console.log('TreeOperationsTest.testChangeNodeType() - 测试修改节点类型');
console.log('TreeOperationsTest.testIsolatedNode() - 测试孤立节点'); 