# Convergence Analysis: Agent A vs Agent B

## Strong convergence (both agents independently propose)

| Concept | Agent A | Agent B | Merged decision |
|---------|---------|---------|-----------------|
| Root entity | TechnologyAppraisal | TechnologyAppraisal | TechnologyAppraisal |
| Intervention | Technology | Intervention | Intervention (clearer name) |
| Condition | Condition | Condition | Condition |
| Comparator with dispute flags | committee_preferred, in_scope | is_established_practice | Merge: keep both perspectives |
| Clinical trial | ClinicalTrial | ClinicalTrial | ClinicalTrial |
| Economic model | EconomicModel | EconomicModel | EconomicModel |
| Reified methodological choices | CommitteeDecisionFactor (16 types) | MethodologicalDecision (17 types) | MethodologicalDecision (Agent B name, merged categories) |
| Commercial arrangement | PatientAccessScheme | CommercialArrangement | CommercialArrangement (broader) |
| ICER as categorical band | In recommendation object | ICERBand as separate entity | ICERBand fields on TA (not separate entity) |
| Cross-TA references | REFERENCES_TA relation | cross_references array | cross_references with relationship type |
| What NOT to extract | Same 6 categories | Same 7 categories | Aligned |

## Partial convergence (same idea, different framing)

| Concept | Agent A | Agent B | Decision |
|---------|---------|---------|----------|
| End-of-life criteria | Separate EndOfLifeCriteria entity | Boolean flags on TA + special_considerations | Fold into special_considerations (simpler for cheap model) |
| Cancer Drugs Fund | Separate CancerDrugsFund entity | Boolean flags on TA | Fold into special_considerations |
| Evidence gaps | Separate EvidenceGap entity (8 gap types) | Captured implicitly in MethodologicalDecision | Keep as separate array — evidence gaps are distinct from disputes |
| Utility source | Separate UtilitySource entity | Within MethodologicalDecision | Both: simple utility_sources array + can also appear as methodological_decision when disputed |
| Survival extrapolation | Separate survival_extrapolation object | Within MethodologicalDecision | Within MethodologicalDecision (it IS a methodological decision) |

## Divergence (one agent proposes, other doesn't)

| Concept | Agent | Include in v0.1? | Rationale |
|---------|-------|-----------------|-----------|
| Innovation as structured object | A | Yes (simplified) | Valuable cross-TA query: "which TAs acknowledged innovation?" |
| Treatment duration type on intervention | B | Yes | Key cost driver, easy to extract |
| Crossover flags on trial | B | Yes | Crossover adjustment is a major methodological issue |
| Generalisability flag on trial | B | Yes | Common committee concern, easy boolean |
| Line of therapy | B | Yes | Essential for cross-TA queries |
| SUPERSEDES_IN_PATHWAY relation | A | No (defer) | Hard to extract reliably, emerges from multiple TAs |
| Methods guide version | A | Yes | Important context for interpreting decisions |
| Scope comment separate schema | B | Defer | Focus on FAD first, add scope comments schema later |
| Company positioning vs committee | A | Captured in MethodologicalDecision | company_position vs committee_preference already there |

## Key design decisions for v0.1

1. **MethodologicalDecision is the highest-value entity** — both agents agree this is what pharma companies want. Keep it as the richest extraction target.
2. **Flat structure preferred** — avoid deep nesting. Each extraction section is a top-level array or object.
3. **All fields nullable** — cheap model should never need to hallucinate. Missing = null.
4. **Evidence gaps separate from methodological decisions** — a gap is "OS data immature", a decision is "company used Weibull, ERG preferred log-logistic, committee chose log-logistic". Different things.
5. **Special considerations grouped** — EOL, CDF, severity modifier, innovation as boolean flags in one object. Simpler than separate entities.
6. **Terminology normalisation in post-processing** — don't burden the cheap model with era-specific vocabulary. Extract as-is, normalise later.
