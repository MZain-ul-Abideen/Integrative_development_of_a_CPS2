import { createRouter, createWebHistory } from 'vue-router'
// import DashBoard from '../views/dashboard-page.vue'
import Create from '../views/create-page.vue'
import Notifications from '../views/notifications-page.vue'
// import Help from '../views/help-page.vue'
import NotFound from '../views/404-page.vue'

const routes = [
  {
    path: '/',
    redirect: '/create' // Redirect root path to /dashboard
  },
  // {
  //   path: '/dashboard',
  //   name: 'DashBoard',
  //   component: DashBoard
  // },
  {
    path: '/create',
    name: 'Create',
    component: Create
  },
  {
    path: '/notifications',
    name: 'Notification',
    component: Notifications
  },
  // {
  //   path: '/help',
  //   name: 'Help',
  //   component: Help
  // },
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
