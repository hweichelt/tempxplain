<script lang="ts">
    import type { ModelMembership } from "$lib/bindings";

    interface TimelineFluentIndicatorProps {
        fluent: string;
        membership: ModelMembership;
        active?: boolean;
    }
    let { fluent, membership, active = false }: TimelineFluentIndicatorProps = $props();

    let classes_membership = {
      "none": "bg-card",
      "ref": "bg-ref",
      "foil": "bg-foil",
      "both": "bg-linear-90 from-foil from-25% to-ref to-75%",
    }
    let classes_active = $derived(active ? "active" : "");
</script>

<div class="h-6 w-full rounded-md {classes_membership[membership]} {classes_active}"></div>

<style>
    div:not(.active){
        opacity: 0.5;
        transition-property: opacity;
        transition-duration: 200ms;
    }
    .active {
        opacity: 1;
    }
</style>
