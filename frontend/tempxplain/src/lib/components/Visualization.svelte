<script lang="ts">
    import type { Model } from "$lib/bindings";
    import { visualization_state } from "$lib/state/visualization_state.svelte";
    import Skeleton from "./ui/skeleton/skeleton.svelte";


    interface VisualizationProps {
        model: Model;
        timestep: number;
        visualization: boolean;
    }
    let { model, timestep, visualization = false }: VisualizationProps = $props();
</script>

<div class="bg-card w-full h-full rounded-md flex flex-row items-center justify-center p-4">
  {#if visualization}
      {#await visualization_state.get(model, timestep)}
          <Skeleton class="w-full h-full" />
      {:then image}
        {#if image === undefined}
            <div class="text-foreground bg-destructive px-4 py-1 text-sm rounded-full">Visualization Error</div>
        {:else}
            <img src={image} alt="Visualization of the {model} model" class="h-full w-full object-contain"/>
        {/if}
      {:catch error}
          <div class="text-foreground bg-destructive px-4 py-1 text-sm rounded-full">{error.message}</div>
      {/await}
  {:else}
    <div class="text-muted-foreground">No Visualization Specified</div>
  {/if}
</div>
