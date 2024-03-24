<script>
export default {
    components: {},
    name: "entercode",
    data() {
        return {
            user_id:0,
            code: ""
        }
    },
    methods: {
    }
}

</script>

<template>

    <!-- Navbar Start-->
    <nav class="navbar navbar-expand-md navbar-light bg-light m-1">
        <div class="container-fluid m-0">
            <a class="navbar-brand m-0" href="#">Schedular</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
                <!-- Added justify-content-center to center align the navbar links -->
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="#"><i class="bi bi-calendar"></i> Calendar</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="#"><i class="bi bi-plus-square"></i> Create</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#"><i class="bi bi-currency-dollar"></i> Billing</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#"><i class="bi bi-person-square"></i> Profile</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container p-4">
        <div class="row justify-content-center">
            <!-- Form Start -->
            <div class="form-container" style="position: relative;">
                <div class="vertical-center" style="text-align:center;">
                    <div style="text-align:center;">
                        <div class="header">Enter Event Code</div>
                    </div>
                    <div class="input-group mb-3" style="float:right;">
                        <input type="text" class="form-control form-input" v-model="code" placeholder="Event Code"
                            aria-label="Event Code" aria-describedby="basic-addon2">
                            <router-link class = "btn btn-go" type = "button" :to="`/RSVP/${this.user_id}/${this.code}`">Go</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</template>

<style scoped>
.form-input {
    padding: 1rem;
    border: 1px solid hsl(231, 11%, 63%);
    font-weight: 500;
    font-size: 1rem;
}

.form-input:focus {
    outline-color: hsl(243, 100%, 62%);
}

.btn-go {
    border: none;
    padding: 1rem 2rem;
    background-color: hsl(213, 96%, 18%);
    color: white;
    cursor: pointer;
}

.header {
    color: hsl(213, 96%, 18%);
    font-size: large;
    margin-bottom: 15px;
}

.vertical-center {
    margin: 0;
    position: absolute;
    top: 50%;
    -ms-transform: translateY(-50%);
    transform: translateY(-50%);
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

.label {
    color: hsl(213, 96%, 18%);
    display: flex;
    align-items: center;
    justify-content: space-between;
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
}
</style>