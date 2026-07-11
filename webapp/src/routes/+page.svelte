<script lang="ts">
	import { browser } from '$app/environment';
	import _ from 'lodash';
	import Papa from 'papaparse';
	import type { Restaurant } from './columns';
	import DataTables from './data-tables.svelte';
	import { columns } from './columns';

	const rawCsv = (await import('$lib/assets/firstcrawl.csv?raw')).default;

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

<h1 class="text-4xl">Problem to solve</h1>

{#if ready}
	We are ready
	<!-- {restaurantData.length} restaurants found
	<br />
	First restaurant: {restaurantData[0].name}
	<DataTables data={restaurantData} {columns} /> -->
{/if}
