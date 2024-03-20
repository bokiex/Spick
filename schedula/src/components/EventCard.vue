<script setup>
import { Clock, Calendar  } from 'lucide-vue-next';
</script>
<template>
    <div class="card shadow-sm rounded-4" style="max-width: 20rem; margin: auto">
        <h1 class="event-title card-header">{{ title }}</h1>
        <div class="event-date-time">
         
            <Calendar class="m-1"/><span>{{ date }}</span>
            <p>{{ time }}</p>
        </div>
        <p class="event-location">{{ location }}</p>
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
.event-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    text-align: start;
}
</style>
