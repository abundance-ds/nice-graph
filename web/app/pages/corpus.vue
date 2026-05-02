<script setup lang="ts">
const route = useRoute();
const router = useRouter();

const searchQuery = ref((route.query.q as string) || "");
const docType = ref((route.query.doc_type as string) || "");
const tocFilter = ref("");
const loading = ref(false);
const results = ref<any[]>([]);
const searched = ref(!!route.query.q);
const expanded = ref<Set<number>>(new Set());

const { data: corpus } = await useFetch("/api/browse/corpus");

const filteredTAs = computed(() => {
  if (!corpus.value) return [];
  const q = tocFilter.value.toLowerCase();
  if (!q) return corpus.value as any[];
  return (corpus.value as any[]).filter(
    (ta: any) =>
      String(ta.ta_number).includes(q) ||
      (ta.title && ta.title.toLowerCase().includes(q))
  );
});

function toggleTA(num: number) {
  if (expanded.value.has(num)) expanded.value.delete(num);
  else expanded.value.add(num);
}

async function search() {
  if (!searchQuery.value.trim()) {
    searched.value = false;
    results.value = [];
    router.replace({ query: {} });
    return;
  }
  loading.value = true;
  searched.value = true;

  router.replace({
    query: {
      q: searchQuery.value,
      ...(docType.value ? { doc_type: docType.value } : {}),
    },
  });

  try {
    const params: Record<string, string> = {
      q: searchQuery.value,
      limit: "30",
    };
    if (docType.value) params.doc_type = docType.value;
    const res = await $fetch("/api/search", { query: params });
    results.value = (res as any).results || [];
  } catch {
    results.value = [];
  } finally {
    loading.value = false;
  }
}

function clearSearch() {
  searchQuery.value = "";
  searched.value = false;
  results.value = [];
  router.replace({ query: {} });
}

function highlightSnippet(snippet: string) {
  return snippet
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(
      /&gt;&gt;&gt;/g,
      '<mark class="bg-yellow-100 text-stone-900 px-0.5 rounded">'
    )
    .replace(/&lt;&lt;&lt;/g, "</mark>");
}

const docLabels: Record<string, string> = {
  FAD: "Final Appraisal Document",
  ACD: "Appraisal Consultation Document",
  committee_papers: "Committee Papers",
  scope: "Scope",
  scope_comments: "Scope Comments",
  evaluation_report: "Evaluation Report",
};

onMounted(() => {
  if (route.query.q) search();
});
</script>

