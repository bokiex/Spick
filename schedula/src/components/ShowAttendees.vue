<script setup>
import { ref } from 'vue'
import Avatar from './Avatar.vue'
import {
    ComboboxContent,
    ComboboxGroup,
    ComboboxInput,
    ComboboxItem,
    PopoverContent,
    PopoverPortal,
    PopoverRoot,
    PopoverTrigger
} from 'radix-vue'
import { defineProps, defineEmits } from 'vue'

import { ComboboxRoot } from 'radix-vue'
import { Search } from 'lucide-vue-next'
import Button from './Button.vue'
import { CaretSortIcon } from '@radix-icons/vue'

const props = defineProps({
    friends: { type: Array, default: () => [] },
    selected_friend: { type: Object, default: () => {} }
})
const emit = defineEmits(['update:selectedFriend'])
const open = ref(false)
</script>

<template>
    <PopoverRoot v-model:open="open">
        <PopoverTrigger class="w-full">
            <Button
                variant="outline"
                role="combobox"
                aria-expanded="open"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >{{ props.selected_friend.name
                }}<CaretSortIcon class="ml-auto h-4 w-4 shrink-0 opacity-50"
            /></Button>
        </PopoverTrigger>
        <PopoverPortal>
            <PopoverContent
                side="bottom"
                :side-offset="5"
                class="z-50 w-72 rounded-md border bg-popover w-full p-0 text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2"
            >
                <ComboboxRoot
                    v-model:open="open"
                    class="flex h-full w-full flex-col overflow-hidden rounded-md bg-popover text-popover-foreground"
                >
                    <ComboboxContent class="max-h-[300px] overflow-y-auto overflow-x-hidden">
                        <div role="presentation">
                            <div class="flex items-center border-b px-3" cmdk-input-wrapper>
                                <Search class="mr-2 h-4 w-4 shrink-0 opacity-50" />
                                <ComboboxInput
                                    class="flex h-11 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50"
                                    placeholder="Search friend..."
                                >
                                </ComboboxInput>
                            </div>
                            <ComboboxGroup
                                class="overflow-hidden p-1 text-foreground [&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:py-1.5 [&_[cmdk-group-heading]]:text-xs [&_[cmdk-group-heading]]:font-medium [&_[cmdk-group-heading]]:text-muted-foreground"
                            >
                                <ComboboxItem
                                    v-for="friend in props.friends"
                                    :value="friend.name"
                                    @select="
                                        () => {
                                            emit('update:selectedFriend', friend)
                                            selected_friend = friend
                                            open = false
                                        }
                                    "
                                    :key="friend.name"
                                    class="relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none data-[highlighted]:bg-accent data-[disabled]:pointer-events-none data-[disabled]:opacity-50"
                                >
                                    <Avatar
                                        :src="friend.avatar"
                                        class="mr-2 w-6 h-6 rounded-full"
                                    />
                                    <span>{{ friend.name }}</span>
                                </ComboboxItem>
                            </ComboboxGroup>
                        </div>
                    </ComboboxContent>
                </ComboboxRoot>
            </PopoverContent>
        </PopoverPortal>
    </PopoverRoot>
</template>
