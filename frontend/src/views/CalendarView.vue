<script setup>
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'
import '@vuepic/vue-datepicker/dist/main.css'
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

var events = ref([])
var loaded = ref(false)
const event_ms = 'http://localhost:8200/event'
const userID = localStorage.getItem('userID')
var today = new Date()
var selected_date = ref(null)

onMounted(async () => {
    selected_date =
        today.getFullYear() +
        '-' +
        ('0' + (today.getMonth() + 1)).slice(-2) +
        '-' +
        ('0' + today.getDate()).slice(-2)
    try {
        await axios.get(event_ms).then((response) => {
            let data = response.data
            for (var i = data.length - 1; i >= 0; i--) {
                console.log(data[i])
                const invitees_user_ids = []
                for (var j in data[i].invitees) {
                    if (data[i].invitees[j].user_id == userID) {
                        invitees_user_ids.push(data[i].invitees[j].user_id)
                    }
                }
                if (
                    (!invitees_user_ids.includes(Number(userID)) && data[i].user_id != userID) ||
                    data[i].reservation_address === null
                ) {
                    data.splice(i, 1)
                } else {
                    data[i].datetime_start = new Date(data[i].datetime_start)
                    data[i].datetime_end = new Date(data[i].datetime_end)
                }
            }
            for (var event of data) {
                var topush = {
                    start:
                        event.datetime_start.getFullYear() +
                        '-' +
                        ('0' + (event.datetime_start.getMonth() + 1)).slice(-2) +
                        '-' +
                        ('0' + event.datetime_start.getDate()).slice(-2) +
                        ' ' +
                        ('0' + event.datetime_start.getHours()).slice(-2) +
                        ':' +
                        ('0' + event.datetime_start.getMinutes()).slice(-2),
                    end:
                        event.datetime_end.getFullYear() +
                        '-' +
                        ('0' + (event.datetime_end.getMonth() + 1)).slice(-2) +
                        '-' +
                        ('0' + event.datetime_end.getDate()).slice(-2) +
                        ' ' +
                        ('0' + event.datetime_end.getHours()).slice(-2) +
                        ':' +
                        ('0' + event.datetime_end.getMinutes()).slice(-2),
                    title: event.event_name,
                    content: event.event_desc
                }
                events.value.push(topush)
            }
        })
        // Example API call - replace with your actual API call
        // const data = await fetch(event_ms).then((res) => res.json())
        // console.log(data)
        // events.value = data.map((event) => ({
        //     start: event.range_start,
        //     end: event.range_end,
        //     title: event.event_name,
        //     desc: event.event_desc,
        //     // Add other custom fields as needed
        //     images: event.image,
        //     recommendations: event.recommendation
        // }))
    } catch (error) {
        console.error('Failed to fetch event data:', error)
    } finally {
        loaded.value = true
    }
})
</script>
<template>
    <div class="">
        <vue-cal
            v-if="loaded"
            :selected-date="selected_date"
            :time-from="0 * 60"
            :time-to="24 * 60"
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
