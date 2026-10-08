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
      "none": "bg-transparent",
      "ref": "bg-ref",
      "foil": "bg-foil",
      "hidden": "bg-foreground/15",
      "both": "both",
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

<div class="h-8 w-full max-h-8 border border-t-transparent border-r-transparent {class_membership} {class_active}"></div>

<style>
    div{
        transition: border-color 600ms;
    }
    div.both{
        background: linear-gradient(90deg, var(--color-ref) 20%, var(--color-foil) 40%, var(--color-foil) 60%, var(--color-ref) 80%);
        background-size: 500% 100%;
        animation: both 5s linear infinite;
    }
    @keyframes both {
        0% {
            background-position-x: 100%;
        }
        100% {
            background-position-x: 0%;
        }
    }
    div:not(.active){
        transition-property: opacity, background-color;
        transition-duration: 100ms;
    }
    .active {
        opacity: 1;
    }
</style>
