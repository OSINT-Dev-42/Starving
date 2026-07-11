<script lang="ts">
	import type { Snippet } from "svelte";

    type Props = {
      title: string;
      children: Snippet;
    }

    const { title, children }: Props = $props();
</script>

<section class="flex flex-col gap-4 mb-8">
    <h1 class="text-4xl font-black">{title}</h1>
    {@render children()}
</section>
