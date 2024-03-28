<script setup>
import axios from 'axios'
import router from '../router'
import { Separator, Label } from 'radix-vue'
import Button from '../components/Button.vue'
</script>

<template>
    <div class="space-y-6 p-10 pb-16 justify-center md:flex">
        <div class="flex-1 lg:max-w-2xl">
            <div class="space-y-6">
                <div>
                    <h3 class="text-lg font-medium">Account Settings</h3>
                    <p class="text-sm text-muted-foreground">Edit your account information here!</p>
                </div>
                <Separator class="shrink-0 bg-border h-px w-full" />
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
                        id="userName"
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
                        id="userName"
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
                <div class="flex justify-start">
                    <Button type="submit">Save Changes</Button>
                </div>
                <div class="flex justify-end">
                    <Button type="submit" @click="logout">Log Out</Button>
                </div>
            </div>
        </div>
    </div>

    <!-- Button -->
</template>

<style>
* {
    font-family: 'Poppins', sans-serif;
}
.card-header {
    background-color: #f5f5f5;
    font-weight: bold;
}

.btn-link {
    padding: 0;
    margin-left: 10px;
}
</style>

<script>
export default {
    data() {
        return {
            userID: localStorage.getItem('userID'),
            user: {
                name: '',
                password: '',
                tele: '',
                email: '',
                newPwd: '',
                confirmPwd: ''
            }
        }
    },
    mounted() {
        this.loadUserData()
    },
    components: { Separator, Label },
    methods: {
        loadUserData() {
            console.log(this.userID)
            axios
                .get(`http://127.0.0.1:3000/users/user_id/${this.userID}`)
                .then((response) => {
                    this.user.name = response.data.username
                    this.user.tele = response.data.telegram_tag
                    this.user.email = response.data.email
                })
                .catch((error) => console.error(error))
        },
        saveSettings() {
            // Logic to save user settings
            axios
                .put(`http://127.0.0.1:3000/users/user_id/${this.userID}`, {
                    username: this.user.name,
                    telegram_tag: this.user.tele,
                    email: this.user.email
                })
                .then((response) => {
                    console.log('Settings saved', response.data)
                    alert('Changed!')
                    // Additional logic upon success
                })
                .catch((error) => console.error(error))
        },
        updatePassword() {
            // Check if new password matches confirm password
            if (this.user.newPwd !== this.user.confirmPwd) {
                alert('New password and confirm password do not match')
                return
            }

            // Check if new password is different from the old password
            if (this.user.password === this.user.newPwd) {
                alert("New password can't be the same as the old password")
                return
            }

            // Send a request to the microservice to update the password
            axios
                .put(`http://127.0.0.1:3000/users/user_id/${userID}/password`, {
                    oldPassword: this.user.password,
                    newPassword: this.user.newPwd
                })
                .then((response) => {
                    console.log('Password updated', response.data)
                    // Additional logic upon success
                })
                .catch((error) => {
                    console.error(error.response.data)
                })
        },
        logout() {
            localStorage.removeItem('user_id')
            router.push({ name: 'SignInSignUp' })
        }
    }
}
</script>
