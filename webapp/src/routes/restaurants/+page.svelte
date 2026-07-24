<script lang="ts">
	import RestaurantTable from '$lib/components/restaurant-table.svelte';
	import Section from '$lib/components/layout/section.svelte';
	import restaurants from '$lib/data/restaurants.json';
</script>

<svelte:head><title>All Restaurants | Starving</title></svelte:head>

<Section title="All restaurants">
	<p>
		Every restaurant we track in Bochum, sorted by star average. Pick one to see its
		measurements.
	</p>
	<RestaurantTable {restaurants} />
</Section>
