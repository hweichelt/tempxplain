<script lang="ts">
    import type { Snippet } from "svelte";

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

<div class="label text-sm px-4 py-1 rounded-md justify-self-start font-semibold text-foreground/75 backdrop-blur-lg select-none {variant_classes[variant]}">
    {@render children()}
</div>


<style>
    div {
        font-family: "JetBrains Mono";
    }
</style>
