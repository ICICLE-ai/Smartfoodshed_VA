import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path:'/',
    name:'dataset',
    component:()=>import('../views/Dataset.vue')
  },
  {
    path: '/dashboard',
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
  routes,
  base: process.env.BASE_URL
})

export default router
