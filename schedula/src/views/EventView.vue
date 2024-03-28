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

const format_date = (datetime) => {
    const date = new Date(datetime)
    const date_options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }

    return date.toLocaleDateString('en-US', date_options)
}

const format_time = (datetime) => {
    const date = new Date(datetime)
    const time_options = { hour: 'numeric', minute: 'numeric', hour12: true }

    return date.toLocaleTimeString('en-US', time_options)
}

const reservation = () => {
    router.push({ path: `/events/${event_id}/RSVP` })
}

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

function getImageUrl(event) {
    if (event && event.image) {
        const url = 'https://spickbucket.s3.ap-southeast-1.amazonaws.com/' + event.image

        return url
    }

    // Return a default image URL or an empty string if event or event.image is not available
    return 'path/to/default/image.jpg'
}
</script>

<template>
    <div class="container mx-auto p-4">
        <div class="bg-white rounded-lg overflow-hidden shadow-lg">
            <div class="relative mb-8">
                <Skeleton v-if="loading" class="h-64 w-full rounded-xl" />
                <img
                    v-else
                    :src="getImageUrl(event)"
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
                                {{ format_date(event?.datetime_start) }}
                            </span>
                        </div>
                        <div class="flex gap-x-1 text-muted-foreground">
                            <Clock class="flex-shrink-0" />
                            <Skeleton v-if="loading" class="w-24 h-6" />
                            <span class="text-sm">
                                {{ format_time(event?.datetime_start) }}
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
                                <Button @click="reservation()">Join</Button>
                            </div>
                        </Card>
                        <Card>
                            <div class="flex flex-col gap-y-1.5 p-4 space-y-1">
                                <h3 class="text-lg font-semibold">Organizer</h3>
                                <p>{{ event?.user_id }}</p>
                                <p>{{ event?.user_id }}</p>
                            </div>
                        </Card>

                        <Card>
                            <div class="flex flex-col gap-y-1.5 p-4 space-y-1">
                                <h3 class="text-lg font-semibold">Attendees</h3>
                                <div class="flex overflow-hidden gap-x-3">
                                    <div
                                        class=" flex flex-col items-center justify-center"
                                        v-for="invitee in event?.invitees"
                                        :key="invitee.user_id"
                                    >
                                        <Avatar
                                            src="https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80"
                                            class="w-12 h-12 rounded-full"
                                        >
                                        </Avatar>
                                        <span class=" p-2 text-center font-light text-xs">
                                            Light
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
