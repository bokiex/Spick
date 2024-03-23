<script setup>
import Card from '@/components/Card.vue'

import Button from '@/components/Button.vue'
import { useRouter, useRoute } from 'vue-router'
import {
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectRoot,
    SelectTrigger,
    SelectValue
} from 'radix-vue'
import { ref, onMounted } from 'vue'

const router = useRouter()
const route = useRoute()
const userID = localStorage.getItem('userID')

const events = ref(null)

onMounted(async () => {
    try {
        // Example API call - replace with your actual API call
        const data = await fetch('http://localhost:8000/event').then((res) => res.json())

        events.value = data
        console.log(data)
    } catch (error) {
        console.error('Failed to fetch event data:', error)
    } finally {
        loading.value = false
    }
})
const navigate = (id) => {
    router.push({ path: `/events/${id}` })
}
</script>

<template>
    <div class="flex justify-center items-center p-4">
        <div class="flex items-center gap-4">
            <Input
                placeholder="Search Events"
                class="w-full sm:w-56 px-4 py-2 border-2 border-gray-300 dark:border-gray-700 rounded-md"
            />
            <Button> Search </Button>
        </div>
    </div>
    <div class="flex flex-wrap justify-around gap-4 items-center p-4">
        <Card
            class="pt-6 hover:bg-accent max-w-64"
            v-for="event in events"
            @click="navigate(event?.event_id)"
        >
            <div class="space-y-2">
                <img :src="event?.image[0].image_path" alt="" />
                <div class="flex flex-col gap-y-1.5">
                    <h1>{{ event?.event_name }}</h1>
                </div>
                <div class="text-sm text-muted-foreground">
                    <p>{{ event?.date }}</p>
                    <p>{{ event?.event_desc }}</p>
                </div>
            </div>
        </Card>
    </div>
</template>
