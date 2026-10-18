<script lang="ts">
    import { Position, type NodeProps, Handle } from "@xyflow/svelte";

    interface NodeBaseProps {
        id: string;
        data: NodeProps["data"];
        variant: "rule_disjunction" | "rule_choice" | "atom";
    }
    let { id, data, variant }: NodeBaseProps = $props();
</script>

<div class="variant-{variant} node h-full w-full nodrag">
    <Handle type="source" position={Position.Right} />
    <Handle type="target" position={Position.Left} />
    <div class="label">
        {data.label}
    </div>
</div>

<style>
    .node {
        font-family: "JetBrains Mono";
        background-color: var(--color-muted);
        border: solid 2px var(--color-border);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .node .label {
        font-size: 0.7rem;
    }
    .variant-rule_disjunction {
        border-radius: 100rem;
    }
    .variant-atom {
        border-radius: 0.5rem;
    }
</style>
