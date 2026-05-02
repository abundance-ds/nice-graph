<script setup lang="ts">
const route = useRoute();
const router = useRouter();

const filters = reactive({
  area: (route.query.area as string) || "",
  recommendation: (route.query.recommendation as string) || "",
  band: (route.query.band as string) || "",
  category: (route.query.category as string) || "",
  drug: (route.query.drug as string) || "",
  search: (route.query.search as string) || "",
  page: parseInt(route.query.page as string) || 1,
});

const activeFilters = computed(() => {
  const q: Record<string, string> = {};
  if (filters.area) q.area = filters.area;
  if (filters.recommendation) q.recommendation = filters.recommendation;
  if (filters.band) q.band = filters.band;
  if (filters.category) q.category = filters.category;
  if (filters.drug) q.drug = filters.drug;
  if (filters.search) q.search = filters.search;
  if (filters.page > 1) q.page = String(filters.page);
  return q;
});

const { data: filterOptions } = await useFetch("/api/browse/filters");
const { data, refresh } = await useFetch("/api/browse/appraisals", {
  query: activeFilters,
});

watch(activeFilters, () => {
  router.replace({ query: activeFilters.value });
  refresh();
});

function setFilter(key: string, value: string) {
  (filters as any)[key] = value;
  filters.page = 1;
}

function clearFilters() {
  filters.area = "";
  filters.recommendation = "";
  filters.band = "";
  filters.category = "";
  filters.drug = "";
  filters.search = "";
  filters.page = 1;
}

const hasFilters = computed(
  () =>
    filters.area ||
    filters.recommendation ||
    filters.band ||
    filters.category ||
    filters.drug ||
    filters.search
);

function formatBand(band: string | null) {
  if (!band) return "";
  const map: Record<string, string> = {
    below_20k: "<20k",
    "20k_to_30k": "20-30k",
    "30k_to_50k": "30-50k",
    "50k_to_100k": "50-100k",
    above_100k: ">100k",
    dominant: "Dominant",
    not_estimable: "N/E",
    confidential: "Conf.",
  };
  return map[band] || band;
}

function formatRec(rec: string | null) {
  if (!rec) return "";
  const map: Record<string, string> = {
    recommended: "Rec.",
    recommended_with_restrictions: "Restricted",
    not_recommended: "Not rec.",
    optimised: "Optimised",
    recommended_for_cdf: "CDF",
  };
  return map[rec] || rec;
}
</script>

