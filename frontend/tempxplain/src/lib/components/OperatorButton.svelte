<script lang="ts">
    import Formula from "./Formula.svelte";

    interface OperatorButtonProps {
        operator: { name: string; tex: string; symbol: string };
    }
    let { operator }: OperatorButtonProps = $props();
</script>

<div class="bg-card rounded-md flex flex-col items-center gap-1.5">
    <div
        class="border-b text-muted-foreground text-xs text-center py-1.5 w-full"
    >
        {operator.name}
    </div>
    <div>
        <Formula tex={operator.tex} />
    </div>
    <div class="symbol bg-muted px-1 rounded-xs mb-1.5">
        {@html operator.symbol}
    </div>
</div>

<style>
    .symbol {
        font-family: "JetBrains Mono";
    }
    :global(.symbol > span) {
        display: inline-block;
        height: 0.85rem;
        width: 0.5rem;
        background: color-mix(
            in srgb,
            var(--color-muted-foreground) 25%,
            transparent
        );
        border-radius: 0.15rem;
        vertical-align: -0.1rem;
        margin: 0 0.1rem;
    }
</style>
