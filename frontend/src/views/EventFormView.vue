<script setup>
import VueDatePicker from '@vuepic/vue-datepicker'
import Button from '@/components/Button.vue'
import {
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogOverlay,
    DialogPortal,
    DialogRoot,
    DialogTitle,
    DialogTrigger,
    ProgressIndicator,
    ProgressRoot,
    RadioGroupIndicator,
    RadioGroupItem,
    RadioGroupRoot,
    Separator
} from 'radix-vue'
import { ref, computed, onMounted } from 'vue'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import ShowAttendees from '@/components/ShowAttendees.vue'
import Avatar from '@/components/Avatar.vue'
import * as z from 'zod'
import { CircleX } from 'lucide-vue-next'
import Label from '@/components/Label.vue'
import router from '../router'

const event_ms = 'http://localhost:8200/create_event'
const user_ms = 'http://localhost:8101/users'

const user_id = localStorage.getItem('userID')
const friends = ref([])
const selected_friend = ref(null)
const loading = ref(true)
const error = ref(null)
onMounted(async () => {
    try {
        // Example API call - replace with your actual API call
        const data = await fetch(user_ms).then((res) => res.json())
        console.log(user_id)
        // for loop to remove the user from the list of friends
        for (let i = 0; i < data.length; i++) {
            if (data[i].user_id == user_id) {
                data.splice(i, 1)
            }
        }
        friends.value = data
        console.log(friends.value)
        selected_friend.value = friends.value[0]
    } catch (error) {
        console.error('Failed to fetch event data:', error)
    } finally {
        loading.value = false
    }
})

const currentStep = ref(0)
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
        datetime_start: z.string().min(1, { message: 'Start time is required' }),
        datetime_end: z.string().min(1, { message: 'End time is required' })
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
        township: '',
        datetime_start: '',
        datetime_end: '',
        time_out: ''
    }
})

const { value: event_name } = useField('event_name')
const { value: event_desc } = useField('event_desc')
const { value: image } = useField('image')
const { value: invitees } = useField('invitees')
const { value: type } = useField('type')
const { value: datetime_start } = useField('datetime_start')
const { value: datetime_end } = useField('datetime_end')
const { value: time_out } = useField('time_out')
const { value: township } = useField('township')

const nextStep = async () => {
    currentStep.value += 50
    console.log(currentStep)
}
function prevStep() {
    currentStep.value -= 50
}

function previewFile(event) {
    const file = event.target.files[0]

    image.value = file
    console.log(image.value)
}

async function submitForm() {
    // Make sure all steps are validated before submitting
    loading.value = true
    if (currentStep.value === 100) {
        // Send the form data to your backend
        console.log(image)
        const create_event = {
            user_id: user_id,
            event_name: event_name.value,
            event_desc: event_desc.value,
            image: image.value.name || 'None',
            invitees: invitees.value,
            type: type.value,
            township: township.value,
            datetime_start: datetime_start.value,
            datetime_end: datetime_end.value,
            time_out: time_out.value
        }
        console.log(JSON.stringify(create_event))

        const formData = new FormData()
        formData.append('event', JSON.stringify(create_event)) // eventData is your form's data as a JS object
        formData.append('file', image.value)

        try {
            const res = await fetch(event_ms, {
                method: 'POST',
                body: formData
            })

            if (!res.ok) {
                const data = await res.json()

                throw new Error(data)
            } else {
                loading.value = false
            }
        } catch (err) {
            error.value = err.message
            loading.value = false
            console.error('Error fetching data: ', error)
        }
    }
}

function viewEvents() {
    router.push({ name: 'events' })
}

