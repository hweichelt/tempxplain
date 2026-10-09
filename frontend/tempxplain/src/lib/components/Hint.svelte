<script lang="ts">
    import type { Snippet } from "svelte";
    import HoverCard from "$lib/components/HoverCard.svelte";

    interface PanelLabelProps {
      variant?: "dark" | "light";
      children: Snippet;
    }
    let { variant = "dark", children }: PanelLabelProps = $props();

    let variant_classes = {
      "dark": "bg-card/75",
      "light": "bg-foreground/10",
    }
</script>

<HoverCard class="w-76" content_align="start">
    {#snippet trigger()}
        <div class="label text-sm h-7 w-7 flex flex-row items-center justify-center rounded-md justify-self-start font-semibold text-foreground/75 backdrop-blur-lg select-none {variant_classes[variant]}">
            ?
        </div>
    {/snippet}
    {@render children()}
</HoverCard>



<style>
    div {
        font-family: "JetBrains Mono";
    }
</style>
