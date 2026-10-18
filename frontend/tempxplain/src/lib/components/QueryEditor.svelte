<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import * as Field from "$lib/components/ui/field/index.js";
    import { Button, buttonVariants } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import BooleanIndicator from "./BooleanIndicator.svelte";
    import { query_state } from "$lib/state/query_state.svelte";
    import Formula from "./Formula.svelte";
    import OperatorButton from "./OperatorButton.svelte";

    interface QueryEditorProps {
        dialog_open: boolean;
    }
    let { dialog_open = $bindable() }: QueryEditorProps = $props();

    let query = $state("");
    let query_correct = $derived(query_state.error === undefined);

    let parsed_queries = $derived(query_state.parsed);

    function parse_query() {
        query_state.set_raw(query);
    }

    const operators = [
        {
            name: "Negation",
            tex: "\\lnot",
            symbol: "-<span></span>",
        },
        {
            name: "And",
            tex: "\\land",
            symbol: "<span></span> & <span></span>",
        },
        {
            name: "Or",
            tex: "\\lor",
            symbol: "<span ></span> | <span></span>",
        },
        {
            name: "Next",
            tex: "\\mathord{\\circ}",
            symbol: "X[<span></span>]",
        },
        {
            name: "Previous",
            tex: "\\bullet",
            symbol: "P[<span></span>]",
        },
        {
            name: "Always",
            tex: "\\square",
            symbol: "G[<span></span>]",
        },
        {
            name: "Eventually",
            tex: "\\lozenge",
            symbol: "F[<span></span>]",
        },
        {
            name: "Until",
            tex: "\\text{U}",
            symbol: "U[<span></span>,<span></span>]",
        },
        {
            name: "Since",
            tex: "\\text{S}",
            symbol: "S[<span></span>,<span></span>]",
        },
    ];
</script>

<Dialog.Root
    open={dialog_open}
    onOpenChange={(open) => {
        dialog_open = open;
    }}
>
    <form>
        <Dialog.Trigger
            type="button"
            class={buttonVariants({ variant: "outline" })}
        >
            Write Query
        </Dialog.Trigger>
        <Dialog.Content class="sm:max-w-3xl">
            <Dialog.Header>
                <Dialog.Title>Write Your Query</Dialog.Title>
                <Dialog.Description>
                    Compose your question query for finding a foil here. The
                    query should use the tempql format for temporal queries.
                    Find more information
                    <a
                        href="https://github.com/hweichelt/tempql#examples"
                        target="_blank"
                    >
                        here
                    </a>.
                </Dialog.Description>
            </Dialog.Header>
            <Field.Group>
                <Field.Field class="relative">
                    <Label for="query" class="mb-2">Operators</Label>
                    <div
                        class="grid gap-2 mb-3"
                        style="grid-template-columns: repeat({operators.length}, 1fr);"
                    >
                        {#each operators as operator}
                            <OperatorButton {operator} />
                        {/each}
                    </div>
                    <Label for="query" class="mb-2">Query</Label>
                    <Input
                        autofocus
                        id="query"
                        name="query"
                        class="font-mono"
                        placeholder="e.g. F[at(3)] @ 2"
                        autocomplete="off"
                        bind:value={query}
                        oninput={parse_query}
                    />
                    <div
                        class="absolute bottom-0 pointer-events-none flex justify-end px-2 py-1.5"
                    >
                        <BooleanIndicator value={query_correct} />
                    </div>
                </Field.Field>
                <Label for="username-1">Preview</Label>
                <div
                    class="previews flex flex-col gap-2 {query_correct
                        ? ''
                        : 'wrong'}"
                >
                    {#if parsed_queries === undefined || parsed_queries.length === 0}
                        <div
                            id="query-preview"
                            class="bg-card h-15 rounded-md"
                        ></div>
                    {:else}
                        {#each parsed_queries as q, i (i)}
                            <div
                                id="query-preview"
                                class="relative bg-card h-15 rounded-md text-base flex items-center justify-center"
                            >
                                <div
                                    class="absolute top-1.5 left-1.5 px-1.5 py-0.5 bg-muted rounded-sm font-semibold text-muted-foreground text-xs"
                                >
                                    Q{i + 1}
                                </div>
                                <Formula tex={q.tex} display={true} />
                            </div>
                        {/each}
                    {/if}
                </div>
            </Field.Group>
            <Dialog.Footer>
                <Dialog.Close
                    type="button"
                    class={buttonVariants({ variant: "outline" })}
                >
                    Exit
                </Dialog.Close>
                <Button
                    type="submit"
                    disabled={!query_correct || query.length === 0}
                >
                    Find Explanation
                </Button>
            </Dialog.Footer>
        </Dialog.Content>
    </form>
</Dialog.Root>

<style>
    .previews {
        transition: opacity 100ms;
    }
    .previews.wrong {
        opacity: 0.5;
    }
</style>
