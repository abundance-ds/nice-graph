<script setup lang="ts">
const route = useRoute();
const num = route.params.number;

const { data, error } = await useFetch(`/api/ta/${num}`);
const { data: docs } = await useFetch(`/api/ta/${num}/documents`);

if (error.value) {
  throw createError({ statusCode: 404, message: `TA${num} not found` });
}

const docLabels: Record<string, string> = {
  FAD: "Final Appraisal Document",
  ACD: "Appraisal Consultation Document",
  committee_papers: "Committee Papers",
  scope: "Scope",
  scope_comments: "Scope Consultation Comments",
  evaluation_report: "Evaluation Report",
};

useHead({ title: `TA${num} — ${(data.value as any)?.meta?.title || "NICE Appraisals"}` });

function formatBand(band: string) {
  const map: Record<string, string> = {
    below_20k: "Below £20,000",
    "20k_to_30k": "£20,000–£30,000",
    "30k_to_50k": "£30,000–£50,000",
    "50k_to_100k": "£50,000–£100,000",
    above_100k: "Above £100,000",
    dominant: "Dominant (cost-saving)",
    not_estimable: "Not estimable",
    confidential: "Confidential (PAS-dependent)",
  };
  return map[band] || band;
}

function formatCategory(cat: string) {
  return cat.replace(/_/g, " ");
}

function formatRec(rec: string) {
  const map: Record<string, string> = {
    recommended: "Recommended",
    recommended_with_restrictions: "Recommended with restrictions",
    not_recommended: "Not recommended",
    optimised: "Optimised",
    recommended_for_cdf: "Recommended for Cancer Drugs Fund",
  };
  return map[rec] || rec;
}
</script>

