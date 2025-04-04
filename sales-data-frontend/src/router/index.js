import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import SalesDashboard from '../components/SalesDashboard.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/dashboard', component: SalesDashboard, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) next('/')
  else next()
})

export default router