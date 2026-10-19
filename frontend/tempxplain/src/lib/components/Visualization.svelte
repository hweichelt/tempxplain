<script lang="ts">
    import type { Model } from "$lib/bindings";
    import { visualization_state } from "$lib/state/visualization_state.svelte";
    import Skeleton from "./ui/skeleton/skeleton.svelte";

    interface VisualizationProps {
        model: Model;
        timestep: number;
        visualization: boolean;
    }
    let {
        model,
        timestep,
        visualization = false,
    }: VisualizationProps = $props();
</script>

<div
    class="bg-card/70 w-full h-full rounded-md flex flex-row items-center justify-center p-4 backdrop-blur-3xl"
>
    {#if visualization}
        {#await visualization_state.get(model, timestep)}
            <Skeleton class="w-full h-full" />
        {:then image}
            {#if image === undefined}
                <div
                    class="text-foreground bg-destructive px-4 py-1 text-sm rounded-full"
                >
                    Visualization Error
                </div>
            {:else}
                <div
                    class="visualization h-full w-full"
                    role="img"
                    aria-label="Visualization of the {model} model"
                >
                    {@html image}
                </div>
            {/if}
        {:catch error}
            <div
                class="text-foreground bg-destructive px-4 py-1 text-sm rounded-full"
            >
                {error.message}
            </div>
        {/await}
    {:else}
        <div class="text-muted-foreground">No Visualization Specified</div>
    {/if}
</div>

<style>
    .visualization :global(svg) {
        width: 100%;
        height: 100%;
    }
    .visualization :global(text) {
        font-family: "JetBrains Mono";
    }

    /* Generic styling rules for the different properties */
    .visualization :global([class*="vb-"] :is(ellipse, polygon, path)) {
        fill: var(--b);
    }
    .visualization :global([class*="vt-"] text) {
        fill: var(--t);
    }
    .visualization :global([class*="vs-"] :is(ellipse, polygon, path)) {
        stroke: var(--s);
    }

    /* BACKGROUND */
    .visualization :global(.vb-red) {
        --b: light-dark(var(--color-red-400), var(--color-red-500));
    }
    .visualization :global(.vb-green) {
        --b: light-dark(var(--color-green-400), var(--color-green-600));
    }
    .visualization :global(.vb-gray-2) {
        --b: light-dark(var(--color-gray-300), var(--color-gray-800));
    }
    .visualization :global(.vb-gray-3) {
        --b: light-dark(var(--color-gray-500), var(--color-gray-600));
    }

    /* TEXT */
    .visualization :global(.vt-foreground) {
        --t: var(--foreground);
    }
    .visualization :global(.vt-muted-foreground) {
        --t: var(--muted-foreground);
    }
    .visualization :global(.vt-gray-3) {
        --t: light-dark(var(--color-gray-500), var(--color-gray-600));
    }

    /* STROKE */
    .visualization :global(.vs-gray-3) {
        --s: light-dark(var(--color-gray-500), var(--color-gray-600));
    }
</style>
