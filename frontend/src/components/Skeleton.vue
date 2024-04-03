<script setup>
import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

const props = defineProps()
</script>

<template>
    <div :class="twMerge(clsx('animate-pulse rounded-md bg-muted', props.class))" />
</template>
