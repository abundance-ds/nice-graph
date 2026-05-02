# NICE Technology Appraisal — Extraction Prompt v0.6

Extract structured data from a ~10-page chunk of a NICE Technology Appraisal document (FAD, ACD, scope comments, or committee papers). Call `report_no_content` for chunks with no extractable information (appendices, member lists, boilerplate, number tables). Otherwise call `extract_appraisal_data`.

## Rules

- Only extract what is explicitly stated. Never infer.
- Use suggested enum values where they fit. If none fit, use a short descriptive string — a normalisation pass follows.
- Extract names as they appear (no normalisation).
- **Methodological decisions are the highest-value target.** Look for company vs ERG disagreements and committee conclusions.
- Do NOT extract: specific numbers (ICERs, QALYs, costs, HRs, p-values), committee member lists, implementation boilerplate, adverse event tables, dosing details, sensitivity analysis tables.
- Cross-references: extract TA numbers where stated. If referenced by title only, set `referenced_ta` to null.

## Decision categories

| Category | When to use |
|----------|-------------|
| survival_extrapolation | Parametric curve choice for extrapolating survival |
| treatment_effect_duration | How long treatment benefit assumed to last |
| treatment_effect_waning | Whether/how treatment effect diminishes over time |
| indirect_comparison_method | NMA, MAIC, ITC, STC validity |
| utility_source | Source of health-state utility values |
| utility_value_choice | Specific utility values disputed |
| surrogate_endpoint_validity | Whether surrogate predicts final outcome |
| comparator_selection | Which comparator is most relevant |
| population_generalisability | Whether trial population represents NHS patients |
| subgroup_definition | Subgroup definition and validity |
| crossover_adjustment | Treatment crossover handling |
| proportional_hazards | Whether PH assumption holds |
| cost_assumption | Disputed cost inputs |
| stopping_rule | Treatment duration caps or criteria |
| model_structure | Model type or health state choice |
| treatment_sequencing | Subsequent treatment modelling |
| cure_assumption | When/whether patients assumed cured |
| discount_rate | Non-reference-case discount rate |
| mortality_assumption | Background/disease-specific mortality disputes |
| equivalence_assumption | Clinical equivalence justifying cost-comparison |
| other | Any dispute not covered above |

## ICER band mapping

| Text signal | Band |
|-------------|------|
| "cost effective" / "within acceptable range" / below £20k | below_20k |
| Lower end of acceptable / £20-30k range | 20k_to_30k |
| Acceptable with end-of-life/severity modifier / £30-50k | 30k_to_50k |
| Above standard range but below £100k | 50k_to_100k |
| Well above acceptable / £100k+ | above_100k |
| Less costly and more effective | dominant |
| Could not be estimated / too uncertain | not_estimable |
| Confidential, no characterisation given | confidential |

## Terminology (extract as-is, do not normalise)

ERG = EAG = Assessment Group · Appraisal Committee = Evaluation Committee · FAD = Final Appraisal Determination = Final Draft Guidance · PAS = Patient Access Scheme = Commercial Access Agreement · STA/MTA/HST = Single/Multiple Technology Appraisal / Highly Specialised Technology
