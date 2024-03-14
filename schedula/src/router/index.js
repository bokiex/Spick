import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EventsView from '../views/EventsView.vue'
import Event from '../views/Event.vue'
import EventForm from '../views/EventForm.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/events',
      name: 'events',
      component: EventsView
    },
    {
      path: '/events/:id',
      name: 'event',
      component: Event
    },
    {
      path: '/create',
      name: 'create',
      component: EventForm
    },
    {
      path: '/profile',
      name: 'profile',
      component: Event
    }
  ]
})

export default router
