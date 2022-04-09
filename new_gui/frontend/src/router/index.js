import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/dashboard-beta',
    name: 'DashboardBeta',
    component: () => import('../views/DashboardBeta.vue') 
  }
]

const router = new VueRouter({
  routes
})

export default router
