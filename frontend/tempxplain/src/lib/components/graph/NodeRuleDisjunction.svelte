<script lang="ts">
    import type { NodeProps } from "./types";
    import NodeBase from "./NodeBase.svelte";

    let { data, selected }: NodeProps = $props();
</script>

{#if data.properties.constraint}
    <NodeBase {data} {selected} variant="rule_constraint" />
{:else}
    <NodeBase {data} {selected} variant="rule_disjunction" />
{/if}
