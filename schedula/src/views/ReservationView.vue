<script>
import { RadioGroupItem, RadioGroupRoot, Label } from 'radix-vue'
export default {
    userID: localStorage.getItem('userID'),
    components: {
        RadioGroupItem,
        RadioGroupRoot,
        Label
    },
    data() {
        return {
            selectedTimeslot: '',
            selectedVenu: '',
            timeslots: [
                {
                    date: '2024-03-14',
                    start_time: '2024-03-14T21:00:00',
                    end_time: '2024-03-14T13:00:00'
                },
                {
                    date: '2024-03-15',
                    start_time: '2024-03-14T21:00:00',
                    end_time: '2024-03-14T13:00:00'
                },
                {
                    date: '2024-03-16',
                    start_time: '2024-03-14T21:00:00',
                    end_time: '2024-03-14T13:00:00'
                }
            ],
            venues: [
                {
                    name: 'SMU',
                    address: 'Victoria Road',
                    imageUrl: 'https://via.placeholder.com/150'
                },
                {
                    name: 'SMU',
                    address: 'Victoria Road',
                    imageUrl: 'https://via.placeholder.com/150'
                },
                {
                    name: 'SMU',
                    address: 'Victoria Road',
                    imageUrl: 'https://via.placeholder.com/150'
                }
            ]
        }
    }
}
</script>

<template>
    <div class="reservation-page">
        <div class="container my-4">
            <h3>Reservation</h3>
            <div class="grid grid-cols-2" style="margin-top: 2rem">
                <!-- Time Slot Start -->

                <div class="timeslots-container">
                    <RadioGroupRoot v-model="selectedTimeslot">
                        <div class="grid grid-row-3 gap-4">
                            <Label
                                v-for="(timeslot, index) in timeslots"
                                :for="index"
                                class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                            >
                                <RadioGroupItem
                                    :id="index"
                                    :value="timeslot"
                                    class="peer sr-only aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                >
                                    <RadioGroupIndicator class="flex items-center justify-center">
                                        <Circle class="h-2.5 w-2.5 fill-current text-current" />
                                    </RadioGroupIndicator>
                                </RadioGroupItem>

                                <p class="text-sm font-medium leading-none">
                                    {{
                                        new Date(timeslot.date).toLocaleDateString('en-US', {
                                            weekday: 'long',
                                            month: 'long',
                                            day: 'numeric'
                                        })
                                    }}
                                </p>
                                <p class="text-sm text-muted-foreground">
                                    {{
                                        new Date(timeslot.start_time).toLocaleTimeString('en-US', {
                                            timeStyle: 'short'
                                        })
                                    }}
                                    -
                                    {{
                                        new Date(timeslot.end_time).toLocaleTimeString('en-US', {
                                            timeStyle: 'short'
                                        })
                                    }}
                                </p>
                            </Label>
                        </div>
                    </RadioGroupRoot>
                </div>

                <!-- Time Slot End -->
                <!-- Venue Start -->

                <div class="venues-container">
                    <RadioGroupRoot v-model="selectedVenue">
                        <div class="grid grid-row-3 gap-4">
                            <Label
                                v-for="(venue, index) in venues"
                                :for="index + 100"
                                class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                            >
                                <RadioGroupItem
                                    :id="index + 100"
                                    :value="venue"
                                    class="peer sr-only aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                >
                                    <RadioGroupIndicator class="flex items-center justify-center">
                                        <Circle class="h-2.5 w-2.5 fill-current text-current" />
                                    </RadioGroupIndicator>
                                </RadioGroupItem>
                                <img :src="venue.imageUrl" :alt="venue.name" />
                                <div class="venue-card-content">
                                    <h3>{{ venue.name }}</h3>
                                    <p>{{ venue.address }}</p>
                                </div>
                            </Label>
                        </div>
                    </RadioGroupRoot>
                </div>

                <!-- Venue end -->
            </div>
        </div>
    </div>
</template>

<style scoped>
.checkbox-box {
    display: block;
    padding: 10px; /* Add padding for better spacing */
}

.checkbox-box input[type='radio'] {
    display: none;
}

.checkbox-box label {
    display: block;
    border: 2px solid #ccc;
    border-radius: 10px;
    background-color: #98c1d9;
    padding: 10px; /* Add padding to style the entire row */
    cursor: pointer; /* Add cursor pointer for better UX */
}

.checkbox-box input[type='radio']:checked + label {
    background-color: #3d5a80;
    color: white;
}

.checkbox-row {
    margin-bottom: 10px; /* Add margin between rows */
}

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

.timeslot-card,
.venue-card {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 10px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-left: 5px;
    margin-right: 5px;
}

.timeslot-card h3,
.venue-card h3 {
    margin: 0;
    font-size: 18px;
    color: #333;
    margin-bottom: 5px;
}

.timeslot-card p,
.venue-card p {
    font-size: 16px;
    color: #555;
}

.venue-card img {
    width: 70%;
    height: 50%;
    object-fit: cover;
    margin-bottom: 10px;
    border-radius: 8px;
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
