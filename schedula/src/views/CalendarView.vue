<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import bootstrap5Plugin from '@fullcalendar/bootstrap5'
import { Modal } from 'bootstrap'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import axios from 'axios'
import Navbar from '@/components/Navbar.vue'

let INITIAL_EVENTS = [
    {
        id: 1,
        title: 'All-day event',
        start: new Date().toISOString().replace(/T.*$/, '')
    },
    {
        id: 2,
        title: 'Timed event',
        start: new Date().toISOString().replace(/T.*$/, '') + 'T12:00:00'
    }
]

export default {
    components: {
        FullCalendar, // make the <FullCalendar> tag available
        VueDatePicker,
        Navbar
    },
    data() {
        return {
            calendarOptions: {
                plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin, bootstrap5Plugin],
                themeSystem: 'bootstrap5',
                initialView: 'timeGridWeek',
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'timeGridWeek,timeGridDay'
                },
                initialEvents: INITIAL_EVENTS, // alternatively, use the `events` setting to fetch from a feed
                editable: true,
                selectable: true,
                selectMirror: true,
                dayMaxEvents: true,
                weekends: true,
                select: this.handleDateSelect,
                eventClick: this.handleEventClick,
                eventsSet: this.handleEvents,
                nowIndicator: true
            },
            selected: {
                startTime: '',
                endTime: '',
                typeOfEvent: '',
                township: ''
            },
            calendar: null,
            locations: [
                'Orchard Road',
                'Sentosa',
                'Marina Bay',
                'Chinatown',
                'Little India',
                'Jurong East'
            ]
        }
    },
    methods: {
        handleWeekendsToggle() {
            this.calendarOptions.weekends = !this.calendarOptions.weekends // update a property
        },
        handleDateSelect(selectInfo) {
            console.log(selectInfo)
            let modal = new Modal('#createEventForm')
            modal.show()
            let calendarApi = selectInfo.view.calendar
            calendarApi.unselect() // clear date selection
            this.selected.startTime = selectInfo.startStr
            this.selected.endTime = selectInfo.endStr
            this.calendar = calendarApi
        },
        handleEventClick(clickInfo) {
            if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
                clickInfo.event.remove()
            }
        },
        handleEvents(events) {
            this.currentEvents = events
        },
        handleEventTypeSelect(event) {
            this.selected.typeOfEvent = event.target.value
        },
        handleTownshipSelect(event) {
            this.selected.township = event.target.value
        },
        async createEvent() {
            if (this.calendar) {
                this.calendar.addEvent({
                    title: document.getElementById('eventName').value,
                    start: this.selected.startTime,
                    end: this.selected.endTime
                })

                await axios
                    .post(
                        'http://localhost:5000/event',
                        {
                            eventName: document.getElementById('eventName').value,
                            eventLocation: 'Garden of Eden',
                            start: this.selected.startTime,
                            end: this.selected.endTime
                        },
                        {
                            headers: {}
                        }
                    )
                    .then((response) => {
                        console.log(response)
                        let modal = Modal.getInstance(document.getElementById('createEventForm'))
                        modal.hide()
                    })
            }
        }
    }
}
</script>
<template>
    <div class="container">
        <FullCalendar :options="calendarOptions">
            <template v-slot:eventContent="arg">
                <b>{{ arg.timeText }}</b>
                <br />
                <p>{{ arg.event.title }}</p>
            </template></FullCalendar
        >
        <!-- Modal -->
        <div
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
        </div>
    </div>
</template>