<template>
  <div class="py-16 px-6 min-h-[calc(100vh-128px)]">
    <div class="max-w-6xl mx-auto">
      <p
        class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-4"
      >
        Browse
      </p>
      <h1
        class="text-2xl md:text-3xl font-serif font-semibold leading-tight tracking-tight text-stone-900"
      >
        Appraisals
      </h1>
      <p class="mt-2 text-sm text-stone-400" v-if="data">
        {{ data.total }} results
        <template v-if="hasFilters">
          (filtered) &middot;
          <button
            @click="clearFilters"
            class="text-stone-400 hover:text-stone-600 underline"
          >
            clear
          </button>
        </template>
      </p>

      <!-- Filters -->
      <div
        class="mt-8 flex flex-wrap gap-3 items-center"
        v-if="filterOptions"
      >
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search titles..."
          class="border border-stone-200 rounded px-3 py-1.5 text-sm text-stone-900 placeholder:text-stone-300 outline-none focus:border-stone-400 w-48"
          @input="filters.page = 1"
        />
        <input
          v-model="filters.drug"
          type="text"
          placeholder="Drug name..."
          class="border border-stone-200 rounded px-3 py-1.5 text-sm text-stone-900 placeholder:text-stone-300 outline-none focus:border-stone-400 w-36"
          @input="filters.page = 1"
        />
        <select
          :value="filters.area"
          @change="setFilter('area', ($event.target as HTMLSelectElement).value)"
          class="border border-stone-200 rounded px-3 py-1.5 text-sm text-stone-600 outline-none focus:border-stone-400"
        >
          <option value="">All areas</option>
          <option
            v-for="a in filterOptions.areas"
            :key="(a as any).value"
            :value="(a as any).value"
          >
            {{ (a as any).value }} ({{ (a as any).count }})
          </option>
        </select>
        <select
          :value="filters.band"
          @change="setFilter('band', ($event.target as HTMLSelectElement).value)"
          class="border border-stone-200 rounded px-3 py-1.5 text-sm text-stone-600 outline-none focus:border-stone-400"
        >
          <option value="">All ICER bands</option>
          <option
            v-for="b in filterOptions.bands"
            :key="(b as any).value"
            :value="(b as any).value"
          >
            {{ formatBand((b as any).value) }} ({{ (b as any).count }})
          </option>
        </select>
        <select
          :value="filters.recommendation"
          @change="
            setFilter(
              'recommendation',
              ($event.target as HTMLSelectElement).value
            )
          "
          class="border border-stone-200 rounded px-3 py-1.5 text-sm text-stone-600 outline-none focus:border-stone-400"
        >
          <option value="">All recommendations</option>
          <option
            v-for="r in filterOptions.recommendations"
            :key="(r as any).value"
            :value="(r as any).value"
          >
            {{ formatRec((r as any).value) }} ({{ (r as any).count }})
          </option>
        </select>
        <select
          :value="filters.category"
          @change="setFilter('category', ($event.target as HTMLSelectElement).value)"
          class="border border-stone-200 rounded px-3 py-1.5 text-sm text-stone-600 outline-none focus:border-stone-400"
        >
          <option value="">All decision categories</option>
          <option
            v-for="c in filterOptions.categories"
            :key="(c as any).value"
            :value="(c as any).value"
          >
            {{ (c as any).value.replace(/_/g, " ") }} ({{ (c as any).count }})
          </option>
        </select>
      </div>

      <!-- Table -->
      <div class="mt-8 overflow-x-auto">
        <table class="w-full text-sm" v-if="data?.rows?.length">
          <thead>
            <tr class="border-b border-stone-200 text-left">
              <th class="py-2 pr-4 font-semibold text-stone-900 w-16">TA</th>
              <th class="py-2 pr-4 font-semibold text-stone-900">Title</th>
              <th class="py-2 pr-4 font-semibold text-stone-900 w-40">Drug</th>
              <th class="py-2 pr-4 font-semibold text-stone-900 w-28">Area</th>
              <th class="py-2 pr-4 font-semibold text-stone-900 w-20">ICER</th>
              <th class="py-2 pr-4 font-semibold text-stone-900 w-24">Rec.</th>
              <th class="py-2 font-semibold text-stone-900 w-12 text-right">
                Dec.
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="row in data.rows"
              :key="(row as any).ta_number"
              class="border-b border-stone-100 hover:bg-stone-50/50 transition-colors"
            >
              <td class="py-2.5 pr-4">
                <NuxtLink
                  :to="`/ta/${(row as any).ta_number}`"
                  class="text-stone-900 font-medium hover:text-cadet-600 transition-colors"
                >
                  {{ (row as any).ta_number }}
                </NuxtLink>
              </td>
              <td class="py-2.5 pr-4 text-stone-600">
                <NuxtLink
                  :to="`/ta/${(row as any).ta_number}`"
                  class="hover:text-stone-900 transition-colors line-clamp-1"
                >
                  {{ (row as any).title || "—" }}
                </NuxtLink>
              </td>
              <td class="py-2.5 pr-4 text-stone-400">
                {{ (row as any).drugs || "—" }}
              </td>
              <td class="py-2.5 pr-4 text-stone-400">
                {{ (row as any).areas?.split(",")[0] || "—" }}
              </td>
              <td class="py-2.5 pr-4 text-stone-400">
                {{ formatBand((row as any).icer_band) || "—" }}
              </td>
              <td class="py-2.5 pr-4">
                <span
                  class="text-xs"
                  :class="{
                    'text-sea-600': (row as any).recommendation_type?.includes('recommended') && !(row as any).recommendation_type?.includes('not'),
                    'text-stone-400': (row as any).recommendation_type?.includes('not'),
                    'text-stone-600': !(row as any).recommendation_type?.includes('recommended'),
                  }"
                >
                  {{ formatRec((row as any).recommendation_type) || "—" }}
                </span>
              </td>
              <td class="py-2.5 text-right text-stone-400">
                {{ (row as any).decision_count || "—" }}
              </td>
            </tr>
          </tbody>
        </table>
        <p
          v-else-if="data"
          class="mt-8 text-sm text-stone-400 text-center py-12"
        >
          No appraisals match these filters.
        </p>
      </div>

      <!-- Pagination -->
      <div
        class="mt-6 flex items-center justify-between text-sm text-stone-400"
        v-if="data && data.pages > 1"
      >
        <button
          :disabled="filters.page <= 1"
          @click="filters.page--"
          class="px-3 py-1 border border-stone-200 rounded hover:border-stone-400 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          Previous
        </button>
        <span>Page {{ data.page }} of {{ data.pages }}</span>
        <button
          :disabled="filters.page >= data.pages"
          @click="filters.page++"
          class="px-3 py-1 border border-stone-200 rounded hover:border-stone-400 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>
