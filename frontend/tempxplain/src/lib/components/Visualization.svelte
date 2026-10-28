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

<!-- prettier-ignore -->
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

    .visualization {
        --c-white: #ffffff;
        --c-black: #000000;
        --c-red: light-dark(var(--color-red-400), var(--color-red-500));
        --c-purple: light-dark(var(--color-purple-400), var(--color-purple-500));
        --c-blue: light-dark(var(--color-blue-400), var(--color-blue-600));
        --c-green: light-dark(var(--color-green-400), var(--color-green-600));
        --c-yellow: light-dark(var(--color-yellow-300), var(--color-yellow-500));
        --c-orange: light-dark(var(--color-orange-300), var(--color-orange-500));
        --c-gray-1: light-dark(var(--color-gray-100), var(--color-gray-900));
        --c-gray-2: light-dark(var(--color-gray-300), var(--color-gray-800));
        --c-gray-3: light-dark(var(--color-gray-500), var(--color-gray-600));
        --c-gray-4: light-dark(var(--color-gray-700), var(--color-gray-400));
    }

    /* BACKGROUND */
    .visualization :global(.vb-t) {--b: transparent}
    .visualization :global(.vb-background) {--b: var(--color-background)}
    .visualization :global(.vb-foreground) {--b: var(--color-foreground)}
    .visualization :global(.vb-muted) {--b: var(--color-muted)}
    .visualization :global(.vb-muted-foreground) {--b: var(--color-muted-foreground)}
    .visualization :global(.vb-red) {--b: var(--c-red)}
    .visualization :global(.vb-purple) {--b: var(--c-purple)}
    .visualization :global(.vb-blue) {--b: var(--c-blue)}
    .visualization :global(.vb-green) {--b: var(--c-green)}
    .visualization :global(.vb-yellow) {--b: var(--c-yellow)}
    .visualization :global(.vb-orange) {--b: var(--c-orange)}
    .visualization :global(.vb-gray-1) {--b: var(--c-gray-1)}
    .visualization :global(.vb-gray-2) {--b: var(--c-gray-2)}
    .visualization :global(.vb-gray-3) {--b: var(--c-gray-3)}
    .visualization :global(.vb-gray-4) {--b: var(--c-gray-4)}
    .visualization :global(.vb-white) {--b: var(--c-white)}
    .visualization :global(.vb-black) {--b: var(--c-black)}

    /* TEXT */
    .visualization :global(.vt-t) {--t: transparent}
    .visualization :global(.vt-background) {--t: var(--color-background)}
    .visualization :global(.vt-foreground) {--t: var(--color-foreground)}
    .visualization :global(.vt-muted) {--t: var(--muted)}
    .visualization :global(.vt-muted-foreground) {--t: var(--muted-foreground)}
    .visualization :global(.vt-red) {--t: var(--c-red)}
    .visualization :global(.vt-purple) {--t: var(--c-purple)}
    .visualization :global(.vt-blue) {--t: var(--c-blue)}
    .visualization :global(.vt-green) {--t: var(--c-green)}
    .visualization :global(.vt-yellow) {--t: var(--c-yellow)}
    .visualization :global(.vt-orange) {--t: var(--c-orange)}
    .visualization :global(.vt-gray-1) {--t: var(--c-gray-1)}
    .visualization :global(.vt-gray-2) {--t: var(--c-gray-2)}
    .visualization :global(.vt-gray-3) {--t: var(--c-gray-3)}
    .visualization :global(.vt-gray-4) {--t: var(--c-gray-4)}
    .visualization :global(.vt-white) {--t: var(--c-white)}
    .visualization :global(.vt-black) {--t: var(--c-black)}

    /* STROKE */
    .visualization :global(.vs-t) {--s: transparent}
    .visualization :global(.vs-background) {--s: var(--color-background)}
    .visualization :global(.vs-foreground) {--s: var(--color-foreground)}
    .visualization :global(.vs-muted) {--s: var(--muted)}
    .visualization :global(.vs-muted-foreground) {--s: var(--muted-foreground)}
    .visualization :global(.vs-red) {--s: var(--c-red)}
    .visualization :global(.vs-purple) {--s: var(--c-purple)}
    .visualization :global(.vs-blue) {--s: var(--c-blue)}
    .visualization :global(.vs-green) {--s: var(--c-green)}
    .visualization :global(.vs-yellow) {--s: var(--c-yellow)}
    .visualization :global(.vs-orange) {--s: var(--c-orange)}
    .visualization :global(.vs-gray-1) {--s: var(--c-gray-1)}
    .visualization :global(.vs-gray-2) {--s: var(--c-gray-2)}
    .visualization :global(.vs-gray-3) {--s: var(--c-gray-3)}
    .visualization :global(.vs-gray-4) {--s: var(--c-gray-4)}
    .visualization :global(.vs-white) {--s: var(--c-white)}
    .visualization :global(.vs-black) {--s: var(--c-black)}
</style>
