<script>
export default {
  user_id: localStorage.getItem('user_id'),
  selectedTimeslot: "",
  data() {
      return {
        timeslots: [
          {date:'2024-03-14', start_time:'2024-03-14T21:00:00', end_time: '2024-03-14T13:00:00'},
          {date:'2024-03-14', start_time:'2024-03-14T21:00:00', end_time: '2024-03-14T13:00:00'},
          {date:'2024-03-14', start_time:'2024-03-14T21:00:00', end_time: '2024-03-14T13:00:00'}
        ],
        venues: [
          {
            name: 'SMU',
            address: 'Victoria Road',
            imageUrl: 'https://via.placeholder.com/150'
          },
          {
            name: 'SMU',
            address: 'Victoria Road',
            imageUrl: 'https://via.placeholder.com/150'
          },
          {
            name: 'SMU',
            address: 'Victoria Road',
            imageUrl: 'https://via.placeholder.com/150'
          },
        ]
      };
    }
}
</script>

<template>
    <div class="reservation-page">
      <div class="container my-4">
        <h3>Reservation</h3>
        <div class="row justify-content-center" style="margin-top: 2rem;">
          <!-- Time Slot Start -->
          <div class="col-lg-3 col-md-3">
            <div class="timeslots-container">
              <div v-for="(timeslot, index) in timeslots" :key="index" class="row">
                <div class="checkbox-row">
                  <div class="checkbox-box">
                    <input type="radio" :id="'timeslot_' + index" :name="'timeslot_radio'" v-model="selectedTimeslot" :value="timeslot">
                    <label :for="'timeslot_' + index">
                      <h5>{{ new Date(timeslot.date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' }) }}</h5>
                      <p>{{ new Date(timeslot.start_time).toLocaleTimeString('en-US', { timeStyle: 'short' }) }} - {{ new Date(timeslot.end_time).toLocaleTimeString('en-US', { timeStyle: 'short' }) }}</p>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Time Slot End -->
          <!-- Venue Start -->
          <div class="col-lg-9 col-md-9">
            <div class="venues-container">
                <div v-for="(venue, index) in venues" :key="index" class="venue-card">
                    <img :src="venue.imageUrl" :alt="venue.name" />
                    <div class="venue-card-content">
                        <h3>{{ venue.name }}</h3>
                        <p>{{ venue.address }}</p>
                    </div>
                </div>
            </div>
          </div>
          <!-- Venue end -->
        </div>
      </div>
    </div>
</template>

<style scoped>
  .checkbox-box {
    display: block;
    padding: 10px; /* Add padding for better spacing */
  }

  .checkbox-box input[type="radio"] {
    display: none;
  }

  .checkbox-box label {
    display: block;
    border: 2px solid #ccc;
    border-radius: 10px;
    background-color: #98c1d9;
    padding: 10px; /* Add padding to style the entire row */
    cursor: pointer; /* Add cursor pointer for better UX */
  }

  .checkbox-box input[type="radio"]:checked + label {
    background-color: #3d5a80;
    color: white;
  }

  .checkbox-row {
    margin-bottom: 10px; /* Add margin between rows */
  }

.reservation-page {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 40px;
    padding: 20px;
    gap: 20px;
    /* height: 100%; */
    margin-left: 5rem;
    margin-right: 5rem;
}

.timeslots-container,
.venues-container {
    flex: 1;
    overflow-y: auto;
    margin: 10px;
    text-align: center;
    height: calc(100vh - 60px);
}

.timeslot-card,
.venue-card {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 10px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-left: 5px;
    margin-right: 5px;
}

.timeslot-card h3,
.venue-card h3 {
    margin: 0;
    font-size: 18px;
    color: #333;
    margin-bottom: 5px;
}

.timeslot-card p,
.venue-card p {
    font-size: 16px;
    color: #555;
}

.venue-card img {
    width: 70%;
    height: 50%;
    object-fit: cover;
    margin-bottom: 10px;
    border-radius: 8px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .reservation-page {
        flex-direction: column;
    }

    .timeslots-container,
    .venues-container {
        flex: none;
        width: 100%;
    }
}

/* Hide scrollbar for Chrome, Safari and Opera */
.timeslots-container::-webkit-scrollbar,
.venues-container::-webkit-scrollbar {
    display: none;
}

.timeslots-container,
.venues-container {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>
