<script>
import VueCal from 'vue-cal';
import 'vue-cal/dist/vuecal.css';
import axios from 'axios';
import { isProxy, toRaw } from 'vue';


// eventID placeholder
var eventID = 0
export default {
    components: { VueCal },
    userID: localStorage.getItem('userID'),
    data() {
        return {
            eventToken: "",
            currentStep: 1,
            steps: [
                { id: 1, label: 'Step 1', description: 'Acceptance' },
                { id: 2, label: 'Step 2', description: 'Availability' },
                { id: 3, label: 'Step 3', description: 'End' }
            ]
        }
    },
    created() {
        this.eventToken = this.$route.params.eventToken;
        console.log(this.eventToken)
    },
    computed: {
        // Get the Monday of the real time current week.
        previousFirstDayOfWeek() {
            return new Date(new Date().setDate(new Date().getDate() - (new Date().getDay() + 6) % 7))
        }
    },
    methods: {
        nextStep() {
            if (this.currentStep < this.steps.length) this.currentStep++
        },
        prevStep() {
            if (this.currentStep > 1) this.currentStep--
        },
        sendAccept() {
            this.nextStep()
            var url = "http://localhost:5100/rsvp/accept"
            var events = this.getEvents()
            var data = {
                "userID": this.userID,
                "token": this.eventToken,
                "eventID": eventID,
                "sched_list": events
            }
            console.log(data)
            axios.post(
                url,
                data
            )
                .then(function (response) {
                    this.$route.push({ path: '/calendarview' })
                })
        },
        getEvents() {
            var events = toRaw(this.$refs.vuecal.mutableEvents)
            var result = []
            var index = 0
            for (var timeslot of events) {
                var event = {
                    scheduleID: this.index,
                    eventID: this.eventID,
                    userID: this.userID,
                    start_time: timeslot.start.format('YYYY-MM-DD').concat("T", timeslot.start.formatTime('HH:mm:00')),
                    end_time: timeslot.end.format('YYYY-MM-DD').concat("T", timeslot.end.formatTime('HH:mm:00'))
                }
                result.push(event)
                index++
            }
            return result
        }
        // onEvent (event, deleteEventFunction) {
        //   var events = toRaw(this.$refs.vuecal.mutableEvents)
        //   var start = event.start
        //   var end = event.end
        //   for (var timeslot of events){
        //     if (timeslot.end >= event.start && event.start >= timeslot.start){
        //       return false
        //     }
        //   }
        // return event}

    }
}
// code
</script>

<template>
    <div class="container p-4">
        <div class="row justify-content-center">
            <!-- Form Start -->
            <div class="form-container">
                <!-- Sidebar start -->
                <div class="form-sidebar">
                    <div class="step" :class="{ active: currentStep == 1 }">
                        <div class="circle">1</div>
                        <div class="step-content">
                            <span>Step 1</span>
                            <b>Acceptance</b>
                        </div>
                    </div>
                    <div class="step" :class="{ active: currentStep == 2 }">
                        <div class="circle">2</div>
                        <div class="step-content">
                            <span>Step 2</span>
                            <b>Availability</b>
                        </div>
                    </div>
                    <div class="step" :class="{ active: currentStep == 3 }">
                        <div class="circle">3</div>
                        <div class="step-content">
                            <span>Step 3</span>
                            <b>End</b>
                        </div>
                    </div>
                </div>
                <!-- Sidebar end -->
                <!-- Step 1 start -->
                <div class="stp step-1" v-if="currentStep === 1">
                    <div class="header">
                        <h1 class="title">Event Invitation</h1>
                        <p class="exp">
                            You have been invited to attend this event.
                        </p>
                    </div>
                    <div class="btns">
                        <button class="decline" @click="prevStep" type="submit">Decline</button>
                        <button class="next-stp" @click="nextStep" type="button" style="float: right">Accept</button>
                    </div>
                </div>
                <!-- Step 1 end -->
                <!-- Step 2 start -->
                <div class="stp step-2" v-if="currentStep === 2">
                    <div class="header">
                        <h1 class="title">Date and time.</h1>
                        <p class="exp">Select the date and time you are available.</p>
                    </div>
                    <div style="width:100%;height:65%;float:right;">
                        <vue-cal id="calendar" ref="vuecal" :time-from="0 * 60" :time-to="24 * 60"
                            :disable-views="['years', 'year']" hide-view-selector resize-x
                            :editable-events="{ title: false, drag: false, resize: true, delete: true, create: true }"
                            :snap-to-time="15" :events="events" class="vuecal--full-height-delete"></vue-cal>
                    </div>

                    <div class="btns">
                        <button class="prev-stp" @click="prevStep" type="button">Go Back</button>
                        <button class="next-stp" @click="sendAccept" type="submit" style="float: right">
                            Next Step
                        </button>
                    </div>
                </div>
                <!-- Step 2 end -->
                <!-- Step 3 Start -->
                <div class="stp step-3" v-if="currentStep === 3">
                    <div class="header">
                        <h1 class="title">Thank you!</h1>
                        <p class="exp">
                            You have submitted your availability.
                        </p>
                    </div>
                    <div class="btns">
                        <button class="prev-stp" @click="prevStep" type="button">Go Back</button>
                        <button class="exit" id="exit" @click="exit" style="float: right">Exit</button>
                    </div>
                </div>
                <!-- Step 3 end -->
            </div>
        </div>
    </div>


