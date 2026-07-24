<script lang="ts">
	import { marked } from 'marked';
	import { asset } from '$app/paths';

	const rawContent = (await import('$lib/content/data_collection.md?raw')).default;
	const rawListContent = (await import('$lib/content/restaurant_list_scraping.md?raw')).default;

	const resolveDocSrc = (html: string) =>
		html.replaceAll(/src="(\/doc\/[^"]*)"/g, (_, path) => `src="${asset(path)}"`);

	const content = resolveDocSrc(marked.parse(rawContent) as string);
	const listContent = resolveDocSrc(marked.parse(rawListContent) as string);
</script>

<article class="prose p-4">
	{@html content}
	{@html listContent}
</article>
