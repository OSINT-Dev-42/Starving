<script lang="ts">
	import { dev } from '$app/environment';
	import icon from '$lib/assets/star-check.svg';
</script>

<nav class="mb-12 flex w-screen items-center justify-between border-b px-12 py-4">
	<div>
		<a class="flex items-center gap-2" href={dev ? '/' : "/Starving"}
			><img src={icon} alt="Starving" class="h-8 w-8" />
			<b class="text-4xl font-black">Starving</b></a
		>
	</div>
	<div class="flex gap-8">
		<a href="ethics"><b class="">Ethics</b></a>
		<a href="methodology"><b class="">Methodology</b></a>
	</div>
</nav>
