<script lang="ts">
    import type { Query } from "$lib/bindings";
    import Formula from "./Formula.svelte";

    interface QueriesProps {
        parsed_queries?: Query[];
        correct: boolean;
    }
    let { parsed_queries, correct }: QueriesProps = $props();
</script>

<div class="previews flex flex-col gap-2 {correct ? '' : 'wrong'}">
    {#if parsed_queries === undefined || parsed_queries.length === 0}
        <div id="query-preview" class="bg-card h-15 rounded-md"></div>
    {:else}
        {#each parsed_queries as q, i (i)}
            <div
                id="query-preview"
                class="relative bg-card h-15 rounded-md text-base flex items-center justify-center overflow-hidden"
            >
                <div
                    class="absolute top-1.5 left-1.5 px-1.5 py-0.5 bg-muted rounded-sm font-semibold text-muted-foreground text-xs"
                >
                    Q{i + 1}
                </div>
                <div
                    class="preview_wrapper absolute left-10 right-0 top-0 bottom-0"
                >
                    <div class="absolute inset-0 overflow-x-scroll">
                        <div class="pl-8 mr-20">
                            <Formula tex={q.tex} display={true} />
                        </div>
                    </div>
                </div>
            </div>
        {/each}
    {/if}
</div>

<style>
    .previews {
        transition: opacity 100ms;
    }
    .previews.wrong {
        opacity: 0.5;
    }
    .preview_wrapper:before,
    .preview_wrapper:after {
        content: "";
        z-index: 5;
        position: absolute;
        top: 0;
        bottom: 0;
        width: 2rem;
    }
    .preview_wrapper:before {
        left: 0;
        background: linear-gradient(90deg, var(--color-card) 15%, transparent);
    }
    .preview_wrapper:after {
        right: 0;
        background: linear-gradient(90deg, transparent, var(--color-card) 85%);
    }
</style>
