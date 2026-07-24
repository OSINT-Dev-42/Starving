<script lang="ts">
	import { asset } from '$app/paths';
	import { marked } from 'marked';

	const rawContent = (await import('$lib/content/analysis.md?raw')).default;
	const content = (marked.parse(rawContent) as string).replaceAll(
		/src="(\/doc\/[^"]*)"/g,
		(_, path) => `src="${asset(path)}"`
	);
</script>

<svelte:head><title>Analysis | Starving</title></svelte:head>

<article class="prose p-4">
	{@html content}
</article>

<style>
	/*how can this wooooork?? */
	article :global(iframe) {
		position: relative;
		width: min(80vw, 1400px);
		max-width: none;
		height: 600px;
		border: 0;
	}
</style>
