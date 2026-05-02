# Round 2 Extraction Test: Oncology / Haematology / Rare Disease TAs

Ontology version: 0.2.0
Tested against: 10 FADs spanning 2009--2024
Tester: Claude Opus (round 2 refinement cycle)

---

## 1. TA171 — Lenalidomide for multiple myeloma (2nd line+, 2009)

### Abbreviated extraction

```json
{
  "ta_number": "TA171",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Lenalidomide for the treatment of multiple myeloma in people who have received at least one prior therapy",
    "issue_date": "April 2009",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Only in people who have received 2+ prior therapies; manufacturer covers drug cost beyond 26 cycles",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "Peninsula Technology Assessment Group (PenTAG)",
    "line_of_therapy": ["third_line_plus"],
    "eligible_population": "~2100 patients",
    "methods_guide_era": "2008"
  },
  "interventions": [{
    "generic_name": "lenalidomide",
    "brand_name": "Revlimid",
    "manufacturer": "Celgene",
    "drug_class": "immunomodulatory derivative",
    "mechanism_of_action": "immunomodulating agent with anti-neoplastic, anti-angiogenic and proerythropoietic properties",
    "route_of_administration": "oral",
    "is_combination_regimen": true,
    "combination_components": ["lenalidomide", "dexamethasone"],
    "treatment_duration_type": "treat_to_progression",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "multiple myeloma after at least one prior therapy",
    "therapeutic_area": "haematology",
    "disease_setting": "other",
    "biomarker_defined_population": false,
    "biomarker_name": null
  }],
  "comparators": [
    {
      "comparator_name": "bortezomib monotherapy",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "dexamethasone",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "MM-009",
      "study_design": "RCT",
      "phase": "phase III",
      "is_pivotal": true,
      "primary_outcome": "time to progression",
      "sample_size": 353,
      "crossover_occurred": true,
      "crossover_adjusted": true,
      "generalisability_concern": false
    },
    {
      "trial_name": "MM-010",
      "study_design": "RCT",
      "phase": "phase III",
      "is_pivotal": true,
      "primary_outcome": "time to progression",
      "sample_size": 351,
      "crossover_occurred": true,
      "crossover_adjusted": true,
      "generalisability_concern": false
    }
  ],
  "economic_model": {
    "model_type": "discrete_event_simulation",
    "model_source": "company",
    "time_horizon": "lifetime",
    "cycle_length": null,
    "health_states": ["response-based states (complete, partial, stable, progressive)"]
  },
  "methodological_decisions": [
    {
      "decision_category": "crossover_adjustment",
      "description": "Calibrating dexamethasone OS curve to mean vs median survival from MRC trials",
      "company_position": "Calibrate to median survival from MRC trials",
      "erg_position": "Calibrate to mean survival from MRC trials (more methodologically correct)",
      "committee_preference": "Agreed with ERG that mean was more appropriate",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "survival_extrapolation",
      "description": "Fit of len/dex OS curve to trial data",
      "company_position": "Original model overestimated OS",
      "erg_position": "Improved fit of len/dex OS curve needed",
      "committee_preference": "Agreed with ERG's improved curve fit",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Bortezomib vs dexamethasone as comparator by line",
      "company_position": "Bortezomib for 1 prior therapy; dexamethasone for 2+ prior therapies",
      "erg_position": "Agreed with subgroup-specific comparators",
      "committee_preference": "Accepted bortezomib for 1 prior therapy, dexamethasone for 2+ prior",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trial of lenalidomide vs bortezomib; indirect comparison via dexamethasone with heterogeneity"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "dose_cap",
    "discount_confidential": false,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "30k_to_50k",
    "comparison_pair": "lenalidomide/dex vs dexamethasone (2+ prior therapies)",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate"
  },
  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": true,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },
  "cross_references": [
    {
      "referenced_ta": "TA129",
      "relationship": "comparator_guidance",
      "context": "Bortezomib monotherapy for relapsed multiple myeloma — established the comparator and its rebate scheme"
    }
  ]
}
```

### Schema stress points
- **dose_cap arrangement**: The 26-cycle cap is not a simple discount; `dose_cap` fits but this is a manufacturer-funded continuation, not a traditional cap. The schema could distinguish "free drug beyond X cycles" more precisely.
- **disease_setting**: "Relapsed" myeloma after 2+ therapies doesn't map cleanly. No `relapsed` or `relapsed_refractory` enum value exists.
- **line_of_therapy as array**: Recommendation is specifically for 3rd line+. Works correctly.
- **Pre-CDF era**: The end-of-life criteria are applied (correctly flagged) but CDF didn't exist yet. The schema handles this fine via separate boolean fields.

---

## 2. TA284 — Topotecan, PLDH, paclitaxel, trabectedin, gemcitabine for recurrent ovarian cancer (MTA, 2013)

### Abbreviated extraction

```json
{
  "ta_number": "TA284",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Topotecan, pegylated liposomal doxorubicin hydrochloride, paclitaxel, trabectedin and gemcitabine for treating recurrent ovarian cancer",
    "issue_date": "December 2014",
    "recommendation_type": "MIXED — see restriction_details",
    "restriction_details": "Paclitaxel+platinum: recommended. PLDH mono: recommended. PLDH+platinum: recommended (off-label). Gemcitabine+carboplatin: NOT recommended for 1st recurrence. Trabectedin+PLDH: NOT recommended for 1st recurrence. Topotecan: NOT recommended.",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "Assessment Group (unnamed in excerpt)",
    "line_of_therapy": ["second_line", "third_line_plus"],
    "methods_guide_era": "2013"
  },
  "interventions": [
    {"generic_name": "paclitaxel", "is_combination_regimen": true, "combination_components": ["paclitaxel", "carboplatin"]},
    {"generic_name": "pegylated liposomal doxorubicin hydrochloride", "brand_name": "Caelyx", "manufacturer": "Jansen-Cilag"},
    {"generic_name": "gemcitabine", "is_combination_regimen": true, "combination_components": ["gemcitabine", "carboplatin"]},
    {"generic_name": "trabectedin", "brand_name": "Yondelis", "manufacturer": "PharmaMar", "is_combination_regimen": true, "combination_components": ["trabectedin", "PLDH"]},
    {"generic_name": "topotecan"}
  ],
  "conditions": [{
    "condition_name": "recurrent ovarian cancer (platinum-sensitive and platinum-resistant/refractory)",
    "therapeutic_area": "oncology",
    "disease_setting": "other"
  }],
  "economic_model": {
    "model_type": "other",
    "model_source": "assessment_group",
    "time_horizon": "15 years",
    "health_states": ["stable disease", "progressive disease", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "Two separate networks needed (platinum-based and non-platinum) — could not simultaneously compare all interventions",
      "company_position": null,
      "erg_position": "Constructed 2 discrete networks for platinum-sensitive disease",
      "committee_preference": "Accepted Assessment Group's approach as reasonable given data",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "other",
      "description": "Retrospective adjustment of treatment effects for platinum-free interval in trabectedin OVA-301 trial",
      "company_position": "Post-hoc adjustment for platinum-free interval, ECOG, CA125 is appropriate — reduces ICER from £77k to £28k",
      "erg_position": "Post-hoc adjustment is an unvalidated approach; unadjusted results more reliable",
      "committee_preference": "Did not accept manufacturer's post-hoc adjustments; preferred Assessment Group's unadjusted ICER of £77k",
      "impact_on_icer": "decreases"
    }
  ],
  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": null,
    "cancer_drugs_fund_considered": false,
    "innovation_acknowledged": false
  },
  "cross_references": [
    {"referenced_ta": "TA91", "relationship": "same_condition", "context": "Previous guidance on 2nd-line ovarian cancer — superseded by this MTA"},
    {"referenced_ta": "TA222", "relationship": "same_drug", "context": "Previous trabectedin guidance — superseded by this MTA"}
  ]
}
```

