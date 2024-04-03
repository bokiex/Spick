<script setup>
import { RadioGroupItem, RadioGroupIndicator, RadioGroupRoot, Label } from 'radix-vue'
import { ref, onMounted, onBeforeMount } from 'vue'
import { format_date, format_time } from '@/utils/format_datetime'
import { useRoute } from 'vue-router'
import { getImageUrl } from '@/utils/get_image'
import Button from '@/components/Button.vue'

const route = useRoute()
const event_id = route.params.id

const timeslots = ref([])
const recommendations = ref([])

onMounted(async () => {
    const timeslots_data = await fetch('http://localhost:8200/timeslot/' + event_id).then((res) =>
        res.json()
    )
    timeslots.value = timeslots_data

    const recommendation_data = await fetch('http://localhost:8100/event/' + event_id).then((res) =>
        res.json()
    )

    recommendations.value = recommendation_data.recommendations

    console.log(timeslots_data)
    console.log(recommendation_data)
})
// const timeslots = [
//     {
//         date: '2024-03-14',
//         start_time: '2024-03-14T21:00:00',
//         end_time: '2024-03-14T13:00:00'
//     },
//     {
//         date: '2024-03-15',
//         start_time: '2024-03-14T21:00:00',
//         end_time: '2024-03-14T13:00:00'
//     },
//     {
//         date: '2024-03-16',
//         start_time: '2024-03-14T21:00:00',
//         end_time: '2024-03-14T13:00:00'
//     }
// ]

const userID = localStorage.getItem('userID')
const selectedTimeslot = ref(0)
const selectedVenue = ref(100)

const reserve = () => {
   
    console.log(JSON.stringify({
            user_id: userID,
            event_id: event_id,
            reservation_address:
                recommendations.value[selectedVenue.value - 100].recommendation_address,
            reservation_name: recommendations.value[selectedVenue.value - 100].recommendation_name,
            datetime_start: timeslots.value[selectedTimeslot.value].start_time,
            datetime_end: timeslots.value[selectedTimeslot.value].end_time,
            attendees: timeslots.value[selectedTimeslot.value].invitees
        }))

    fetch('http://localhost:8202/reserve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userID,
            event_id: event_id,
            reservation_address:
                recommendations.value[selectedVenue.value - 100].recommendation_address,
            reservation_name: recommendations.value[selectedVenue.value - 100].recommendation_name,
            datetime_start: timeslots.value[selectedTimeslot.value].start_time,
            datetime_end: timeslots.value[selectedTimeslot.value].end_time,
            attendees: timeslots.value[selectedTimeslot.value].invitees
        })
    })
}
</script>

<template>
    <div class="reservation-page">
        <div class="container my-4">
            <div style="display: flex; justify-content: space-between; align-items: center">
                <div>
                    <h3 class="text-lg font-medium">Reservation</h3>
                    <p class="text-sm text-muted-foreground">
                        Select the time and place a reservation!
                    </p>
                </div>
                <div class="flex justify-end">
                    <Button type="submit" @click="reserve">Reserve</Button>
                </div>
            </div>
            <Separator class="shrink-0 bg-border h-px w-full" />
            <div class="grid grid-cols-2" style="margin-top: 2rem">
                <!-- Time Slot Start -->

                <div class="timeslots-container">
                    <RadioGroupRoot v-model="selectedTimeslot" :default-value="timeslots[0]">
                        <div class="grid grid-row-3 gap-4">
                            <div v-for="(timeslot, index) in timeslots">
                                <RadioGroupItem :id="index" :value="index" class="peer sr-only" />
                                <Label
                                    :for="index"
                                    class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                                >
                                    <p class="text-sm font-medium leading-none">
                                        {{ format_date(timeslot.start_time) }}
                                    </p>
                                    <p class="text-sm text-muted-foreground">
                                        {{ format_time(timeslot.start_time) }}
                                        -
                                        {{ format_time(timeslot.end_time) }}
                                    </p>
                                    <div class="flex flex-col gap-y-1.5 p-4 space-y-1">
                                        <h3 class="text-lg font-semibold">Attendees</h3>
                                        <div class="flex overflow-hidden gap-x-3">
                                            <div
                                                class="flex flex-col items-center justify-center"
                                                v-for="invitee in timeslot.invitees"
                                                :key="invitee.user_id"
                                            >
                                                <Avatar
                                                    :src="getImageUrl(invitee.image)"
                                                    class="w-12 h-12 rounded-full"
                                                >
                                                </Avatar>
                                                <span class="p-2 text-center font-light text-xs">
                                                    {{ invitee.username }}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </Label>
                            </div>
                        </div>
                    </RadioGroupRoot>
                </div>

                <!-- Time Slot End -->
                <!-- Venue Start -->

                <div class="venues-container">
                    <RadioGroupRoot v-model="selectedVenue">
                        <div class="grid grid-row-3 gap-4">
                            <div v-for="(recommendation, index) in recommendations">
                                <RadioGroupItem
                                    :id="index + 100"
                                    :value="index + 100"
                                    class="peer sr-only"
                                />
                                <Label
                                    :for="index + 100"
                                    class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                                >
                                    <img
                                        :src="recommendation.recommendation_photo"
                                        :alt="recommendation.recommendation_name"
                                    />
                                    <div class="recommendation-card-content">
                                        <h3>{{ recommendation.recommendation_name }}</h3>
                                        <p>{{ recommendation.recommendation_address }}</p>
                                    </div>
                                </Label>
                            </div>
                        </div>
                    </RadioGroupRoot>
                </div>

                <!-- Venue end -->
            </div>
        </div>
    </div>
</template>

<style scoped>
.reservation-page {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 40px;
    padding: 20px;
    gap: 20px;
    /* height: 100%; */
    margin-left: 5rem;
    margin-right: 5rem;
}

.timeslots-container,
.venues-container {
    flex: 1;
    overflow-y: auto;
    margin: 10px;
    text-align: center;
    height: calc(100vh - 60px);
}

/* Responsive Design */
@media (max-width: 768px) {
    .reservation-page {
        flex-direction: column;
    }

    .timeslots-container,
    .venues-container {
        flex: none;
        width: 100%;
    }
}

/* Hide scrollbar for Chrome, Safari and Opera */
.timeslots-container::-webkit-scrollbar,
.venues-container::-webkit-scrollbar {
    display: none;
}

.timeslots-container,
.venues-container {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>
