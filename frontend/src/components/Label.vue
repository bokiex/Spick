<script setup>
import { Label } from 'radix-vue'
import { defineProps, computed } from 'vue'
import { twMerge } from 'tailwind-merge'
import clsx from 'clsx'

const props = defineProps({
    class: { type: String, default: '' },
    click: { type: Function, default: () => {} },
    disabled: { type: Boolean, default: false },
    for: { type: String, default: '' },
    required: { type: Boolean, default: false },
    value: { type: String, default: '' },
    type: { type: String, default: 'text' },
    placeholder: { type: String, default: '' },
    name: { type: String, default: '' },
    id: { type: String, default: '' },
    autocomplete: { type: String, default: '' },
    autofocus: { type: Boolean, default: false },
    maxlength: { type: Number, default: 0 },
    minlength: { type: Number, default: 0 },
    pattern: { type: String, default: '' },
    readonly: { type: Boolean, default: false },
    size: { type: Number, default: 0 },
    spellcheck: { type: Boolean, default: false },
    step: { type: Number, default: 0 },
    tabindex: { type: Number, default: 0 },
    title: { type: String, default: '' },
    inputmode: { type: String, default: '' },
    list: { type: String, default: '' },
    form: { type: String, default: '' },
    formaction: { type: String, default: '' },
    formenctype: { type: String, default: '' },
    formmethod: { type: String, default: '' },
    formnovalidate: { type: Boolean, default: false },
    formtarget: { type: String, default: '' },
    height: { type: Number, default: 0 },
    width: { type: Number, default: 0 },
    accept: { type: String, default: '' },
    alt: { type: String, default: '' },
    src: { type: String, default: '' },
    srcset: { type: String, default: '' },
    usemap: { type: String, default: '' },
    align: { type: String, default: '' },
    border: { type: Number, default: 0 },
    hspace: { type: Number, default: 0 }
})

const delegatedProps = computed(() => {
    const { class: _, ...delegated } = props

    return delegated
})
</script>

<template>
    <Label
        v-bind="delegatedProps"
        :class="
            twMerge(
                clsx(
                    'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
                    props.class
                )
            )
        "
    >
        <slot />
    </Label>
</template>
