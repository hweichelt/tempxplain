<script lang="ts">
    import Button from "./ui/button/button.svelte";
    import { ChevronRight, ChevronLeft } from "@lucide/svelte";
    import Skeleton from "./ui/skeleton/skeleton.svelte";
    import FluentLabel from "./FluentLabel.svelte";
    import TimelineFluentIndicator from "./TimelineFluentIndicator.svelte";
    import type { ModelMembership } from "$lib/bindings";

    interface TimelineProps {
        interval: [number, number];
        timestep: number;
        filter: ModelMembership;
        fluents: Record<string, ModelMembership[]>;
    }
    let { interval, timestep = $bindable(), filter = $bindable(), fluents }: TimelineProps = $props();

    let span = $derived(interval[1] + 1 - interval[0]);
    let grid_cols_steps = $derived(`9rem repeat(${span}, 1fr)`);

    function t_class(t: number, c: string): string {
        return timestep === t ? c : "";
    }

    function next(): void {
        timestep = Math.min(timestep + 1, interval[1]);
    }
    function prev(): void {
        timestep = Math.max(timestep - 1, interval[0]);
    }
    function go_to(t: number): void {
        timestep = Math.max(Math.min(t, interval[1]), interval[0]);
    }
</script>

<div class="grid grid-rows-[auto_auto_minmax(0,1fr)] h-full">
    <div class="grid shadow-lg z-30" style:grid-template-columns={grid_cols_steps}>
        <!-- TIMELINE -->
        <div class="bg-card border-b"></div>
        {#each { length: span } as _, i (i)}
            <div class="rounded-none bg-card border border-transparent border-b-border border-l-border text-sm h-8 flex flex-row items-center justify-center select-none">{interval[0] + i}</div>
        {/each}
    </div>
    <div
        class="grid overflow-y-scroll"
        style:grid-template-columns={grid_cols_steps}
    >
        <!-- FLUENTS -->
        {#each Object.entries(fluents).sort() as [fluent, values]}
            <FluentLabel {fluent} />
            {#each { length: span } as _, t (t)}
                <TimelineFluentIndicator fluent={fluent} membership={values[t]} active={t === timestep} model_filter={filter} />
            {/each}
        {/each}
    </div>
    <div></div>
</div>
