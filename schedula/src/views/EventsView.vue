<template>
    <div class="container py-5">
        <div class="row">
            <div class="col-sm-12 col-md-6 col-lg-4 mb-4" v-for="event in events" :key="event.id">
                <Card
                    :id="event.id"
                    :title="event.title"
                    :image="event.image"
                    :description="event.description"
                />
            </div>
        </div>
    </div>
</template>

<script>
import Card from '@/components/Card.vue'

export default {
    name: 'EventsPage',
    userID: localStorage.getItem('userID'),
    data() {
        return {
            // Sample events data
            events: [
                {
                    id: 1,
                    title: 'Event 1',
                    description: 'This is the first event.',
                    date: '2023-03-15',
                    image: 'https://via.placeholder.com/600x350'
                },
                {
                    id: 2,
                    title: 'Event 2',
                    description: 'This is the second event.',
                    date: '2023-03-20',
                    image: 'https://via.placeholder.com/600x350'
                }
                // Add more events as needed
            ]
        }
    },
    methods: {},
    components: { Card }
}
</script>
