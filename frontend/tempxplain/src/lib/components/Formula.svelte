<script lang="ts">
    import katex from "katex";

    interface FormulaProps {
        tex: string;
        display?: boolean;
    }
    let { tex, display = false }: FormulaProps = $props();

    let html = $derived(
        katex.renderToString(tex, {
            displayMode: display,
            throwOnError: false,
        }),
    );
</script>

<div class="formula">{@html html}</div>
