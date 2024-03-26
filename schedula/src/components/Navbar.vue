<script setup>
import {
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuRoot
} from 'radix-vue'
import Button from './Button.vue'
import Label from './Label.vue'
import { ArrowRight, SendHorizonal } from 'lucide-vue-next'
import { ref } from 'vue'

const code = ref(null)
</script>
<template>
    <NavigationMenuRoot class="flex w-full justify-center">
        <div
            class="flex w-full justify-center m-0 list-none rounded-[6px] bg-white p-1"
        >
        <div class="flex-grow"></div>
            <div class="flex justify-center gap-4 ">
                <NavigationMenuItem
                    class="flex items-center transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus:bg-accent focus:text-accent-foreground block select-none rounded-[4px] px-3 py-2 text-[15px] font-medium leading-none no-underline outline-none"
                >
                    <NavigationMenuLink href="/"> Calendar </NavigationMenuLink>
                </NavigationMenuItem>

                <NavigationMenuItem
                    class="flex items-center transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus:bg-accent focus:text-accent-foreground block select-none rounded-[4px] px-3 py-2 text-[15px] font-medium leading-none no-underline outline-none"
                >
                    <NavigationMenuLink href="/create"> Create </NavigationMenuLink>
                </NavigationMenuItem>

                <NavigationMenuItem
                    class="flex items-center transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus:bg-accent focus:text-accent-foreground block select-none rounded-[4px] px-3 py-2 text-[15px] font-medium leading-none no-underline outline-none"
                >
                    <NavigationMenuLink href="/events"> Events</NavigationMenuLink>
                </NavigationMenuItem>
                <NavigationMenuItem
                    class="flex items-center transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus:bg-accent focus:text-accent-foreground block select-none rounded-[4px] px-3 py-2 text-[15px] font-medium leading-none no-underline outline-none"
                >
                    <NavigationMenuLink href="/profile"> Profile</NavigationMenuLink>
                </NavigationMenuItem>
            </div>
            <div class="flex-grow"></div>

            <NavigationMenuItem
                class="items-center flex gap-1.5 transition-colors focus:outline-none focus:bg-accent focus:text-accent-foreground block select-none rounded-[4px] px-3 py-2 text-[15px] font-medium leading-none no-underline outline-none"
            >
                <Label for="code">Enter Code</Label>
                <input
                    name="code"
                    required
                    id="code"
                    v-model="code"
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder="XJSDFD"
                />
                <router-link class = "btn btn-go" type = "button" :to="`/RSVP/${code}`"><SendHorizonal /></router-link>
            </NavigationMenuItem>
            <div class="flex-grow-0"></div>
        </div>
    </NavigationMenuRoot>
</template>
