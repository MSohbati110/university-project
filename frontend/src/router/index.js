import Vue from 'vue'
import VueRouter from 'vue-router'
import ScraperView from '@/views/ScraperView'
import HomeView from '@/views/HomeView'
import DashboardView from '@/views/DashboardView'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/scraper',
    name: 'Scraper',
    component: ScraperView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