### Schema stress points
- **CRITICAL: Multi-intervention MTA with mixed recommendations.** `recommendation_type` is a single enum. TA284 recommends some drugs, does not recommend others. The schema design note says "capture as restriction_details text" but this loses queryability. An array of recommendation objects per intervention would be far more powerful.
- **SUPERSEDES**: TA284 explicitly supersedes TA91 and TA222. This maps to the `SUPERSEDES` cross-TA relation nicely.
- **model_source**: Should be "assessment_group" but the enum doesn't include this — only "company" is implied. Need an explicit enum for model_source.
- **disease_setting**: "Recurrent" is not in the enum. Platinum-sensitive recurrence is a key clinical concept in ovarian cancer. Missing value.

---

## 3. TA538 — Dinutuximab beta for neuroblastoma (2018, paediatric, rare)

### Abbreviated extraction

```json
{
  "ta_number": "TA538",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Dinutuximab beta for treating neuroblastoma",
    "issue_date": "July 2018",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Only for high-risk neuroblastoma in people aged 12 months+, whose disease has at least partially responded to induction chemo + myeloablative therapy + SCT; must not have had prior anti-GD2 immunotherapy; commercial arrangement required",
    "appraisal_type": "STA",
    "committee_name": "committee D",
    "erg_or_eag_name": "ERG (unnamed) + NICE Decision Support Unit (DSU)",
    "line_of_therapy": ["maintenance"],
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "dinutuximab beta",
    "brand_name": "Qarziba",
    "manufacturer": "EUSA Pharma",
    "drug_class": "anti-GD2 monoclonal antibody",
    "route_of_administration": "intravenous",
    "is_combination_regimen": false,
    "treatment_duration_type": "fixed_duration",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "high-risk neuroblastoma",
    "therapeutic_area": "oncology",
    "disease_setting": "maintenance",
    "biomarker_defined_population": false
  }],
  "comparators": [{
    "comparator_name": "isotretinoin",
    "comparator_type": "active_drug",
    "is_established_practice": true,
    "committee_preferred": true
  }],
  "clinical_trials": [{
    "trial_name": "APN311-302 (HR-NBL-1)",
    "study_design": "RCT",
    "phase": "phase III",
    "blinding": "open_label",
    "is_pivotal": true,
    "primary_outcome": "event-free survival at 3 years",
    "sample_size": 379,
    "crossover_occurred": false,
    "generalisability_concern": false
  }],
  "economic_model": {
    "model_type": "partitioned_survival",
    "model_source": "company",
    "time_horizon": "10 years (with cure threshold)",
    "health_states": ["event-free", "failure", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "survival_extrapolation",
      "description": "Extrapolation of dinutuximab beta event-free and overall survival beyond 70 months with choice of parametric curve",
      "company_position": "Gompertz extrapolation preferred; reflects expected plateau after 5 years",
      "erg_position": "DSU explored spline models; considered Gompertz or 2-knot spline most plausible for OS",
      "committee_preference": "Gompertz or 2-knot spline for OS, Gompertz or 1-knot spline for EFS; all extrapolations uncertain",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "other",
      "description": "Cure threshold — time point after which surviving patients are considered cured",
      "company_position": "10-year cure threshold",
      "erg_position": "Range of cure thresholds plausible (5, 7, 10 years)",
      "committee_preference": "Preferred 10-year cure threshold but considered others plausible",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "indirect_comparison_method",
      "description": "Matched-adjusted indirect comparison (MAIC) of dinutuximab beta vs isotretinoin using ANBL0032 trial data",
      "company_position": "MAIC using ANBL0032 (Yu et al. 2010) shows dinutuximab beta improves EFS and OS",
      "erg_position": "DSU cautioned re exponential assumption; used Yu et al. 2014 longer-term data",
      "committee_preference": "MAIC results accepted; latest ANBL0032 data (2014) most appropriate",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "other",
      "description": "Discount rate — 1.5% vs 3.5% reference case",
      "company_position": "1.5% discount rate appropriate for potentially curative treatment in children",
      "erg_position": null,
      "committee_preference": "Accepted 1.5% discount rate for both costs and outcomes",
      "impact_on_icer": "decreases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No trial comparing dinutuximab beta with isotretinoin; all patients in APN311-302 had dinutuximab beta"
    },
    {
      "gap_type": "immature_overall_survival",
      "description": "Long-term benefit is main source of uncertainty; marketing authorisation granted under exceptional circumstances due to immature data"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "above_50k",
    "comparison_pair": "dinutuximab beta vs isotretinoin",
    "is_committee_preferred": true,
    "uncertainty_level": "very_high"
  },
  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": false,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": true,
    "cancer_drugs_fund_eligible": false,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  }
}
```

