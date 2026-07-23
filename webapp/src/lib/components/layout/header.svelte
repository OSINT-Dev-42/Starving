<script lang="ts">
	import { base } from '$app/paths';
	import icon from '$lib/assets/star-check.svg';
	import { buttonVariants } from '$lib/components/ui/button/index.js';
	import * as NavigationMenu from '$lib/components/ui/navigation-menu/index.js';
	import { navigationMenuTriggerStyle } from '$lib/components/ui/navigation-menu/navigation-menu-trigger.svelte';
	import * as Sheet from '$lib/components/ui/sheet/index.js';
	import MenuIcon from '@lucide/svelte/icons/menu';

	const links: { title: string; href: string }[] = [
		{ title: 'Methodology', href: 'methodology' },
		{ title: 'Analysis', href: 'analysis' },
		{ title: 'Ethics', href: 'ethics' }
	];

	let mobileOpen = $state(false);
</script>

<nav class="w-full border-b-2 border-border bg-secondary">
	<div class="container mx-auto flex items-center justify-between px-4 py-4">
		<a class="flex items-center gap-2" href="{base}/">
			<img src={icon} alt="Starving" class="h-8 w-8" />
			<b class="text-4xl font-black">Starving</b>
		</a>

		<!-- Desktop menu -->
		<NavigationMenu.Root class="hidden md:flex">
			<NavigationMenu.List>
				{#each links as link (link.href)}
					<NavigationMenu.Item>
						<NavigationMenu.Link>
							{#snippet child()}
								<a href="{base}/{link.href}" class={navigationMenuTriggerStyle()}>
									<b>{link.title}</b>
								</a>
							{/snippet}
						</NavigationMenu.Link>
					</NavigationMenu.Item>
				{/each}
			</NavigationMenu.List>
		</NavigationMenu.Root>

		<!-- Mobile menu -->
		<Sheet.Root bind:open={mobileOpen}>
			<Sheet.Trigger class={buttonVariants({ variant: 'ghost', size: 'icon' }) + ' md:hidden'}>
				<MenuIcon class="size-6" />
				<span class="sr-only">Toggle menu</span>
			</Sheet.Trigger>
			<Sheet.Content side="right">
				<Sheet.Header>
					<Sheet.Title>Menu</Sheet.Title>
				</Sheet.Header>
				<nav class="flex flex-col gap-1 px-4">
					{#each links as link (link.href)}
						<a
							href="{base}/{link.href}"
							class="rounded-md px-3 py-2 text-lg font-bold transition-colors hover:bg-accent hover:text-accent-foreground"
							onclick={() => (mobileOpen = false)}
						>
							{link.title}
						</a>
					{/each}
				</nav>
			</Sheet.Content>
		</Sheet.Root>
	</div>
</nav>
