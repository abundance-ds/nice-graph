<script setup lang="ts">
import { marked } from "marked";

const route = useRoute();
const num = route.params.number;
const name = route.params.name;

const { data, error } = await useFetch(`/api/ta/${num}/doc/${name}`);

if (error.value) {
  throw createError({ statusCode: 404, message: `Document not found` });
}

const showDropdown = ref(false);

function closeDropdown() {
  showDropdown.value = false;
}

const renderedHtml = computed(() => {
  if (!data.value) return "";
  const content = (data.value as any).content.replace(
    /<!-- page (\d+) -->/g,
    '<div id="page-$1" class="page-marker border-t border-stone-100 mt-8 pt-2 mb-4"><span class="text-xs text-stone-300 font-mono">Page $1</span></div>'
  );
  return marked.parse(content);
});

const docLabels: Record<string, string> = {
  FAD: "Final Appraisal Document",
  ACD: "Appraisal Consultation Document",
  committee_papers: "Committee Papers",
  scope: "Scope",
  scope_comments: "Scope Consultation Comments",
  evaluation_report: "Evaluation Report",
};

const docTitle = computed(() => {
  const n = name as string;
  const base = n.replace(/_\d+$/, "");
  return docLabels[base] || n.replace(/_/g, " ");
});

useHead({ title: `${docTitle.value} — TA${num}` });
</script>

<template>
  <div class="py-16 px-6" v-if="data" @click="closeDropdown">
    <div class="max-w-3xl mx-auto">
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-2 text-xs text-stone-400">
          <NuxtLink
            :to="`/ta/${num}`"
            class="hover:text-stone-600 transition-colors"
          >
            TA{{ num }}
          </NuxtLink>
          <span>/</span>
          <span
            class="text-cadet-500 font-semibold uppercase tracking-[0.15em]"
          >
            {{ docTitle }}
          </span>
        </div>

        <!-- Dropdown -->
        <div class="relative">
          <button
            @click.stop="showDropdown = !showDropdown"
            class="text-xs text-stone-400 hover:text-stone-600 border border-stone-200 rounded px-3 py-1.5 transition-colors"
          >
            Options
          </button>
          <div
            v-if="showDropdown"
            class="absolute right-0 top-full mt-1 bg-white border border-stone-200 rounded shadow-sm py-1 z-20 min-w-40"
          >
            <a
              :href="`/api/corpus/ta${num}/${name}.md`"
              target="_blank"
              class="block px-4 py-2 text-sm text-stone-600 hover:bg-stone-50 hover:text-stone-900 transition-colors"
            >
              View markdown
            </a>
            <a
              :href="`/api/corpus/ta${num}/${name}.md?download=true`"
              class="block px-4 py-2 text-sm text-stone-600 hover:bg-stone-50 hover:text-stone-900 transition-colors"
            >
              Download .md
            </a>
          </div>
        </div>
      </div>

      <article
        class="prose prose-stone max-w-none
          prose-headings:font-serif prose-headings:font-semibold prose-headings:tracking-tight prose-headings:text-stone-900
          prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg
          prose-p:text-base prose-p:text-stone-600 prose-p:leading-relaxed
          prose-li:text-base prose-li:text-stone-600
          prose-table:text-sm
          prose-td:py-1.5 prose-td:px-3 prose-td:border-stone-100
          prose-th:py-1.5 prose-th:px-3 prose-th:font-semibold prose-th:text-stone-900 prose-th:border-stone-200
          prose-strong:text-stone-900 prose-strong:font-semibold
          prose-a:text-cadet-600 prose-a:no-underline hover:prose-a:text-cadet-800"
        v-html="renderedHtml"
      />
    </div>
  </div>
</template>
