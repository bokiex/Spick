<script setup lang="ts">
import { AvatarFallback, AvatarImage, AvatarRoot } from 'radix-vue'

const props = defineProps<{
    src: string
    alt: string
    onload: () => void
}>()
</script>

<template>
    <AvatarRoot
        class="bg-blackA3 inline-flex h-[45px] w-[45px] select-none items-center justify-center overflow-hidden rounded-full align-middle"
    >
        <AvatarImage v-bind="props" class="h-full w-full rounded-[inherit] object-cover" />
        <AvatarFallback
            class="text-grass11 leading-1 flex h-full w-full items-center justify-center bg-white text-[15px] font-medium"
            :delay-ms="600"
        >
            CT
        </AvatarFallback>
    </AvatarRoot>
</template>
