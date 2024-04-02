<script setup>
import Card from '@/components/Card.vue'
import Button from '@/components/Button.vue'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

const router = useRouter()
const userID = localStorage.getItem('userID')
const loading = ref(null)
const events = ref(null)

onMounted(async () => {
    try {
        // Example API call - replace with your actual API call
        const data = await fetch('http://localhost:8100/event').then((res) => res.json())
        events.value = data
        console.log(data)
    } catch (error) {
        console.error('Failed to fetch event data:', error)
    } finally {
        loading.value = false
    }
})

const navigate = (id) => {
    console.log(id)
    router.push({ path: `/events/${id}` })
}

function getImageUrl(event) {
    if (event && event.image && event.image !== 'None') {
        // Need to check if event.image !== None is necessary
        console.log(event.image)
        return `https://spickbucket.s3.ap-southeast-1.amazonaws.com/${event.image}`
    }
    // Return a default image URL or an empty string if event or event.image is not available
    return '../../public/default.png'
}
</script>

<template>
    <div>
        <div class="flex justify-center items-center p-4">
            <div class="flex items-center gap-4">
                <Input
                    placeholder="Search Events"
                    class="w-full sm:w-56 px-4 py-2 border-2 border-gray-300 dark:border-gray-700 rounded-md"
                />
                <Button> Search </Button>
            </div>
        </div>
        <div class="flex flex-wrap justify-around gap-4 items-center p-4">
            <Card
                class="pt-6 hover:bg-accent max-w-64"
                v-for="event in events"
                :key="event.event_id"
                @click="navigate(event?.event_id)"
            >
                <div class="space-y-2">
                    <img :src="getImageUrl(event)" alt="" class="w-[200px] h-[150px]" />
                    <div class="flex flex-col gap-y-1.5">
                        <h1>{{ event?.event_name }}</h1>
                        <div
                            v-if="event.time_out"
                            class="rounded-lg font-bold w-1/2 bg-green-300 text-center"
                        >
                            RSVP open
                        </div>
                        <div
                            v-else-if="!event.time_out"
                            class="rounded-lg font-bold w-1/2 bg-destructive text-center"
                        >
                            RSVP closed
                        </div>
                        <div
                            v-if="event.user_id == userID"
                            class="rounded-lg font-bold w-1/2 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-center"
                        >
                            Host
                        </div>
                        <div
                            v-else-if="event.user_id != userID"
                            class="rounded-lg font-bold w-1/2 bg-border text-center"
                        >
                            Invitee
                        </div>
                    </div>
                    <div class="text-sm text-muted-foreground">
                        <p>{{ event?.datetime_start }}</p>
                        <p>{{ event?.event_desc }}</p>
                    </div>
                </div>
            </Card>
        </div>
    </div>
</template>
