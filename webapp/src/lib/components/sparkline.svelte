<script lang="ts">
	type Props = {
		values: number[];
		class?: string;
	};

	const { values, class: className = '' }: Props = $props();

	const width = 120;
	const height = 28;

	// MATHS MAGIC
	const points = $derived.by(() => {
		if (values.length < 2) return '';
		const min = Math.min(...values);
		const max = Math.max(...values);
		const span = max - min || 1;
		return values
			.map((v, i) => {
				const x = (i / (values.length - 1)) * width;
				const y = height - ((v - min) / span) * height;
				return `${x.toFixed(1)},${y.toFixed(1)}`;
			})
			.join(' ');
	});
</script>

<!-- magician trick -->
{#if points}
	<svg
		viewBox="0 0 {width} {height}"
		{width}
		{height}
		preserveAspectRatio="none"
		aria-hidden="true"
		class={className}
	>
		<polyline
			{points}
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
			vector-effect="non-scaling-stroke"
		/>
	</svg>
{/if}
