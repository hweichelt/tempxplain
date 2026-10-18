<script lang="ts">
    import { Position, type NodeProps, Handle } from "@xyflow/svelte";
    import type { NodeData } from "./types";
    import type { ModelMembership } from "$lib/bindings";
    import bot from "../../../assets/bot.svg";

    interface NodeBaseProps {
        data: NodeData;
        variant:
            "rule_disjunction" | "rule_choice" | "rule_constraint" | "atom";
    }
    let { data, variant }: NodeBaseProps = $props();

    let model_membership: ModelMembership = $derived.by(() => {
        if (data.properties.models.length === 2) {
            return "both";
        } else if (data.properties.models.includes("ref")) {
            return "ref";
        } else if (data.properties.models.includes("foil")) {
            return "foil";
        }
        return "none";
    });
</script>

<div
    class="variant-{variant} models-{model_membership} node h-full w-full nodrag"
>
    {#if variant !== "rule_constraint"}
        <Handle type="source" position={Position.Right} isConnectable={false} />
    {/if}
    <Handle type="target" position={Position.Left} isConnectable={false} />
    <div class="label">
        {data.label}
    </div>
    {#if variant === "rule_constraint"}
        <div
            class="indicator-constraint bg-destructive flex items-center justify-center"
        >
            <img src={bot} alt="F" class="invert h-1.5 w-1.5" />
        </div>
    {/if}
</div>

<style>
    .node {
        --border-color: light-dark(#c3c3c3, #3c3c3c);
        font-family: "JetBrains Mono";
        background-color: var(--color-muted);
        border: solid 2px var(--color-border);
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(1rem);
    }
    .node .label {
        font-size: 0.7rem;
    }
    .node.models-foil {
        --border-color: var(--color-foil);
        border-color: var(--color-foil);
        background: color-mix(in srgb, var(--color-foil) 35%, transparent);
    }
    .node.models-ref {
        --border-color: var(--color-ref);
        border-color: var(--color-ref);
        background: color-mix(in srgb, var(--color-ref) 35%, transparent);
        opacity: 0.5;
    }
    .node.models-both {
        animation: node-both 3s linear infinite alternate-reverse;
    }
    @keyframes node-both {
        0% {
            --border-color: var(--color-foil);
            border-color: var(--color-foil);
            background: color-mix(in srgb, var(--color-foil) 35%, transparent);
        }
        100% {
            --border-color: var(--color-ref);
            border-color: var(--color-ref);
            background: color-mix(in srgb, var(--color-ref) 35%, transparent);
        }
    }
    .variant-rule_disjunction,
    .variant-rule_choice,
    .variant-rule_constraint {
        border-radius: 100rem;
    }
    .variant-rule_constraint {
        border-color: var(--color-destructive);
        background: color-mix(
            in srgb,
            var(--color-destructive) 35%,
            transparent
        );
        opacity: 0.5;
    }
    .variant-rule_choice::after {
        content: "*";
        position: absolute;
        top: -0.2rem;
        right: -0.2rem;
        height: 1rem;
        width: 1rem;
        border-radius: 50%;
        background: var(--border-color);
        font-size: 0.7rem;
        text-align: center;
    }
    .variant-rule_choice.models-both::after {
        animation: choice-both 3s linear infinite alternate-reverse;
    }
    @keyframes choice-both {
        0% {
            background: var(--color-foil);
        }
        100% {
            background: var(--color-ref);
        }
    }
    .variant-atom {
        border-radius: 0.5rem;
    }
    .indicator-constraint {
        position: absolute;
        height: 1rem;
        width: 1rem;
        padding-right: 0.15rem;
        right: -1rem;
        border-radius: 0 1rem 1rem 0;
    }
</style>