function tryAgain() {
    error.value = null
}
</script>
<template>
    <div class="m-auto relative w-full h-screen space-y-6 sm:w-[450px]">
        <div class="my-10 relative h-[700px] space-y-6">
            <ProgressRoot
                v-model="currentStep"
                class="relative h-4 w-full overflow-hidden rounded-full bg-secondary"
            >
                <ProgressIndicator
                    class="h-full w-full flex-1 bg-primary transition-all"
                    :style="`transform: translateX(-${100 - (currentStep ?? 0)}%);`"
                />
            </ProgressRoot>
            <form class="form" @submit.prevent="nextStep">
                <div v-if="currentStep === 0" class="h-full">
                    <!-- Content omitted for brevity -->
                    <div class="space-y-6">
                        <div>
                            <h3 class="text-lg font-medium">Event Details</h3>
                            <p class="text-sm text-muted-foreground">
                                Please provide the event title, event description, and attendees.
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
                                class="flex flex-col items-center justify-center relative"
                            >
                                <Avatar :src="invitee.image" :name="invitee.username" />

                                <CircleX
                                    class="absolute -top-2 -right-2 cursor-pointer hover:text-destructive transition-colors duration-150"
                                    @click="() => invitees.splice(index, 1)"
                                /><span class="p-2 font-light text-xs">
                                    {{ invitee.username }}
                                </span>
                            </div>
                        </div>

                        <div class="flex justify-end">
                            <Button @click="nextStep" type="button"> Next Step </Button>
                        </div>
                    </div>
                </div>

                <!-- Step 1 end -->
                <!-- Step 2 start -->
                <div v-if="currentStep === 50" class="h-full">
                    <div class="space-y-6">
                        <div>
                            <h3 class="text-lg font-medium">Pick the type of event.</h3>
                            <p class="text-sm text-muted-foreground">
                                Select the type to get a venue recommendation.
                            </p>
                        </div>
                        <Separator class="shrink-0 bg-border h-px w-full" />

                        <RadioGroupRoot default-value="restaurant" v-model="type">
                            <div class="grid grid-row-3 gap-7 space-y-2">
                                <Label
                                    for="restaurant"
                                    class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                                >
                                    <RadioGroupItem
                                        id="restaurant"
                                        value="restaurant"
                                        class="peer sr-only aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    >
                                        <RadioGroupIndicator
                                            class="flex items-center justify-center"
                                        >
                                            <Circle class="h-2.5 w-2.5 fill-current text-current" />
                                        </RadioGroupIndicator>
                                    </RadioGroupItem>

                                    <p class="text-sm font-medium leading-none">Restaurant</p>
                                    <p class="text-sm text-muted-foreground">
                                        Recommended for a casual event.
                                    </p>
                                </Label>
                                <Label
                                    for="bar"
                                    class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                                >
                                    <RadioGroupItem
                                        id="bar"
                                        value="bar"
                                        class="peer sr-only aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    >
                                        <RadioGroupIndicator
                                            class="flex items-center justify-center"
                                        >
                                            <Circle class="h-2.5 w-2.5 fill-current text-current" />
                                        </RadioGroupIndicator>
                                    </RadioGroupItem>
                                    <p class="text-sm font-medium leading-none">Bar</p>
                                    <p class="text-sm text-muted-foreground">
                                        If you want to have a drink and have a good time
                                    </p>
                                </Label>
                                <Label
                                    for="hotel"
                                    class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                                >
                                    <RadioGroupItem
                                        id="hotel"
                                        value="hotel"
                                        class="peer sr-only aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    >
                                        <RadioGroupIndicator
                                            class="flex items-center justify-center"
                                        >
                                            <Circle class="h-2.5 w-2.5 fill-current text-current" />
                                        </RadioGroupIndicator>
                                    </RadioGroupItem>
                                    <p class="text-sm font-medium leading-none">Hotels</p>
                                    <p class="text-sm text-muted-foreground">For a formal event.</p>
                                </Label>
                                <Label
                                    for="conventioncenter"
                                    class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                                >
                                    <RadioGroupItem
                                        id="conventioncenter"
                                        value="conventioncenter"
                                        class="peer sr-only aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    >
                                        <RadioGroupIndicator
                                            class="flex items-center justify-center"
                                        >
                                            <Circle class="h-2.5 w-2.5 fill-current text-current" />
                                        </RadioGroupIndicator>
                                    </RadioGroupItem>
                                    <p class="text-sm font-medium leading-none">
                                        Convention Centers
                                    </p>
                                    <p class="text-sm text-muted-foreground">
                                        Serious and large events.
                                    </p>
                                </Label>
                            </div>
                        </RadioGroupRoot>
                    </div>
                    <div class="m-5">
                        <Button variant="outline" @click="prevStep" type="button">Go Back</Button>
                        <Button @click="nextStep" type="button" style="float: right">
                            Next Step
                        </Button>
                    </div>
                </div>
                <!-- Step 2 end -->
                <!-- Step 3 Start -->
                <div v-if="currentStep >= 66" class="">
                    <div class="space-y-6">
                        <div>
                            <h3 class="text-lg font-medium">Pick the type of event.</h3>
                            <p class="text-sm text-muted-foreground">
                                Select the type to get a venue recommendation.
                            </p>
                        </div>
                        <Separator class="shrink-0 bg-border h-px w-full" />

                        <div class="space-y-2">
                            <Label for="datetime_start">Range Start</Label>
                            <VueDatePicker v-model="datetime_start" time-picker-inline />
                        </div>
                        <div class="space-y-2">
                            <Label for="datetime_end">Range End</Label>
                            <VueDatePicker v-model="datetime_end" time-picker-inline />
                        </div>
                        <div class="space-y-2">
                            <Label for="time_out">Event Invite Expiry</Label>
                            <VueDatePicker v-model="time_out" time-picker-inline />
                        </div>
                        <div class="space-y-2">
                            <div class="label">
                                <label for="township">Preferred Area</label>
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
                    <div class="flex justify-between m-5">
                        <Button variant="outline" @click="prevStep" type="button">Go Back</Button>

                        <DialogRoot>
                            <DialogTrigger>
                                <Button @click="submitForm" type="button"> Submit </Button>
                            </DialogTrigger>
                            <DialogPortal v-if="!loading">
                                <DialogOverlay
                                    class="fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0"
                                />
                                <DialogContent
                                    class="data-[state=open]:animate-contentShow fixed top-[50%] left-[50%] max-h-[85vh] w-[90vw] max-w-[450px] translate-x-[-50%] translate-y-[-50%] rounded-[6px] bg-white p-[25px] shadow-[hsl(206_22%_7%_/_35%)_0px_10px_38px_-10px,_hsl(206_22%_7%_/_20%)_0px_10px_20px_-15px] focus:outline-none z-[100]"
                                >
                                    <DialogTitle class="text-mauve12 m-0 text-[17px] font-semibold">
                                        <div v-if="error">Error</div>
                                        <div v-else>Thank you!</div>
                                    </DialogTitle>
                                    <DialogDescription
                                        class="text-mauve11 mt-[10px] mb-5 text-[15px] leading-normal"
                                    >
                                        <div v-if="error">
                                            Sorry, seems like our servers are down at the moment
                                        </div>
                                        <div v-else>
                                            Your event invite has been created and sent to the
                                            invitees.
                                        </div>
                                    </DialogDescription>

                                    <div class="mt-[25px] flex justify-end">
                                        <DialogClose as-child>
                                            <Button variant="outline" @click="tryAgain" v-if="error"
                                                >Try Again
                                            </Button>
                                            <Button variant="outline" @click="viewEvents" v-else
                                                >View Event
                                            </Button>
                                        </DialogClose>
                                    </div>
                                </DialogContent>
                            </DialogPortal>
                        </DialogRoot>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
