<script setup>
import { twMerge } from 'tailwind-merge'
import clsx from 'clsx'

const props = defineProps({
    class: { type: String, default: '' },
    click: { type: Function, default: () => {} }
})
</script>
<template>
    <div
        :class="
            twMerge(clsx('rounded-lg border bg-card text-card-foreground shadow-sm', props.class))
        "
    
        :click="props.click"
    >
        <div class="p-6 pt-0">
            <slot />
        </div>
    </div>
</template>
