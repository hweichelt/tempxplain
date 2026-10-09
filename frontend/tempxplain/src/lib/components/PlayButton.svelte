<script lang="ts">
    import { Pause, Play, Undo2 } from "@lucide/svelte";
    import TooltipButton from "./TooltipButton.svelte";
    import { onMount } from "svelte";

    interface PlayButtonProps {
        t_start: number;
        t_end: number;
        timestep: number;
        step_seconds?: number;
        polling_ms?: number;
        counter: number;
        active: boolean;
        running: boolean;
    }
    let { t_start, t_end, step_seconds = 2, polling_ms = 100, timestep = $bindable(), counter = $bindable(), active = $bindable(), running = $bindable() }: PlayButtonProps = $props();

    let tooltip = $derived(running? "Pause Playing" : timestep === t_end ? "Restart the Timeline": "Play the Timeline");

    let counter_ms = $derived(step_seconds * 1000);

   	onMount(() => {
		const interval = setInterval(() => {
		   if (running) {
				active = true;
				counter_ms = counter_ms - polling_ms;
				if (counter_ms < 0) {
				    // Reset ms counter and stop playing
					reset_counter()
					timestep = Math.min(t_end, timestep + 1)
					if (timestep === t_end) running = false;
				}
			} else {
			  reset_counter()
			}
		}, polling_ms);

		return () => {
			clearInterval(interval);
		};
	});

    function reset_counter() {
        active = false;
        counter_ms = step_seconds * 1000;
    }

    $effect(() => {
        // Calculate fractional counter
        counter = counter_ms / (step_seconds * 1000);
    });

    function onclick() {
        if (timestep === t_end) {
            timestep = t_start;
        }
        running = !running;
    }
</script>

<TooltipButton {tooltip} side="bottom" size="icon" {onclick}>
    {#if running}
        <Pause />
    {:else if timestep === t_end}
        <Undo2 />
    {:else}
        <Play />
    {/if}
</TooltipButton>
