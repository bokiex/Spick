import { createRouter, createWebHistory } from 'vue-router'
import CalendarView from '../views/CalendarView.vue'
import AuthenticationView from '../views/AuthenticationView.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: CalendarView
        },
        {
            path: '/authentication',
            name: 'authentication',
            component: AuthenticationView
        }
    ]
})

export default router
