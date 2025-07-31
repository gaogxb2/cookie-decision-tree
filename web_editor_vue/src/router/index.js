import { createRouter, createWebHistory } from 'vue-router'
import DecisionTreeEditor from '../views/DecisionTreeEditor.vue'

const routes = [
  {
    path: '/',
    name: 'DecisionTreeEditor',
    component: DecisionTreeEditor
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 