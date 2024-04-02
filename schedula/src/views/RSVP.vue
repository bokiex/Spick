<script setup>
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'
import axios from 'axios'
import { onMounted, ref, toRaw } from 'vue'
import {
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogOverlay,
    DialogPortal,
    DialogRoot,
    DialogTitle,
    DialogTrigger,
    Separator
} from 'radix-vue'
import Button from '@/components/Button.vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const eventurl = 'http://localhost:8100/event/'
const rsvpurl = 'http://localhost:8201/rsvp/'

// eventID placeholder
const userID = localStorage.getItem('userID')

const vuecal = ref()
const event_id = route.params.id
var timeout = ref(null)
var invited = false
var event = null
var minDate = ref(null)
var maxDate = ref(null)
var valid = ref(null)
var online = ref(null)

onMounted(() => {
    try {
    axios.get(eventurl.concat(event_id))
        .then((response) => {
            online = true
            event = response.data
            console.log(event)
            if (event.detail !== undefined) {
                valid = false
            }
            else {
                valid = true
                var startdate = new Date(Date.parse(event.datetime_start))
                var enddate = new Date(Date.parse(event.datetime_end))
                minDate = startdate.getFullYear()+'-'+(startdate.getMonth()+1)+'-'+startdate.getDate()
                maxDate = enddate.getFullYear()+'-'+(enddate.getMonth()+1)+'-'+enddate.getDate()
                timeout.value = event.time_out
                for (var user of event.invitees) {
                    
                    if (user.user_id == userID) {
                     
                        if(user.status === null){
                            console.log('invited')
                            invited = true
                        }
                        else if (user.status === 'Y'){
                            invited = 'Y'
                        }
                        else if (user.status === 'N'){
                            invited = 'N'
                        }
                    }
                }
            }
        })}
        catch{
            online = false
        }
})

