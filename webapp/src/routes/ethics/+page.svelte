<script lang="ts">
	import { marked } from 'marked';

	const rawContent = (await import('$lib/content/ethics.md?raw')).default;

	const content = marked.parse(rawContent);
</script>

<article class="prose p-4">
	{@html content}
</article>
