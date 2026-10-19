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
        counter: number;
        counter_seconds: number;
        counter_active: boolean;
    }
    let {
        interval,
        timestep = $bindable(),
        filter = $bindable(),
        fluents,
        counter,
        counter_seconds,
        counter_active,
    }: TimelineProps = $props();

    let span = $derived(interval[1] + 1 - interval[0]);
    let grid_cols_steps = $derived(`9rem repeat(${span}, 1fr)`);
    let timestep_width = $state(0);
    let counter_percent = $derived(100 - counter * 100);

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
    <div
        class="grid shadow-lg z-30"
        style:grid-template-columns={grid_cols_steps}
    >
        <!-- TIMELINE -->
        <div class="relative bg-card border-b">
            <div
                class="absolute inset-2 border-2 border-muted-foreground/50 rounded-full overflow-hidden"
            >
                <div
                    id="progress"
                    class="absolute top-0 left-0 bottom-0 {counter_active
                        ? 'playing'
                        : ''}"
                    style:--length={`${counter_seconds * 1000}ms`}
                ></div>
            </div>
        </div>
        {#each { length: span } as _, i (i)}
            <div
                class="rounded-none bg-card border border-transparent border-b-border border-l-border text-sm h-8 flex flex-row items-center justify-center select-none"
            >
                {interval[0] + i}
            </div>
        {/each}
    </div>
    <div
        class="grid relative overflow-y-scroll"
        style:grid-template-columns={grid_cols_steps}
    >
        <!-- FLUENTS -->
        {#each Object.entries(fluents).sort() as [fluent, values]}
            <FluentLabel {fluent} />
            {#each { length: span } as _, t (t)}
                <div bind:clientWidth={timestep_width}>
                    <TimelineFluentIndicator
                        {fluent}
                        membership={values[t]}
                        active={t === timestep}
                        model_filter={filter}
                    />
                </div>
            {/each}
        {/each}
        <div class="absolute top-0 bottom-0 left-36 right-0 overflow-hidden">
            <div
                id="current"
                class="absolute border-2 border-white border-t-transparent border-b-transparent"
                style:--step-size={`${timestep_width}px`}
                style:--step={timestep}
            ></div>
        </div>
    </div>
    <div></div>
</div>

<style>
    #current {
        --border-width: 2px;

        width: calc(var(--step-size) + 2 * 0.05rem);
        height: calc(100% + 2 * var(--border-width));
        top: calc(-1 * var(--border-width));
        left: calc(var(--step) * (var(--step-size) + 0.01rem));
        transition: left 100ms;
        z-index: 10;
    }
    #current:before,
    #current:after {
        --width: 10rem;
        --border-width: 2px;
        --gradient-alpha: 25%;
        --gradient-color: var(--color-black);
        content: "";
        position: absolute;
        top: calc(-1 * var(--border-width));
        height: calc(100% + 2 * var(--border-width));
        width: var(--width);
    }
    #current:before {
        left: calc(-1 * var(--width) - var(--border-width));
        background: linear-gradient(
            to left,
            color-mix(
                in srgb,
                var(--gradient-color) var(--gradient-alpha),
                transparent
            ),
            transparent
        );
    }
    #current:after {
        right: calc(-1 * var(--width) - var(--border-width));
        background: linear-gradient(
            to right,
            color-mix(
                in srgb,
                var(--gradient-color) var(--gradient-alpha),
                transparent
            ),
            transparent
        );
    }
    #progress {
        --length: 0ms;

        background: linear-gradient(
            to left,
            color-mix(in srgb, var(--color-foreground) 50%, transparent),
            color-mix(in srgb, var(--color-foreground) 25%, transparent) 9rem
        );
    }
    #progress.playing {
        animation: progress-fill linear var(--length);
    }
    @keyframes progress-fill {
        from {
            width: 0;
        }
        to {
            width: 100%;
        }
    }
</style>
