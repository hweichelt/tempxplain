<script lang="ts">
    import type { Snippet } from "svelte";

    interface InlineCodeProps {
        children: Snippet;
    }
    let { children }: InlineCodeProps = $props();
</script>

<div class="bg-foreground/10 text-xs px-1.5 py-0.5 rounded-sm inline">
    {@render children()}
</div>

<style>
    div {
        font-family: "JetBrains Mono";
    }
</style>
