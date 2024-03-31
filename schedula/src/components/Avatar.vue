<script setup lang="ts">
import { AvatarFallback, AvatarImage, AvatarRoot } from 'radix-vue'
import { computed, defineProps } from 'vue'

const props = defineProps<{
    src: string
    alt: string
    onload: () => void
}>()

const imageSrc = computed(() => {
    return (
        props.src || 'https://source.unsplash.com/black-dog-wearing-blue-denim-collar-K4mSJ7kc0As'
    )
})
</script>

<template>
    <AvatarRoot
        class="bg-blackA3 inline-flex h-[45px] w-[45px] select-none items-center justify-center overflow-hidden rounded-full align-middle"
    >
        <AvatarImage
            :src="imageSrc"
            @load="props.onload"
            :alt="props.alt"
            class="h-full w-full rounded-[inherit] object-cover"
        />
        <AvatarFallback
            class="text-grass11 leading-1 flex h-full w-full items-center justify-center bg-white text-[15px] font-medium"
            :delay-ms="600"
        >
            CT
        </AvatarFallback>
    </AvatarRoot>
</template>
