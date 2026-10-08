<script lang="ts">
  import * as Tooltip from "$lib/components/ui/tooltip/index.js";
  import { Kbd } from "$lib/components/ui/kbd/index.js";
  import type { Snippet } from "svelte";
  import Button, { type ButtonProps } from "./ui/button/button.svelte";

  // All other button props (`onclick`, `disabled`, ...) are forwarded to the button
  type TooltipButtonProps = ButtonProps & {
      tooltip: string;
      children: Snippet;
      kbd?: string;
      side?: "top" | "bottom" | "left" | "right";
  };
  let {
      tooltip,
      children,
      kbd,
      variant = "secondary",
      size = "default",
      side = "top",
      ...restProps
  }: TooltipButtonProps = $props();
</script>

<Tooltip.Root delayDuration={100}>
  <!-- Render the button itself as trigger instead of nesting it in the trigger's button -->
  <Tooltip.Trigger>
    {#snippet child({ props })}
      <Button {variant} {size} {...props} {...restProps}>
        {@render children()}
      </Button>
    {/snippet}
  </Tooltip.Trigger>
  <Tooltip.Content {side}>
    {tooltip} {#if kbd !== undefined}<Kbd>{kbd}</Kbd>{/if}
  </Tooltip.Content>
</Tooltip.Root>
