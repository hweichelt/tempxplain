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
    import SectionNode from "./SectionNode.svelte";
    import FlowControl from "./FlowControl.svelte";
    import { layout_graph, section_id } from "./layout";
    import { program_state } from "$lib/state/program_state.svelte";
    import type { Graph } from "$lib/bindings";

    interface ExplanationGraphProps {
        graph: Graph;
        timestep: number;
    }
    let { graph, timestep }: ExplanationGraphProps = $props();

    const nodeTypes: NodeTypes = { section: SectionNode };

    let nodes = $state.raw<Node[]>([]);
    let edges = $state.raw<Edge[]>([]);
    let flow_control = $state<FlowControl>();

    async function layout(graph: Graph): Promise<void> {
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
            <FlowControl bind:this={flow_control} />
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
