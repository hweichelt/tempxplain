<script lang="ts">
    import "./app.css";
    import { ModeWatcher } from "mode-watcher";
    import ModeToggle from "$lib/components/ModeToggle.svelte";
    import ConnectionIndicator from "$lib/components/ConnectionIndicator.svelte";
    import { backend } from "$lib/backend.svelte";
    import Badge from "$lib/components/ui/badge/badge.svelte";
    import Skeleton from "$lib/components/ui/skeleton/skeleton.svelte";
    import Timeline from "$lib/components/Timeline.svelte";
    import text_dark from "./assets/tempxplain_text.svg";
    import text_light from "./assets/tempxplain_text_light.svg";
    import { program_state } from "$lib/state/program_state.svelte";
    import ModelFilter from "$lib/components/ModelFilter.svelte";
    import ModelVisuals from "$lib/components/ModelVisuals.svelte";
    import type { ModelMembership } from "$lib/bindings";

    $effect(() => {
        backend.connect().catch(() => {});
        return () => backend.close();
    });

    let timeframe = $derived(program_state.explanation?.timeframe_explanation);
    let timestep = $state(0);
    let fluents = $derived(program_state.explanation?.fluent_matrix);
    let visualization = $state(true);
    let filter: ModelMembership = $state("both");
</script>

<ModeWatcher />
<div id="content">
    <header class="border-b flex items-center justify-between">
        <div class="px-6">
            <img
                src={text_dark}
                alt="TempXplain"
                class="h-6 dark:invert not-dark:hidden"
            />
            <img
                src={text_light}
                alt="TempXplain"
                class="h-6 dark:invert dark:hidden"
            />
        </div>
        <div class="flex items-center gap-2 p-4">
            <ModelFilter bind:filter />
            <ConnectionIndicator />
            <ModeToggle />
        </div>
    </header>
    <main>
        <div id="graph" class="p-4 grid grid-rows-[auto_minmax(0,1fr)] gap-4">
            <div class="flex flex-row gap-2 items-center">
                <Badge variant="secondary">EXPLANATION</Badge>
            </div>
            <div>
                <Skeleton class="w-full h-full" />
            </div>
        </div>
        <div id="visualization" class="border-l">
            <ModelVisuals bind:filter bind:timestep bind:visualization />
        </div>
        <div id="timeline" class="p-4 border-t">
            {#if timeframe !== undefined && fluents !== undefined}
                <Timeline
                    interval={timeframe}
                    bind:timestep={timestep}
                    bind:filter
                    fluents={fluents}
                />
            {:else}
                <Skeleton class="w-full h-full" />
            {/if}
        </div>
    </main>
</div>

<style>
    #content {
        display: grid;
        grid-template-rows: auto minmax(0, 1fr);
        width: 100vw;
        height: 100vh;
        max-height: 100vh;
    }
    main {
        display: grid;
        grid-template-columns: 2fr 1fr;
        grid-template-rows: minmax(0, 2fr) minmax(0, 1fr);
        grid-template-areas:
            "exp viz"
            "tim viz";
    }
    #graph {
        grid-area: exp;
    }
    #visualization {
        grid-area: viz;
    }
    #timeline {
        grid-area: tim;
    }
    .logo-bg {
        background: light-dark(#cfd8dc, #37474f);
    }
</style>
