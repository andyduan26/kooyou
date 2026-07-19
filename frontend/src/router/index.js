import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
  { path: '/category', name: 'category', component: () => import('@/views/CategoryView.vue') },
  { path: '/play/:id', name: 'play', component: () => import('@/views/PlayView.vue') },
  { path: '/profile', name: 'profile', component: () => import('@/views/ProfileView.vue') }
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})
