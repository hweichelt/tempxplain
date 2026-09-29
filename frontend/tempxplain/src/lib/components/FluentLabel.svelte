<script lang="ts">
    interface FluentLabelProps {
        fluent: string;
    }
    let { fluent }: FluentLabelProps = $props();
</script>

<div
    class="bg-muted text-card-foreground py-0.5 px-2 rounded-md text-sm text-right"
>
    {fluent}
</div>

<style>
    div {
        font-family: "JetBrains Mono";
    }
</style>
