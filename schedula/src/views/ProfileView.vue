<template>
    <div class="container my-4">
        <!-- Personal Information -->
        <div class="row justify-content-center" style="margin-top: 2rem;">
            <div class="col-lg-8 col-md-10">
                <div class="card">
                    <div class="card-body">
                        <h4>Account Settings</h4>
                        <p>Edit your account information here!</p>
                        <form @submit.prevent="saveSettings">
                            <!-- First Row of Information -->
                            <div class="form-group mb-3 row">
                                <div class="col-md-6 col-sm-12">
                                    <label for="userName">Name</label>
                                    <input
                                        type="text"
                                        class="form-control"
                                        id="userName"
                                        v-model="user.name"
                                    />
                                </div>
                                <div class="col-md-6 col-sm-12">
                                    <label for="userTele">Tele Handle</label>
                                    <input
                                        type="text"
                                        class="form-control"
                                        id="userTele"
                                        v-model="user.tele"
                                    />
                                </div>
                            </div>
                            <!-- Second Row of Information -->
                            <div class="form-group mb-3">
                                <label for="userEmail">Email</label>
                                <input
                                    type="text"
                                    class="form-control"
                                    id="userEmail"
                                    v-model="user.email"
                                />
                            </div>                           
                            <!-- Buttons -->
                            <div class="d-flex justify-content-end mb-3">
                                <div>
                                    <button type="submit" class="btn btn-primary">Save Changes</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <!-- Change Password -->
        <div class="row justify-content-center" style="margin-top: 2rem;">
            <div class="col-lg-8 col-md-10">
                <div class="card">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-lg-8 col-sm-12">
                                <h4>Change Password</h4>
                                <form @submit.prevent="updatePassword">
                                    <div class="form-group mb-3">
                                        <label for="userPassword">Current Password</label>
                                        <input
                                            type="password"
                                            class="form-control"
                                            v-model="user.password"
                                            required
                                        />
                                    </div>
                                    <div class="form-group mb-3">
                                        <label for="usernewPwd">New Password</label>
                                        <input
                                            type="password"
                                            class="form-control"
                                            v-model="user.newPwd"
                                            required
                                        />
                                    </div>
                                    <div class="form-group mb-3">
                                        <label for="userconfirmPwd">Confirm Password</label>
                                        <input
                                            type="password"
                                            class="form-control"
                                            v-model="user.confirmPwd"
                                            required
                                        />
                                    </div>
                                    <!-- Button -->
                                    <div class="d-flex justify-content-end mb-3">
                                        <div>
                                            <button type="submit" class="btn btn-primary">Save Changes</button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                            <!-- Information on Password Change-->
                            <div class="col-lg-4 col-sm-12">
                                <div class="card" style="background-color: lightgray; border: none;">
                                    <div class="card-content m-3">
                                        <label style="font-weight: 600;">Password requirement</label>
                                        <p>
                                            In order to create a strong password, here are some rules to keep in mind:
                                            <ul>
                                                <li>Minimum 8 characters</li>
                                                <li>At least one lowercase character</li>
                                                <li>At least one uppercase character</li>
                                                <li>Can't be the same as previous password</li>
                                            </ul>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            user: {
                name: '',
                password: '',
                tele: '',
                email: ''
            }
        }
    },
    methods: {
        saveSettings() {
            // Logic to save user settings
            axios.post('http://localhost:5000/signup', {
                name : document.getElementById("userName").value,
                tele: document.getElementById("userTele").value,
                email: document.getElementById("userEmail").value
            });
            console.log('Saved', this.user);
        },
        updatePassword() {
            // Check if new password matches confirm password
            if (this.newPwd !== this.confirmPwd) {
                alert('New password and confirm password do not match');
                return;
            }
            
            // Send a request to the microservice to update the password
            axios.post('http://localhost:5000/signup', {
                password: this.newPwd
            });
            console.log('Saved', this.user);
        }
    }
}
</script>

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
