<script lang="ts">
    interface FluentLabelProps {
        fluent: string;
    }
    let { fluent }: FluentLabelProps = $props();
</script>

<div
    class="px-2 flex flex-row items-center justify-end h-8 max-h-8 border border-transparent border-b-border select-none"
>
    <div class="bg-card rounded-sm h-6 px-3 flex flex-row items-center text-sm text-foreground">{fluent}</div>
</div>

<style>
    div {
        font-family: "JetBrains Mono";
    }
</style>
