<script lang="ts">
	import { marked } from 'marked';

	const rawContent = (await import('$lib/content/ethics.md?raw')).default;

	const content = marked.parse(rawContent);
</script>

<article class="prose lg:prose-xl">
	{@html content}
</article>
