<script lang="ts">
    import type { NodeProps } from "./types";
    import NodeBase from "./NodeBase.svelte";

    let { data, selected }: NodeProps = $props();
</script>

<NodeBase {data} {selected} variant="rule_choice" />
