import { createRouter, createWebHistory } from 'vue-router'

import CalendarView from '../views/CalendarView.vue'
import EventsView from '../views/EventsView.vue'
import EventView from '../views/EventView.vue'
import EventFormView from '../views/EventFormView.vue'
import SignInSignUpView from '../views/SignInSignUpView.vue'
import ProfileView from '../views/ProfileView.vue'
import ReservationView from '@/views/ReservationView.vue'
import RSVP from '../views/RSVP.vue'
import EnterCode from '@/views/EnterCode.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: CalendarView,
            meta: { requiresAuth: true }
        },
        {
            path: '/events',
            name: 'events',
            component: EventsView,
            meta: { requiresAuth: true }
        },
        {
            path: '/events/:id',
            name: 'event',
            component: EventView,
            meta: { requiresAuth: true }
        },
        {
            path: '/create',
            name: 'create',
            component: EventFormView
        },
        {
            path: '/profile',
            name: 'profile',
            component: ProfileView,
            meta: { requiresAuth: true }
        },
        {
            path: '/SignInSignUp',
            name: 'SignInSignUp',
            component: SignInSignUpView
        },
        {
            path: '/reservation',
            name: 'reservation',
            component: ReservationView
        },
        {
            path: '/RSVP/:userID/:eventToken',
            name: 'RSVP',
            component: RSVP,
            meta: { hideNavbar: true },
        },
        {
            path: '/entercode',
            name: 'entercode',
            component: EnterCode
        }
    ]
})
router.beforeEach((to, from, next) => {
    // Check if the route requires the user to be logged in
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        const userID = localStorage.getItem('userID')
        if (!userID) {
            // If no userid, redirect to the SignInSignUp page
            next({ name: 'SignInSignUp', query: { redirect: to.fullPath } })
        } else {
            next() // if userid is found, proceed to the route
        }
    } else {
        next() // if the route does not require auth, proceed
    }
})

export default router
