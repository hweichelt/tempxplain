<script lang="ts">
    import type { NodeProps } from "./types";
    import NodeBase from "./NodeBase.svelte";

    let { data }: NodeProps = $props();
</script>

<NodeBase {data} variant="atom" />
