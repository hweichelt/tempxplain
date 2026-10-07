<script lang="ts">
    import type { ModelMembership } from "$lib/bindings";

    interface TimelineFluentIndicatorProps {
        fluent: string;
        membership: ModelMembership;
        model_filter?: ModelMembership;
        active?: boolean;
    }
    let { fluent, membership, model_filter = "both", active = false }: TimelineFluentIndicatorProps = $props();

    let classes_membership = {
      "none": "bg-card",
      "ref": "bg-ref",
      "foil": "bg-foil",
      "hidden": "bg-foreground/15",
      "both": "bg-linear-90 from-foil from-25% to-ref to-75%",
    }
    function apply_filter(membership: ModelMembership, filter: ModelMembership): string {
      if (filter === "both") return classes_membership[membership];
      if (filter === "ref"){
        if (membership === "ref" || membership === "both") {return classes_membership["ref"]}
        if (membership === "foil") {return classes_membership["hidden"]}
      } else if (filter === "foil") {
        if (membership === "foil" || membership === "both") {return classes_membership["foil"]}
        if (membership === "ref") {return classes_membership["hidden"]}
      }
      return classes_membership["none"];
    }
    let class_membership = $derived(apply_filter(membership, model_filter));
    let class_active = $derived(active ? "active" : "");
</script>

<div class="h-6 w-full rounded-md {class_membership} {class_active}"></div>

<style>
    div:not(.active){
        opacity: 0.5;
        transition-property: opacity, background-color;
        transition-duration: 100ms;
    }
    .active {
        opacity: 1;
    }
    div:hover{
        border-color: var(--color-foreground);
    }
</style>
