<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import bootstrap5Plugin from '@fullcalendar/bootstrap5'
import { Modal } from 'bootstrap'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
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
        VueDatePicker
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
                endTime: ''
            }
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
            calendarApi.addEvent({
                id: 1,
                title: 'dynamic event',
                start: selectInfo.startStr,
                end: selectInfo.endStr,
                allDay: selectInfo.allDay
            })
        },
        handleEventClick(clickInfo) {
            if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
                clickInfo.event.remove()
            }
        },
        handleEvents(events) {
            this.currentEvents = events
        }
    }
}
</script>
<template>
    <div class="container">
        <FullCalendar :options="calendarOptions">
            <template v-slot:eventContent="arg">
                <b>{{ arg.timeText }}</b>
                <i>{{ arg.event.title }}</i>
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
                        <button type="button" class="btn btn-primary">Create</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