### Schema stress points
- **CRITICAL: "Cure threshold/cure point"** is a major methodological concept in oncology/haematology (appears in 4 of 10 TAs in this round). Not represented in `decision_categories`. Needs its own category like `cure_assumption` or `cure_threshold`.
- **Non-reference-case discount rate (1.5%)**: This is a significant methodological decision. The schema has no dedicated decision category for this. It's not `cost_assumption` exactly — it's a framework-level methods choice. Could be `other` but this loses important query capability.
- **"Rarity/severity weighting"**: The committee explicitly states it is being flexible because of rarity and severity. The schema has no field to capture severity-based flexibility in decision-making (distinct from the `severity_modifier_applied` in the 2022 methods guide). This is a predecessor concept.
- **Paediatric population**: No field to indicate this is a paediatric appraisal. This matters for contextual queries.
- **therapeutic_area**: Neuroblastoma is both oncology and rare_disease. The schema allows only one value. Needs to be an array or have a separate `is_rare_disease` flag.

---

## 4. TA587 — Lenalidomide + dexamethasone for previously untreated multiple myeloma (2019)

### Abbreviated extraction

```json
{
  "ta_number": "TA587",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Lenalidomide plus dexamethasone for previously untreated multiple myeloma",
    "issue_date": "May 2019",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Only for adults not eligible for SCT AND (thalidomide contraindicated OR not tolerated)",
    "appraisal_type": "STA",
    "committee_name": "committee B",
    "erg_or_eag_name": "ERG (unnamed)",
    "line_of_therapy": ["first_line"],
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "lenalidomide",
    "brand_name": "Revlimid",
    "manufacturer": "Celgene",
    "drug_class": "immunomodulatory derivative",
    "route_of_administration": "oral",
    "is_combination_regimen": true,
    "combination_components": ["lenalidomide", "dexamethasone"],
    "treatment_duration_type": "treat_to_progression",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "previously untreated multiple myeloma in adults not eligible for stem cell transplant",
    "therapeutic_area": "haematology",
    "disease_setting": "chronic",
    "biomarker_defined_population": false
  }],
  "comparators": [{
    "comparator_name": "bortezomib plus melphalan plus prednisone (VMP)",
    "comparator_type": "active_drug",
    "is_established_practice": true,
    "committee_preferred": true
  }],
  "clinical_trials": [{
    "trial_name": "FIRST",
    "study_design": "RCT",
    "phase": "phase III",
    "blinding": "open_label",
    "is_pivotal": true,
    "primary_outcome": "progression-free survival",
    "sample_size": 1082,
    "crossover_occurred": false,
    "generalisability_concern": true
  }],
  "economic_model": {
    "model_type": "other",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": ["pre-progression", "progressed disease", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "model_structure",
      "description": "Hybrid model: partitioned survival (KM data) for first 92 weeks then multi-state Markov with constant transition probabilities",
      "company_position": "Hybrid approach accounts for structural link between progression and mortality",
      "erg_position": "92-week cut-off appropriate; not sensitive to cut-off; but partitioned survival would have allowed more flexible modelling",
      "committee_preference": "Accepted 92-week cut-off but unclear on advantage of hybrid vs standard partitioned survival",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "utility_value_choice",
      "description": "Whether VMP utility decrement continues after VMP treatment stops",
      "company_position": "Utility decrement during VMP continues even after stopping",
      "erg_position": "No evidence for continuing decrement; utility should be same after VMP stops",
      "committee_preference": "Agreed with ERG — same utility after VMP treatment stops",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "treatment_sequencing",
      "description": "Second-line and later treatments in the model do not reflect current NHS practice (includes thalidomide and retreatment with lenalidomide for patients who cannot take thalidomide)",
      "company_position": "Used treatments from FIRST trial",
      "erg_position": "Inappropriate treatments included; could remove costs but not effects",
      "committee_preference": "Concluded model does not reflect clinical practice but unclear what effect this has on ICER",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "population_generalisability",
      "description": "FIRST trial only enrolled patients who could take thalidomide; results applied to thalidomide-intolerant population",
      "company_position": "Results for lenalidomide arm generalisable regardless of thalidomide tolerance",
      "erg_position": null,
      "committee_preference": "Accepted results unlikely to differ markedly in thalidomide-intolerant group, but concerned about mismatch",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "lenalidomide/dex vs VMP (with new simple-discount PAS in both arms scenario: ~£27k)",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate"
  },
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "cancer_drugs_fund_considered": false,
    "innovation_acknowledged": true,
    "equality_issues_raised": false
  },
  "cross_references": [
    {
      "referenced_ta": "TA171",
      "relationship": "same_drug",
      "context": "Lenalidomide previously recommended for 2+ prior therapies; this appraises first-line use"
    }
  ]
}
```

### Schema stress points
- **Multiple PAS scenarios**: The ICER depends on which PAS applies (new simple discount in intervention only, or in both arms). The `icer_band` field captures one band but the FAD discusses two scenarios (£20k and £27k). Need ability to record multiple ICER bands with different PAS assumptions.
- **Transplant eligibility**: The eligible population is defined by transplant ineligibility. No field captures this surgical eligibility criterion.
- **disease_setting = "chronic"** is the closest fit for untreated myeloma, but "newly_diagnosed" or "first_line" would be more accurate as disease_setting values.

---

## 5. TA642 — Gilteritinib for relapsed/refractory AML (2020, targeted therapy)

### Abbreviated extraction

