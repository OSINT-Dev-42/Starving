<script lang="ts">
	import { base } from '$app/paths';
	import Sparkline from '$lib/components/sparkline.svelte';
	import * as Table from '$lib/components/ui/table/index.js';

	type Change = { stars: string; delta: number };

	type Restaurant = {
		name: string;
		address: string;
		slug: string;
		latest: { total: number; average: number; notice: string };
		lastChange: { date: string; changes: Change[] } | null;
		spark: number[];
	};

	const { restaurants }: { restaurants: Restaurant[] } = $props();

	function formatDate(date: string) {
		return new Date(date).toLocaleDateString('de-DE', { month: 'short', day: 'numeric' });
	}

	function formatChange(change: Change) {
		return `${change.delta > 0 ? '+' : ''}${change.delta} ${change.stars}`;
	}
</script>

<div class="overflow-x-auto rounded-base border-2 border-border bg-card shadow-shadow">
	<Table.Root class="min-w-[40rem]">
		<Table.Header>
			<Table.Row class="bg-foreground hover:bg-foreground">
				<Table.Head class="font-heading text-background">Restaurant</Table.Head>
				<Table.Head class="font-heading text-background">Rating</Table.Head>
				<Table.Head class="font-heading text-background">Last change</Table.Head>
				<Table.Head class="font-heading text-background">Reviews over time</Table.Head>
			</Table.Row>
		</Table.Header>
		<Table.Body>
			{#each restaurants as restaurant (restaurant.slug)}
				<Table.Row class="border-t-2 border-border">
					<Table.Cell>
						<a
							href="{base}/restaurants/{restaurant.slug}"
							class="font-heading underline-offset-4 hover:underline"
						>
							{restaurant.name}
						</a>
						<div class="text-xs text-muted-foreground">{restaurant.address}</div>
					</Table.Cell>
					<Table.Cell>
						<div class="font-medium">{restaurant.latest.average}</div>
						<div class="text-xs text-muted-foreground">
							{restaurant.latest.total} reviews
						</div>
					</Table.Cell>
					<Table.Cell>
						{#if restaurant.lastChange}
							<div class="font-medium">{formatDate(restaurant.lastChange.date)}</div>
							<div class="text-xs text-muted-foreground">
								{restaurant.lastChange.changes.map(formatChange).join(', ')}
							</div>
						{:else}
							<span class="text-xs text-muted-foreground">no change</span>
						{/if}
					</Table.Cell>
					<Table.Cell>
						<Sparkline values={restaurant.spark} />
					</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	</Table.Root>
</div>
