<script setup>
import Card from '../components/Card.vue'
import Avatar from '@/components/Avatar.vue'
import { Calendar, Clock, MapPin, Pin } from 'lucide-vue-next'
import Button from '@/components/Button.vue'
import { useRouter, useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'
import Skeleton from '@/components/Skeleton.vue'

const router = useRouter()
const route = useRoute()

const event_id = route.params.id
const event = ref(null)
const loading = ref(true)

onMounted(async () => {
    try {
        // Example API call - replace with your actual API call
        const data = await fetch('http://localhost:3800/event' + `/${event_id}`).then((res) =>
            res.json()
        )

        event.value = data
        console.log(data)
    } catch (error) {
        console.error('Failed to fetch event data:', error)
    } finally {
        loading.value = false
    }
})

// const event = {
//     title: 'Dinner Party',
//     image: '/event.jpg',
//     date: 'Saturday, Feb 23 2024',
//     time: '5:00 PM - 11:00 PM',
//     location: '5323 Gilroy St, Gilroy, CA',
//     description:
//         'We are hosting a dinner party just for our best clients. We are excited to see you there.',
//     organizer: {
//         name: 'American Bar',
//         contact: 'Phone: (415)444-3434 | Email: info@americanbar.com'
//     },
//     attendees: [
//         { id: 1, avatar: 'path-to-avatar1.jpg' },
//         { id: 2, avatar: 'path-to-avatar2.jpg' }
//         // More attendees...
//     ]
// }
</script>

<template>
    <div class="container mx-auto p-4">
        <div class="bg-white rounded-lg overflow-hidden shadow-lg">
            <div class="relative mb-8">
                <Skeleton v-if="loading" class="h-64 w-full rounded-xl" />
                <img
                    v-else
                    :src="event?.image[0]?.image_path"
                    alt="Event banner"
                    class="w-full h-64 object-cover"
                />

                <Card
                    class="absolute bottom-0 left-0 right-0 transform translate-y-1/2 mx-auto w-1/2"
                    :click="() => {}"
                >
                    <div class="flex flex-col gap-y-1.5 p-6 space-y-1">
                        <Skeleton v-if="loading" class="w-24 h-6" />
                        <h3 v-else class="font-semibold tracking-tight text-2xl">
                            {{ event?.event_name }}
                        </h3>
                        <div class="flex gap-x-1 text-muted-foreground">
                            <Calendar class="flex-shrink-0" />
                            <Skeleton v-if="loading" class="w-24 h-6" />
                            <span v-else class="text-sm">
                                {{ event?.event_time }}
                            </span>
                        </div>
                        <div class="flex gap-x-1 text-muted-foreground">
                            <Clock class="flex-shrink-0 " />
                            <Skeleton v-if="loading" class="w-24 h-6" />
                            <span class="text-sm">
                                {{ event?.event_time }}
                            </span>
                        </div>
                        <div class="flex gap-x-1 text-muted-foreground">
                            <MapPin class="flex-shrink-0" />
                            <Skeleton v-if="loading" class="w-24 h-6" />
                            <span class="text-sm">
                                {{ event?.reservation_address }}
                            </span>
                        </div>
                    </div>
                </Card>
            </div>
            <div class="grid grid-cols-5 mt-36 p-4">
                <div class="col-span-3 p-4">
                    <h3 class="font-semibold tracking-tight text-2xl">Event Description</h3>
                    <Skeleton v-if="loading" class="w-24 h-6" />
                    <div v-else class="text-muted-foreground">{{ event?.event_desc }}</div>
                </div>
                <div class="col-span-2 p-4">
                    <div class="space-y-4 w-full">
                        <Card>
                            <div class="flex flex-col gap-y-1.5 p-4 space-y-1">
                                <h3 class="text-lg font-semibold">RSVP now</h3>
                                <p class="text-muted-foreground">Click to RSVP</p>
                                <Button>Join</Button>
                            </div>
                        </Card>
                        <Card>
                            <div class="flex flex-col gap-y-1.5 p-4 space-y-1">
                                <h3 class="text-lg font-semibold">Organizer</h3>
                                <p>{{ event?.organizer.name }}</p>
                                <p>{{ event?.organizer.contact }}</p>
                            </div>
                        </Card>

                        <Card>
                            <div class="flex flex-col gap-y-1.5 p-4 space-y-1">
                                <h3 class="text-lg font-semibold">Attendees</h3>
                                <div class="flex space-x-2 overflow-hidden">
                                    <Avatar v-for="attendee in event?.invitees"> </Avatar>
                                </div>
                            </div>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
