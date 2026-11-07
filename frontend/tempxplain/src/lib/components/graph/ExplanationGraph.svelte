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
    import { untrack } from "svelte";
    import { mode } from "mode-watcher";
    import Skeleton from "../ui/skeleton/skeleton.svelte";
    import SectionNode from "./SectionNode.svelte";
    import FlowControl from "./FlowControl.svelte";
    import { layout_graph, section_id } from "./layout";
    import type { Graph } from "$lib/bindings";
    import type { NodeData } from "./types";
    import { Button } from "$lib/components/ui/button";
    import { Minus, Plus } from "@lucide/svelte";
    import NodeRuleChoice from "$lib/components/graph/NodeRuleChoice.svelte";
    import NodeRuleDisjunction from "$lib/components/graph/NodeRuleDisjunction.svelte";
    import NodeAtom from "$lib/components/graph/NodeAtom.svelte";

    interface ExplanationGraphProps {
        graph: Graph;
        timestep: number;
    }
    let { graph, timestep }: ExplanationGraphProps = $props();

    const nodeTypes: NodeTypes = {
        section: SectionNode,
        rule_choice: NodeRuleChoice,
        rule_disjunction: NodeRuleDisjunction,
        atom: NodeAtom,
        default: NodeAtom,
    };

    let nodes = $state.raw<Node[]>([]);
    let edges = $state.raw<Edge[]>([]);
    let selected: Node | undefined = $state();

    let flow_control = $state<FlowControl>();

    type ChangeKind = "added" | "removed";
    const changed_nodes = $derived(
        nodes.flatMap(
            (node): { node: Node; kind: ChangeKind; constraint: boolean }[] => {
                const properties = (node.data as Partial<NodeData>).properties;
                if (properties === undefined) return []; // section nodes
                const in_ref = properties.programs.includes("ref");
                const in_foil = properties.programs.includes("foil");
                const is_constraint = properties.constraint === true;
                if (in_ref && !in_foil)
                    return [
                        { node, kind: "removed", constraint: is_constraint },
                    ];
                if (in_foil && !in_ref)
                    return [{ node, kind: "added", constraint: is_constraint }];
                return [];
            },
        ),
    );

    function change_classes(kind: ChangeKind, is_constraint: boolean): string {
        if (is_constraint)
            return "bg-destructive hover:bg-destructive dark:hover:bg-destructive";
        return {
            added: "bg-foil hover:bg-foil dark:hover:bg-foil",
            removed: "bg-ref hover:bg-ref dark:hover:bg-ref",
        }[kind];
    }

    // updater variable for focusing the current timestep
    let initialized = $state(0);

    const timepoints = $derived(
        new Set(
            graph.nodes.map((node) => node.time).filter((t) => t !== undefined),
        ),
    );

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

    // pan to the current timestep if the flow has been initialized
    $effect(() => {
        if (initialized === 0) return;
        const ids = timepoints.has(timestep)
            ? [section_id(timestep)]
            : undefined;
        untrack(() => focus(ids));
    });
</script>

{#await layout(graph)}
    <Skeleton class="w-full h-full" />
{:then}
    <div class="grid grid-cols-[1fr_auto] h-full gap-2">
        <div class="w-full h-full border rounded-md overflow-hidden">
            <SvelteFlow
                bind:nodes
                bind:edges
                {nodeTypes}
                fitView
                colorMode={mode.current}
                proOptions={{ hideAttribution: true }}
                oninit={() => initialized++}
                nodesDraggable={false}
                selectionKey={null}
                multiSelectionKey={null}
                selectionOnDrag={false}
                onselectionchange={({ nodes: selected_nodes }) => {
                    selected = selected_nodes[0];
                }}
            >
                <FlowControl bind:this={flow_control} />
                <Background variant={BackgroundVariant.Dots} />
                <Controls />
            </SvelteFlow>
        </div>
        <div
            class="p-4 border rounded-md max-w-12 flex flex-col gap-2 items-center"
        >
            {#each changed_nodes as { node, kind, constraint } (node.id)}
                <Button
                    variant="ghost"
                    size="icon-sm"
                    class="rounded-full border-2 cursor-pointer {change_classes(
                        kind,
                        constraint,
                    )}"
                    title="{kind}: {node.data.label}"
                    onclick={() => focus([node.id], { maxZoom: 1.5 })}
                >
                    {#if kind === "added"}
                        <Plus
                            size={12}
                            stroke-width={3}
                            class="not-dark:invert"
                        />
                    {:else}
                        <Minus
                            size={12}
                            stroke-width={3}
                            class="not-dark:invert"
                        />
                    {/if}
                </Button>
            {/each}
        </div>
    </div>
{:catch error}
    <div
        class="text-foreground bg-destructive px-4 py-1 text-sm rounded-full justify-self-center self-center"
    >
        Layout failed: {error.message}
    </div>
{/await}
