<template>
    <div class="card shadow-sm rounded-3" style="max-width: 20rem; margin: auto" @click="navigate">
        <img :src="image" class="card-img-top" alt="Event image" />
        <div class="card-body">
            <h5 class="card-title">{{ title }}</h5>
            <p class="card-text">{{ description }}</p>
            <p class="card-text">
                <small class="text-muted">{{ date }}</small>
            </p>
            <a href="#" class="stretched-link">Learn More</a>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Card',
    props: {
        title: String,
        id: Number,
        description: String,
        image: String,
        link: String,
        date: String
    },
    methods: {
        navigate() {
            this.$router.push({ name: 'event', params: { id: this.id } })
        }
    }
}
</script>
