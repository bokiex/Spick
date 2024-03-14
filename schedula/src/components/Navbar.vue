<script setup>
import { CalendarDays, SquarePlus, UserRound, TentTree } from 'lucide-vue-next'
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light m-3">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Spick</a>
            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/">
                            <CalendarDays /><span>Calendar</span>
                        </RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/create">
                            <SquarePlus /><span>Create</span>
                        </RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/events">
                            <TentTree /><span>Events</span> </RouterLink
                        >
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/profile">
                            <UserRound /><span>Profile</span>
                        </RouterLink>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
