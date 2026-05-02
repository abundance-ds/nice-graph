export default defineEventHandler((event) => {
  const db = useDb();

  const taCount = (
    db
      .prepare("SELECT COUNT(DISTINCT ta_number) as n FROM corpus")
      .get() as { n: number }
  ).n;
  const docCount = (
    db.prepare("SELECT COUNT(*) as n FROM corpus").get() as { n: number }
  ).n;
  const graphCount = (
    db.prepare("SELECT COUNT(*) as n FROM ta_resolved").get() as { n: number }
  ).n;

  const text = `# NICE Technology Appraisals
# https://nice.shoulde.rs

${taCount} UK health technology assessments published by NICE (National Institute for Health and Care Excellence). ${docCount.toLocaleString()} source documents available as plain-text markdown. ${graphCount} appraisals have structured entity extraction covering drugs, conditions, methodological decisions, ICER bands, comparators, clinical trials, and economic models.

## How to use

Full corpus index (all ${taCount} TAs with document listings):
  GET /llms-full.txt

Search across all documents:
  GET /api/search?q={query}&format=plain
  Returns matching passages with TA number, document type, and page references.

Read a specific document:
  GET /api/corpus/ta{N}/{doc}.md
  Example: GET /api/corpus/ta876/FAD.md
  Returns markdown with <!-- page N --> markers for source tracing.

List documents for a TA:
  GET /api/corpus/ta{N}/
  Returns document names and page counts.

Download a document file:
  GET /api/corpus/ta{N}/{doc}.md?download=true

Ask a question (queries the knowledge graph via SQL):
  POST /api/chat
  Body: {"question": "Which TAs used partitioned survival models for lung cancer?", "history": []}
  Returns: Server-Sent Events stream.

## Knowledge graph (${graphCount} TAs with structured data)

Extracted from Final Appraisal Documents using Claude Haiku 4.5 with tool calling.

Tables:
  interventions — generic_name, drug_class, mechanism, route
  conditions — condition_name, therapeutic_area, disease_setting
  ta_resolved — title, recommendation_type, committee, line_of_therapy
  ta_methodological_decisions — decision_category, company_position, erg_position, committee_preference, impact_on_icer
    Categories: survival_extrapolation, treatment_effect_duration, treatment_effect_waning, indirect_comparison_method, utility_source, utility_value_choice, surrogate_endpoint_validity, comparator_selection, population_generalisability, subgroup_definition, crossover_adjustment, proportional_hazards, cost_assumption, stopping_rule, model_structure, treatment_sequencing, carer_utility, baseline_risk, cure_assumption, discount_rate, mortality_assumption, equivalence_assumption, other
  ta_comparators — comparator_name, type, is_established_practice
  ta_trials — trial_name, design, phase, blinding, crossover
  ta_economic_models — model_type, time_horizon, health_states
  ta_icer_bands — band (below_20k / 20k_to_30k / 30k_to_50k / 50k_to_100k / above_100k / dominant / not_estimable / confidential)
  ta_evidence_gaps — gap_type, description
  ta_commercial_arrangements — arrangement_type, confidential
  ta_cross_references — referenced_ta, relationship

## Source

GitHub: https://github.com/shoulders-ai/nice-graph
Data: https://www.nice.org.uk
`;

  setHeader(event, "Content-Type", "text/plain; charset=utf-8");
  return text;
});