<template>
  <div class="py-16 px-6 min-h-[calc(100vh-128px)]">
    <div class="max-w-4xl mx-auto">
      <p
        class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-4"
      >
        Corpus
      </p>
      <h1
        class="text-2xl md:text-3xl font-serif font-semibold leading-tight tracking-tight text-stone-900"
      >
        3,307 documents across {{ (corpus as any[])?.length || 826 }} appraisals
      </h1>

      <!-- Search -->
      <form class="mt-8 flex gap-3" @submit.prevent="search">
        <div
          class="flex-1 flex items-center border border-stone-200 rounded px-4 py-2.5 focus-within:border-stone-400 transition-colors"
        >
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Full-text search..."
            class="flex-1 text-base text-stone-900 placeholder:text-stone-300 outline-none bg-transparent font-mono"
          />
          <button
            v-if="searched"
            type="button"
            @click="clearSearch"
            class="text-stone-300 hover:text-stone-500 transition-colors mr-2 text-sm"
          >
            clear
          </button>
        </div>
        <select
          v-model="docType"
          class="border border-stone-200 rounded px-3 py-2 text-sm text-stone-600 outline-none focus:border-stone-400 font-mono"
        >
          <option value="">all types</option>
          <option value="FAD">FAD</option>
          <option value="ACD">ACD</option>
          <option value="committee_papers">committee_papers</option>
          <option value="scope">scope</option>
          <option value="scope_comments">scope_comments</option>
          <option value="evaluation_report">evaluation_report</option>
        </select>
        <button
          type="submit"
          class="px-5 py-2 text-sm font-medium bg-stone-900 hover:bg-stone-800 text-white rounded tracking-wide transition-colors"
        >
          Search
        </button>
      </form>

      <div class="mt-2 text-xs text-stone-300 font-mono">
        <a href="/llms.txt" class="hover:text-stone-500 transition-colors">/llms.txt</a>
        <span class="mx-2">&middot;</span>
        <span>/api/search?q=...&amp;format=plain</span>
        <span class="mx-2">&middot;</span>
        <span>/api/corpus/ta{N}/{doc}.md</span>
      </div>

      <!-- Downloads -->
      <div class="mt-10 border-t border-stone-100 pt-8">
        <p class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-4">
          Download
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <a
            href="/downloads/nice-corpus-fad.zip"
            class="border border-stone-200 rounded px-5 py-4 hover:border-stone-400 transition-colors group block"
          >
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-semibold text-stone-900 group-hover:text-cadet-600 transition-colors">
                FADs only
              </h3>
              <span class="text-xs text-stone-300 font-mono">.zip</span>
            </div>
            <p class="mt-1 text-xs text-stone-400">
              561 Final Appraisal Documents. The committee's final reasoning and decision for each TA.
            </p>
          </a>
          <a
            href="/downloads/nice-corpus-full.zip"
            class="border border-stone-200 rounded px-5 py-4 hover:border-stone-400 transition-colors group block"
          >
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-semibold text-stone-900 group-hover:text-cadet-600 transition-colors">
                Full corpus
              </h3>
              <span class="text-xs text-stone-300 font-mono">.zip</span>
            </div>
            <p class="mt-1 text-xs text-stone-400">
              3,307 documents across 826 TAs. FADs, committee papers, scoping documents, consultation comments.
            </p>
          </a>
        </div>
        <p class="mt-3 text-xs text-stone-300">
          Plain text markdown extracted from NICE PDFs. Includes README and llms.txt index. For research use.
        </p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="mt-12 text-center">
        <p class="text-sm text-stone-400 font-mono">searching...</p>
      </div>

      <!-- Search results -->
      <div v-if="searched && !loading" class="mt-8">
        <p class="text-xs text-stone-400 font-mono mb-4">
          {{ results.length }} result{{ results.length === 1 ? "" : "s" }}
        </p>

        <div v-if="results.length" class="space-y-1">
          <NuxtLink
            v-for="(r, i) in results"
            :key="i"
            :to="`/ta/${r.ta_number}/doc/${r.filename.replace('.md', '')}`"
            class="block border-t border-stone-100 py-3 hover:bg-stone-50/50 transition-colors -mx-3 px-3 rounded"
          >
            <div class="flex items-center gap-2 text-xs font-mono">
              <span class="text-stone-900 font-semibold">
                TA{{ r.ta_number }}
              </span>
              <span class="text-stone-300">/</span>
              <span class="text-stone-600">{{ r.filename }}</span>
              <span
                v-if="r.ta_title"
                class="text-stone-400 ml-2 font-sans truncate"
              >
                {{ r.ta_title }}
              </span>
              <span class="text-stone-300 ml-auto flex-shrink-0">
                {{ r.doc_type }}
              </span>
            </div>
            <div
              class="mt-1.5 text-sm text-stone-500 font-mono leading-relaxed"
              v-html="highlightSnippet(r.snippet)"
            />
          </NuxtLink>
        </div>

        <p
          v-else
          class="text-sm text-stone-400 font-mono text-center py-12"
        >
          no results
        </p>
      </div>

      <!-- TOC (when not searching) -->
      <div v-if="!searched && !loading" class="mt-10">
        <div class="flex items-center gap-4 mb-4">
          <p class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em]">
            Documents
          </p>
          <input
            v-model="tocFilter"
            type="text"
            placeholder="Filter TAs..."
            class="border border-stone-200 rounded px-3 py-1 text-sm text-stone-900 placeholder:text-stone-300 outline-none focus:border-stone-400 font-mono w-48"
          />
        </div>

        <div class="space-y-0">
          <div
            v-for="ta in filteredTAs"
            :key="ta.ta_number"
            class="border-t border-stone-100"
          >
            <button
              @click="toggleTA(ta.ta_number)"
              class="w-full text-left py-2 flex items-start gap-3 hover:bg-stone-50/50 transition-colors -mx-2 px-2 rounded"
            >
              <span
                class="text-xs text-stone-300 mt-1 w-3 flex-shrink-0 transition-transform"
                :class="{ 'rotate-90': expanded.has(ta.ta_number) }"
              >
                &#9656;
              </span>
              <span class="text-sm font-mono text-stone-900 font-medium w-14 flex-shrink-0">
                {{ ta.ta_number }}
              </span>
              <span class="text-sm text-stone-600 line-clamp-1">
                {{ ta.title || "Untitled" }}
              </span>
              <span class="text-xs text-stone-300 ml-auto flex-shrink-0 font-mono">
                {{ ta.documents.length }}
              </span>
            </button>

            <div
              v-if="expanded.has(ta.ta_number)"
              class="pl-10 pb-2 flex flex-wrap gap-2"
            >
              <NuxtLink
                v-for="doc in ta.documents"
                :key="doc.filename"
                :to="`/ta/${ta.ta_number}/doc/${doc.filename.replace('.md', '')}`"
                class="text-xs font-mono px-2 py-1 border border-stone-200 rounded hover:border-stone-400 text-stone-600 hover:text-stone-900 transition-colors"
              >
                {{ doc.filename }}
                <span v-if="doc.page_count" class="text-stone-300 ml-1">{{ doc.page_count }}p</span>
              </NuxtLink>
              <a
                :href="`/api/corpus/ta${ta.ta_number}/`"
                class="text-xs font-mono text-stone-300 hover:text-stone-500 transition-colors px-2 py-1"
                target="_blank"
              >
                index.md
              </a>
            </div>
          </div>
        </div>

        <p v-if="!filteredTAs.length" class="text-sm text-stone-400 text-center py-8">
          No TAs match "{{ tocFilter }}"
        </p>
      </div>
    </div>
  </div>
</template>
