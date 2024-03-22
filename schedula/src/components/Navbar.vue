<script setup>
import { CalendarDays, SquarePlus, UserRound, TentTree } from 'lucide-vue-next'
import {
    NavigationMenuContent,
    NavigationMenuIndicator,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuRoot,
    NavigationMenuTrigger,
    NavigationMenuViewport
} from 'radix-vue'
</script>

<template>
    <NavigationMenuRoot class="flex w-full justify-center">
        <NavigationMenuList class="center m-0 flex list-none rounded-[6px] bg-white p-1">
            <NavigationMenuItem>
                <NavigationMenuLink
                    class="transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus:bg-accent focus:text-accent-foreground block select-none rounded-[4px] px-3 py-2 text-[15px] font-medium leading-none no-underline outline-none"
                    href="/"
                >
                    Calendar
                </NavigationMenuLink>
            </NavigationMenuItem>

            <NavigationMenuItem
                class="transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus:bg-accent focus:text-accent-foreground block select-none rounded-[4px] px-3 py-2 text-[15px] font-medium leading-none no-underline outline-none"
            >
                <NavigationMenuLink href="/create"> Create </NavigationMenuLink>
            </NavigationMenuItem>

            <NavigationMenuItem
                class="transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus:bg-accent focus:text-accent-foreground block select-none rounded-[4px] px-3 py-2 text-[15px] font-medium leading-none no-underline outline-none"
            >
                <NavigationMenuLink href="/events"> Events</NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem
                class="transition-colors hover:bg-accent hover:text-accent-foreground focus:outline-none focus:bg-accent focus:text-accent-foreground block select-none rounded-[4px] px-3 py-2 text-[15px] font-medium leading-none no-underline outline-none"
            >
                <NavigationMenuLink href="/profile"> Profile</NavigationMenuLink>
            </NavigationMenuItem>
        </NavigationMenuList>
    </NavigationMenuRoot>
</template>
