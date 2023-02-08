import store from '@/store'
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
    component: () => import('../views/Dashboard.vue'),
    beforeEnter: (to, from, next)=>{
      console.log(store.state.database)
      if(store.state.database!=""){
        next() 
      }else{
        next('/')
      }
    }
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
