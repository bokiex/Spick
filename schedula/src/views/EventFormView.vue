<script setup>
import VueDatePicker from '@vuepic/vue-datepicker'
import Button from '@/components/Button.vue'
import { RadioGroupIndicator, RadioGroupItem, RadioGroupRoot, Separator } from 'radix-vue'
import { ref, computed } from 'vue'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import ShowAttendees from '@/components/ShowAttendees.vue'
import Avatar from '@/components/Avatar.vue'
import * as z from 'zod'
import { CircleX } from 'lucide-vue-next'
import Label from '@/components/Label.vue'

const userID = localStorage.getItem('userID')
const currentStep = ref(1)
const steps = [
    { id: 1, label: 'Step 1', description: 'Details' },
    { id: 2, label: 'Step 2', description: 'Type' },
    { id: 3, label: 'Step 3', description: 'Date & Time' },
    { id: 4, label: 'Step 4', description: 'End' }
]

const event_detail_schema = toTypedSchema(
    z.object({
        event_name: z.string().min(1, { message: 'Event name is required' }),
        event_desc: z.string().min(1, { message: 'Event description is required' })
        // invitees: z.array(z.string()).min(1, { message: 'At least one invitee is required' })
    })
)

const event_type_schema = toTypedSchema(
    z.object({
        type: z.string().min(1, { message: 'Event type is required' })
    })
)

const date_time_schema = toTypedSchema(
    z.object({
        start_time: z.string().min(1, { message: 'Start time is required' }),
        end_time: z.string().min(1, { message: 'End time is required' })
    })
)

const schemas = [event_detail_schema, event_type_schema, date_time_schema]

const { handleSubmit, validate } = useForm({
    validationSchema: computed(() => schemas[currentStep.value - 1]),
    initialValues: {
        event_name: '',
        event_desc: '',
        image: '',
        invitees: [],
        type: '',
        start_time: '',
        end_time: ''
    }
})

const { value: event_name } = useField('event_name')
const { value: event_desc } = useField('event_desc')
const { value: image } = useField('image')
const { value: invitees } = useField('invitees')
const { value: type } = useField('type')
const { value: start_time } = useField('start_time')
const { value: end_time } = useField('end_time')

const nextStep = async () => {
    if (currentStep.value < steps.length) {
        currentStep.value++
        console.log(currentStep)
    }
}
function prevStep() {
    if (currentStep.value > 1) {
        currentStep.value--
    }
}

function previewFile(event) {
    const file = image.value
    console.log(event.target.files[0])
    const reader = new FileReader()
    reader.onloadend = () => {
        selected.value = reader.result
    }
    if (file) {
        reader.readAsDataURL(file)
    }
}

function submitForm() {
    // Make sure all steps are validated before submitting
    if (currentStep.value === 3) {
        console.log(
            event_name.value,
            event_desc.value,
            invitees.value,
            type.value,
            start_time.value,
            end_time.value
        )
        currentStep++
        // Send the form data to your backend
        create_event = {
            event_name: event_name.value,
            event_desc: event_desc.value,
            invitees: invitees.value,
            type: type.value,
            start_time: start_time.value,
            end_time: end_time.value
        }
    }
}

