<script lang="ts">
    import Visualization from "./Visualization.svelte";

 interface ModelVisualsProps {
     filter: string;
     timestep: number;
     visualization: boolean;
 }
 let { filter = $bindable(), timestep = $bindable(), visualization = $bindable() }: ModelVisualsProps = $props();
</script>

<div class="models h-full filter-{filter}">
    <div class="model ref relative p-4 grid grid-rows-[auto_minmax(0,1fr)] gap-2 overflow-hidden">
        <div class="bg-card/75 label text-sm px-4 py-1 rounded-md justify-self-start font-semibold text-foreground/75 backdrop-blur-lg z-50">REFERENCE</div>
        <div class="viz z-50">
            <Visualization model="ref" timestep={timestep} {visualization}/>
        </div>
        <div class="grad absolute inset-0 bg-linear-180 from-ref/35 to-transparent z-10"></div>
        <div class="grad absolute bottom-0 left-[50%] translate-x-[-50%] translate-y-[50%] aspect-square w-full z-10 rounded-full bg-radial from-background to-70% to-transparent"></div>
    </div>
    <div class="border-t model foil relative p-4 grid grid-rows-[auto_minmax(0,1fr)] gap-2 overflow-hidden">
        <div class="bg-card/75 label text-sm px-4 py-1 rounded-md justify-self-start font-semibold text-foreground/75 backdrop-blur-lg z-50">FOIL</div>
        <div class="viz z-50">
            <Visualization model="foil" timestep={timestep} {visualization} />
        </div>
        <div class="grad absolute inset-0 bg-linear-180 from-foil/35 to-transparent z-10 "></div>
        <div class="grad absolute bottom-0 left-[50%] translate-x-[-50%] translate-y-[50%] aspect-square w-full z-10 rounded-full bg-radial from-background to-70% to-transparent"></div>
    </div>
</div>

<style>
    .models {
        display: grid;
        grid-template-rows: 50% 50%;
        transition: grid-template-rows var(--transition);

        --transition: 350ms;
        --height-hidden: 0px;
    }
    .grad{
        transition: opacity var(--transition);
    }
    .viz,
    .label{
        transition: opacity calc(var(--transition) / 1.5);
    }
    .models.filter-ref {
        grid-template-rows: calc(100% - var(--height-hidden)) var(--height-hidden);
    }
    .models.filter-ref .model.foil .grad{
        opacity: 0;
    }
    .models.filter-ref .model.foil *{
        opacity: 0;
    }
    .models.filter-foil {
        grid-template-rows: var(--height-hidden) calc(100% - var(--height-hidden));
    }
    .models.filter-foil .model.ref .grad{
        opacity: 0;
    }
    .models.filter-foil .model.ref *{
        opacity: 0;
    }
</style>
