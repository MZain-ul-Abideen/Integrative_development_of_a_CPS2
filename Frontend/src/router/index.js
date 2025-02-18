import { createRouter, createWebHistory } from 'vue-router'
import Create from '../views/create-page.vue'
import RulesList from '../views/rules-list.vue'
import NotFound from '../views/404-page.vue'

const routes = [
  {
    path: '/',
    redirect: '/create'
  },
  {
    path: '/create',
    name: 'Create',
    component: Create
  },
  {
    path: '/rules',
    name: 'RulesList',
    component: RulesList
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
