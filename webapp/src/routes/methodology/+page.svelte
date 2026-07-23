<script lang="ts">
	import { marked } from 'marked';
	import { base } from '$app/paths';

	const rawContent = (await import('$lib/content/data_collection.md?raw')).default;

	const content = (marked.parse(rawContent) as string).replaceAll('src="/doc/', `src="${base}/doc/`);
</script>

<article class="prose p-4">
	{@html content}
</article>
