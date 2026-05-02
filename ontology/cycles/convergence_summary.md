# Ontology Development — Convergence Summary

## Overview

Developed a knowledge graph ontology for NICE Technology Appraisals through 7 phases:
1. Independent exploration by 2 Opus agents (20 TAs)
2. Convergence analysis and v0.1 merge
3. Five iterative refinement rounds (50 TAs)

**Total TAs tested: 70** across 2003-2025, covering all therapeutic areas, recommendation types, appraisal types, and methods guide eras.

**Final version: v0.5.1** — declared stable and ready for bulk extraction.

---

## Convergence trajectory

| Round | TAs | Focus | New decision categories | New entity types | Structural changes | `other` usage estimate |
|-------|-----|-------|------------------------|------------------|--------------------|----------------------|
| Exploration | 20 | All areas | 17 (initial) | 9 (initial) | N/A | ~25% |
| Round 1 | 10 | Non-cancer diversity | +2 (carer_utility, baseline_risk) | 0 | +3 enum expansions | ~18% |
| Round 2 | 10 | Oncology/rare disease | +2 (cure_assumption, discount_rate) | 0 | therapeutic_area→array, icer_band→array | ~12% |
| Round 3 | 10 | Complex CE stress test | +2 (mortality_assumption, equivalence_assumption) | 0 | ICER direction field | ~8% |
| Round 4 | 10 | Edge cases (old, devices) | 0 | 0 | +intervention_type enum | ~5% |
| Round 5 | 10 | Final stability test | 0 | 0 | +1 enum value (as_needed) | ~3-5% |

**Key signal: new issues per round declining monotonically to zero.**

---

## Final schema summary

### Entity types (9, stable since v0.1)

| Entity | Definition | Extraction difficulty |
|--------|-----------|----------------------|
| TechnologyAppraisal | Root entity: TA number, recommendation, dates | Easy |
| Intervention | Drug/device/procedure under appraisal | Easy |
| Condition | Disease at marketing-authorisation specificity | Easy |
| Comparator | Treatment compared against | Easy-Medium |
| ClinicalTrial | Named study providing key evidence | Easy |
| EconomicModel | Model type, health states, time horizon | Medium |
| MethodologicalDecision | Company vs ERG vs committee on a specific issue | Hard (highest value) |
| EvidenceGap | Explicit gap in evidence flagged by committee | Medium |
| CommercialArrangement | PAS, MAA, CAA | Easy |

### Decision categories (21)

survival_extrapolation, treatment_effect_duration, treatment_effect_waning, indirect_comparison_method, utility_source, utility_value_choice, surrogate_endpoint_validity, comparator_selection, population_generalisability, subgroup_definition, crossover_adjustment, proportional_hazards, cost_assumption, stopping_rule, model_structure, treatment_sequencing, carer_utility, baseline_risk, cure_assumption, discount_rate, mortality_assumption, equivalence_assumption + other

### Evidence gap types (12)

immature_overall_survival, no_direct_comparison, no_uk_data, surrogate_not_validated, missing_subgroup_data, missing_quality_of_life_data, short_follow_up, no_comparator_data, missing_real_world_evidence, single_arm_evidence_only, instrument_insensitivity + other

---

## What the schema captures well

1. **Methodological decisions** — the core value proposition. Every TA from 2003-2025 yielded 2-6 extractable decisions with company/ERG/committee positions. This enables the key use case: "What has NICE decided about [topic] across TAs?"

2. **Cross-TA references** — TAs cite each other for precedent, utility values, comparator guidance. This creates a queryable citation network.

3. **ICER categorisation** — avoiding exact numbers while preserving decision-relevant information (band + direction + uncertainty).

4. **Therapeutic diversity** — schema handles oncology, cardiovascular, neurology, rare disease, devices, procedures, and digital health without specialised entity types.

5. **Temporal diversity** — pre-2008 through 2025, with methods_guide_era flagging framework changes.

## Known limitations (acceptable)

1. **Multi-intervention MTAs** — recommendation_type is per-TA, not per-intervention. For MTAs with mixed recommendations (e.g. TA284: 4 recommended, 2 not recommended), the recommendation details go in restriction_details text. This loses queryability but affects <5% of TAs.

2. **Complex treatment pathways** — sequential biologic positioning (e.g. "after failure of TNF inhibitor but before JAK inhibitor") is captured in restriction_details text, not structured. Structuring this would require a pathway entity that adds complexity for limited gain.

3. **Cross-references without TA numbers** — older documents reference other NICE guidance by title without citing TA numbers. Post-processing can resolve these via title matching against the TA index.

4. **Scope comments** — deferred to v0.2 of the extraction pipeline. The FAD-focused schema captures the committee's final positions; scope comments capture earlier stakeholder arguments.

5. **~5% `other` usage** — residual for highly idiosyncratic issues (consent procedures in ECT, wig provision for alopecia). Not worth adding categories for.

---

## Readiness for bulk extraction

**Verdict: READY.**

- Schema structurally stable (0 changes in rounds 4-5)
- 21 decision categories cover >95% of methodological disputes
- 12 evidence gap types cover >95% of gaps
- All enums tested across the full temporal and therapeutic range
- Extraction prompt tested and refined through 50 TAs

**Next step: Model comparison test** — run 100 diverse chunks through Haiku, Flash Lite, and Flash to evaluate extraction quality at the cheap-model tier.

---

## Files produced

| File | Description |
|------|-------------|
| `ontology/ontology.json` | Formal schema v0.5.1 |
| `ontology/extraction_prompt.md` | Extraction prompt v0.5 |
| `ontology/methods.md` | Methodology documentation |
| `ontology/cycles/exploration_agent_a.md` | Agent A initial proposal (10 TAs) |
| `ontology/cycles/exploration_agent_b.md` | Agent B initial proposal (10 TAs) |
| `ontology/cycles/convergence_analysis.md` | Merge analysis |
| `ontology/cycles/round1_extraction.md` | Round 1: non-cancer (10 TAs) |
| `ontology/cycles/round2_extraction.md` | Round 2: oncology/rare (10 TAs) |
| `ontology/cycles/round3_extraction.md` | Round 3: complex CE (10 TAs) |
| `ontology/cycles/round4_extraction.md` | Round 4: edge cases (10 TAs) |
| `ontology/cycles/round5_extraction.md` | Round 5: stability test (10 TAs) |
| `ontology/cycles/convergence_summary.md` | This document |
