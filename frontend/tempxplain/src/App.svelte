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
    import { ChevronLeft, ChevronRight } from "@lucide/svelte";
    import TooltipButton from "$lib/components/TooltipButton.svelte";
    import * as Tooltip from "$lib/components/ui/tooltip/index.js";
    import PanelLabel from "$lib/components/PanelLabel.svelte";
    import PlayButton from "$lib/components/PlayButton.svelte";
    import ExplanationGraph from "$lib/components/graph/ExplanationGraph.svelte";
    import QueryEditor from "$lib/components/QueryEditor.svelte";

    $effect(() => {
        backend.connect().catch(() => {});
        return () => backend.close();
    });

    let timeframe = $derived(program_state.explanation?.timeframe_explanation);
    let t_start = $derived(timeframe !== undefined ? timeframe[0] : 0);
    let t_end = $derived(timeframe !== undefined ? timeframe[1] : 0);
    let timestep = $derived(timeframe !== undefined ? timeframe[0] : 0);
    let fluents = $derived(program_state.explanation?.fluent_matrix);
    let visualization = $state(true);
    let filter: ModelMembership = $state("both");
    let t_counter = $state(1);
    let t_counter_seconds = $state(2);
    let t_conter_poll = $state(250);
    let t_counter_active = $state(false);
    let t_counter_running = $state(false);
    let query_dialog_open = $state(true);

    let keyboard_controls_blocked = $derived(
        t_counter_running || query_dialog_open,
    );

    function prev() {
        timestep = Math.max(t_start, timestep - 1);
    }
    function next() {
        timestep = Math.min(t_end, timestep + 1);
    }
    function onKeyDown(e: KeyboardEvent) {
        switch (e.key) {
            case "ArrowLeft":
                if (keyboard_controls_blocked) return;
                e.preventDefault();
                prev();
                break;
            case "ArrowRight":
                if (keyboard_controls_blocked) return;
                e.preventDefault();
                next();
                break;
        }
    }
</script>

<ModeWatcher />
<!-- Tooltips require a provider above every Tooltip.Root -->
<Tooltip.Provider>
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
            <QueryEditor bind:dialog_open={query_dialog_open} />
            <div class="flex items-center gap-2 p-4">
                <PlayButton
                    {t_start}
                    {t_end}
                    bind:timestep
                    bind:counter={t_counter}
                    step_seconds={t_counter_seconds}
                    polling_ms={t_conter_poll}
                    bind:active={t_counter_active}
                    bind:running={t_counter_running}
                />
                <TooltipButton
                    tooltip="Previous"
                    kbd="◄"
                    size="icon"
                    variant="secondary"
                    onclick={prev}
                    disabled={timestep === t_start || t_counter_running}
                    ><ChevronLeft /></TooltipButton
                >
                <div
                    class="bg-card h-8 w-8 rounded-md flex flex-row items-center justify-center select-none border"
                >
                    {timestep}
                </div>
                <TooltipButton
                    tooltip="Next"
                    kbd="►"
                    size="icon"
                    variant="secondary"
                    onclick={next}
                    disabled={timestep === t_end || t_counter_running}
                    ><ChevronRight /></TooltipButton
                >
                <ModelFilter bind:filter />
                <ConnectionIndicator />
                <ModeToggle />
            </div>
        </header>
        <main>
            <div
                id="graph"
                class="p-4 grid grid-rows-[auto_minmax(0,1fr)] gap-2"
            >
                <div class="flex flex-row gap-2 items-center">
                    <PanelLabel variant="light">EXPLANATION</PanelLabel>
                </div>
                <div>
                    {#if program_state.explanation === undefined}
                        <Skeleton class="w-full h-full" />
                    {:else}
                        <ExplanationGraph
                            graph={program_state.explanation.graph}
                            {timestep}
                        />
                    {/if}
                </div>
            </div>
            <div id="visualization" class="border-l">
                <ModelVisuals bind:filter bind:timestep bind:visualization />
            </div>
            <div id="timeline" class="border-t">
                {#if timeframe !== undefined && fluents !== undefined}
                    <Timeline
                        interval={timeframe}
                        bind:timestep
                        bind:filter
                        counter={t_counter}
                        counter_seconds={t_counter_seconds}
                        counter_active={t_counter_active}
                        {fluents}
                    />
                {:else}
                    <Skeleton class="w-full h-full" />
                {/if}
            </div>
        </main>
    </div>
</Tooltip.Provider>

<svelte:window on:keydown={onKeyDown} />

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
