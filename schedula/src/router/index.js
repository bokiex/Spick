import { createRouter, createWebHistory } from 'vue-router'

import CalendarView from '../views/CalendarView.vue'
import EventsView from '../views/EventsView.vue'
import EventView from '../views/EventView.vue'
import EventFormView from '../views/EventFormView.vue'
import SignInSignUpView from '../views/SignInSignUpView.vue'
import AuthenticationView from '../views/AuthenticationView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: CalendarView
        },
        {
            path: '/events',
            name: 'events',
            component: EventsView
        },
        {
            path: '/events/:id',
            name: 'event',
            component: EventView
        },
        {
            path: '/create',
            name: 'create',
            component: EventFormView
        },
        {
            path: '/profile',
            name: 'profile',
            component: ProfileView
        },
        {
            path: '/SignInSignUp',
            name: 'SignInSignUp',
            component: SignInSignUpView
        }
    ]
})

export default router
