<script setup lang="ts">
const { data: stats } = await useFetch("/api/stats");
</script>

<template>
  <div class="py-24 md:py-32 px-6 min-h-[calc(100vh-128px)]">
    <div class="max-w-4xl mx-auto">
      <p
        class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-4 text-center"
      >
        NICE Technology Appraisals
      </p>
      <h1
        class="text-3xl md:text-4xl font-serif font-semibold leading-tight tracking-tight text-stone-900 text-center"
      >
        {{ stats?.tas || 826 }} appraisals, structured and searchable
      </h1>

      <div
        class="mt-8 flex items-center justify-center gap-6 text-sm text-stone-400"
        v-if="stats"
      >
        <span>{{ stats.interventions }} drugs</span>
        <span class="text-stone-200">&middot;</span>
        <span>{{ stats.decisions?.toLocaleString() }} decisions</span>
        <span class="text-stone-200">&middot;</span>
        <span>{{ stats.icers }} ICER estimates</span>
      </div>

      <div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
        <NuxtLink
          to="/chat"
          class="border border-stone-200 rounded px-6 py-6 hover:border-stone-400 transition-colors group"
        >
          <h2
            class="text-lg font-serif font-semibold text-stone-900 tracking-tight group-hover:text-cadet-600 transition-colors"
          >
            Ask
          </h2>
          <p class="mt-2 text-sm text-stone-400 leading-relaxed">
            Query the knowledge graph in plain English. Ask follow-up questions.
          </p>
        </NuxtLink>

        <NuxtLink
          to="/browse"
          class="border border-stone-200 rounded px-6 py-6 hover:border-stone-400 transition-colors group"
        >
          <h2
            class="text-lg font-serif font-semibold text-stone-900 tracking-tight group-hover:text-cadet-600 transition-colors"
          >
            Browse
          </h2>
          <p class="mt-2 text-sm text-stone-400 leading-relaxed">
            Filter appraisals by drug, condition, ICER band, and decision
            category.
          </p>
        </NuxtLink>

        <NuxtLink
          to="/corpus"
          class="border border-stone-200 rounded px-6 py-6 hover:border-stone-400 transition-colors group"
        >
          <h2
            class="text-lg font-serif font-semibold text-stone-900 tracking-tight group-hover:text-cadet-600 transition-colors font-mono"
          >
            Corpus
          </h2>
          <p class="mt-2 text-sm text-stone-400 leading-relaxed">
            3,307 source documents. Full-text search across all NICE TA
            papers.
          </p>
        </NuxtLink>
      </div>

      <div class="mt-16 text-center">
        <a
          href="/llms.txt"
          class="inline-flex items-center gap-2 border border-dashed border-stone-200 rounded px-5 py-3 text-xs text-stone-400 hover:border-stone-400 hover:text-stone-600 transition-colors"
        >
          <span class="font-mono">/llms.txt</span>
          <span>&mdash; machine-readable index for AI agents</span>
        </a>
      </div>
    </div>
  </div>
</template>