// Get the Monday of the real time current week.
function previousFirstDayOfWeek() {
    return new Date(new Date().setDate(new Date().getDate() - ((new Date().getDay() + 6) % 7)))
}
function sendDecline() {
    var url = rsvpurl.concat('decline')
    var data = {
        user_id: userID,
        event_id: event_id
    }
    console.log(data)
    axios.post(url, data).then(function (response) {
        router.push({path : '/'})
    })
}
function exit(){
    router.push({path : '/'})
}
function sendAccept() {
    var url = rsvpurl.concat('accept')
    var events = getEvents()
    var data = {
        user_id: userID,
        event_id: event_id,
        sched_list: events
    }
    console.log(data)
    axios.post(url, data).then(function (response) {
        console.log("success")
        router.push({path : '/'})
    })
}
function getEvents() {
    console.log(vuecal.value.mutableEvents)
    var events = toRaw(vuecal.value.mutableEvents)
    
    var result = []
    
    for (var timeslot of events) {
        var event = {
            
            event_id: event_id,
            user_id: userID,
            start_time: timeslot.start
                .format('YYYY-MM-DD')
                .concat('T', timeslot.start.formatTime('HH:mm:00')),
            end_time: timeslot.end
                .format('YYYY-MM-DD')
                .concat('T', timeslot.end.formatTime('HH:mm:00'))
        }
        result.push(event)
        
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

// code
</script>

<template>
    <div class="m-auto relative w-full h-screen space-y-6 sm:w-[450px]">
        <div class="my-10 relative h-[700px] space-y-6">
            <div class="container p-4" v-if="online === false">
                <div class="row justify-content-center">
                    <!-- Form Start -->
                    <div class="form-container" style="position: relative">
                        <div class="center" style="text-align: center">
                            <div style="text-align: center">
                                <h1 class="header form-input" style="font-size: x-large">
                                    Unable to access event information
                                </h1>
                                <router-link class="btn exit" type="button" :to="`/`">
                                    Home
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container p-4" v-else-if="valid === false">
                <div class="row justify-content-center">
                    <!-- Form Start -->
                    <div class="form-container" style="position: relative">
                        <div class="center" style="text-align: center">
                            <div style="text-align: center">
                                <h1 class="header form-input" style="font-size: x-large">
                                    Event code is invalid
                                </h1>
                                <router-link class="btn exit" type="button" :to="`/`">
                                    Home
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container p-4" v-else-if="timeout === null">
                <div class="row justify-content-center">
                    <!-- Form Start -->
                    <div class="form-container" style="position: relative">
                        <div class="center" style="text-align: center">
                            <div style="text-align: center">
                                <h1 class="header form-input" style="font-size: x-large">
                                    Event signup period is over
                                </h1>
                                <router-link class="btn exit" type="button" :to="`/`">
                                    Home
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container p-4" v-else-if="invited === false">
                <div class="row justify-content-center">
                    <!-- Form Start -->
                    <div class="form-container" style="position: relative">
                        <div class="center" style="text-align: center">
                            <div style="text-align: center">
                                <h1 class="header form-input" style="font-size: x-large">
                                    You are not invited
                                </h1>
                                <router-link class="btn exit" type="button" :to="`/`">
                                    Home
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container p-4" v-else-if="invited === 'Y' || invited === 'N'">
                <div class="row justify-content-center">
                    <!-- Form Start -->
                    <div class="form-container" style="position: relative">
                        <div class="center" style="text-align: center">
                            <div style="text-align: center">
                                <h1 class="header form-input" style="font-size: x-large">
                                    You have already responded
                                </h1>
                                <router-link class="btn exit" type="button" :to="`/`">
                                    Home
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <form class="form" v-else>
                <div class="h-full">
                    <!-- Content omitted for brevity -->
                    <div class="space-y-6">
                        <div>
                            <h3 class="text-lg font-medium">Event Invitation</h3>
                            <p class="text-sm text-muted-foreground">
                                You have been invited to attend
                            </p>
                        </div>
                        <Separator class="shrink-0 bg-border h-px w-full" />
                        <div>
                            <h3 class="text-lg font-medium">Date and time.</h3>
                            <p class="text-sm text-muted-foreground">
                                Select the date and time you are available.
                            </p>
                        </div>
                    </div>
                    <!-- Step 1 start -->
                </div>

                <!-- Step 1 end -->
                <!-- Step 2 start -->

                <div class="h-[500px]">
                    <VueCal id="calendar" ref="vuecal" :time-from="0 * 60" :time-to="24 * 60"
                        :disable-views="['years', 'year']" hide-view-selector resize-x :editable-events="{
                title: false,
                drag: false,
                resize: true,
                delete: true,
                create: true
            }" :snap-to-time="15" :events="events" :min-date="minDate" :max-date="maxDate"
                        :selected-date="minDate">
                    </VueCal>
                </div>

                <!-- Step 2 end -->
                <!-- Step 3 Start -->
                <div>
                    <div class="flex justify-between m-5">
                        <DialogRoot>
                            <DialogTrigger>
                                <Button type="button" @click = "sendDecline">Decline</Button>
                            </DialogTrigger>

                            <DialogTrigger>
                                <Button type="button" @click = "sendAccept"> Submit </Button>
                            </DialogTrigger>
                            <DialogPortal>
                                <DialogOverlay
                                    class="fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
                                <DialogContent
                                    class="data-[state=open]:animate-contentShow fixed top-[50%] left-[50%] max-h-[85vh] w-[90vw] max-w-[450px] translate-x-[-50%] translate-y-[-50%] rounded-[6px] bg-white p-[25px] shadow-[hsl(206_22%_7%_/_35%)_0px_10px_38px_-10px,_hsl(206_22%_7%_/_20%)_0px_10px_20px_-15px] focus:outline-none z-[100]">
                                    <DialogTitle class="text-mauve12 m-0 text-[17px] font-semibold">
                                        Thank you!
                                    </DialogTitle>
                                    <DialogDescription class="text-mauve11 mt-[10px] mb-5 text-[15px] leading-normal">
                                        You have submitted your availability.
                                    </DialogDescription>

                                    <div class="mt-[25px] flex justify-end">
                                        <DialogClose as-child>
                                            <button variant="outline" @click = "exit()"
                                                class="inline-flex h-[35px] items-center justify-center rounded-[4px] px-[15px] font-semibold leading-none focus:shadow-[0_0_0_2px] focus:outline-none">
                                                Exit
                                            </button>
                                        </DialogClose>
                                    </div>
                                    <DialogClose
                                        class="text-grass11 hover:bg-green4 focus:shadow-green7 absolute top-[10px] right-[10px] inline-flex h-[25px] w-[25px] appearance-none items-center justify-center rounded-full focus:shadow-[0_0_0_2px] focus:outline-none"
                                        aria-label="Close">
                                        <Icon icon="lucide:x" />
                                    </DialogClose>
                                </DialogContent>
                            </DialogPortal>
                        </DialogRoot>
                    </div>
                </div>

                <!-- Step 3 end -->
            </form>
        </div>
    </div>
</template>
<style>
.vuecal__event {
    background-color: rgba(76, 172, 175, 0.35);
}
</style>
<style scoped language="scss">
.center {
    margin: auto;
    width: 50%;
    padding: 10px;
}

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