```json
{
  "ta_number": "TA642",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Gilteritinib for treating relapsed or refractory acute myeloid leukaemia",
    "issue_date": "June 2020",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Only for FLT3-mutation-positive AML in adults; must not restart as maintenance after stem cell transplant",
    "appraisal_type": "STA",
    "committee_name": "committee C",
    "line_of_therapy": ["second_line"],
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "gilteritinib",
    "brand_name": "Xospata",
    "manufacturer": "Astellas Pharma",
    "drug_class": "FLT3 inhibitor",
    "mechanism_of_action": "FLT3 tyrosine kinase inhibitor",
    "route_of_administration": "oral",
    "is_combination_regimen": false,
    "treatment_duration_type": "treat_to_progression"
  }],
  "conditions": [{
    "condition_name": "relapsed or refractory FLT3-mutation-positive acute myeloid leukaemia",
    "therapeutic_area": "haematology",
    "disease_setting": "other",
    "biomarker_defined_population": true,
    "biomarker_name": "FLT3 mutation"
  }],
  "comparators": [{
    "comparator_name": "salvage chemotherapy (LoDAC, MEC, FLAG-IDA)",
    "comparator_type": "standard_of_care",
    "is_established_practice": true,
    "committee_preferred": true
  }],
  "clinical_trials": [{
    "trial_name": "ADMIRAL",
    "study_design": "RCT",
    "phase": "phase III",
    "blinding": "open_label",
    "is_pivotal": true,
    "primary_outcome": "overall survival",
    "crossover_occurred": false,
    "generalisability_concern": true
  }],
  "methodological_decisions": [
    {
      "decision_category": "other",
      "description": "Cure point assumption — 2 years vs 3 years",
      "company_position": "Originally 3-year cure point; updated to 2-year without clear rationale",
      "erg_position": "KM curves from ADMIRAL did not show plateau suggesting cure",
      "committee_preference": "Cure point between 2 and 3 years plausible, more likely closer to 2 years",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "treatment_effect_duration",
      "description": "Whether gilteritinib maintenance therapy after SCT provides additional survival benefit",
      "company_position": "Applied HR 0.69 for maintenance benefit based on naive indirect comparison",
      "erg_position": "ADMIRAL data show no favourable effect of gilteritinib post-SCT (HR 1.108); HR 1 (no benefit) preferred",
      "committee_preference": "No robust evidence of post-transplant maintenance benefit; excluded from model; gilteritinib should not restart after SCT",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Drug costs applied as one-off in first cycle vs spread across cycles",
      "company_position": "One-off drug costs in first cycle",
      "erg_position": "Drug costs should be applied per cycle to allow proper discounting and link to progression",
      "committee_preference": "Drug costs should be applied in each cycle",
      "impact_on_icer": "increases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "short_follow_up",
      "description": "Considerable uncertainty about long-term survival, particularly after stem cell transplant"
    }
  ],
  "icer_band": {
    "band": "30k_to_50k",
    "comparison_pair": "gilteritinib vs salvage chemotherapy",
    "is_committee_preferred": true,
    "uncertainty_level": "high"
  },
  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": true,
    "cancer_drugs_fund_considered": false,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },
  "cross_references": [
    {
      "referenced_ta": "midostaurin TA",
      "relationship": "same_condition",
      "context": "Midostaurin recommended for newly diagnosed FLT3+ AML; gilteritinib for relapsed/refractory. Prior midostaurin use in clinical practice may be higher than in ADMIRAL trial"
    }
  ]
}
```

### Schema stress points
- **Cure point/cure assumption**: Again needs its own `decision_category`. This is the 2nd of 4 TAs where it appears.
- **disease_setting**: "Relapsed or refractory" is not in the enum. This is an extremely common oncology/haematology setting. Needs `relapsed_refractory` value.
- **Post-transplant maintenance restriction**: The recommendation explicitly prohibits restarting treatment after SCT. The restriction_details captures this as text, but it's a novel pattern — treatment is recommended but with a negative condition on a subsequent event. May need structured representation.
- **Sequencing after biomarker-selected prior therapy**: The fact that prior midostaurin use might affect gilteritinib efficacy is a treatment-sequencing concern specific to targeted therapies. The ontology captures this as a decision but the concept of "prior biomarker-matched therapy impact" is increasingly important.

---

## 6. TA741 — Apalutamide + ADT for hormone-sensitive metastatic prostate cancer (2021)

### Abbreviated extraction

```json
{
  "ta_number": "TA741",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Apalutamide with androgen deprivation therapy for treating hormone-sensitive metastatic prostate cancer",
    "issue_date": "October 2021",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Only when docetaxel is not suitable",
    "appraisal_type": "STA",
    "committee_name": "committee B",
    "line_of_therapy": ["first_line"],
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "apalutamide",
    "brand_name": "Erleada",
    "manufacturer": "Janssen",
    "drug_class": "second-generation androgen receptor inhibitor",
    "route_of_administration": "oral",
    "is_combination_regimen": true,
    "combination_components": ["apalutamide", "androgen deprivation therapy"],
    "treatment_duration_type": "treat_to_progression"
  }],
  "conditions": [{
    "condition_name": "hormone-sensitive metastatic prostate cancer",
    "therapeutic_area": "oncology",
    "disease_setting": "metastatic",
    "biomarker_defined_population": false
  }],
  "comparators": [
    {"comparator_name": "ADT alone", "comparator_type": "active_drug", "is_established_practice": true, "committee_preferred": true},
    {"comparator_name": "docetaxel plus ADT", "comparator_type": "active_drug", "is_established_practice": true, "committee_preferred": false}
  ],
  "clinical_trials": [{
    "trial_name": "TITAN",
    "study_design": "RCT",
    "phase": "phase III",
    "is_pivotal": true,
    "primary_outcome": "overall survival and radiographic progression-free survival (coprimary)",
    "sample_size": 1052,
    "crossover_occurred": true,
    "crossover_adjusted": true,
    "generalisability_concern": true
  }],
  "economic_model": {
    "model_type": "partitioned_survival",
    "model_source": "company",
    "health_states": ["progression-free survival", "progressed disease (3 lines)", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "crossover_adjustment",
      "description": "Modified RPSFTM to adjust for crossover from placebo+ADT to apalutamide+ADT and for having second AR inhibitor",
      "company_position": "Modified RPSFTM using COU-AA-302 data to adjust for both crossover and second AR inhibitor",
      "erg_position": "Could not verify results; agreed with using COU-AA-302 but noted potential bias from adjusting for 2nd AR inhibitor",
      "committee_preference": "Modified RPSFTM acceptable but uncertain; considered both adjusted and unadjusted results",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "survival_extrapolation",
      "description": "Weibull model for rPFS extrapolation despite worse statistical fit; refusal to explore flexible models",
      "company_position": "Weibull curves based on clinical plausibility",
      "erg_position": "Weibull has worse AIC/BIC; more flexible models would be more appropriate",
      "committee_preference": "Disappointed company declined flexible models; Weibull uncertain but acceptable for decision-making",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "treatment_effect_waning",
      "description": "Whether apalutamide treatment benefit wanes over time",
      "company_position": "No waning; no evidence of convergence in TITAN OS curves",
      "erg_position": "Unclear from hazard plots; resistance to AR inhibitors likely develops over time",
      "committee_preference": "Waning affects ICER by ~£2000; factored into decision making",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "treatment_sequencing",
      "description": "Only one AR inhibitor would be used in the NHS pathway; choosing apalutamide first-line removes later options",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "Confirmed only 1 newer AR inhibitor would be commissioned; choosing apalutamide removes enzalutamide/abiraterone later",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "icer_band": {
    "band": "above_50k",
    "comparison_pair": "apalutamide+ADT vs docetaxel+ADT",
    "is_committee_preferred": false,
    "uncertainty_level": "high"
  },
  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": false,
    "cancer_drugs_fund_considered": false,
    "innovation_acknowledged": false,
    "equality_issues_raised": true
  },
  "cross_references": [
    {"referenced_ta": "TA387", "relationship": "utility_reuse", "context": "Utility values for 2nd/3rd line treatments from abiraterone TA387"},
    {"referenced_ta": "TA377", "relationship": "utility_reuse", "context": "ERG preferred unadjusted utility values from enzalutamide TA377"},
    {"referenced_ta": "TA580", "relationship": "utility_reuse", "context": "Utility values compared with enzalutamide for HR non-metastatic TA580"}
  ]
}
```

