<script setup>
import axios from 'axios'
import router from '../router'
import { Separator, Label } from 'radix-vue'
import Button from '../components/Button.vue'
import Avatar from '../components/Avatar.vue'
import { ref, onMounted } from 'vue'
import { getImageUrl } from '@/utils/get_image'

const userID = localStorage.getItem('userID')
const user = ref({
    name: '',
    password: '',
    image: '',
    preview_image: '',
    tele: '',
    email: '',
    newPwd: '',
    confirmPwd: ''
})
onMounted(async () => {
    await axios
        .get(`http://localhost:8101/users/user_id/${userID}`)
        .then((response) => {
            user.value.name = response.data.username
            user.value.tele = response.data.telegram_tag
            user.value.email = response.data.email
            user.value.image = response.data.image
            user.value.preview_image = getImageUrl(response.data.image)
            console.log(response.data)
        })
        .catch((error) => console.error(error))
})

function previewFile(event) {
    const file = event.target.files[0]

    user.value.preview_image = URL.createObjectURL(file)
    user.value.image = file
}

async function saveSettings() {
    // Logic to save user settings
    const formData = new FormData()
    formData.append(
        'user',
        JSON.stringify({
            username: user.value.name,
            telegram_tag: user.value.tele,
            email: user.value.email,
            image: user.value.image.name
        })
    ) // eventData is your form's data as a JS object
    if (user.value.image instanceof File) {
        formData.append('files', user.value.image)
    }
 
    console.log(JSON.stringify({
            username: user.value.name,
            telegram_tag: user.value.tele,
            email: user.value.email,
            image: user.value.image.name,
        }),
            user.value.image)

    try {
        const res = await fetch(`http://localhost:8101/users/user_id/${userID}`, {
            method: 'PUT',
            body: formData
        })

        if (!res.ok) {
            const data = await res.json()

            throw new Error(data.error)
        }
    } catch (error) {
        console.log(error)
        console.error('Error fetching data: ', error)
    }
}

async function updatePassword() {
    // Check if new password matches confirm password
    if (user.value.newPwd !== user.value.confirmPwd) {
        alert('New password and confirm password do not match')
        return
    }

    // Check if new password is different from the old password
    if (user.value.password === user.value.newPwd) {
        alert("New password can't be the same as the old password")
        return
    }

    // Send a request to the microservice to update the password

    try {
        console.log({
            username: user.value.name,
            email: user.value.email,
            password: user.value.confirmPwd
        })
        const res = await fetch(`http://localhost:8001/users/user_id/${userID}/password`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json' // Specify that we're sending JSON data
            },
            body: JSON.stringify({
                username: user.value.name,
                email: user.value.email,
                password: user.value.confirmPwd
            })
        })

        if (!res.ok) {
            const data = await res.json()

            throw new Error(data.error)
        }
    } catch (error) {
        console.log(error)
        console.error('Error fetching data: ', error)
    }
}
function logout() {
    localStorage.removeItem('userID')
    router.push({ name: 'SignInSignUp' })
}
</script>

<template>
    <div class="space-y-6 p-10 pb-16 justify-center md:flex">
        <div class="flex-1 lg:max-w-2xl">
            <div class="space-y-6">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 class="text-lg font-medium">Account Settings</h3>
                        <p class="text-sm text-muted-foreground">Edit your account information here!</p>
                    </div>
                    <div class="flex justify-end">
                        <Button type="submit" @click="logout">Log Out</Button>
                    </div>
                </div>
                <Separator class="shrink-0 bg-border h-px w-full" />
                <div class="space-y-2">
                    <div class="flex flex-col space-y-2">
                        <Label
                            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                            Profile Picture
                        </Label>

                        <Avatar
                            onload="() => URL.revokeObjectURL(user.preview_image)"
                            :src="user.preview_image"
                            class="w-12 h-12 rounded-full"
                        ></Avatar>

                        <input
                            name="image"
                            type="file"
                            @change="(event) => previewFile(event)"
                            required
                            id="image"
                            class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                        />
                    </div>
                </div>
                <div class="space-y-2">
                    <Label
                        class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                        Name
                    </Label>
                    <input
                        id="userName"
                        v-model="user.name"
                        class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    />
                </div>
                <div class="space-y-2">
                    <Label
                        class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                        Tele Handle
                    </Label>
                    <input
                        type="text"
                        id="userTele"
                        v-model="user.tele"
                        class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    />
                </div>
                <div class="space-y-2">
                    <Label
                        class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                        Email
                    </Label>
                    <input
                        type="text"
                        id="userEmail"
                        v-model="user.email"
                        class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    />
                </div>

                <div class="flex justify-start">
                    <Button type="submit" @click="saveSettings">Save</Button>
                </div>
            </div>
        </div>
    </div>
    <div class="space-y-6 p-10 pb-16 justify-center md:flex">
        <div class="flex-1 lg:max-w-2xl">
            <div class="space-y-6">
                <div>
                    <h3 class="text-lg font-medium">Change Password</h3>
                </div>
                <Separator class="shrink-0 bg-border h-px w-full" />
                <div class="space-y-2">
                    <Label
                        class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                        Current Password
                    </Label>
                    <input
                        type="password"
                        required
                        v-model="user.password"
                        class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    />
                </div>
                <div class="space-y-2">
                    <Label
                        class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                        New Password
                    </Label>
                    <input
                        type="password"
                        v-model="user.newPwd"
                        class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    />
                </div>
                <div class="space-y-2">
                    <Label
                        class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                        Confirm Password
                    </Label>
                    <input
                        type="password"
                        v-model="user.confirmPwd"
                        class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    />
                </div>
                <div class="flex justify-start">
                    <Button type="button" @click="updatePassword()">Save Changes</Button>
                </div>
                <!-- <div class="flex justify-end">
                    <Button type="submit" @click="logout">Log Out</Button>
                </div> -->
            </div>
        </div>
    </div>

    <!-- Button -->
</template>
