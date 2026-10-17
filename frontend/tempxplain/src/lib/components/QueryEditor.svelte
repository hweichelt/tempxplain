<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import * as Field from "$lib/components/ui/field/index.js";
    import { Button, buttonVariants } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { Check, Cross, X } from "@lucide/svelte";
    import { derived } from "svelte/store";

    interface QueryEditorProps {
        dialog_open: boolean;
    }
    let { dialog_open = $bindable() }: QueryEditorProps = $props();

    let query = $state("");
    let query_correct = $state(false);

    let query_correct_class = $derived(
        query_correct
            ? "bg-success/40 border-success"
            : "bg-destructive/40 border-destructive",
    );
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
        <Dialog.Content class="sm:max-w-xl">
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
                    <Label for="query" class="mb-2">Query</Label>
                    <Input
                        autofocus
                        id="query"
                        name="query"
                        class="font-mono"
                        placeholder="e.g. F[at(3)] @ 2"
                        autocomplete="off"
                        bind:value={query}
                    />
                    <div
                        class="absolute bottom-1.5 right-2 h-5 w-5! flex items-center justify-center border-2 rounded-full border {query_correct_class}"
                    >
                        {#if query_correct}
                            <Check class="h-3 w-3" />
                        {:else}
                            <X class="h-3 w-3" />
                        {/if}
                    </div>
                </Field.Field>
                <Label for="username-1">Preview</Label>
                <div id="query-preview" class="bg-card h-25 rounded-md"></div>
            </Field.Group>
            <Dialog.Footer>
                <Dialog.Close
                    type="button"
                    class={buttonVariants({ variant: "outline" })}
                >
                    Exit
                </Dialog.Close>
                <Button type="submit" disabled={!query_correct}>
                    Find Explanation
                </Button>
            </Dialog.Footer>
        </Dialog.Content>
    </form>
</Dialog.Root>
