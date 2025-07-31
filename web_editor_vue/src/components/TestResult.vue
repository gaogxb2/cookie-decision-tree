<template>
  <div class="test-result">
    <el-alert 
      v-if="result.success" 
      title="测试成功" 
      type="success" 
      :closable="false"
      show-icon
    />
    <el-alert 
      v-else 
      :title="`测试失败: ${result.error}`" 
      type="error" 
      :closable="false"
      show-icon
    />
    
    <div v-if="result.success" class="result-content">
      <el-divider content-position="left">测试路径</el-divider>
      <el-timeline>
        <el-timeline-item 
          v-for="(step, index) in result.path" 
          :key="index"
          :timestamp="`步骤 ${index + 1}`"
          placement="top"
        >
          <el-card class="step-card">
            <div class="step-content">
              <el-icon class="step-icon"><ArrowRight /></el-icon>
              <span class="step-text">{{ step }}</span>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
      
      <el-divider content-position="left">最终解决方案</el-divider>
      <el-card class="solution-card">
        <div class="solution-content">
          <el-icon class="solution-icon"><Lightbulb /></el-icon>
          <div class="solution-text">
            {{ result.solution }}
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestResult',
  props: {
    result: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.test-result {
  padding: 20px;
}

.result-content {
  margin-top: 20px;
}

.step-card {
  margin-bottom: 10px;
}

.step-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.step-icon {
  color: #409eff;
  font-size: 16px;
}

.step-text {
  font-weight: 500;
  color: #303133;
}

.solution-card {
  background: #f0f9ff;
  border: 1px solid #b3d8ff;
}

.solution-content {
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.solution-icon {
  color: #e6a23c;
  font-size: 20px;
  margin-top: 2px;
}

.solution-text {
  flex: 1;
  line-height: 1.6;
  color: #606266;
}
</style> 