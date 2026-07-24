<script lang="ts">
	import { resolve } from '$app/paths';
	import Hero from '$lib/components/layout/hero.svelte';
	import Section from '$lib/components/layout/section.svelte';
	import RestaurantTable from '$lib/components/restaurant-table.svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index';
	import restaurants from '$lib/data/restaurants.json';
	import ArrowRight from '@tabler/icons-svelte/icons/arrow-right';

	// the list is sorted by star average, best first
	const bestRated = restaurants.slice(0, 20);
</script>

<Hero />
<Section title="How we did it">
	<Card.Root class="mb-4 flex-row items-stretch gap-0 p-0">
		<img
			src="step-by-step.gif"
			alt="Step by step animation of scraper"
			loading="lazy"
			class="w-1/2"
		/>
		<div class="flex w-1/2 flex-col justify-center gap-4 p-6">
			<Card.Title>Methodology</Card.Title>
			<p class="text-muted-foreground">
				None of the official solutions met our requirements. So, we build our own. Here you can see
				how our scraper works internally.
			</p>
			<Button href={resolve('/methodology')} size="lg">
				Learn more <ArrowRight />
			</Button>
		</div>
	</Card.Root>
	<div class="flex w-full gap-4 overflow-x-auto pb-4">
		<Card.Root class="min-w-80 flex-1">
			<Card.Header>
				<Card.Title>Analysis</Card.Title>
				<Card.Description
					>With all this data at hand, we found some anomalies. Our analysis takes a deeper look at
					the data and presents some case studies.</Card.Description
				>
			</Card.Header>
			<Card.Content>
				<Button href={resolve('/analysis')} size="sm">Learn more <ArrowRight /></Button>
			</Card.Content>
		</Card.Root>
		<Card.Root class="min-w-80 flex-1">
			<Card.Header>
				<Card.Title>Ethics</Card.Title>
				<Card.Description>
					During our data collection we had to, but maybe did not, comply a lot of regulations. Here
					we explain our approach to ethics.
				</Card.Description>
			</Card.Header>
			<Card.Content>
				<Button href={resolve('/ethics')} size="sm">Learn more <ArrowRight /></Button>
			</Card.Content>
		</Card.Root>
	</div>
</Section>
<Section title="Highest rated">
	<p>The 20 restaurants with the best star average. Pick one to see all of its measurements.</p>
	<RestaurantTable restaurants={bestRated} />
	<Button href={resolve('/restaurants')} size="sm" class="self-start">
		All 118 restaurants <ArrowRight />
	</Button>
</Section>
