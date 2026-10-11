<script lang="ts">
    import {
        SvelteFlow,
        Background,
        type Edge,
        type Node,
        type NodeTypes,
        Controls,
        BackgroundVariant,
    } from "@xyflow/svelte";
    import "@xyflow/svelte/dist/style.css";
    import { mode } from "mode-watcher";
    import Skeleton from "../ui/skeleton/skeleton.svelte";
    import SectionNode from "./SectionNode.svelte";
    import { example_graph, type GraphData } from "./graph_data";
    import { layout_graph } from "./layout";

    interface ExplanationGraphProps {
        graph?: GraphData;
    }
    let { graph = example_graph }: ExplanationGraphProps = $props();

    const nodeTypes: NodeTypes = { section: SectionNode };

    let nodes = $state.raw<Node[]>([]);
    let edges = $state.raw<Edge[]>([]);

    async function layout(graph: GraphData): Promise<void> {
        const result = await layout_graph(graph);
        nodes = result.nodes;
        edges = result.edges;
    }
</script>

{#await layout(graph)}
    <Skeleton class="w-full h-full" />
{:then}
    <div class="w-full h-full border rounded-md overflow-hidden">
        <SvelteFlow
            bind:nodes
            bind:edges
            {nodeTypes}
            fitView
            colorMode={mode.current}
            proOptions={{ hideAttribution: true }}
        >
            <Background variant={BackgroundVariant.Dots} />
            <Controls />
        </SvelteFlow>
    </div>
{:catch error}
    <div
        class="text-foreground bg-destructive px-4 py-1 text-sm rounded-full justify-self-center self-center"
    >
        Layout failed: {error.message}
    </div>
{/await}