### Schema stress points
- **Coprimary endpoints**: `primary_outcome` is a string, not an array. TITAN had coprimary endpoints (OS + rPFS). Need array.
- **PFS2 / radiographic PFS**: The schema doesn't have a concept for "PFS on next treatment line" (PFS2), which is increasingly used in prostate cancer and myeloma.
- **Equality: gender reassignment**: The committee explicitly notes prostate cancer recommendations apply to "all people with a prostate" regardless of gender identity. This is a recurring equality consideration for sex-specific cancers. The schema captures `equality_issues_raised` as boolean but not the nature of the issue.
- **Subgroup-specific recommendations without subgroup data**: The recommendation is for "docetaxel-unsuitable" patients but TITAN excluded these patients (ECOG 2+). The schema doesn't capture the gap between the recommended population and the trial population.
- **Multiple ICER bands needed**: Not cost-effective vs docetaxel (above_50k) but acceptable vs ADT alone for docetaxel-unsuitable patients. Two distinct comparisons, two bands.

---

## 7. TA802 — Cemiplimab for advanced cutaneous squamous cell carcinoma (2022, CDF exit)

### Abbreviated extraction

```json
{
  "ta_number": "TA802",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Cemiplimab for treating advanced cutaneous squamous cell carcinoma",
    "issue_date": "May 2022",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Stopping rule at 24 months or earlier if disease progresses",
    "appraisal_type": "STA",
    "committee_name": "committee A",
    "line_of_therapy": ["first_line"],
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "cemiplimab",
    "brand_name": "Libtayo",
    "manufacturer": "Sanofi",
    "drug_class": "anti-PD-1 monoclonal antibody",
    "route_of_administration": "intravenous",
    "is_combination_regimen": false,
    "treatment_duration_type": "fixed_duration"
  }],
  "conditions": [{
    "condition_name": "metastatic or locally advanced cutaneous squamous cell carcinoma not suitable for curative surgery or radiotherapy",
    "therapeutic_area": "dermatology",
    "disease_setting": "metastatic",
    "biomarker_defined_population": false
  }],
  "comparators": [{
    "comparator_name": "best supportive care",
    "comparator_type": "best_supportive_care",
    "is_established_practice": true,
    "committee_preferred": true
  }],
  "clinical_trials": [{
    "trial_name": "EMPOWER-CSCC 1",
    "study_design": "single_arm",
    "phase": "phase II",
    "is_pivotal": true,
    "primary_outcome": "objective response rate",
    "sample_size": 219,
    "crossover_occurred": false,
    "generalisability_concern": true
  }],
  "methodological_decisions": [
    {
      "decision_category": "population_generalisability",
      "description": "SACT (real-world) data shows lower OS and older population than trial; uncertain whether trial results generalisable to UK practice",
      "company_position": "SACT data limited by COVID-19 impact, shorter follow-up, less experienced clinicians",
      "erg_position": "Concerned about generalisability; SACT patients older with lower OS",
      "committee_preference": "Uncertain whether trial results generalisable; would have liked SACT OS modelled as scenario",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Best supportive care vs platinum-based chemotherapy as comparator",
      "company_position": "Presented evidence vs both; accepted BSC as primary comparator",
      "erg_position": "Agreed BSC most appropriate",
      "committee_preference": "BSC is the most appropriate comparator; <5% of patients receive chemotherapy",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Treatment duration capped at 24 months (aligned with trial stopping rule)",
      "company_position": "2-year stopping rule aligned with EMPOWER-CSCC 1 protocol",
      "erg_position": null,
      "committee_preference": "24-month stopping rule appropriate",
      "impact_on_icer": "decreases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No trials directly comparing cemiplimab with BSC; STC and MAIC attempted but data highly uncertain"
    },
    {
      "gap_type": "no_comparator_data",
      "description": "Comparator data for BSC extremely limited; based on sub-set of 20 patients from non-UK retrospective chart review"
    }
  ],
  "icer_band": {
    "band": "30k_to_50k",
    "comparison_pair": "cemiplimab vs BSC",
    "is_committee_preferred": true,
    "uncertainty_level": "very_high"
  },
  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": true,
    "cancer_drugs_fund_considered": true,
    "cancer_drugs_fund_eligible": false,
    "innovation_acknowledged": true,
    "equality_issues_raised": false
  },
  "cross_references": [
    {"referenced_ta": "TA592", "relationship": "same_drug", "context": "Original CDF entry for cemiplimab; this TA is the CDF exit review with additional data"}
  ]
}
```

### Schema stress points
- **CDF exit review**: TA802 is a review of TA592 (CDF entry). This is best captured as a `PARTIALLY_UPDATES` relationship. The new relation type works well here.
- **SACT data as evidence source**: Real-world SACT data is increasingly important in CDF exits. The schema has no entity for real-world evidence sources (distinct from clinical trials). Consider adding `study_design: "registry"` or `"real_world_evidence"`.
- **Conditional marketing authorisation**: The marketing authorisation was conditional. No field captures this (which affects data maturity expectations).
- **therapeutic_area**: CSCC could be `dermatology` or `oncology`. The disease is a cancer but arises in a dermatological context. Same array-vs-single issue as TA538.

---

## 8. TA895 — Axicabtagene ciloleucel for relapsed/refractory DLBCL (2023, CAR-T)

### Abbreviated extraction

