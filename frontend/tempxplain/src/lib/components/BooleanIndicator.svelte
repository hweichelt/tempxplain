<script lang="ts">
    import { Check, X } from "@lucide/svelte";

    interface BooleanIndicator {
        value: boolean;
    }
    let { value }: BooleanIndicator = $props();

    let value_class = $derived(
        value
            ? "bg-success/40 border-success"
            : "bg-destructive/40 border-destructive",
    );
</script>

<div
    class="h-5 w-5! flex items-center justify-center border-2 rounded-full backdrop-blur-lg {value_class} transition-colors"
>
    {#if value}
        <Check class="h-3 w-3" />
    {:else}
        <X class="h-3 w-3" />
    {/if}
</div>

<style>
    div {
        font-family: "JetBrains Mono";
    }
</style>
