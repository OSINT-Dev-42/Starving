<script lang="ts">
	import { browser } from '$app/environment';
	import _ from 'lodash';
	import Papa from 'papaparse';
	import type { Restaurant } from './columns';
	import DataTables from './data-tables.svelte';
	import { columns } from './columns';
	import * as Card from '$lib/components/ui/card/index';
	import ArrowRight from '@tabler/icons-svelte/icons/arrow-right';
	import Section from '$lib/components/layout/section.svelte';

	let ready = $state(false);

	// let restaurantData: Restaurant[] = [];

	// const parsedCsv = Papa.parse(rawCsv, {
	// 	header: true,
	// 	worker: true,
	// 	// step: (row) => {
	// 	// 	const { name, date } = row.data;
	// 	// 	restaurantData.push({
	// 	// 		name,
	// 	// 		date: new Date(date),
	// 	// 		'1 stars': Number(row.data['1 stars']),
	// 	// 		'2 stars': Number(row.data['2 stars']),
	// 	// 		'3 stars': Number(row.data['3 stars']),
	// 	// 		'4 stars': Number(row.data['4 stars']),
	// 	// 		'5 stars': Number(row.data['5 stars'])
	// 	// 	});
	// 	// },
	// 	complete: () => {
	// 		ready = true;
	// 	}
	// });

	$inspect(ready);
</script>

<Section title="Problem to solve">
	<p>
	So, you and your friends are looking for a place to eat in the evening.
	</p>
</Section>
<Section title="How we did it">
    Here is an example of our scraper in action:
    <img src="step-by-step.gif" alt="Step by step animation of scraper" loading="lazy" />
    <div class="flex gap-4 w-full items-center">
        <Card.Root class="min-w-80">
            <Card.Header>
                <Card.Title>
                    Ethics
                </Card.Title>
                <Card.Description>
                    How we decided on what data to use and where to get it...
                </Card.Description>
            </Card.Header>
            <Card.Content>
                <a class="flex items-center gap-1" href="/ethics">Learn more <ArrowRight/> </a>
            </Card.Content>
        </Card.Root>
        <Card.Root class="min-w-80">
            <Card.Header>
                <Card.Title>
                    Methodology
                </Card.Title>
                <Card.Description>
                    The special secret sauce to gather the needed data...
                </Card.Description>
            </Card.Header>
            <Card.Content>
                <a class="flex items-center gap-1" href="/methodology">Learn more <ArrowRight/> </a>
            </Card.Content>
        </Card.Root>
    </div>
</Section>
<Section title="Analysis">
    Test
</Section>
