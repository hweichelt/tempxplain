<script lang="ts">
    import { type NodeProps } from "@xyflow/svelte";
    import NodeBase from "./NodeBase.svelte";

    let { id, data }: NodeProps = $props();
</script>

<NodeBase {id} {data} variant="rule_choice" />
