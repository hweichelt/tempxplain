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
    let grid_cols_steps = $derived(`7rem repeat(${span}, 1fr) auto`);

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

<div class="grid grid-rows-[auto_minmax(0,1fr)] gap-4 h-full">
    <div class="grid gap-2" style:grid-template-columns={grid_cols_steps}>
        <!-- TIMELINE -->
        <Button
            variant="secondary"
            size="icon"
            class="flex flex-row justify-self-end"
            onclick={prev}
        >
            <ChevronLeft />
        </Button>
        {#each { length: span } as _, i (i)}
            <Button
                variant="secondary"
                class={t_class(
                    interval[0] + i,
                    "bg-primary text-primary-foreground",
                )}
                onclick={() => go_to(interval[0] + i)}>{interval[0] + i}</Button
            >
        {/each}
        <Button variant="secondary" size="icon" onclick={next}>
            <ChevronRight />
        </Button>
    </div>
    <div
        class="grid overflow-y-scroll gap-2"
        style:grid-template-columns={grid_cols_steps}
    >
        <!-- FLUENTS -->
        {#each Object.entries(fluents).sort() as [fluent, values]}
            <FluentLabel {fluent} />
            {#each { length: span } as _, t (t)}
                <TimelineFluentIndicator fluent={fluent} membership={values[t]} active={t === timestep} model_filter={filter} />
            {/each}
            <div class="w-8"></div>
        {/each}
    </div>
</div>