const friends = [
    {
        name: 'Colm Tuite',
        avatar: 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80'
    },
    {
        name: 'Adam Wathan',
        avatar: 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80'
    },
    {
        name: 'Sarah Drasner',
        avatar: 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80'
    },
    {
        name: 'Cassidy Williams',
        avatar: 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80'
    },
    {
        name: 'Evan You',
        avatar: 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80'
    },
    {
        name: 'John Otander',
        avatar: 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80'
    },
    {
        name: 'Sarah Dayan',
        avatar: 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80'
    },
    {
        name: 'Tim Neutkens',
        avatar: 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80'
    },
    {
        name: 'Chris Biscardi',
        avatar: 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80'
    }
]
const selected_friend = ref(friends[0])
</script>
<template>
    <Navbar />
    <div class="flex flex-wrap justify-around gap-4 items-center p-4">
        <div class="row justify-content-center">
            <!-- Form Start -->
            <div class="form-container">
                <!-- Sidebar start -->
                <div class="form-sidebar">
                    <div class="step" :class="{ active: currentStep == 1 }">
                        <div class="circle">1</div>
                        <div class="step-content">
                            <span>Step 1</span>
                            <b>Details</b>
                        </div>
                    </div>
                    <div class="step" :class="{ active: currentStep == 2 }">
                        <div class="circle">2</div>
                        <div class="step-content">
                            <span>Step 2</span>
                            <b>Type</b>
                        </div>
                    </div>
                    <div class="step" :class="{ active: currentStep == 3 }">
                        <div class="circle">3</div>
                        <div class="step-content">
                            <span>Step 3</span>
                            <b>Date & Time</b>
                        </div>
                    </div>
                    <div class="step" :class="{ active: currentStep == 4 }">
                        <div class="circle">4</div>
                        <div class="step-content">
                            <span>Step 4</span>
                            <b>End</b>
                        </div>
                    </div>
                </div>
                <!-- Sidebar end -->
                <!-- Step 1 start -->
                <form class="form" @submit.prevent="nextStep">
                    <div v-if="currentStep === 1" class="stp step-1">
                        <!-- Content omitted for brevity -->
                        <div class="space-y-6">
                            <div>
                                <h3 class="text-lg font-medium">Event Details</h3>
                                <p class="text-sm text-muted-foreground">
                                    Please provide the event title, event description, and
                                    attendees.
                                </p>
                            </div>
                            <Separator class="shrink-0 bg-border h-px w-full" />
                            <div class="space-y-2">
                                <Label for="event_name">Event Title</Label>
                                <input
                                    name="event_name"
                                    required
                                    id="event_name"
                                    v-model="event_name"
                                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    placeholder="e.g. ESD Meeting"
                                />
                            </div>
                            <div class="space-y-2">
                                <Label for="event_desc">Event Description</Label>
                                <input
                                    name="event_desc"
                                    required
                                    id="event_desc"
                                    v-model="event_desc"
                                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    placeholder="e.g. Deployment of site"
                                />
                            </div>
                            <div class="space-y-2">
                                <Label for="image">Image</Label>
                                <input
                                    name="image"
                                    type="file"
                                    @change="(event) => previewFile(event)"
                                    required
                                    id="image"
                                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    placeholder="e.g. Deployment of site"
                                />
                            </div>
                            <div class="space-y-2">
                                <Label for="invitees">Event Attendees</Label>

                                <ShowAttendees
                                    @update:selectedFriend="
                                        (selected_friend) => invitees.push(selected_friend)
                                    "
                                    :selected_friend="selected_friend"
                                    :friends="friends"
                                />
                            </div>

                            <div class="flex gap-5">
                                <div
                                    v-for="(invitee, index) in invitees"
                                    :key="index"
                                    class="relative"
                                >
                                    <Avatar />

                                    <CircleX
                                        class="absolute -top-2 -right-2 cursor-pointer hover:text-destructive transition-colors duration-150"
                                        @click="() => invitees.splice(index, 1)"
                                    />
                                </div>
                            </div>

                            <div class="flex justify-end">
                                <Button @click="nextStep" type="button"> Next Step </Button>
                            </div>
                        </div>
                    </div>

                    <!-- Step 1 end -->
                    <!-- Step 2 start -->
                    <div v-if="currentStep === 2" class="stp step-2">
                        <div class="space-y-6">
                            <div>
                                <h3 class="text-lg font-medium">Pick the type of event.</h3>
                                <p class="text-sm text-muted-foreground">
                                    Select the type to get a venue recommendation.
                                </p>
                            </div>
                            <Separator class="shrink-0 bg-border h-px w-full" />

                            <RadioGroupRoot default-value="school" v-model="type">
                                <div class="grid grid-row-3 gap-4">
                                    <Label
                                        for="school"
                                        class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                                    >
                                        <RadioGroupItem
                                            id="school"
                                            value="school"
                                            class="peer sr-only aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                        >
                                            <RadioGroupIndicator
                                                class="flex items-center justify-center"
                                            >
                                                <Circle
                                                    class="h-2.5 w-2.5 fill-current text-current"
                                                />
                                            </RadioGroupIndicator>
                                        </RadioGroupItem>

                                        <p class="text-sm font-medium leading-none">
                                            School Meeting
                                        </p>
                                        <p class="text-sm text-muted-foreground">
                                            School project meeting done in school.
                                        </p>
                                    </Label>
                                    <Label
                                        for="personal"
                                        class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                                    >
                                        <RadioGroupItem
                                            id="personal"
                                            value="personal"
                                            class="peer sr-only aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                        >
                                            <RadioGroupIndicator
                                                class="flex items-center justify-center"
                                            >
                                                <Circle
                                                    class="h-2.5 w-2.5 fill-current text-current"
                                                />
                                            </RadioGroupIndicator>
                                        </RadioGroupItem>
                                        <p class="text-sm font-medium leading-none">Personal</p>
                                        <p class="text-sm text-muted-foreground">
                                            Meeting with friends
                                        </p>
                                    </Label>
                                    <Label
                                        for="celebration"
                                        class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                                    >
                                        <RadioGroupItem
                                            id="celebration"
                                            value="celebration"
                                            class="peer sr-only aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                        >
                                            <RadioGroupIndicator
                                                class="flex items-center justify-center"
                                            >
                                                <Circle
                                                    class="h-2.5 w-2.5 fill-current text-current"
                                                />
                                            </RadioGroupIndicator>
                                        </RadioGroupItem>
                                        <p class="text-sm font-medium leading-none">Celebrations</p>
                                        <p class="text-sm text-muted-foreground">
                                            Custom celebrations such as birthday parties.
                                        </p>
                                    </Label>
                                </div>
                            </RadioGroupRoot>
                        </div>
                        <div class="m-5">
                            <Button variant="outline" @click="prevStep" type="button"
                                >Go Back</Button
                            >
                            <Button @click="nextStep" type="button" style="float: right">
                                Next Step
                            </Button>
                        </div>
                    </div>
                    <!-- Step 2 end -->
                    <!-- Step 3 Start -->
                    <div v-if="currentStep === 3" class="stp step-3">
                        <div class="space-y-6">
                            <div>
                                <h3 class="text-lg font-medium">Pick the type of event.</h3>
                                <p class="text-sm text-muted-foreground">
                                    Select the type to get a venue recommendation.
                                </p>
                            </div>
                            <Separator class="shrink-0 bg-border h-px w-full" />

                            <div class="space-y-2">
                                <Label for="start_time">Start Time</Label>
                                <VueDatePicker v-model="start_time" time-picker-inline />
                            </div>
                            <div class="space-y-2">
                                <Label for="end_time">End Time</Label>
                                <VueDatePicker v-model="end_time" time-picker-inline />
                            </div>
                            <div class="space-y-2">
                                <Label for="time_out">Time Out</Label>
                                <VueDatePicker v-model="time_out" time-picker-inline />
                            </div>
                            <div class="space-y-2">
                                <div class="label">
                                    <label for="township">Prefered Area</label>
                                </div>
                                <input
                                    required
                                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    type="text"
                                    v-model="township"
                                    id="township"
                                    placeholder="e.g. Marina Bay"
                                />
                            </div>
                        </div>
                        <div class="m-5">
                            <Button variant="outline" @click="prevStep" type="button"
                                >Go Back</Button
                            >
                            <Button @click="submitForm" type="button" style="float: right">
                                Submit
                            </Button>
                        </div>
                    </div>
                    <!-- Step 3 End-->
                    <!-- Step 4 start -->
                    <div v-if="currentStep === 4" class="stp step-4">
                        <div class="header">
                            <h1 class="title">Thank you!</h1>
                            <p class="exp">
                                Your event invite has been created and sent to the invitees.
                            </p>
                        </div>
                        <Button class="mt-5 mx-auto">Return</Button>
                    </div>
                    <!-- Step 4 end -->
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
nav {
    border-radius: 15px;
}

