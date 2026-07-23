<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		title: string;
		children: Snippet;
	};

	const { title, children }: Props = $props();
</script>

<section class="mb-8 flex flex-col gap-4 p-4">
	<h1 class="text-4xl font-black">{title}</h1>
	{@render children()}
</section>
