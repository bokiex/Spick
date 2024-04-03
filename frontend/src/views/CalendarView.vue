<script setup>
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'
import '@vuepic/vue-datepicker/dist/main.css'
import { ref, onMounted } from 'vue'

const events = ref([])
const loading = ref(true)
const event_ms = 'http://localhost:8200/event'
const userID = localStorage.getItem('userID')
onMounted(async () => {
    try {
        // Example API call - replace with your actual API call
        const data = await fetch(event_ms).then((res) => {
            if (res.status != 200) {
                console.error('Failed to fetch event data:', res)
                return []
            } else {
                console.log(res.json())
            }
        })
    } catch (error) {
        console.error('Failed to fetch event data:', error)
    } finally {
        loading.value = false
    }
})
</script>
<template>
    <div class="">
        <vue-cal
            selected-date="2024-03-19"
            :time-from="9 * 60"
            :time-to="23 * 60"
            :disable-views="['years']"
            events-count-on-year-view
            :events="events"
        ></vue-cal>
        <!-- Modal -->
        <!-- <div
            class="modal fade"
            id="createEventForm"
            tabindex="-1"
            aria-labelledby="exampleModalLabel"
            aria-hidden="true"
        >
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Create an event</h1>
                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                        ></button>
                    </div>
                    <div class="modal-body">
                        <div class="row mb-3 align-items-center">
                            <div class="col-3">
                                <label for="eventName" class="col-form-label">Event Name:</label>
                            </div>
                            <div class="col-9">
                                <input type="text" id="eventName" class="form-control" />
                            </div>
                        </div>
                        <div class="row align-items-center mb-1">
                            <div class="col-3">
                                <label for="eventName" class="col-form-label">Type of Event:</label>
                            </div>
                            <div class="col-9">
                                <select class="form-select" @click="handleSelect">
                                    <option value="Restaurant">Restaurant</option>
                                    <option value="Picnic">Picnic</option>
                                    <option value="Birthday">Birthday</option>
                                </select>
                            </div>
                        </div>
                        <div class="row align-items-center mb-1">
                            <div class="col-3">
                                <label for="eventName" class="col-form-label">Where:</label>
                            </div>
                            <div class="col-9">
                                <select class="form-select" @click="handleSelect">
                                    <option
                                        v-for="place in this.locations"
                                        :key="place"
                                        :value="place"
                                    >
                                        {{ place }}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-6 text-center">
                                <label class="col-form-label">Start Time</label>
                            </div>
                            <div class="col-6 text-center">
                                <label class="col-form-label">End Time</label>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-6">
                                <VueDatePicker v-model="selected.startTime" time-picker-inline />
                            </div>

                            <div class="col-6">
                                <VueDatePicker v-model="selected.endTime" time-picker-inline />
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer align-items-center">
                        <button type="button" class="btn btn-primary" @click="createEvent()">
                            Create
                        </button>
                    </div>
                </div>
            </div>
        </div> -->
    </div>
</template>
