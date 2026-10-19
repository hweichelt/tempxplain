<svelte:options runes={true} />

<script lang="ts">
    import * as HoverCard from "$lib/components/ui/hover-card/index";
    import type { Snippet } from "svelte";

    interface HoverCardProps {
        class?: string;
        href?: string;
        content_align?: "start" | "center" | "end";
        trigger: Snippet;
        children: Snippet;
    }
    let {
        class: className,
        href,
        content_align = "end",
        trigger,
        children,
    }: HoverCardProps = $props();
</script>

<HoverCard.Root openDelay={100}>
    <HoverCard.Trigger rel="noreferrer noopener" {href}>
        {@render trigger()}
    </HoverCard.Trigger>
    <HoverCard.Content
        class="w-80 {className} rounded-sm mt-1 duration-200"
        side="bottom"
        align={content_align}
    >
        {@render children()}
    </HoverCard.Content>
</HoverCard.Root>
