<script setup>
import { Clock, Calendar, MapPin } from 'lucide-vue-next'
</script>
<template>
    <div class="rounded-xl border bg-card text-card-foreground shadow" style="max-width: 20rem; margin: auto">
        <h1 class="event-title rounded-xl">{{ title }}</h1>
        <div class="container">
            <div class="event-date-time">
                <div class="m-2">
                    <Calendar class="me-1" /><span>{{ date }}</span>
                </div>
                <div class="m-2">
                    <Clock class="me-1" /><span>{{ time }}</span>
                </div>
                <div class="m-2">
                    <MapPin class="me-1" /><span>{{ location }}</span>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'EventCard',
    props: {
        title: String,
        date: String,
        time: String,
        location: String
    },
    methods: {}
}
</script>
<style scoped>
.event-date-time {
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: center;
    margin: 1rem 0;
}
.event-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    text-align: start;
}
</style>
