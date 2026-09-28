<script lang="ts">
    import { backend } from "$lib/backend.svelte";
    import HoverCard from "$lib/components/HoverCard.svelte";

    let class_connected = $derived(
        backend.connected ? "connected" : "disconnected",
    );
</script>

<HoverCard class="w-56">
    {#snippet trigger()}
        <div
            class="border w-8 h-8 flex justify-center items-center rounded-lg bg-background dark:bg-input/30"
        >
            <div
                class="indicator w-3 h-3 rounded-full transition-colors {class_connected}"
            ></div>
        </div>
    {/snippet}
    <div class="grid grid-cols-[1fr_auto] items-center gap-2">
        <div>Backend</div>
        <div class="text-sm font-mono bg-card px-2 py-0.5 rounded-sm">
            {backend.connected ? "Connected" : "Disconnected"}
        </div>
    </div>
</HoverCard>

<style>
    .indicator.connected {
        background: var(--color-success);
    }
    .indicator.disconnected {
        background: var(--color-destructive);
    }
</style>
