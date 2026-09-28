<svelte:options runes={true} />

<script lang="ts">
    import * as HoverCard from "$lib/components/ui/hover-card/index.ts";
    import { fly } from "svelte/transition";
    import type { Snippet } from "svelte";

    interface HoverCardProps {
        class?: string;
        href?: string;
        content_align?: "start" | "center" | "end";
        trigger: Snippet;
        children: Snippet;
        variant?: "default" | "error";
    }
    let {
        class: className,
        href,
        content_align = "center",
        trigger,
        children,
        variant = "default",
    }: HoverCardProps = $props();
</script>

<HoverCard.Root openDelay={200}>
    <HoverCard.Trigger rel="noreferrer noopener" {href}>
        {@render trigger()}
    </HoverCard.Trigger>
    <HoverCard.Content
        class="w-80 {className} variant-{variant}"
        forceMount
        side="bottom"
        align={content_align}
    >
        {#snippet child({ wrapperProps, props, open })}
            {#if open}
                <div {...wrapperProps}>
                    <div {...props} transition:fly={{ y: -10, duration: 300 }}>
                        {@render children()}
                    </div>
                </div>
            {/if}
        {/snippet}
    </HoverCard.Content>
</HoverCard.Root>