<template>
  <div class="py-16 px-6 min-h-[calc(100vh-128px)]" v-if="data">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <p
        class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-4"
      >
        TA{{ (data as any).meta.ta_number }}
        <span v-if="(data as any).meta.appraisal_type" class="text-stone-300">
          &middot; {{ (data as any).meta.appraisal_type }}
        </span>
      </p>
      <h1
        class="text-2xl md:text-3xl font-serif font-semibold leading-tight tracking-tight text-stone-900"
      >
        {{ (data as any).meta.title || `Technology Appraisal ${num}` }}
      </h1>

      <div class="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-sm text-stone-400">
        <span v-if="(data as any).meta.recommendation_type">
          {{ formatRec((data as any).meta.recommendation_type) }}
        </span>
        <span v-if="(data as any).meta.committee_name">
          {{ (data as any).meta.committee_name }}
        </span>
        <span v-if="(data as any).meta.issue_date">
          {{ (data as any).meta.issue_date }}
        </span>
      </div>

      <p
        v-if="(data as any).meta.restriction_details"
        class="mt-4 text-sm text-stone-600 leading-relaxed border-l-2 border-stone-200 pl-4"
      >
        {{ (data as any).meta.restriction_details }}
      </p>

      <!-- Source Documents -->
      <section v-if="(docs as any)?.documents?.length" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Source documents
        </p>
        <div class="flex flex-wrap gap-2">
          <NuxtLink
            v-for="doc in (docs as any).documents"
            :key="doc.filename"
            :to="`/ta/${num}/doc/${doc.name}`"
            class="text-sm px-3 py-1.5 border border-stone-200 rounded hover:border-stone-400 text-stone-600 hover:text-stone-900 transition-colors"
          >
            {{ docLabels[doc.docType] || doc.name.replace(/_/g, ' ') }}
          </NuxtLink>
        </div>
      </section>

      <!-- Interventions -->
      <section v-if="(data as any).interventions?.length" class="mt-12">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Intervention{{ (data as any).interventions.length > 1 ? "s" : "" }}
        </p>
        <div class="space-y-2">
          <div v-for="i in (data as any).interventions" :key="i.id">
            <span class="text-base font-semibold text-stone-900">{{
              i.generic_name
            }}</span>
            <span v-if="i.brand_name" class="text-sm text-stone-400 ml-2">
              ({{ i.brand_name }})
            </span>
            <div class="text-sm text-stone-400 mt-0.5">
              <span v-if="i.drug_class">{{ i.drug_class }}</span>
              <span v-if="i.mechanism_of_action">
                &middot; {{ i.mechanism_of_action }}
              </span>
              <span v-if="i.route_of_administration">
                &middot; {{ i.route_of_administration }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Conditions -->
      <section v-if="(data as any).conditions?.length" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Condition{{ (data as any).conditions.length > 1 ? "s" : "" }}
        </p>
        <div class="space-y-1">
          <div v-for="c in (data as any).conditions" :key="c.id" class="text-sm">
            <span class="text-stone-900">{{ c.condition_name }}</span>
            <span v-if="c.therapeutic_area" class="text-stone-400 ml-2">
              {{ c.therapeutic_area }}
            </span>
            <span v-if="c.disease_setting" class="text-stone-300 ml-1">
              &middot; {{ c.disease_setting }}
            </span>
          </div>
        </div>
      </section>

      <!-- Comparators -->
      <section v-if="(data as any).comparators?.length" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Comparators
        </p>
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-stone-200 text-left">
              <th class="py-1.5 pr-4 font-semibold text-stone-900">Name</th>
              <th class="py-1.5 pr-4 font-semibold text-stone-900">Type</th>
              <th class="py-1.5 pr-4 font-semibold text-stone-900">
                Established
              </th>
              <th class="py-1.5 font-semibold text-stone-900">
                Committee preferred
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="c in (data as any).comparators"
              :key="c.id"
              class="border-b border-stone-100"
            >
              <td class="py-1.5 pr-4 text-stone-600">
                {{ c.comparator_name }}
              </td>
              <td class="py-1.5 pr-4 text-stone-400">
                {{ c.comparator_type?.replace(/_/g, " ") || "—" }}
              </td>
              <td class="py-1.5 pr-4">
                <span v-if="c.is_established_practice" class="text-sea-500"
                  >Yes</span
                >
                <span v-else class="text-stone-300">—</span>
              </td>
              <td class="py-1.5">
                <span v-if="c.committee_preferred" class="text-sea-500"
                  >Yes</span
                >
                <span v-else class="text-stone-300">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Clinical Trials -->
      <section v-if="(data as any).trials?.length" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Clinical trials
        </p>
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-stone-200 text-left">
              <th class="py-1.5 pr-4 font-semibold text-stone-900">Trial</th>
              <th class="py-1.5 pr-4 font-semibold text-stone-900">Design</th>
              <th class="py-1.5 pr-4 font-semibold text-stone-900">Phase</th>
              <th class="py-1.5 font-semibold text-stone-900">Pivotal</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="t in (data as any).trials"
              :key="t.id"
              class="border-b border-stone-100"
            >
              <td class="py-1.5 pr-4 text-stone-600">{{ t.trial_name }}</td>
              <td class="py-1.5 pr-4 text-stone-400">
                {{ t.study_design || "—" }}
              </td>
              <td class="py-1.5 pr-4 text-stone-400">
                {{ t.phase || "—" }}
              </td>
              <td class="py-1.5">
                <span v-if="t.is_pivotal" class="text-sea-500">Yes</span>
                <span v-else class="text-stone-300">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Economic Model -->
      <section v-if="(data as any).models?.length" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Economic model
        </p>
        <div v-for="m in (data as any).models" :key="m.id" class="text-sm space-y-1">
          <div>
            <span class="text-stone-900 font-medium">{{
              m.model_type?.replace(/_/g, " ") || "Not specified"
            }}</span>
            <span v-if="m.model_source" class="text-stone-400 ml-2">
              ({{ m.model_source }})
            </span>
          </div>
          <div v-if="m.time_horizon" class="text-stone-400">
            Time horizon: {{ m.time_horizon }}
          </div>
          <div v-if="m.cycle_length" class="text-stone-400">
            Cycle length: {{ m.cycle_length }}
          </div>
        </div>
      </section>

      <!-- ICER Bands -->
      <section v-if="(data as any).icers?.length" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          ICER
        </p>
        <div v-for="icer in (data as any).icers" :key="icer.id" class="text-sm mb-2">
          <span class="text-stone-900 font-medium">{{
            formatBand(icer.band)
          }}</span>
          <span v-if="icer.comparison_pair" class="text-stone-400 ml-2">
            ({{ icer.comparison_pair }})
          </span>
          <span v-if="icer.uncertainty_level" class="text-stone-300 ml-2">
            &middot; {{ icer.uncertainty_level }} uncertainty
          </span>
        </div>
      </section>

      <!-- Methodological Decisions -->
      <section v-if="(data as any).decisions?.length" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Methodological decisions ({{ (data as any).decisions.length }})
        </p>
        <div class="space-y-4">
          <div
            v-for="d in (data as any).decisions"
            :key="d.id"
            class="border-t border-stone-100 pt-3"
          >
            <div class="flex items-start gap-3">
              <span
                class="text-xs font-medium text-stone-400 bg-stone-50 px-2 py-0.5 rounded whitespace-nowrap mt-0.5"
              >
                {{ formatCategory(d.decision_category) }}
              </span>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-stone-600 leading-relaxed">
                  {{ d.description }}
                </p>
                <div class="mt-2 space-y-1 text-xs text-stone-400">
                  <p v-if="d.company_position">
                    <span class="font-medium text-stone-500">Company:</span>
                    {{ d.company_position }}
                  </p>
                  <p v-if="d.erg_position">
                    <span class="font-medium text-stone-500">ERG:</span>
                    {{ d.erg_position }}
                  </p>
                  <p v-if="d.committee_preference">
                    <span class="font-medium text-stone-500">Committee:</span>
                    {{ d.committee_preference }}
                  </p>
                  <p
                    v-if="d.impact_on_icer"
                    class="text-stone-300"
                  >
                    ICER impact: {{ d.impact_on_icer }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Evidence Gaps -->
      <section v-if="(data as any).gaps?.length" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Evidence gaps
        </p>
        <div class="space-y-2">
          <div v-for="g in (data as any).gaps" :key="g.id" class="text-sm">
            <span class="text-stone-400">{{
              g.gap_type?.replace(/_/g, " ")
            }}</span>
            <span class="text-stone-300 mx-1">&mdash;</span>
            <span class="text-stone-600">{{ g.description }}</span>
          </div>
        </div>
      </section>

      <!-- Commercial Arrangement -->
      <section v-if="(data as any).arrangement" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Commercial arrangement
        </p>
        <div class="text-sm">
          <span class="text-stone-900">{{
            (data as any).arrangement.arrangement_type?.replace(/_/g, " ")
          }}</span>
          <span
            v-if="(data as any).arrangement.discount_confidential"
            class="text-stone-400 ml-2"
          >
            &middot; confidential
          </span>
          <span
            v-if="(data as any).arrangement.critical_for_recommendation"
            class="text-stone-400 ml-2"
          >
            &middot; critical for recommendation
          </span>
        </div>
      </section>

      <!-- Special Considerations -->
      <section v-if="(data as any).special" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Special considerations
        </p>
        <div class="flex flex-wrap gap-3 text-sm">
          <span
            v-if="(data as any).special.end_of_life_met"
            class="text-sea-600"
          >
            End of life criteria met
          </span>
          <span
            v-else-if="(data as any).special.end_of_life_considered"
            class="text-stone-400"
          >
            End of life considered (not met)
          </span>
          <span
            v-if="(data as any).special.severity_modifier_applied"
            class="text-sea-600"
          >
            Severity modifier applied
          </span>
          <span
            v-if="(data as any).special.cancer_drugs_fund_eligible"
            class="text-sea-600"
          >
            Cancer Drugs Fund eligible
          </span>
          <span
            v-if="(data as any).special.innovation_acknowledged"
            class="text-sea-600"
          >
            Innovation acknowledged
          </span>
          <span
            v-if="(data as any).special.equality_issues_raised"
            class="text-stone-600"
          >
            Equality issues raised
          </span>
        </div>
      </section>

      <!-- Cross References -->
      <section v-if="(data as any).crossRefs?.length" class="mt-10">
        <p
          class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-3"
        >
          Cross-references
        </p>
        <div class="space-y-1">
          <div v-for="xr in (data as any).crossRefs" :key="xr.id" class="text-sm">
            <NuxtLink
              v-if="xr.referenced_ta"
              :to="`/ta/${xr.referenced_ta}`"
              class="text-stone-900 font-medium hover:text-cadet-600 transition-colors"
            >
              TA{{ xr.referenced_ta }}
            </NuxtLink>
            <span class="text-stone-400 ml-2">
              {{ xr.relationship?.replace(/_/g, " ") }}
            </span>
            <span v-if="xr.context" class="text-stone-300 ml-1">
              &mdash; {{ xr.context }}
            </span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