```json
{
  "ta_number": "TA895",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Axicabtagene ciloleucel for treating relapsed or refractory diffuse large B-cell lymphoma after first-line chemoimmunotherapy",
    "issue_date": "April 2023",
    "recommendation_type": "recommended_for_cdf",
    "restriction_details": "Only when autologous SCT is suitable; disease relapsed within 12 months or refractory to first-line chemoimmunotherapy; subject to managed access agreement",
    "appraisal_type": "STA",
    "committee_name": "committee C",
    "line_of_therapy": ["second_line"],
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "axicabtagene ciloleucel",
    "brand_name": "Yescarta",
    "manufacturer": "Kite (Gilead)",
    "drug_class": "CAR T-cell therapy",
    "mechanism_of_action": "chimeric antigen receptor T-cell therapy targeting CD19",
    "route_of_administration": "intravenous",
    "is_combination_regimen": false,
    "treatment_duration_type": "fixed_duration"
  }],
  "conditions": [{
    "condition_name": "relapsed or refractory diffuse large B-cell lymphoma after first-line chemoimmunotherapy",
    "therapeutic_area": "haematology",
    "disease_setting": "other",
    "biomarker_defined_population": false
  }],
  "comparators": [{
    "comparator_name": "salvage chemotherapy + high-dose chemotherapy + autologous SCT (standard care)",
    "comparator_type": "standard_of_care",
    "is_established_practice": true,
    "committee_preferred": true
  }],
  "clinical_trials": [{
    "trial_name": "ZUMA-7",
    "study_design": "RCT",
    "phase": "phase III",
    "blinding": "open_label",
    "is_pivotal": true,
    "primary_outcome": "event-free survival",
    "sample_size": 359,
    "crossover_occurred": false,
    "generalisability_concern": true
  }],
  "economic_model": {
    "model_type": "partitioned_survival",
    "model_source": "company",
    "health_states": ["event-free", "post-event", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "crossover_adjustment",
      "description": "56% of standard care arm had subsequent CAR T-cell therapy off-protocol; RPSFT model with full re-censoring used to adjust OS",
      "company_position": "RPSFT with full re-censoring preferred; gives HR 0.42",
      "erg_position": "Agreed RPSFT with full re-censoring most appropriate but remaining uncertainty",
      "committee_preference": "RPSFT with full re-censoring suitable but adds uncertainty",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "survival_extrapolation",
      "description": "Choice of mixture cure model for axi-cel OS — generalised gamma vs log-logistic",
      "company_position": "Generalised gamma preferred — good statistical fit, validated by clinical experts",
      "erg_position": "Log-logistic preferred — marginally better statistical fit, more conservative given immature data",
      "committee_preference": "Both plausible; log-logistic appropriate given uncertainty",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "other",
      "description": "Cure point assumption at 5 years — patients alive and event-free assumed cured with general population mortality",
      "company_position": "5-year cure threshold appropriate",
      "erg_position": null,
      "committee_preference": "Accepted 5-year cure threshold for both treatment arms",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "population_generalisability",
      "description": "Chemotherapy bridging not used in ZUMA-7 but used in 75% of NHS patients; generalisability uncertain",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "Generalisability to NHS practice very uncertain; CDF data collection could reduce this uncertainty",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "cost_assumption",
      "description": "CAR T-cell delivery costs — company bottom-up costing vs NHS England tariff",
      "company_position": "Bottom-up costing of £41,101 for first 100 days",
      "erg_position": "Company approach likely underestimates costs; NHS tariff higher but methods unclear",
      "committee_preference": "Company's £41,101 plus separate costs for conditioning chemo, SCT, IVIg accepted; NHS England agreed this was acceptable",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "immature_overall_survival",
      "description": "Only ~2 years of follow-up for axi-cel OS; long-term cure rate uncertain"
    },
    {
      "gap_type": "missing_real_world_evidence",
      "description": "Generalisability to NHS practice uncertain due to lack of chemotherapy bridging in trial; SACT data collection planned during CDF"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "managed_access_agreement",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "30k_to_50k",
    "comparison_pair": "axicabtagene ciloleucel vs standard care",
    "is_committee_preferred": true,
    "uncertainty_level": "very_high"
  },
  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": true,
    "cancer_drugs_fund_considered": true,
    "cancer_drugs_fund_eligible": true,
    "innovation_acknowledged": false,
    "equality_issues_raised": true
  }
}
```

### Schema stress points
- **CAR-T therapy modelling**: The single-infusion, potentially curative nature of CAR-T doesn't fit neatly into `treatment_duration_type`. `fixed_duration` is closest but doesn't capture "single administration".
- **Mixture cure models**: These are increasingly standard for haemato-oncology. `model_type` has no `mixture_cure` option. Currently forced into `partitioned_survival` but the cure component is fundamental.
- **NHS delivery infrastructure costs**: The debate about CAR-T tariff vs bottom-up costing is a novel cost assumption type that recurs across CAR-T TAs.
- **Event-free survival as primary endpoint**: Different from PFS — includes "best response of stable disease" as an event. The schema has no way to flag non-standard endpoint definitions.
- **Maximum acceptable ICER modulation**: Committee explicitly says it would normally accept up to £50k (end of life) but because of uncertainty, maximum acceptable ICER is "substantially less than £50k". This nuance is lost in the `icer_band` categorisation.

---

## 9. TA946 — Olaparib + bevacizumab for ovarian cancer maintenance (2024, CDF entry)

### Abbreviated extraction

Note: The FAD file for TA946 contains the MAA/Data Collection Arrangement document rather than the full committee discussion. Extraction based on available content.

