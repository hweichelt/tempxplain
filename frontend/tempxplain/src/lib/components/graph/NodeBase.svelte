<script lang="ts">
    import { Position, type NodeProps, Handle } from "@xyflow/svelte";
    import type { NodeData } from "./types";
    import type { ModelMembership } from "$lib/bindings";
    import * as Popover from "$lib/components/ui/popover/index.js";
    import bot from "../../../assets/bot.svg";
    import { Asterisk, Minus, Plus, X } from "@lucide/svelte";

    interface NodeBaseProps {
        data: NodeData;
        variant:
            "rule_disjunction" | "rule_choice" | "rule_constraint" | "atom";
        selected?: boolean;
    }
    let { data, variant, selected = false }: NodeBaseProps = $props();

    let context_menu_open = $derived(selected);

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
    const rule_type_labels = {
        rule_disjunction: "Disjunction",
        rule_choice: "Choice",
        rule_constraint: "Constraint",
        atom: "Atom",
    };
    let rule_type_label: string = $derived(rule_type_labels[variant]);
    const atom_type_labels = {
        action: "Action",
        fluent: "Fluent",
    };
    let atom_type_label: string | undefined = $derived(
        data.properties.atom_type !== undefined
            ? atom_type_labels[data.properties.atom_type]
            : undefined,
    );
</script>

<div
    class="variant-{variant} models-{model_membership} node h-full w-full"
    class:selected
