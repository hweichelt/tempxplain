<script lang="ts">
    import type { NodeProps } from "./types";
    import NodeBase from "./NodeBase.svelte";

    let { data }: NodeProps = $props();
</script>

{#if data.properties.constraint}
    <NodeBase {data} variant="rule_constraint" />
{:else}
    <NodeBase {data} variant="rule_disjunction" />
{/if}
