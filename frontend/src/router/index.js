import Vue from 'vue'
import VueRouter from 'vue-router'
import ScraperView from '@/views/ScraperView'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'ScraperView',
    component: ScraperView
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
