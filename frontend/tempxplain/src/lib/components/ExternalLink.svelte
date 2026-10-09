<script lang="ts">
    import { ExternalLink } from "@lucide/svelte";

    interface ExternalLinkProps {
        title: string
        href: string;
    }
    let { title, href }: ExternalLinkProps = $props();
</script>

<a {href} target="_blank" class="flex flex-row items-center gap-1 text-foreground/85 hover:text-foreground border rounded-sm px-2 py-0.75" >
    <ExternalLink size={13} />
    <div class="text-xs">{title}</div>
</a>

<style>
    a{
        --link-color: light-dark(var(--color-blue-400), var(--color-blue-800));

        border-color: var(--link-color);
        background: color-mix(in srgb, var(--link-color) 25%, transparent);

        transition: color 200ms;
    }
</style>