```json
{
  "ta_number": "TA946",
  "doc_type": "FAD (MAA/Data Collection Arrangement)",
  "appraisal_metadata": {
    "title": "Olaparib with bevacizumab for maintenance treatment of advanced ovarian, fallopian tube or primary peritoneal cancer",
    "recommendation_type": "recommended_for_cdf",
    "restriction_details": "Only for HRD-positive advanced ovarian cancer; first-line maintenance after platinum-taxane chemotherapy with bevacizumab",
    "appraisal_type": "STA",
    "line_of_therapy": ["maintenance"],
    "methods_guide_era": "2022"
  },
  "interventions": [{
    "generic_name": "olaparib",
    "manufacturer": "AstraZeneca",
    "drug_class": "PARP inhibitor",
    "route_of_administration": "oral",
    "is_combination_regimen": true,
    "combination_components": ["olaparib", "bevacizumab"],
    "treatment_duration_type": "fixed_duration"
  }],
  "conditions": [{
    "condition_name": "HRD-positive advanced (FIGO Stage III-IV) ovarian, fallopian tube or primary peritoneal cancer",
    "therapeutic_area": "oncology",
    "disease_setting": "maintenance",
    "biomarker_defined_population": true,
    "biomarker_name": "homologous recombination deficiency (HRD) — BRCA1/2 mutation or genomic instability score ≥42 (Myriad HRD test)"
  }],
  "comparators": [{
    "comparator_name": "bevacizumab maintenance alone",
    "comparator_type": "active_drug",
    "is_established_practice": true,
    "committee_preferred": true
  }],
  "clinical_trials": [{
    "trial_name": "PAOLA-1",
    "study_design": "RCT",
    "phase": "phase III",
    "blinding": "double_blind",
    "is_pivotal": true,
    "primary_outcome": "progression-free survival",
    "sample_size": 806,
    "crossover_occurred": false,
    "generalisability_concern": true
  }],
  "evidence_gaps": [
    {
      "gap_type": "immature_overall_survival",
      "description": "PFS and OS data immature at time of appraisal; CDF data collection to await ~60% OS maturity"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "managed_access_agreement",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "special_considerations": {
    "cancer_drugs_fund_considered": true,
    "cancer_drugs_fund_eligible": true
  }
}
```

### Schema stress points
- **Biomarker complexity**: HRD-positive is defined by EITHER BRCA mutation OR a composite genomic instability score on a specific proprietary test (Myriad). The `biomarker_name` field is a simple string — this is a compound biomarker definition requiring either a structured sub-entity or at minimum an acknowledgment that biomarkers can be composite.
- **Subgroup of a subgroup**: The HRD+ population is a pre-specified subgroup (47-49% of trial arms). The schema captures `biomarker_defined_population` but doesn't distinguish "whole trial population" from "subgroup analysis".
- **Treatment duration with dual stopping rules**: Olaparib continues up to 2 years; bevacizumab up to 15 months. Different stopping times for combination components. `treatment_duration_type` cannot capture this.

---

## 10. TA1018 — Fedratinib for myelofibrosis (2024, CDF entry, rare haematology)

### Abbreviated extraction

Note: The FAD file contains the MAA/Data Collection Arrangement. Limited committee discussion text.

```json
{
  "ta_number": "TA1018",
  "doc_type": "FAD (MAA/Data Collection Arrangement)",
  "appraisal_metadata": {
    "title": "Fedratinib for treating disease-related splenomegaly or symptoms in myelofibrosis",
    "recommendation_type": "recommended_for_cdf",
    "restriction_details": "Intermediate-2 or high-risk myelofibrosis; previously treated with ruxolitinib; ECOG 0-2",
    "appraisal_type": "STA",
    "line_of_therapy": ["second_line"],
    "methods_guide_era": "2022"
  },
  "interventions": [{
    "generic_name": "fedratinib",
    "manufacturer": "Bristol Myers Squibb",
    "drug_class": "JAK2 inhibitor",
    "route_of_administration": "oral",
    "is_combination_regimen": false,
    "treatment_duration_type": "treat_to_progression"
  }],
  "conditions": [{
    "condition_name": "primary myelofibrosis, post-polycythaemia vera myelofibrosis, or post-essential thrombocythaemia myelofibrosis (intermediate-2 or high-risk)",
    "therapeutic_area": "haematology",
    "disease_setting": "chronic",
    "biomarker_defined_population": false
  }],
  "comparators": [{
    "comparator_name": "best available therapy (BAT)",
    "comparator_type": "standard_of_care",
    "is_established_practice": true,
    "committee_preferred": true
  }],
  "clinical_trials": [{
    "trial_name": "FREEDOM 2",
    "study_design": "RCT",
    "phase": null,
    "blinding": "open_label",
    "is_pivotal": true,
    "primary_outcome": "spleen volume response at end of cycle 6",
    "crossover_occurred": true,
    "generalisability_concern": false
  }],
  "evidence_gaps": [
    {
      "gap_type": "immature_overall_survival",
      "description": "Whether fedratinib extends overall survival compared to BAT is uncertain"
    },
    {
      "gap_type": "no_comparator_data",
      "description": "Overall survival for those on best available therapy is uncertain"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "managed_access_agreement",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "special_considerations": {
    "cancer_drugs_fund_considered": true,
    "cancer_drugs_fund_eligible": true
  }
}
```

