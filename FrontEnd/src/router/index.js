import { createRouter, createWebHistory } from 'vue-router'
import DashBoard from '../views/dashboard-page.vue'
import Manager from '../views/manager-page.vue'
import Notifications from '../views/notifications-page.vue'
import Settings from '../views/settings-page.vue'
import Help from '../views/help-page.vue'
import NotFound from '../views/404-page.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard' // Redirect root path to /dashboard
  },
  {
    path: '/dashboard',
    name: 'DashBoard',
    component: DashBoard
  },
  {
    path: '/manager',
    name: 'Manager',
    component: Manager
  },
  {
    path: '/notifications',
    name: 'Notification',
    component: Notifications
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/help',
    name: 'Help',
    component: Help
  },
  {
    path: '/:pathMatch(.*)*', // Catch-all for undefined paths
    name: 'NotFound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
