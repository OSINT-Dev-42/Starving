<script lang="ts">
	import Hero from '$lib/components/layout/hero.svelte';
	import Section from '$lib/components/layout/section.svelte';
	import RestaurantTable from '$lib/components/restaurant-table.svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index';
	import ArrowRight from '@tabler/icons-svelte/icons/arrow-right';
	import { base } from '$app/paths';
	import restaurants from '$lib/data/restaurants.json';

	// the list is sorted by star average, best first
	const bestRated = restaurants.slice(0, 20);
</script>

<Hero />
<Section title="How we did it">
	Here is an example of our scraper in action:
	<img src="step-by-step.gif" alt="Step by step animation of scraper" loading="lazy" />
	<div class="flex w-full gap-4 overflow-x-auto pb-4">
		<Card.Root class="min-w-80 shrink-0">
			<Card.Header>
				<Card.Title>Ethics</Card.Title>
				<Card.Description>
					How we decided on what data to use and where to get it...
				</Card.Description>
			</Card.Header>
			<Card.Content>
				<Button href="{base}/ethics" size="sm">Learn more <ArrowRight /></Button>
			</Card.Content>
		</Card.Root>
		<Card.Root class="min-w-80 shrink-0">
			<Card.Header>
				<Card.Title>Methodology</Card.Title>
				<Card.Description>The special secret sauce to gather the needed data...</Card.Description>
			</Card.Header>
			<Card.Content>
				<Button href="{base}/methodology" size="sm">Learn more <ArrowRight /></Button>
			</Card.Content>
		</Card.Root>
	</div>
</Section>
<Section title="Highest rated">
	<p>The 20 restaurants with the best star average. Pick one to see all of its measurements.</p>
	<RestaurantTable restaurants={bestRated} />
	<Button href="{base}/restaurants" size="sm" class="self-start">
		All 118 restaurants <ArrowRight />
	</Button>
</Section>