### Schema stress points
- **Surrogate primary endpoint**: Spleen volume response (SVR) is a surrogate endpoint that is not OS or PFS. The schema has `surrogate_endpoint_validity` as a decision category but no way to flag the primary endpoint type as surrogate vs clinical.
- **CDF review of earlier TA**: This is a CDF review of TA756. The `PARTIALLY_UPDATES` relation fits well.
- **disease_setting**: Myelofibrosis is chronic but the patients are specifically post-ruxolitinib (second-line). The disease_setting doesn't capture "after failure of prior targeted therapy" which is the defining clinical context.
- **Safety monitoring requirement (thiamine)**: Fedratinib requires thiamine level testing. This is a unique safety/implementation requirement not captured in the schema (by design, in the `do_not_extract` list — but it's a decision-relevant fact, not a dosing detail).

---

## CRITIQUE: What Worked, What's Missing, What Needs Changing

### What worked well

1. **MethodologicalDecision entity is extremely valuable.** Every single FAD produced 2-6 high-quality methodological decisions. The company/ERG/committee three-way structure captures the essential dynamics.
2. **decision_categories cover the bulk of disputes.** `survival_extrapolation`, `crossover_adjustment`, `treatment_effect_waning`, `comparator_selection`, `cost_assumption`, and `model_structure` were all used frequently and correctly.
3. **icer_band categorisation works.** With confidential PAS, the band approach correctly abstracts away specific numbers. The `uncertainty_level` field is crucial.
4. **EvidenceGap entity captures CDF-relevant uncertainties.** `immature_overall_survival` and `no_direct_comparison` appear repeatedly and motivate CDF entries.
5. **cross_ta relations**: `SUPERSEDES` (TA284 superseding TA91 and TA222), `PARTIALLY_UPDATES` (TA802 reviewing TA592, TA1018 reviewing TA756), `utility_reuse` (TA741 referencing TA377/TA387) all mapped cleanly.
6. **CommercialArrangement types work well** across simple discount PAS, managed access agreements, and the TA171 dose-cap scheme.
7. **The "do_not_extract" list is well-calibrated.** None of the 10 TAs required extraction of dosing details or adverse event tables to capture the key decisions.

### What's missing — proposed changes for v0.3

#### HIGH PRIORITY (appeared in 3+ TAs, would cause Haiku systematic errors)

1. **Add `decision_category: "cure_assumption"`** — Appeared in TA538 (10-year cure point), TA642 (2-3 year cure), TA895 (5-year cure), and TA802 (duration of effectiveness). This is one of the most consequential and disputed assumptions in oncology/haematology modelling. Currently forced into `other`.

2. **Add `disease_setting: "relapsed_refractory"`** — Appeared in TA642 (relapsed/refractory AML), TA895 (relapsed/refractory DLBCL), TA538 (relapsed neuroblastoma mentioned). This is the single most common disease setting in oncology TAs and is missing from the enum.

3. **Add `disease_setting: "recurrent"`** — For ovarian cancer (TA284, TA946). Distinct from relapsed_refractory, which implies treatment failure rather than disease return.

4. **Make `therapeutic_area` an array** — TA538 (neuroblastoma = oncology + rare_disease), TA802 (CSCC = dermatology + oncology), TA1018 (myelofibrosis = haematology + rare_disease). Many diseases sit at the intersection. Current single-value forces lossy classification.

5. **Add `model_type: "mixture_cure"`** — Used in TA895 explicitly and conceptually in TA538, TA642. Standard partitioned survival does not adequately describe models with a cure fraction.

6. **Allow `icer_band` as an array of objects** — TA741 has fundamentally different ICERs for different comparators (above_50k vs docetaxel, acceptable vs ADT alone). TA587 has different bands depending on PAS scenario. Currently, the schema captures one band, losing critical information.

#### MEDIUM PRIORITY (appeared in 1-2 TAs but represent structural limitations)

7. **Add `decision_category: "discount_rate"`** — TA538 used a non-reference-case 1.5% discount rate. This is a framework-level methodological choice that has appeared in other paediatric/curative TAs. Currently forced into `other`.

8. **Add `recommendation_type` per intervention for MTAs** — TA284 is impossible to represent faithfully with a single recommendation_type. Consider making the recommendation a junction between TA and Intervention.

9. **Add `primary_outcome` as array on ClinicalTrial** — TITAN (TA741) had coprimary endpoints. Other trials may have co-primary or key secondary endpoints that drive the appraisal. A simple array would suffice.

10. **Add `study_design: "single_arm_phase_1_2"` or refine study_design** — TA802 relied on a phase 1 + phase 2 single-arm study. The current enum has `single_arm` which works, but phase is a separate field — ensure extractors know both are needed.

11. **Add `model_source` enum: `["company", "erg", "assessment_group", "dsu"]`** — TA284 used an assessment group model (MTA). TA538 involved DSU re-analysis. Currently no enum for model_source.

12. **Add a `biomarker_definition` structured sub-field or note** — TA946 (HRD = BRCA mutation OR genomic instability score on Myriad test) shows that biomarker definitions can be composite. A simple string is insufficient for precise querying.

13. **Add `is_paediatric` boolean on TechnologyAppraisal** — TA538 is a paediatric appraisal with different methods (discount rate, carer utilities, lifetime horizon interpretation). This is decision-relevant.

#### LOW PRIORITY (nice to have, edge cases)

14. **Add `conditional_marketing_authorisation` boolean on Intervention** — TA538 and TA802 both had conditional/exceptional-circumstances marketing authorisation. This correlates with data immaturity.

15. **Add `cdf_exit_review` boolean or `cdf_phase: "entry" | "exit" | "review"` on TA** — TA802 is explicitly a CDF exit review. Distinguishing CDF entry from exit would improve queries.

16. **Consider `treatment_duration_type: "single_administration"` for CAR-T** — TA895. The treatment is given once. `fixed_duration` implies a time period.

### What would Haiku struggle with?

1. **Mixed MTA recommendations**: TA284 is the hardest case. Haiku would need explicit instructions that MTAs can have different recommendation types per intervention, and how to encode this.

2. **Cure point as methodological decision**: Without `cure_assumption` in the decision categories, Haiku would likely classify cure points as `survival_extrapolation` (close but distinct) or `other` (loses queryability).

3. **Distinguishing disease settings**: `relapsed_refractory` vs `recurrent` vs `metastatic` — Haiku might conflate these without explicit definitions and examples.

4. **ICER band for confidential results**: When the FAD says "the ICER is confidential and cannot be reported" but also says "within the range normally considered acceptable for end-of-life treatments", Haiku needs to infer `30k_to_50k` from the contextual signal. This requires careful prompt engineering.

5. **Multiple PAS scenarios affecting ICER**: TA587 has two ICER estimates depending on which PAS applies. Haiku would need to decide which to extract as the "committee preferred" band.

6. **CDF entry documents as FADs**: TA946 and TA1018 have FADs that are primarily MAA/data collection arrangement documents with minimal committee discussion text. The extraction prompt assumes a committee discussion section. Haiku would extract minimal content and might hallucinate fields.

7. **Cross-TA references embedded in discussion**: References to other TAs are often made without explicit TA numbers (e.g., "NICE technology appraisal guidance on midostaurin"). Haiku would need to either extract the drug name and let post-processing resolve the TA number, or be given a lookup table.

### Summary of proposed decision_categories additions for v0.3

| New category | Definition | TAs where it appeared |
|---|---|---|
| `cure_assumption` | When/whether patients are assumed "cured" with general population mortality | TA538, TA642, TA895, TA802 |
| `discount_rate` | Choice of discount rate when non-reference-case rate is applied | TA538 |
| `real_world_generalisability` | Whether real-world data (SACT, registries) confirms or contradicts trial results | TA802, TA895 |

### Summary statistics

| Metric | Value |
|---|---|
| TAs tested | 10 |
| Methodological decisions extracted | 34 |
| Evidence gaps extracted | 14 |
| Cross-TA references extracted | 11 |
| Schema-breaking issues found | 6 (high priority) |
| New enum values needed | 4 (relapsed_refractory, recurrent, mixture_cure, cure_assumption) |
| Structural changes needed | 3 (therapeutic_area -> array, icer_band -> array, recommendation per intervention for MTA) |
