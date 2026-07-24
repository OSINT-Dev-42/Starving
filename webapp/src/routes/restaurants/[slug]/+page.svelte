<script lang="ts">
	import { resolve } from '$app/paths';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Chart from '$lib/components/ui/chart/index.js';
	import * as Table from '$lib/components/ui/table/index.js';
	import ArrowLeft from '@tabler/icons-svelte/icons/arrow-left';
	import { scaleUtc } from 'd3-scale';
	import { curveNatural } from 'd3-shape';
	import { Area, AreaChart } from 'layerchart';

	const { data } = $props();
	const restaurant = $derived(data.restaurant);
	const rows = $derived(data.rows);

	const chartData = $derived(rows.map((row) => ({ ...row, date: new Date(row.date) })));

	const chartConfig = {
		s5: { label: '5 stars', color: 'var(--chart-4)' },
		s4: { label: '4 stars', color: 'var(--chart-1)' },
		s3: { label: '3 stars', color: 'var(--chart-3)' },
		s2: { label: '2 stars', color: 'var(--chart-5)' },
		s1: { label: '1 star', color: 'var(--chart-2)' }
	} satisfies Chart.ChartConfig;

	const series = [
		{ key: 's5', label: '5 stars', color: chartConfig.s5.color },
		{ key: 's4', label: '4 stars', color: chartConfig.s4.color },
		{ key: 's3', label: '3 stars', color: chartConfig.s3.color },
		{ key: 's2', label: '2 stars', color: chartConfig.s2.color },
		{ key: 's1', label: '1 star', color: chartConfig.s1.color }
	];
</script>

<svelte:head><title>{restaurant.name} | Starving</title></svelte:head>

<section class="mb-8 flex flex-col gap-4 p-4">
	<Button href={resolve('/restaurants')} variant="outline" size="sm" class="self-start">
		<ArrowLeft /> All restaurants
	</Button>

	<div>
		<h1 class="text-4xl font-black">{restaurant.name}</h1>
		<p class="text-muted-foreground">{restaurant.address}</p>
	</div>

	<p>
		{restaurant.latest.average} stars from {restaurant.latest.total} reviews, measured
		{rows.length} times.
	</p>

	{#if restaurant.latest.notice}
		<p class="rounded-base border-2 border-border bg-card p-3 text-sm shadow-shadow">
			Google notice: {restaurant.latest.notice}
		</p>
	{/if}

	<Card.Root>
		<Card.Header>
			<Card.Title>Reviews over time</Card.Title>
			<Card.Description>Click a star level in the legend to show or hide it.</Card.Description>
		</Card.Header>
		<Card.Content>
			<Chart.Container config={chartConfig} class="aspect-auto h-[280px] w-full">
				<AreaChart
					legend
					data={chartData}
					x="date"
					xScale={scaleUtc()}
					{series}
					props={{
						xAxis: {
							format: (v: Date) => v.toLocaleDateString('de-DE', { month: 'short', day: 'numeric' })
						},
						yAxis: { format: (v: number) => `${v}` }
					}}
				>
					{#snippet marks({ context })}
						{#each context.series.visibleSeries as s (s.key)}
							<Area
								seriesKey={s.key}
								curve={curveNatural}
								fillOpacity={0.2}
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

	<div class="overflow-x-auto rounded-base border-2 border-border bg-card shadow-shadow">
		<Table.Root class="min-w-[36rem]">
			<Table.Header>
				<Table.Row class="bg-foreground hover:bg-foreground">
					<Table.Head class="font-heading text-background">Date</Table.Head>
					<Table.Head class="font-heading text-background">5 stars</Table.Head>
					<Table.Head class="font-heading text-background">4 stars</Table.Head>
					<Table.Head class="font-heading text-background">3 stars</Table.Head>
					<Table.Head class="font-heading text-background">2 stars</Table.Head>
					<Table.Head class="font-heading text-background">1 star</Table.Head>
					<Table.Head class="font-heading text-background">Total</Table.Head>
				</Table.Row>
			</Table.Header>
			<Table.Body>
				{#each rows as row (row.date)}
					<Table.Row class="border-t-2 border-border">
						<Table.Cell class="font-medium">{row.date}</Table.Cell>
						<Table.Cell>{row.s5}</Table.Cell>
						<Table.Cell>{row.s4}</Table.Cell>
						<Table.Cell>{row.s3}</Table.Cell>
						<Table.Cell>{row.s2}</Table.Cell>
						<Table.Cell>{row.s1}</Table.Cell>
						<Table.Cell>{row.total}</Table.Cell>
					</Table.Row>
				{/each}
			</Table.Body>
		</Table.Root>
	</div>
</section>
