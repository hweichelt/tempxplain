<script lang="ts">
    import PanelLabel from "./PanelLabel.svelte";
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
        <div class="header z-50 flex flex-row justify-start">
            <PanelLabel>REFERENCE</PanelLabel>
        </div>
        <div class="viz z-50">
            <Visualization model="ref" timestep={timestep} {visualization}/>
        </div>
        <div class="grad absolute inset-0 bg-linear-180 from-ref/45 dark:from-ref/55 to-transparent z-10"></div>
        <div class="grad absolute bottom-0 left-[50%] translate-x-[-50%] translate-y-[50%] aspect-square w-full z-10 rounded-full bg-radial from-background to-70% to-transparent"></div>
    </div>
    <div class="border-t model foil relative p-4 grid grid-rows-[auto_minmax(0,1fr)] gap-2 overflow-hidden">
        <div class="header z-50 flex flex-row justify-start">
            <PanelLabel>FOIL</PanelLabel>
        </div>
        <div class="viz z-50">
            <Visualization model="foil" timestep={timestep} {visualization} />
        </div>
        <div class="grad absolute inset-0 bg-linear-180 from-foil/45 dark:from-foil/55 to-transparent z-10 "></div>
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
    .model{
        min-height: 0;
        transition: padding var(--transition);
    }
    .grad{
        transition: opacity var(--transition);
    }
    .viz,
    .header,
    .label{
        transition: opacity calc(var(--transition) / 1.5);
    }
    .models.filter-ref {
        grid-template-rows: calc(100% - var(--height-hidden)) var(--height-hidden);
    }
    .models.filter-ref .model.foil {
        padding-top: 0;
        padding-bottom: 0;
        border-top-width: 0;
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
    .models.filter-foil .model.ref {
        padding-top: 0;
        padding-bottom: 0;
    }
    .models.filter-foil .model.ref .grad{
        opacity: 0;
    }
    .models.filter-foil .model.ref *{
        opacity: 0;
    }
</style>
