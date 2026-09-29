<script lang="ts">
    import "./app.css";
    import { ModeWatcher } from "mode-watcher";
    import ModeToggle from "$lib/components/ModeToggle.svelte";
    import ConnectionIndicator from "$lib/components/ConnectionIndicator.svelte";
    import { backend } from "$lib/backend.svelte";
    import Badge from "$lib/components/ui/badge/badge.svelte";
    import Skeleton from "$lib/components/ui/skeleton/skeleton.svelte";
    import Timeline from "$lib/components/Timeline.svelte";

    $effect(() => {
        backend.connect().catch(() => {});
        return () => backend.close();
    });

    let timestep = $state(3);
    let timestep_min = $state(0);
    let timestep_max = $state(6);
</script>

<ModeWatcher />
<div id="content">
    <header class="border-b p-4 flex items-center justify-between">
        <div>TempXplain</div>
        <div class="flex items-center gap-2">
            <ConnectionIndicator />
            <ModeToggle />
        </div>
    </header>
    <main>
        <div id="graph" class="p-4 grid grid-rows-[auto_1fr] gap-4">
            <div class="flex flex-row gap-2 items-center">
                <Badge variant="secondary">EXPLANATION GRAPH</Badge>
            </div>
            <div>
                <Skeleton class="w-full h-full" />
            </div>
        </div>
        <div id="visualization" class="border-l grid grid-rows-2">
            <div class="p-4 grid grid-rows-[auto_1fr] gap-4">
                <Badge variant="secondary">REFERENCE</Badge>
                <div>
                    <Skeleton class="w-full h-full" />
                </div>
            </div>
            <div class="border-t p-4 grid grid-rows-[auto_1fr] gap-4">
                <Badge variant="secondary">FOIL</Badge>
                <div>
                    <Skeleton class="w-full h-full" />
                </div>
            </div>
        </div>
        <div id="timeline" class="p-4 border-t">
            <Timeline
                interval={[0, 10]}
                fluents={[
                    "at(1)",
                    "at(2)",
                    "at(3)",
                    "at(4)",
                    "called(1)",
                    "called(2)",
                    "called(3)",
                    "called(4)",
                    "served(1)",
                    "served(2)",
                    "served(3)",
                    "served(4)",
                ]}
            />
        </div>
    </main>
</div>

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
</style>