>
    {#if variant !== "rule_constraint"}
        <Handle type="source" position={Position.Right} isConnectable={false} />
    {/if}
    <Handle type="target" position={Position.Left} isConnectable={false} />
    <div class="content">
        <div class="label px-3 text-nowrap">
            {data.label}
        </div>
    </div>
    {#if variant === "rule_constraint"}
        <div
            class="indicator-constraint bg-destructive flex items-center justify-center"
        >
            <img src={bot} alt="F" class="invert h-1.5 w-1.5" />
        </div>
    {/if}
    {#if variant === "rule_choice"}
        <div class="indicator-choice flex items-center justify-center">
            <Asterisk size={11.5} stroke-width={2.75} color="white" />
        </div>
    {/if}
    {#if data.properties.addable}
        <div class="indicator-added flex items-center justify-center">
            <Plus size={11.5} stroke-width={2.75} color="white" />
        </div>
    {/if}
    {#if data.properties.removable}
        <div class="indicator-added flex items-center justify-center">
            <Minus size={11.5} stroke-width={2.75} color="white" />
        </div>
    {/if}
    {#if variant === "atom"}
        <div
            class="context absolute w-47 bg-muted border rounded-md shadow-2xl flex flex-col"
        >
            <div class="p-2 flex flex-col gap-2">
                <div
                    class="bg-card text-xs h-6 flex items-center px-2 rounded-sm"
                >
                    {rule_type_label}
                </div>
                <div
                    class="grid grid-cols-[1fr_auto] text-xs text-muted-foreground px-2 items-center gap-1"
                >
                    <div>Models</div>
                    <div class="justify-self-end">
                        <div class="flex flex-row gap-1">
                            {#if ["both", "ref"].includes(model_membership)}
                                <div class="bg-ref h-3 w-3 rounded-xs"></div>
                            {/if}
                            {#if ["both", "foil"].includes(model_membership)}
                                <div class="bg-foil h-3 w-3 rounded-xs"></div>
                            {/if}
                            {#if model_membership === "none"}
                                <div
                                    class="border h-3 w-3 rounded-xs flex items-center justify-center"
                                >
                                    <X width={9} class="opacity-25" />
                                </div>
                            {/if}
                        </div>
                    </div>
                    <div>Timestep</div>
                    <div class="justify-self-end">
                        {data.properties.time}
                    </div>
                    <div>Type</div>
                    <div class="justify-self-end">
                        {atom_type_label}
                    </div>
                </div>
            </div>
        </div>
    {:else}
        <div
            class="context absolute w-110 bg-muted border rounded-md shadow-2xl flex flex-col"
        >
            <div class="grid grid-cols-[3fr_4fr] border-b">
                <div class="border-r p-2 flex flex-col gap-2">
                    <div
                        class="bg-card text-xs h-6 flex items-center px-2 rounded-sm"
                    >
                        {rule_type_label}
                    </div>
                    <div
                        class="grid grid-cols-[1fr_auto] text-xs text-muted-foreground px-2 items-center gap-1"
                    >
                        <div>Models</div>
                        <div>
                            <div class="flex flex-row gap-1">
                                {#if ["both", "ref"].includes(model_membership)}
                                    <div
                                        class="bg-ref h-3 w-3 rounded-xs"
                                    ></div>
                                {/if}
                                {#if ["both", "foil"].includes(model_membership)}
                                    <div
                                        class="bg-foil h-3 w-3 rounded-xs"
                                    ></div>
                                {/if}
                                {#if model_membership === "none"}
                                    <div
                                        class="border h-3 w-3 rounded-xs flex items-center justify-center"
                                    >
                                        <X width={9} class="opacity-25" />
                                    </div>
                                {/if}
                            </div>
                        </div>
                        <div>Timestep</div>
                        <div class="justify-self-end">
                            {data.properties.time}
                        </div>
                        {#if data.properties.addable}
                            <div
                                class="col-span-2 rounded-sm bg-foreground/10 grid grid-cols-[auto_1fr] px-1 py-0.5 gap-1.5 items-center text-foreground mt-1"
                            >
                                <Plus
                                    color="var(--color-foreground)"
                                    size={12}
                                    stroke-width={3}
                                />
                                <div>Added in Foil</div>
                            </div>
                        {/if}
                        {#if data.properties.removable}
                            <div
                                class="col-span-2 rounded-sm bg-foreground/10 grid grid-cols-[auto_1fr] px-1 py-0.5 gap-1.5 items-center text-foreground mt-1"
                            >
                                <Minus
                                    color="var(--color-foreground)"
                                    size={12}
                                    stroke-width={3}
                                />
                                <div>Removed in Foil</div>
                            </div>
                        {/if}
                    </div>
                </div>
                <div class="text-xs text-muted-foreground p-2 rounded-sm">
                    {data.properties.label}
                </div>
            </div>
            <div
                class="codeblock text-[0.6rem] bg-card px-2 py-1 rounded-sm m-2 overflow-x-scroll"
            >
                <div class="text-nowrap">
                    {data.properties.first_order}
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .node {
        --border-color: light-dark(#c3c3c3, #3c3c3c);
        background-color: var(--color-muted);
        border: solid 2px var(--color-border);
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(1rem);
        outline: solid 0.1rem transparent;
        transition-property: outline-color, opacity;
        transition-duration: 200ms;
    }
    .node.selected {
        outline-color: var(--color-foreground);
        opacity: 1 !important;
    }
    .node .content {
        mask-image: linear-gradient(
            90deg,
            transparent,
            white 15%,
            white 80%,
            transparent
        );
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .node.variant-atom .content {
        justify-content: start;
        overflow-x: scroll;
    }
    .node .label {
        font-family: "JetBrains Mono";
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
        animation: node-both 5s linear infinite;
        background: linear-gradient(
            90deg,
            color-mix(in srgb, var(--color-ref) 35%, transparent) 20%,
            color-mix(in srgb, var(--color-foil) 35%, transparent) 40%,
            color-mix(in srgb, var(--color-foil) 35%, transparent) 60%,
            color-mix(in srgb, var(--color-ref) 35%, transparent) 80%
        );
        background-size: 500% 100%;
    }
    @keyframes node-both {
        0% {
            --border-color: var(--color-ref);
            border-color: var(--color-ref);
            background-position-x: 100%;
        }
        50% {
            --border-color: var(--color-foil);
            border-color: var(--color-foil);
        }
        100% {
            --border-color: var(--color-ref);
            border-color: var(--color-ref);
            background-position-x: 0%;
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
    @keyframes choice-both {
        0% {
            background: var(--color-ref);
        }
        50% {
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
    .indicator-choice {
        position: absolute;
        left: -0.2rem;
        top: -0.2rem;
        height: 1rem;
        width: 1rem;
        border-radius: 50%;
        background: var(--border-color);
        font-size: 0.7rem;
        text-align: center;
    }
    .indicator-added {
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
    .models-both .indicator-choice {
        animation: choice-both 5s linear infinite;
    }
    .node .context {
        position: absolute;
        bottom: 0;
        transform: translateY(100%);
        pointer-events: none;
        opacity: 0;
        transition-property: opacity, bottom;
        transition-duration: 200ms;
    }
    .node.selected .context {
        pointer-events: auto;
        bottom: -0.5rem;
        opacity: 1;
    }
    .node .context .codeblock {
        font-family: "JetBrains Mono";
    }
</style>
