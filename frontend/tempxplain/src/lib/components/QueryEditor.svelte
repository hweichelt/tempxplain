<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import * as Field from "$lib/components/ui/field/index.js";
    import { Button, buttonVariants } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import BooleanIndicator from "./BooleanIndicator.svelte";

    interface QueryEditorProps {
        dialog_open: boolean;
    }
    let { dialog_open = $bindable() }: QueryEditorProps = $props();

    let query = $state("");
    let query_correct = $derived(query.length % 2 === 0 && query.length > 0);
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
                        class="absolute bottom-0 pointer-events-none flex justify-end px-2 py-1.5"
                    >
                        <BooleanIndicator value={query_correct} />
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
