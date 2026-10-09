<script lang="ts">
    import ExternalLink from "./ExternalLink.svelte";
import Hint from "./Hint.svelte";
    import InlineCode from "./InlineCode.svelte";
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
        <div class="header z-50 flex flex-row justify-start gap-2">
            <PanelLabel>REFERENCE</PanelLabel>
            <Hint>
                <div class="flex flex-col gap-2">
                    <div class="grid grid-cols-[1fr_auto] gap-2">
                        <div class="bg-muted dark:bg-card px-3 py-1 rounded-sm">What is the REFERENCE Model?</div>
                        <div class="h-7 w-7 rounded-sm bg-ref"></div>
                    </div>
                    <div class="text-sm text-muted-foreground px-3 border-l">
                        The reference model is the answer set of your original program (the world as it actually is).
                        If foil and reference models diverge, the query does not hold in this world.
                        Thus, the reference instance visualized here illustrates a valid solution without the query in the original program world.
                    </div>
                    <div class="bg-muted dark:bg-card text-muted-foreground px-3 py-1 rounded-sm text-sm items self-start">External Resources</div>
                    <div class="flex flex-row gap-2 flex-wrap">
                        <ExternalLink href="https://docs.potassco.org" title="Asplain Docs"/>
                        <ExternalLink href="https://docs.potassco.org" title="Asplain Paper"/>
                    </div>
                </div>
            </Hint>
        </div>
        <div class="viz z-50">
            <Visualization model="ref" timestep={timestep} {visualization}/>
        </div>
        <div class="grad absolute inset-0 bg-linear-180 from-ref/45 dark:from-ref/55 to-transparent z-10"></div>
        <div class="grad absolute bottom-0 left-[50%] translate-x-[-50%] translate-y-[50%] aspect-square w-full z-10 rounded-full bg-radial from-background to-70% to-transparent"></div>
    </div>
    <div class="border-t model foil relative p-4 grid grid-rows-[auto_minmax(0,1fr)] gap-2 overflow-hidden">
        <div class="header z-50 flex flex-row justify-start gap-2">
            <PanelLabel>FOIL</PanelLabel>
            <Hint>
                <div class="flex flex-col gap-2">
                    <div class="grid grid-cols-[1fr_auto] gap-2">
                        <div class="bg-muted dark:bg-card px-3 py-1 rounded-sm">What is the FOIL Model?</div>
                        <div class="h-7 w-7 rounded-sm bg-foil"></div>
                    </div>
                    <div class="text-sm text-muted-foreground px-3 border-l">
                        The foil model is the answer set of a minimally modified version of the reference program where the query holds.
                        We find this foil by selecting from the rules tagged with <InlineCode>@removable</InlineCode> to be removed and <InlineCode>@addable</InlineCode> to be added to the program.
                        Thus, through the atoms and rules that only hold in the foil, we can see what needed to change for the query to become true.
                    </div>
                    <div class="bg-muted dark:bg-card text-muted-foreground px-3 py-1 rounded-sm text-sm items self-start">External Resources</div>
                    <div class="flex flex-row gap-2 flex-wrap">
                        <ExternalLink href="https://docs.potassco.org" title="Asplain Docs"/>
                        <ExternalLink href="https://docs.potassco.org" title="Asplain Paper"/>
                    </div>
                </div>
            </Hint>
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