.navbar-nav .nav-link:hover {
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.5); /* Add shadow effect on hover */
    border-radius: 15px;
}

.navbar-nav .nav-link.active,
.navbar-nav .nav-link:active {
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.5); /* Add shadow effect when clicked */
    border-radius: 15px;
}

.navbar-nav .nav-item {
    margin-right: 20px; /* Adjust margin as needed */
}

:root {
    --Marine-blue: hsl(213, 96%, 18%);
    --Purplish-blue: hsl(243, 100%, 62%);
    --Pastel-blue: hsl(228, 100%, 84%);
    --Light-blue: hsl(206, 94%, 87%);
    --Strawberry-red: hsl(354, 84%, 57%);

    --Cool-gray: hsl(231, 11%, 63%);
    --Light-gray: hsl(229, 24%, 87%);
    --Magnolia: hsl(217, 100%, 97%);
    --Alabaster: hsl(231, 100%, 99%);
    --White: hsl(0, 0%, 100%);
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
    width: 900px;
    background-color: hsl(0, 0%, 100%);
    border-radius: 1rem;
    box-shadow: 0px 0px 1px black;
    height: 600px;
}
.form-sidebar {
    padding: 2rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    background-color: lightpink;
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
    margin: 0px;
    color: hsl(354, 84%, 57%);
    font-size: 0.9rem;
    font-weight: 700;
}

form .error.show {
    display: flex;
    justify-content: end;
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
    background-color: var(--Magnolia);
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
    background-color: var(--Magnolia);
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
        height: 750px; /* Allow height to adjust to content */
        padding: 0; /* Remove padding if needed */
    }

    /* Adjust the sidebar to display horizontally */
    .form-sidebar {
        flex-direction: row;
        justify-content: center;
        padding: 10; /* Remove padding if needed */
        width: 100%; /* Full width */
        margin-bottom: 1rem; /* Add some space between the steps and the form */
        border-top-right-radius: 1rem; /* Add this line to round the top-right corner */
        border-bottom-right-radius: 1rem; /* Add this line to round the bottom-right corner when stacked */
    }

    /* Hide all step content, only show the circle/number */
    .form-sidebar .step .step-content {
        display: none;
    }

    /* Align the circles horizontally */
    .form-sidebar .step {
        margin-right: 0.5rem; /* Space out the circles */
    }

    .stp {
        flex: 1;
    }
}
</style>
