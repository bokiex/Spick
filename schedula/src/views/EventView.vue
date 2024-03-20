<template>
    <div class="event-page">
        <!-- Event Header with Image and Title -->
        <div class="event-header">
            <img class="event-image" :src="event.image" alt="Header image of the event" />
            <div class="event-card">
                <EventCard
                    :title="event.title"
                    :date="event.date"
                    :time="event.time"
                    :location="event.location"
                />
            </div>
        </div>

        <!-- Event Content Section -->
        <div class="event-content">
            <div class="event-details">
                <h2 class="section-title">Events Details</h2>
                <p>{{ event.description }}</p>
            </div>

            <!-- Sidebar for Additional Information -->
            <div class="event-sidebar">
                <div class="subscription-box">
                    <h3>Subscribe Now</h3>
                    <!-- Additional content like QR codes or calendar links would go here -->
                </div>
                <div class="event-organizer">
                    <h3>Event Organizer</h3>
                    <p>{{ event.organizer.name }}</p>
                    <p>{{ event.organizer.contact }}</p>
                    <p>{{ event.organizer.email }}</p>
                    <p>
                        <a :href="event.organizer.website">{{ event.organizer.website }}</a>
                    </p>
                </div>
            </div>
        </div>

        <!-- Event Media Section for Photos and Videos -->
        <div class="event-media">
            <h2 class="section-title">Event Photos and Videos</h2>
            <div class="media-grid">
                <div v-for="mediaItem in event.media" :key="mediaItem.id" class="media-item">
                    <img
                        v-if="mediaItem.type === 'image'"
                        :src="mediaItem.url"
                        :alt="mediaItem.alt"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import EventCard from '@/components/EventCard.vue'
export default {
    name: 'EventPage',
    data() {
        return {
            event: {
                title: 'Dinner Party',
                image: '../public/event.jpg',
                date: 'Saturday, Feb 23, 2019',
                time: '5:00 PM - 11:00 PM',
                location: '5323 Gilroy St, Gilroy, CA',
                description:
                    'We are hosting a dinner party just for our best clients. We are excited to see you there.',
                organizer: {
                    name: 'American Bar',
                    contact: '(415) 444-3434',
                    email: 'info@americanbar.com',
                    website: 'https://www.americanbar.com'
                },
                media: [
                    { id: 1, type: 'image', url: 'path-to-photo.jpg', alt: 'Event photo' },
                    { id: 2, type: 'video', url: 'path-to-video.mp4', mimeType: 'video/mp4' }
                    // Add more media items as needed
                ]
            }
        }
    },
    components: {
        EventCard
    }
}
</script>

<style scoped>
/* Basic styles, add more to match your design */
.event-page {
    margin: auto;
}

.event-header {
    text-align: center;
    color: white;
    position: relative;
    min-height: 500px;
}

.event-header-content {
    bottom: 20px;
    left: 20px;
}

.event-image {
    width: 100%;
    max-height: 300px;
    object-fit: cover;
    display: block;
}

.event-card {
    position: absolute;
    top: 50%;
    color: white;
    width: 100%;
}

.event-content {
    margin:auto;
    max-width: 900px;
    display: grid;
    grid-template-columns: 3fr 1fr;
    gap: 20px;
}
.section-title {
    font-size: 24px;
    margin-bottom: 15px;
}

.media-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.media-item {
    border: 1px solid #ccc;
    padding: 10px;
}

/* Add responsive design and other styles as required */
</style>