</template>
<style>
.vuecal__event {
    background-color: rgba(76, 172, 175, 0.35);
}
</style>
<style scoped language="scss">
nav {
    border-radius: 15px;
}

.navbar-nav .nav-link:hover {
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
    /* Add shadow effect on hover */
    border-radius: 15px;
}

.navbar-nav .nav-link.active,
.navbar-nav .nav-link:active {
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
    /* Add shadow effect when clicked */
    border-radius: 15px;
}

.navbar-nav .nav-item {
    margin-right: 20px;
    /* Adjust margin as needed */
}

* {
    font-family: 'Poppins', sans-serif;
}

.hidden {
    display: none;
}

img {
    max-width: 100%;
}

.form-container {
    display: flex;
    padding: 1rem;
    justify-content: center;
    width: 100%;
    background-color: hsl(0, 0%, 100%);
    border-radius: 1rem;
    box-shadow: 0px 0px 1px black;
    height: 578px;
}

.form-sidebar {
    padding: 2rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    background-color: black;
    border-top-left-radius: 1rem;
    border-bottom-left-radius: 1rem;
    width: 250px;
}

.circle {
    width: 40px;
    height: 40px;
    border: 2px solid hsl(0, 0%, 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: hsl(0, 0%, 100%);
    font-weight: 700;
}

.active .circle {
    background-color: hsl(206, 94%, 87%) !important;
    color: hsl(213, 96%, 18%) !important;
}

.err {
    border: 2px solid hsl(354, 84%, 57%) !important;
}

.step {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.step-content {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.step-content span {
    text-transform: uppercase;
    color: hsl(229, 24%, 87%);
    font-size: 13px;
}

.step-content b {
    text-transform: uppercase;
    color: hsl(0, 0%, 100%);
}

.stp {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.stp .header {
    margin-bottom: auto;
    padding-top: 2rem;
    line-height: 2.5rem;
}

.header .title {
    color: hsl(213, 96%, 18%);
}

.header .exp {
    color: hsl(231, 11%, 63%);
}

.next-stp {
    margin-top: 1rem;
    margin-bottom: 2rem;
    margin-left: auto;
    border: none;
    padding: 1rem 2rem;
    border-radius: 7px;
    background-color: hsl(213, 96%, 18%);
    color: white;
    cursor: pointer;
}

.exit {
    margin-top: 1rem;
    margin-bottom: 2rem;
    margin-left: auto;
    border: none;
    padding: 1rem 2rem;
    border-radius: 7px;
    background-color: hsl(213, 96%, 18%);
    color: white;
    cursor: pointer;
}

.prev-stp {
    margin-top: 1rem;
    margin-bottom: 2rem;
    border: none;
    font-weight: 700;
    background-color: transparent;
    padding: 1rem 2rem;
    border-radius: 7px;
    color: hsl(231, 11%, 63%);
    cursor: pointer;
}

.decline {
    margin-top: 1rem;
    margin-bottom: 2rem;
    border: none;
    font-weight: 700;
    background-color: transparent;
    padding: 1rem 2rem;
    border-radius: 7px;
    color: hsl(231, 11%, 63%);
    cursor: pointer;
}

/* STEP 1 */
.step-1 {
    display: flex;
    width: 80%;
    margin-left: 1rem;
    margin-right: 1rem;
}

.step-1 form {
    display: flex;
    flex-direction: column;
    flex: 1;
    justify-content: center;
    gap: 1rem;
}

.label {
    color: hsl(213, 96%, 18%);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.step-1 form input {
    padding: 1rem;
    border: 1px solid hsl(231, 11%, 63%);
    border-radius: 7px;
    font-weight: 500;
    font-size: 1rem;
}

.step-1 form input:focus {
    outline-color: hsl(243, 100%, 62%);
}

form input::placeholder {
    font-weight: 500;
    font-size: 1rem;
    font-family: inherit;
}

form .error {
    display: none;
    color: hsl(354, 84%, 57%);
    font-size: 0.9rem;
    font-weight: 700;
}

/* STEP 2 */
.step-2 {
    width: 80%;
    margin-left: 1rem;
    margin-right: 1rem;
}

.step-2 form {
    display: flex;
    flex-direction: column;
    flex: 1;
    justify-content: center;
    gap: 1.5rem;
}

.box {
    border: 1px solid hsl(231, 11%, 63%);
    border-radius: 10px;
    padding: 1rem;
    display: flex;
    align-items: center;
    cursor: pointer;
}

.description {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    margin-left: 12px;
}

.ad-selected {
    border: 1px solid hsl(243, 100%, 62%);
    background-color: hsl(217, 100%, 97%);
}

.step-2 form input {
    accent-color: hsl(243, 100%, 62%);
    transform: scale(1.3);
    user-select: none;
}

.description label {
    color: hsl(213, 96%, 18%);
    font-weight: 700;
    user-select: none;
}

.description small {
    color: hsl(231, 11%, 63%);
    font-weight: 700;
}

.price {
    color: hsl(243, 100%, 62%);
}

/* STEP 3 */
.step-3 {
    width: 80%;
    margin-left: 1rem;
    margin-right: 1rem;
}

/* STEP 4 */
.step-4 {
    align-items: center;
    width: 80%;
    text-align: center;
    justify-content: center;
    margin: auto;
}

.step-4 button {
    display: none;
}

/* SWITCH classes */
.switcher {
    background-color: hsl(217, 100%, 97%);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem;
    margin-bottom: 5rem;
    justify-content: center;
}

.switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 24px;
}

/* Hide default HTML checkbox */
.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

@media (max-width: 600px) {

    /* Stack sidebar above the form content on small screens */
    .form-container {
        flex-direction: column;
        align-items: center;
        height: 750px;
        /* Allow height to adjust to content */
        padding: 0;
        /* Remove padding if needed */
    }

    /* Adjust the sidebar to display horizontally */
    .form-sidebar {
        flex-direction: row;
        justify-content: center;
        padding: 10;
        /* Remove padding if needed */
        width: 100%;
        /* Full width */
        margin-bottom: 1rem;
        /* Add some space between the steps and the form */
        border-top-right-radius: 1rem;
        /* Add this line to round the top-right corner */
        border-bottom-right-radius: 1rem;
        /* Add this line to round the bottom-right corner when stacked */
    }

    /* Hide all step content, only show the circle/number */
    .form-sidebar .step .step-content {
        display: none;
    }

    /* Align the circles horizontally */
    .form-sidebar .step {
        margin-right: 0.5rem;
        /* Space out the circles */
    }

    .stp {
        flex: 1;
    }
}
</style>