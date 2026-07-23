<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Chart from '$lib/components/ui/chart/index.js';
	import { scaleUtc } from 'd3-scale';
	import { curveNatural } from 'd3-shape';
	import { Area, AreaChart } from 'layerchart';
	import ArrowRight from '@tabler/icons-svelte/icons/arrow-right';
	import summary from '$lib/data/summary.json';
	import { base } from '$app/paths';

	// featured restaurant series, with real Date objects for the time axis
	const data = summary.featured.series.map((d) => ({ ...d, date: new Date(d.date) }));

	const chartConfig = {
		s1: { label: '1 star', color: 'var(--chart-2)' },
		s2: { label: '2 star', color: 'var(--chart-3)' }
	} satisfies Chart.ChartConfig;
</script>

<section class="grid items-center gap-8 p-4 md:grid-cols-2 md:py-12">
	<div class="flex flex-col items-start gap-6">
		<h1 class="text-4xl font-black tracking-tight sm:text-5xl">
			Are there patterns in the changes of reviews in restaurants in Bochum?
		</h1>
		<p class="text-lg text-muted-foreground">
			We tracked Google Maps ratings over time. Here is one real restaurant whose
			negative reviews vanished overnight.
		</p>
		<Button href="{base}/analysis" size="lg">See the analysis <ArrowRight /></Button>
	</div>

	<Card.Root>
		<Card.Header>
			<Card.Title>{summary.featured.name}</Card.Title>
			<Card.Description>1★ and 2★ reviews over time</Card.Description>
		</Card.Header>
		<Card.Content>
			<Chart.Container config={chartConfig} class="aspect-auto h-[240px] w-full">
				<AreaChart
					legend
					{data}
					x="date"
					xScale={scaleUtc()}
					series={[
						{ key: 's1', label: '1 star', color: chartConfig.s1.color },
						{ key: 's2', label: '2 star', color: chartConfig.s2.color }
					]}
					props={{
						xAxis: {
							format: (v: Date) =>
								v.toLocaleDateString('de-DE', { month: 'short', day: 'numeric' })
						},
						yAxis: { format: (v: number) => `${v}` }
					}}
				>
					{#snippet marks({ context })}
						{#each context.series.visibleSeries as s (s.key)}
							<Area
								seriesKey={s.key}
								curve={curveNatural}
								fillOpacity={0.3}
								line={{ class: 'stroke-2' }}
								motion="tween"
								{...s.props}
							/>
						{/each}
					{/snippet}
					{#snippet tooltip()}
						<Chart.Tooltip
							labelFormatter={(v: Date) =>
								v.toLocaleDateString('de-DE', { month: 'short', day: 'numeric' })}
							indicator="line"
						/>
					{/snippet}
				</AreaChart>
			</Chart.Container>
		</Card.Content>
	</Card.Root>
</section>
