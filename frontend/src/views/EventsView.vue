<script setup>
import Card from '@/components/Card.vue'
import Button from '@/components/Button.vue'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { format_date, format_time } from '@/utils/format_datetime'
import { getImageUrl } from '@/utils/get_image'
import Skeleton from '@/components/Skeleton.vue'

const router = useRouter()
const userID = Number(localStorage.getItem('userID'))
var loading = ref(true)
const events = ref(null)
var problem = ref(null)
const event_ms = 'http://localhost:8100/event'
console.log(event_ms)
onMounted(async () => {
    // Example API call - replace with your actual API call
    const res = await fetch(event_ms).then(
        // if status code is not 200, then set events to empty array
        (res) => {
            if (res.status != 200) {
                console.error('Failed to fetch event data:', res)
                problem.value = 'fetch failed'
                events.value = []
                loading.value = false
                return []
            } else {
                loading.value = false
                return res.json()
            }
        }
    )
    const data = res
    console.log(res)
    for (var i = data.length - 1; i >= 0; i--) {
        console.log(data[i])
        const invitees_user_ids = []
        data[i].datetime_start = new Date(data[i].datetime_start)
        data[i].datetime_end = new Date(data[i].datetime_end)
        // check if userID is in invitees
        for (var j in data[i].invitees) {
            if (data[i].invitees[j].user_id == userID) {
                invitees_user_ids.push(data[i].invitees[j].user_id)
            }
        }

        // if userID doesn't exist in invitee and is not equal to user_id, then remove the event
        if (!invitees_user_ids.includes(Number(userID)) && data[i].user_id != userID) {
            console.log(data[i].user_id, userID, 'removed')
            data.splice(i, 1)
        } else {
            console.log(data[i].user_id, userID, 'kept')
        }
    }

    if (data == null || data.length == 0) {
        problem.value = 'no events'

        events.value = []
    }
    events.value = data
})

const navigate = (id) => {
    router.push({ path: `/events/${id}` })
}
</script>

<template>
    <div>
        <div class="container p-4" v-if="problem === 'fetch failed'">
            <div class="row justify-content-center">
                <!-- Form Start -->
                <div class="form-container" style="position: relative">
                    <div class="center" style="text-align: center">
                        <div style="text-align: center">
                            <h1 class="header form-input" style="font-size: x-large">
                                Could not fetch events, please try again later
                            </h1>
                            <router-link class="btn exit" type="button" :to="`/`">
                                Home
                            </router-link>
                        </div>
                    </div>
                    <div class="text-sm text-muted-foreground">
                        <p>{{ format_date(event?.datetime_start) }}</p>
                        <p>{{ format_time(event?.datetime_start) }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="container p-4" v-else-if="problem === 'no events'">
            <div class="row justify-content-center">
                <!-- Form Start -->
                <div class="form-container" style="position: relative">
                    <div class="center" style="text-align: center">
                        <div style="text-align: center">
                            <h1 class="header form-input" style="font-size: x-large">
                                No events to be found, create an event here!
                            </h1>
                            <router-link class="btn exit" type="button" :to="`/create`">
                                Event
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else-if="problem === null">
            <div class="flex justify-center items-center p-4">
                <div class="flex items-center gap-4">
                    <Input
                        placeholder="Search Events"
                        class="w-full sm:w-56 px-4 py-2 border-2 border-gray-300 dark:border-gray-700 rounded-md"
                    />
                    <Button> Search </Button>
                </div>
            </div>
            <div class="flex flex-wrap justify-around gap-4 items-center p-4" v-if="!loading">
                <Card
                    class="pt-6 hover:bg-accent max-w-64"
                    v-for="event in events"
                    :key="event.event_id"
                    @click="navigate(event?.event_id)"
                >
                    <div class="space-y-2">
                        <img :src="getImageUrl(event?.image)" alt="" class="w-[200px] h-[150px]" />
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
                            <p>{{ format_date(event?.datetime_start) }}</p>
                            <p>{{ format_time(event?.datetime_start) }}</p>
                            <p>{{ event?.event_desc }}</p>
                        </div>
                    </div>
                </Card>
            </div>
        </div>
    </div>
 
        <div class="flex flex-wrap justify-around gap-4 items-center p-4" v-if="loading">
            <Skeleton class="h-80 pt-6 w-64 rounded-xl" />
            <Skeleton class="h-80 pt-6 w-64 rounded-xl" />
            <Skeleton class="h-80 pt-6 w-64 rounded-xl" />
            <Skeleton class="h-80 pt-6 w-64 rounded-xl" />
        </div>

</template>
