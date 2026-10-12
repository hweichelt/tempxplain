<script lang="ts">
    import {
        SvelteFlow,
        Background,
        BackgroundVariant,
        Controls,
        type Edge,
        type FitViewOptions,
        type Node,
        type NodeTypes,
    } from "@xyflow/svelte";
    import "@xyflow/svelte/dist/style.css";
    import { mode } from "mode-watcher";
    import Skeleton from "../ui/skeleton/skeleton.svelte";
    import Button from "../ui/button/button.svelte";
    import SectionNode from "./SectionNode.svelte";
    import FlowControl from "./FlowControl.svelte";
    import { example_graph, type GraphData } from "./graph_data";
    import { layout_graph, section_id } from "./layout";

    interface ExplanationGraphProps {
        graph?: GraphData;
    }
    let { graph = example_graph }: ExplanationGraphProps = $props();

    const nodeTypes: NodeTypes = { section: SectionNode };

    let nodes = $state.raw<Node[]>([]);
    let edges = $state.raw<Edge[]>([]);
    let flow_control = $state<FlowControl>();

    async function layout(graph: GraphData): Promise<void> {
        const result = await layout_graph(graph);
        nodes = result.nodes;
        edges = result.edges;
    }

    export function focus(
        ids?: string[],
        options?: FitViewOptions,
    ): Promise<boolean> {
        return flow_control?.pan(ids, options) ?? Promise.resolve(false);
    }

    const timepoints = $state([0, 1, 2]);
</script>

{#await layout(graph)}
    <Skeleton class="w-full h-full" />
{:then}
    <div class="relative h-full w-full">
        <div
            class="absolute top-2 right-2 z-20 flex gap-1 mb-2 bg-card p-2 rounded-lg border"
        >
            <Button size="sm" variant="outline" onclick={() => focus()}
                >all</Button
            >
            {#each timepoints as t (t)}
                <Button
                    size="sm"
                    variant="outline"
                    onclick={() => focus([section_id(t)])}
                >
                    {t ?? "static"}
                </Button>
            {/each}
        </div>
        <div class="w-full h-full border rounded-md overflow-hidden">
            <SvelteFlow
                bind:nodes
                bind:edges
                {nodeTypes}
                fitView
                colorMode={mode.current}
                proOptions={{ hideAttribution: true }}
            >
                <FlowControl bind:this={flow_control} />
                <Background variant={BackgroundVariant.Dots} />
                <Controls />
            </SvelteFlow>
        </div>
    </div>
{:catch error}
    <div
        class="text-foreground bg-destructive px-4 py-1 text-sm rounded-full justify-self-center self-center"
    >
        Layout failed: {error.message}
    </div>
{/await}
