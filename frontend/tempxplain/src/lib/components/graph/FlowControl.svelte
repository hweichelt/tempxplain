<script lang="ts">
    import { useSvelteFlow, type FitViewOptions } from "@xyflow/svelte";

    const flow = useSvelteFlow();

    export function pan(
        ids?: string[],
        options: FitViewOptions = {},
    ): Promise<boolean> {
        return flow.fitView({
            duration: 200,
            padding: 0.2,
            ...options,
            nodes: ids?.map((id) => ({ id })),
        });
    }
</script>
