<script lang="ts">
    import "./app.css";
    import { ModeWatcher } from "mode-watcher";
    import ModeToggle from "$lib/components/ModeToggle.svelte";
    import ConnectionIndicator from "$lib/components/ConnectionIndicator.svelte";
    import { backend } from "$lib/backend.svelte";
    import Badge from "$lib/components/ui/badge/badge.svelte";
    import Skeleton from "$lib/components/ui/skeleton/skeleton.svelte";
    import Timeline from "$lib/components/Timeline.svelte";
    import logo_dark from "./assets/logo.svg";
    import logo_light from "./assets/logo_light.svg";
    import text_dark from "./assets/tempxplain_text.svg";
    import text_light from "./assets/tempxplain_text_light.svg";
    import grad_dark from "./assets/gradient_color.png";
    import grad_light from "./assets/gradient_light.png";
    import Button from "$lib/components/ui/button/button.svelte";
    import { program_state } from "$lib/state/program_state.svelte";

    $effect(() => {
        backend.connect().catch(() => {});
        return () => backend.close();
    });

    let timeframe = $derived(program_state.explanation?.timeframe_explanation);
</script>

<ModeWatcher />
<div id="content">
    <header class="border-b flex items-center justify-between">
        <div class="h-full flex flex-row">
            <div class="logo-bg h-full flex flex-row items-center pl-6 pr-6">
                <img
                    src={logo_dark}
                    alt="logo"
                    class="size-8 dark:invert not-dark:hidden"
                />
                <img
                    src={logo_light}
                    alt="logo"
                    class="size-8 dark:invert dark:hidden"
                />
            </div>
            <img src={grad_dark} alt="" class="h-16 not-dark:hidden" />
            <img src={grad_light} alt="" class="h-16 dark:hidden" />
        </div>
        <img
            src={text_dark}
            alt="TempXplain"
            class="h-6 dark:invert not-dark:hidden"
        />
        <img
            src={text_light}
            alt="TempXplain"
            class="h-6 dark:invert dark:hidden"
        />
        <div class="flex items-center gap-2 p-4">
            <Button
                onclick={() =>
                    console.log(program_state.set_program(":- a, not a."))}
                >SET</Button
            >
            <Button onclick={() => console.log(program_state.program)}
                >GET</Button
            >
            <ConnectionIndicator />
            <ModeToggle />
        </div>
    </header>
    <main>
        <div id="graph" class="p-4 grid grid-rows-[auto_1fr] gap-4">
            <div class="flex flex-row gap-2 items-center">
                <Badge variant="secondary">EXPLANATION</Badge>
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
            {#if timeframe !== undefined}
                <Timeline
                    interval={timeframe}
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
            {:else}
                <Skeleton class="w-full h-full" />
            {/if}
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
    .logo-bg {
        background: light-dark(#cfd8dc, #37474f);
    }
</style>
