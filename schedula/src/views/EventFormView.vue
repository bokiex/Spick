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
                    <div class="step" :class="{ active: isActcurrentStep == 4 }">
                        <div class="circle">4</div>
                        <div class="step-content">
                            <span>Step 4</span>
                            <b>End</b>
                        </div>
                    </div>
                </div>
                <!-- Sidebar end -->
                <!-- Step 1 start -->
                <div v-if="currentStep === 1" class="stp step-1">
                    <!-- Content omitted for brevity -->
                    <div class="header">
                        <h1 class="title">Event Details</h1>
                        <p class="exp">
                            Please provide the event title, event description, and attendees.
                        </p>
                    </div>
                    <form>
                        <div class="label">
                            <label for="title">Event Title</label>
                            <p class="error">This Field Is Required</p>
                        </div>
                        <input required type="text" id="title" placeholder="e.g. ESD Meeting" />
                        <div class="label">
                            <label for="description">Event Description</label>
                            <p class="error">This Field Is Required</p>
                        </div>
                        <input
                            required
                            type="text"
                            id="description"
                            placeholder="e.g. Deployment of site"
                        />
                        <div class="label">
                            <label for="attendees">Event Attendees</label>
                            <p class="error">This Field Is Required</p>
                        </div>
                        <input required type="text" id="attendees" placeholder="e.g. Ben Tan" />
                    </form>

                    <div class="btns">
                        <button @click="nextStep" class="next-stp" type="button">Next Step</button>
                    </div>
                </div>

                <!-- Step 1 end -->
                <!-- Step 2 start -->
                <div v-if="currentStep === 2" class="stp step-2">
                    <div class="header">
                        <h1 class="title">Pick the type of event.</h1>
                        <p class="exp">Select the type to get a venue recommendation.</p>
                    </div>
                    <form>
                        <div class="box" data-id="1">
                            <input type="checkbox" id="school" />
                            <div class="description">
                                <label for="school">School Meeting</label>
                                <small>School project meeting done in school.</small>
                            </div>
                        </div>
                        <div class="box" data-id="2">
                            <input type="checkbox" id="personal" />
                            <div class="description">
                                <label for="personal">Personal</label>
                                <small>Meeting with friends</small>
                            </div>
                        </div>
                        <div class="box" data-id="3">
                            <input type="checkbox" id="celebrations" />
                            <div class="description">
                                <label for="celebrations">Celebrations</label>
                                <small>Custom celebrations such as birthday parties.</small>
                            </div>
                        </div>
                    </form>
                    <div class="btns">
                        <button class="prev-stp" @click="prevStep" type="button">Go Back</button>
                        <button
                            class="next-stp"
                            @click="nextStep"
                            type="submit"
                            style="float: right"
                        >
                            Next Step
                        </button>
                    </div>
                </div>
                <!-- Step 2 end -->
                <!-- Step 3 Start -->
                <div v-if="currentStep === 3" class="stp step-3">
                    <div class="header">
                        <h1 class="title">Date and time.</h1>
                        <p class="exp">Select the date and time for the event.</p>
                    </div>
                    <div class="btns">
                        <button class="prev-stp" @click="prevStep" type="button">Go Back</button>
                        <button
                            class="next-stp"
                            @click="nextStep"
                            type="submit"
                            style="float: right"
                        >
                            Next Step
                        </button>
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
                    <button class="next-stp"></button>
                </div>
                <!-- Step 4 end -->
            </div>
        </div>
    </div>
</template>

<script>
export default {
    userID: localStorage.getItem('userID'),
    data() {
        return {
            currentStep: 1,
            steps: [
                { id: 1, label: 'Step 1', description: 'Details' },
                { id: 2, label: 'Step 2', description: 'Type' },
                { id: 3, label: 'Step 3', description: 'Date & Time' },
                { id: 4, label: 'Step 4', description: 'End' }
            ]
        }
    },
    methods: {
        nextStep() {
            if (this.currentStep < this.steps.length) this.currentStep++
        },
        prevStep() {
            if (this.currentStep > 1) this.currentStep--
        }
    }
}
</script>

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
    height: 578px;
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
