<script lang="ts">
    import type { ModelMembership } from "$lib/bindings";
    import * as Tabs from "$lib/components/ui/tabs/index.js";

    interface ModelFilterProps {
        filter: string;
        model_status: ModelMembership;
    }
    let { filter = $bindable(), model_status }: ModelFilterProps = $props();

    let status_has_been_both = $state(false);
    const tabs = [
        {
            value: "ref",
            title: "Reference",
        },
        {
            value: "foil",
            title: "Foil",
        },
        {
            value: "both",
            title: "Both",
        },
    ];
    $effect(() => {
        // Set filter to "both" when a foil first becomes available
        if (model_status === "both" && !status_has_been_both) {
            status_has_been_both = true;
            filter = "both";
        }
    });
</script>

<Tabs.Root bind:value={filter}>
    <Tabs.List>
        <Tabs.Trigger value="ref" class="cursor-pointer">Reference</Tabs.Trigger
        >
        <Tabs.Trigger
            value="foil"
            class="cursor-pointer"
            disabled={model_status !== "both"}>Foil</Tabs.Trigger
        >
        <Tabs.Trigger
            value="both"
            class="cursor-pointer"
            disabled={model_status !== "both"}>Both</Tabs.Trigger
        >
    </Tabs.List>
    <div
        class="relative h-8 w-8 bg-card rounded-md flex flex-row overflow-hidden"
    >
        <div
            class="absolute z-10 inset-0 border-3 border-white/25 rounded-md"
        ></div>
        <Tabs.Content value="ref"
            ><div class="w-8 h-8 bg-ref"></div></Tabs.Content
        >
        <Tabs.Content value="foil"
            ><div class="w-8 h-8 bg-foil"></div></Tabs.Content
        >
        <Tabs.Content value="both"
            ><div
                class="w-8 h-8 bg-linear-90 from-10% to-90% from-foil to-ref"
            ></div></Tabs.Content
        >
    </div>
</Tabs.Root>
