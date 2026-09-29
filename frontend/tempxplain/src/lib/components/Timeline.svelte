<script lang="ts">
    import Button from "./ui/button/button.svelte";
    import { ChevronRight, ChevronLeft } from "@lucide/svelte";
    import Skeleton from "./ui/skeleton/skeleton.svelte";
    import FluentLabel from "./FluentLabel.svelte";

    interface TimelineProps {
        interval: [number, number];
        fluents: string[];
    }
    let { interval, fluents }: TimelineProps = $props();

    let span = $derived(interval[1] + 1 - interval[0]);
    let grid_cols_steps = $derived(`7rem repeat(${span}, 1fr) auto`);

    let timestep_current: number = $state(interval[0]);

    function t_class(t: number, c: string): string {
        return timestep_current === t ? c : "";
    }

    function next(): void {
        timestep_current = Math.min(timestep_current + 1, interval[1]);
    }
    function prev(): void {
        timestep_current = Math.max(timestep_current - 1, interval[0]);
    }
    function go_to(t: number): void {
        timestep_current = Math.max(Math.min(t, interval[1]), interval[0]);
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
                class={t_class(i, "bg-primary text-primary-foreground")}
                onclick={() => go_to(i)}>{i}</Button
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
        {#each fluents as fluent}
            <FluentLabel {fluent} />
            {#each { length: span } as _, i (i)}
                <Skeleton />
            {/each}
            <div class="w-8"></div>
        {/each}
    </div>
</div>
