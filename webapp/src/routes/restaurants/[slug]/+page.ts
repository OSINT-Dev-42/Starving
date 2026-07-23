import { error } from '@sveltejs/kit';
import index from '$lib/data/restaurants.json';
import details from '$lib/data/restaurant-details.json';
import type { EntryGenerator, PageLoad } from './$types';

export const prerender = true;

export const entries: EntryGenerator = () => index.map((r) => ({ slug: r.slug }));

export const load: PageLoad = ({ params }) => {
	const restaurant = index.find((r) => r.slug === params.slug);
	if (!restaurant) error(404, 'Restaurant not found');

	return {
		restaurant,
		rows: details[params.slug as keyof typeof details] ?? []
	};
};
