<script>
export default {
  userID: localStorage.getItem('userID'),
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
};
</script>

<template>
    <div class="reservation-page">
      <div class="timeslots-container">
        <div v-for="(timeslot, index) in timeslots" :key="index" class="time-card">
          <div class="time-card-content">
            <h3>{{ new Date(timeslot.date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' }) }}</h3>
            <p>{{ new Date(timeslot.start_time).toLocaleTimeString('en-US', { timeStyle: 'short' }) }} - {{ new Date(timeslot.end_time).toLocaleTimeString('en-US', { timeStyle: 'short' }) }}</p>
          </div>
        </div>
      </div>
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
  </template>
  
<style scoped>
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
  