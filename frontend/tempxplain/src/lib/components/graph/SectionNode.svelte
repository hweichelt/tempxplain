<script lang="ts">
    import type { NodeProps } from "@xyflow/svelte";
    import type { SectionData } from "./layout";

    let { data, width, height }: NodeProps & { data: SectionData } = $props();
</script>

<div
    class="h-full w-full rounded-lg border bg-muted/40 dark:bg-card/40"
    style:width="{width}px"
    style:height="{height}px"
>
    <div
        class="px-3 py-1 text-sm font-semibold text-muted-foreground select-none"
    >
        {data.label}
    </div>
</div>
