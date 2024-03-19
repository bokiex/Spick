<script>
    export default {
        userID: localStorage.getItem('userID'),
    }
</script>
<template>
    <div>this is event {{ $route.params.id }}</div>
</template>
