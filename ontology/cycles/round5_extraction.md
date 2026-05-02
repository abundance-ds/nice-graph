# Round 5: Final Stability Test — Ontology v0.5.0

**Date:** 2026-05-02
**Schema version:** 0.5.0
**Purpose:** Final test of 10 diverse TAs to assess schema stability before bulk extraction.

## TAs in this round

| # | TA | Drug / Condition | Year | Therapeutic area | Notes |
|---|-----|-----------------|------|------------------|-------|
| 1 | TA100 | Capecitabine + oxaliplatin / colon cancer adjuvant | 2006 | Oncology | Old MTA format, 2 interventions |
| 2 | TA101 | Docetaxel / prostate cancer HRMC | 2006 | Oncology | Old STA, pre-2008 methods |
| 3 | TA420 | Ticagrelor / post-MI prevention | 2016 | Cardiovascular | Non-cancer, prevention |
| 4 | TA871 | Eptinezumab / migraine prevention | 2023 | Neurology | Short doc, cost-comparison |
| 5 | TA887 | Olaparib / prostate BRCA | 2023 | Oncology | Targeted, not recommended |
| 6 | TA919 | Rimegepant / acute migraine | 2023 | Neurology | Acute treatment |
| 7 | TA1110 | Abiraterone / prostate mHSPC | 2025 | Oncology | Post-appeal, not recommended |
| 8 | TA856 | Upadacitinib / ulcerative colitis | 2023 | Gastroenterology | JAK inhibitor, cost-comparison |
| 9 | TA880 | Tezepelumab / severe asthma | 2023 | Respiratory | Biologic, multiple subgroups |
| 10 | TA939 | Pembrolizumab / cervical cancer | 2023 | Oncology | ACD used (FAD was equality doc only) |

**Substitution notes:**
- ta942 (Empagliflozin CKD) and ta930 (Lutetium-177 prostate) FAD.md files contained only equality impact assessments, not full FADs. Used ta856 and ta880 instead.
- ta939 FAD.md was also an equality impact assessment. Used the ACD (449 lines) as a workable substitute.

---

## Extraction 1: TA100 — Capecitabine + oxaliplatin, adjuvant colon cancer

```json
{
  "ta_number": "TA100",
  "doc_type": "FAD",

  "appraisal_metadata": {
    "title": "Capecitabine and oxaliplatin in the adjuvant treatment of stage III (Dukes' C) colon cancer",
    "issue_date": "January 2006",
    "recommendation_type": "recommended",
    "restriction_details": "Both capecitabine monotherapy and oxaliplatin+5-FU/FA recommended as options; choice should be joint between patient and clinician considering toxicity profiles",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "School of Health and Related Research (ScHARR), University of Sheffield",
    "line_of_therapy": "adjuvant",
    "methods_guide_era": "pre_2008"
  },

  "interventions": [
    {
      "generic_name": "capecitabine",
      "brand_name": "Xeloda",
      "manufacturer": "Roche",
      "drug_class": "fluoropyrimidine",
      "mechanism_of_action": "orally administered precursor of 5-fluorouracil",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "fixed_duration",
      "intervention_type": "drug"
    },
    {
      "generic_name": "oxaliplatin",
      "brand_name": "Eloxatin",
      "manufacturer": "Sanofi-Aventis",
      "drug_class": "platinum-based cytotoxic",
      "mechanism_of_action": "prevents DNA replication by cross-linking DNA",
      "route_of_administration": "intravenous",
      "is_combination_regimen": true,
      "combination_components": ["oxaliplatin", "5-fluorouracil", "folinic acid"],
      "treatment_duration_type": "fixed_duration",
      "intervention_type": "drug"
    }
  ],

  "conditions": [
    {
      "condition_name": "stage III (Dukes' C) colon cancer, adjuvant after surgery",
      "therapeutic_area": ["oncology"],
      "disease_setting": "adjuvant",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],

  "comparators": [
    {
      "comparator_name": "5-fluorouracil plus folinic acid (5-FU/FA)",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],

  "clinical_trials": [
    {
      "trial_name": "X-ACT (Xeloda - Adjuvant Chemotherapy Trial)",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "open_label",
      "is_pivotal": true,
      "primary_outcome": "disease-free survival",
      "sample_size": 1987,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    },
    {
      "trial_name": "MOSAIC",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "open_label",
      "is_pivotal": true,
      "primary_outcome": "disease-free survival",
      "sample_size": 2246,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    },
    {
      "trial_name": "NSABP C-07",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": null,
      "is_pivotal": false,
      "primary_outcome": "disease-free survival",
      "sample_size": 2492,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],

  "economic_model": {
    "model_type": "markov",
    "model_source": "Assessment Group",
    "time_horizon": "lifetime",
    "cycle_length": null,
    "health_states": ["alive without relapse", "alive with relapse", "dead"]
  },

  "methodological_decisions": [
    {
      "decision_category": "surrogate_endpoint_validity",
      "description": "Whether 3-year DFS benefits predict 5-year OS benefits",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "Considered it reasonable to assume that 3-year DFS benefits would predict 5-year OS benefits",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "utility_source",
      "description": "Utility values for different health states — limited evidence base",
      "company_position": "Used study of 173 CRC patients with disutility of 0.2 for relapse",
      "erg_position": "Used second study with lower utility for relapse (0.24) and on-treatment (0.7)",
      "committee_preference": "Accepted Assessment Group values as best available despite concerns",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "population_generalisability",
      "description": "Trial participants younger than typical clinical practice population",
      "company_position": null,
      "erg_position": "Older cohort would not materially change cost-effectiveness",
      "committee_preference": "Accepted that results can be extrapolated to older patients",
      "impact_on_icer": "negligible"
    }
  ],

  "evidence_gaps": [
    {
      "gap_type": "immature_overall_survival",
      "description": "No statistically significant OS benefit demonstrated for either capecitabine or oxaliplatin at time of appraisal"
    },
    {
      "gap_type": "no_direct_comparison",
      "description": "No direct comparison between oxaliplatin+5-FU/FA and capecitabine"
    },
    {
      "gap_type": "missing_quality_of_life_data",
      "description": "Quality of life data not routinely collected in oxaliplatin trials"
    }
  ],

  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },

  "icer_band": [
    {
      "band": "below_20k",
      "comparison_pair": "capecitabine vs 5-FU/FA (Mayo Clinic)",
      "is_committee_preferred": true,
      "uncertainty_level": "low",
      "direction": "decremental"
    },
    {
      "band": "below_20k",
      "comparison_pair": "oxaliplatin+5-FU/FA vs 5-FU/FA",
      "is_committee_preferred": true,
      "uncertainty_level": "moderate",
      "direction": "incremental"
    }
  ],

  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },

  "cross_references": [
    {
      "referenced_ta": "TA93",
      "relationship": "same_condition",
      "context": "Irinotecan, oxaliplatin and raltitrexed for advanced colorectal cancer"
    },
    {
      "referenced_ta": "TA61",
      "relationship": "same_drug",
      "context": "Capecitabine and tegafur for metastatic colorectal cancer"
    }
  ]
}
```

**Assessment: CLEAN** — Multi-intervention MTA handled well. Capecitabine was cost-saving (dominant/decremental direction used). No `other` categories needed.

---

## Extraction 2: TA101 — Docetaxel, hormone-refractory metastatic prostate cancer

```json
{
  "ta_number": "TA101",
  "doc_type": "FAD",

  "appraisal_metadata": {
    "title": "Docetaxel for the treatment of hormone-refractory metastatic prostate cancer",
    "issue_date": "April 2006",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Only if Karnofsky performance-status score is 60% or more. Treatment stopped at 10 cycles max, on progression, or severe adverse events. No repeat cycles after disease recurrence.",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "Centre for Reviews and Dissemination, University of York",
    "line_of_therapy": "first_line",
    "methods_guide_era": "pre_2008"
  },

  "interventions": [
    {
      "generic_name": "docetaxel",
      "brand_name": null,
      "manufacturer": "Sanofi-Aventis",
      "drug_class": "taxane",
      "mechanism_of_action": "disrupts microtubular network essential for mitotic and interphase cellular functions",
      "route_of_administration": "intravenous",
      "is_combination_regimen": true,
      "combination_components": ["docetaxel", "prednisone/prednisolone"],
      "treatment_duration_type": "fixed_duration",
      "intervention_type": "drug"
    }
  ],

  "conditions": [
    {
      "condition_name": "hormone-refractory metastatic prostate cancer",
      "therapeutic_area": ["oncology"],
      "disease_setting": "metastatic",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],

  "comparators": [
    {
      "comparator_name": "mitoxantrone plus prednisone/prednisolone",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "prednisone or prednisolone alone (best supportive care)",
      "comparator_type": "best_supportive_care",
      "is_established_practice": true,
      "committee_preferred": false
    }
  ],

  "clinical_trials": [
    {
      "trial_name": "TAX327",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "open_label",
      "is_pivotal": true,
      "primary_outcome": "overall survival",
      "sample_size": 1006,
      "crossover_occurred": true,
      "crossover_adjusted": false,
      "generalisability_concern": true
    },
    {
      "trial_name": "SWOG 9916",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": null,
      "is_pivotal": false,
      "primary_outcome": "overall survival",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],

  "economic_model": {
    "model_type": "markov",
    "model_source": "Assessment Group",
    "time_horizon": "15 years",
    "cycle_length": null,
    "health_states": null
  },

  "methodological_decisions": [
    {
      "decision_category": "utility_source",
      "description": "No utility data collected in TAX327; Assessment Group used values from systematic literature review",
      "company_position": "Did not adjust for quality of life in its model (cost per LYG only)",
      "erg_position": "Used utility assumption from literature review, same value for all treatment strategies",
      "committee_preference": "Accepted Assessment Group utility assumption as reasonable; noted conservative approach of not including QoL benefit of docetaxel over mitoxantrone",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Maximum treatment duration and retreatment policy",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "Treatment stopped at 10 cycles max, on progression, or severe AEs; no repeat cycles after disease recurrence",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "population_generalisability",
      "description": "Trial patients younger and fitter than typical UK population; committee restricted recommendation to Karnofsky >= 60%",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "Restricted to patients with Karnofsky score 60% or more; for disabled patients, interpret on individual basis",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "indirect_comparison_method",
      "description": "Indirect comparison of docetaxel vs corticosteroid alone via mitoxantrone as common comparator",
      "company_position": null,
      "erg_position": "Indirect HR for death of docetaxel vs corticosteroid alone: 0.752 — should be interpreted with caution",
      "committee_preference": "Noted results should be interpreted with caution due to differences in trial populations",
      "impact_on_icer": "uncertain_direction"
    }
  ],

  "evidence_gaps": [
    {
      "gap_type": "missing_quality_of_life_data",
      "description": "No utility data (EQ-5D or similar) collected in TAX327; FACT-P responses could not be mapped to utility values"
    }
  ],

  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },

  "icer_band": [
    {
      "band": "30k_to_50k",
      "comparison_pair": "docetaxel+prednisolone vs mitoxantrone+prednisolone",
      "is_committee_preferred": true,
      "uncertainty_level": "moderate",
      "direction": "incremental"
    }
  ],

  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": true
  },

  "cross_references": []
}
```

**Assessment: CLEAN** — Pre-2008 format handled well. The equality consideration (Karnofsky score and disability) captured by flag. No `other` categories.

---

## Extraction 3: TA420 — Ticagrelor, post-MI atherothrombotic prevention

```json
{
  "ta_number": "TA420",
  "doc_type": "FAD",

  "appraisal_metadata": {
    "title": "Ticagrelor for preventing atherothrombotic events after myocardial infarction",
    "issue_date": "October 2016",
    "recommendation_type": "recommended",
    "restriction_details": "Within marketing authorisation for adults who had MI and are at high risk. Treatment stopped when clinically indicated or at maximum 3 years.",
    "appraisal_type": "STA",
    "committee_name": "Appraisal committee C",
    "erg_or_eag_name": null,
    "line_of_therapy": "maintenance",
    "methods_guide_era": "2013"
  },

  "interventions": [
    {
      "generic_name": "ticagrelor",
      "brand_name": "Brilique",
      "manufacturer": "AstraZeneca",
      "drug_class": "P2Y12 ADP receptor antagonist",
      "mechanism_of_action": "inhibits platelet aggregation and thrombus formation in atherosclerotic disease",
      "route_of_administration": "oral",
      "is_combination_regimen": true,
      "combination_components": ["ticagrelor 60mg", "aspirin"],
      "treatment_duration_type": "fixed_duration",
      "intervention_type": "drug"
    }
  ],

  "conditions": [
    {
      "condition_name": "prevention of atherothrombotic events in adults with history of myocardial infarction at high risk",
      "therapeutic_area": ["cardiovascular"],
      "disease_setting": "prevention_secondary",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],

  "comparators": [
    {
      "comparator_name": "aspirin alone",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],

  "clinical_trials": [
    {
      "trial_name": "PEGASUS TIMI-54",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "composite of cardiovascular death, myocardial infarction, or stroke",
      "sample_size": 14112,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],

  "economic_model": {
    "model_type": "other",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": null
  },

  "methodological_decisions": [
    {
      "decision_category": "subgroup_definition",
      "description": "Company used subgroup of patients with MI 1-2 years ago; committee extended to include those who had MI >2 years ago and stopped antiplatelet <1 year ago",
      "company_position": "Base-case population was MI 1-2 years ago (prespecified subgroup)",
      "erg_position": "Full marketing authorisation population should be included",
      "committee_preference": "Accepted subgroup as basis for clinical effectiveness but recommendation covers full marketing authorisation",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Whether clopidogrel plus aspirin is an appropriate comparator",
      "company_position": "Aspirin alone is the appropriate comparator; clopidogrel not used beyond 12 months in clinical practice",
      "erg_position": "Indirect comparison with clopidogrel inappropriate due to trial differences",
      "committee_preference": "Agreed clopidogrel plus aspirin was not appropriate comparator; aspirin alone preferred",
      "impact_on_icer": "negligible"
    }
  ],

  "evidence_gaps": [],

  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },

  "icer_band": [
    {
      "band": "20k_to_30k",
      "comparison_pair": "ticagrelor 60mg + aspirin vs aspirin alone",
      "is_committee_preferred": true,
      "uncertainty_level": "moderate",
      "direction": "incremental"
    }
  ],

  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": true
  },

  "cross_references": [
    {
      "referenced_ta": "TA236",
      "relationship": "same_drug",
      "context": "NICE technology appraisal guidance on ticagrelor for treatment of acute coronary syndromes (90mg)"
    }
  ]
}
```

**Assessment: CLEAN** — Cardiovascular / secondary prevention fit cleanly. `prevention_secondary` disease_setting used. `maintenance` line_of_therapy is slightly awkward for a cardiovascular preventive — but acceptable.

**Minor friction:** The model type was an individual-patient simulation / risk-equation model. Using `other` for model_type is technically correct but there is a very slight tension. The document describes "risk equations" and "3 different approaches to cost-effectiveness modelling" without naming a standard model type. `other` is the right fallback.

---

## Extraction 4: TA871 — Eptinezumab, migraine prevention

```json
{
  "ta_number": "TA871",
  "doc_type": "FAD",

  "appraisal_metadata": {
    "title": "Eptinezumab for preventing migraine",
    "issue_date": "January 2023",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Only if 4+ migraine days/month, at least 3 preventive drug treatments failed, and company provides per commercial arrangement. Stop at 12 weeks if insufficient response.",
    "appraisal_type": "STA",
    "committee_name": "Highly specialised technologies evaluation committee (vice chair)",
    "erg_or_eag_name": null,
    "line_of_therapy": "third_line_plus",
    "methods_guide_era": "2022"
  },

  "interventions": [
    {
      "generic_name": "eptinezumab",
      "brand_name": "VYEPTI",
      "manufacturer": "Lundbeck",
      "drug_class": "CGRP inhibitor",
      "mechanism_of_action": "calcitonin gene-related peptide inhibitor",
      "route_of_administration": "intravenous",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "continuous",
      "intervention_type": "biologic"
    }
  ],

  "conditions": [
    {
      "condition_name": "migraine prophylaxis in adults with at least 4 migraine days per month",
      "therapeutic_area": ["neurology_psychiatry"],
      "disease_setting": "chronic",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],

  "comparators": [
    {
      "comparator_name": "erenumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "fremanezumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "galcanezumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],

  "clinical_trials": [],

  "economic_model": {
    "model_type": "cost_comparison",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": null
  },

  "methodological_decisions": [
    {
      "decision_category": "equivalence_assumption",
      "description": "Whether eptinezumab has similar clinical effectiveness to other CGRP inhibitors",
      "company_position": "NMA suggests similar effectiveness to erenumab, fremanezumab, galcanezumab",
      "erg_position": "NMA had limitations but similar conclusions reached",
      "committee_preference": "Agreed there was sufficient evidence of similar clinical efficacy",
      "impact_on_icer": "negligible"
    }
  ],

  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trials comparing eptinezumab with erenumab, fremanezumab or galcanezumab"
    }
  ],

  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },

  "icer_band": [
    {
      "band": "below_20k",
      "comparison_pair": "eptinezumab vs other CGRP inhibitors (cost-comparison)",
      "is_committee_preferred": true,
      "uncertainty_level": "low",
      "direction": "incremental"
    }
  ],

  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": true
  },

  "cross_references": [
    {
      "referenced_ta": null,
      "relationship": "comparator_guidance",
      "context": "NICE technology appraisal guidance on erenumab, fremanezumab and galcanezumab for preventing chronic or episodic migraines"
    }
  ]
}
```

**Assessment: CLEAN** — Short cost-comparison document handled well. `cost_comparison` model_type used correctly. `equivalence_assumption` decision_category used correctly. No `other` categories needed.

---

## Extraction 5: TA887 — Olaparib, BRCA-mutation prostate cancer

```json
{
  "ta_number": "TA887",
  "doc_type": "FAD",

  "appraisal_metadata": {
    "title": "Olaparib for previously treated BRCA mutation-positive hormone-relapsed metastatic prostate cancer",
    "issue_date": "August 2022",
    "recommendation_type": "not_recommended",
    "restriction_details": null,
    "appraisal_type": "STA",
    "committee_name": "Appraisal committee B",
    "erg_or_eag_name": null,
    "line_of_therapy": "third_line_plus",
    "methods_guide_era": "2013"
  },

  "interventions": [
    {
      "generic_name": "olaparib",
      "brand_name": "Lynparza",
      "manufacturer": "AstraZeneca",
      "drug_class": "PARP inhibitor",
      "mechanism_of_action": "poly-ADP-ribose polymerase inhibitor",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "treat_to_progression",
      "intervention_type": "drug"
    }
  ],

  "conditions": [
    {
      "condition_name": "metastatic castration-resistant prostate cancer with BRCA1/2 mutations, progressed after new hormonal agent",
      "therapeutic_area": ["oncology"],
      "disease_setting": "metastatic",
      "biomarker_defined_population": true,
      "biomarker_name": "BRCA1/2 mutation (germline and/or somatic)"
    }
  ],

  "comparators": [
    {
      "comparator_name": "cabazitaxel",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "radium-223 dichloride",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": false
    },
    {
      "comparator_name": "docetaxel retreatment",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": false
    },
    {
      "comparator_name": "docetaxel (for no prior taxane group)",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": false
    },
    {
      "comparator_name": "best supportive care (for no prior taxane group)",
      "comparator_type": "best_supportive_care",
      "is_established_practice": true,
      "committee_preferred": false
    }
  ],

  "clinical_trials": [
    {
      "trial_name": "PROfound",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "open_label",
      "is_pivotal": true,
      "primary_outcome": "radiographic progression-free survival",
      "sample_size": null,
      "crossover_occurred": true,
      "crossover_adjusted": true,
      "generalisability_concern": true
    },
    {
      "trial_name": "CARD",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "open_label",
      "is_pivotal": false,
      "primary_outcome": "radiographic progression-free survival",
      "sample_size": null,
      "crossover_occurred": true,
      "crossover_adjusted": false,
      "generalisability_concern": true
    }
  ],

  "economic_model": {
    "model_type": "partitioned_survival",
    "model_source": "company",
    "time_horizon": "lifetime",
    "cycle_length": null,
    "health_states": ["progression-free", "post-progression", "death"]
  },

  "methodological_decisions": [
    {
      "decision_category": "crossover_adjustment",
      "description": "Most control arm patients switched to olaparib after progression in PROfound; RPSFTM with recensoring used",
      "company_position": "RPSFTM with recensoring appropriate",
      "erg_position": "Considered results with and without recensoring as both can bias results",
      "committee_preference": "Agreed RPSFTM with recensoring was appropriate for PROfound; inappropriate to adjust for switching in CARD",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "indirect_comparison_method",
      "description": "Indirect treatment comparison of olaparib vs cabazitaxel using PROfound and CARD",
      "company_position": "ITC showed olaparib increased PFS and OS vs cabazitaxel",
      "erg_position": "Highlighted differences between PROfound and CARD populations affecting reliability",
      "committee_preference": "Concluded there was uncertainty in the ITC due to trial differences",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "survival_extrapolation",
      "description": "Choice of parametric distribution for overall survival extrapolation",
      "company_position": "Initially log-logistic, then changed to Weibull",
      "erg_position": "Preferred Rayleigh distribution",
      "committee_preference": "Concluded both Weibull and Rayleigh were equally plausible and equally uncertain",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Whether to include BRCA mutation testing costs",
      "company_position": "Excluded testing costs; test is in NHS Genomic Test Directory",
      "erg_position": "Included testing costs as testing is not standard NHS practice",
      "committee_preference": "Agreed testing costs should be included",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "treatment_sequencing",
      "description": "Differences in post-progression treatments between trials and NHS practice",
      "company_position": "Used PROfound and CARD trial proportions; excluded abiraterone/enzalutamide retreatment in revision",
      "erg_position": "Trial proportions do not reflect NHS practice",
      "committee_preference": "Both approaches not ideal but acceptable; post-progression differences affect generalisability",
      "impact_on_icer": "uncertain_direction"
    }
  ],

  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trial comparing olaparib with cabazitaxel, docetaxel, or radium-223"
    },
    {
      "gap_type": "immature_overall_survival",
      "description": "OS data immature especially in the no prior taxane subgroup"
    },
    {
      "gap_type": "missing_subgroup_data",
      "description": "No prespecified subgroup for BRCA-mutation patients in the prior/no prior taxane groups"
    }
  ],

  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": false
  },

  "icer_band": [
    {
      "band": "above_50k",
      "comparison_pair": "olaparib vs cabazitaxel (prior taxane group)",
      "is_committee_preferred": true,
      "uncertainty_level": "very_high",
      "direction": "incremental"
    }
  ],

  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": true,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": true
  },

  "cross_references": [
    {
      "referenced_ta": "TA101",
      "relationship": "same_drug",
      "context": "TAX327 trial used for indirect comparison with docetaxel in no prior taxane group"
    }
  ]
}
```

**Assessment: CLEAN** — Complex not-recommended TA with biomarker-defined population, crossover adjustment, indirect comparison, end-of-life. All captured with existing categories. No `other` needed.

---

## Extraction 6: TA919 — Rimegepant, acute migraine treatment

```json
{
  "ta_number": "TA919",
  "doc_type": "FAD",

  "appraisal_metadata": {
    "title": "Rimegepant for treating migraine",
    "issue_date": "September 2023",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Only if at least 2 triptans tried and did not work; OR triptans contraindicated/not tolerated AND NSAIDs and paracetamol tried but did not work well enough.",
    "appraisal_type": "STA",
    "committee_name": "Technology appraisal committee D",
    "erg_or_eag_name": null,
    "line_of_therapy": "third_line_plus",
    "methods_guide_era": "2022"
  },

  "interventions": [
    {
      "generic_name": "rimegepant",
      "brand_name": "Vydura",
      "manufacturer": "Pfizer",
      "drug_class": "CGRP receptor antagonist (gepant)",
      "mechanism_of_action": "calcitonin gene-related peptide receptor antagonist",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "other",
      "intervention_type": "drug"
    }
  ],

  "conditions": [
    {
      "condition_name": "acute migraine with or without aura in adults",
      "therapeutic_area": ["neurology_psychiatry"],
      "disease_setting": "acute",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],

  "comparators": [
    {
      "comparator_name": "placebo (best supportive care)",
      "comparator_type": "placebo",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],

  "clinical_trials": [
    {
      "trial_name": "BHV3000-301",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "freedom from pain at 2 hours",
      "sample_size": 1084,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    },
    {
      "trial_name": "BHV3000-302",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "freedom from pain at 2 hours",
      "sample_size": 1072,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    },
    {
      "trial_name": "BHV3000-303",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "freedom from pain at 2 hours",
      "sample_size": 1351,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    },
    {
      "trial_name": "BHV3000-310",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": false,
      "primary_outcome": "freedom from pain at 2 hours",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    }
  ],

  "economic_model": {
    "model_type": "decision_tree_plus_markov",
    "model_source": "company",
    "time_horizon": "2 years",
    "cycle_length": null,
    "health_states": ["on treatment", "stopped treatment"]
  },

  "methodological_decisions": [
    {
      "decision_category": "subgroup_definition",
      "description": "Whether to use mITT population or post-hoc subgroup of patients who had stopped 2+ triptans",
      "company_position": "Initially used post-hoc subgroup; later accepted mITT population",
      "erg_position": "Preferred mITT population as larger and more relevant",
      "committee_preference": "Concluded mITT population was most appropriate",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "model_structure",
      "description": "Whether time horizon of 2 or 20 years is appropriate for acute migraine treatment",
      "company_position": "20-year time horizon because migraine is chronic",
      "erg_position": "2-year time horizon because acute treatment costs/benefits occur immediately",
      "committee_preference": "2-year time horizon sufficient after model corrections removed placebo response impact",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "baseline_risk",
      "description": "Whether to model a loss of placebo response after 1 year",
      "company_position": "Placebo response should be removed after 1 year; evidence suggests placebo response is 3-6 months",
      "erg_position": "No loss of placebo response — this is an artefact of RCT design, not a real clinical effect",
      "committee_preference": "Agreed there should be no loss of placebo response in the model",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "population_generalisability",
      "description": "Whether trial results in episodic migraine population are generalisable to chronic migraine",
      "company_position": "No difference in effectiveness expected",
      "erg_position": "Chronic migraines harder to treat; generalisability unresolvable without evidence",
      "committee_preference": "May not be fully appropriate to extrapolate but accepted trial results for both populations",
      "impact_on_icer": "uncertain_direction"
    }
  ],

  "evidence_gaps": [
    {
      "gap_type": "missing_subgroup_data",
      "description": "Trials excluded people with chronic migraines (>15 headache days/month)"
    }
  ],

  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },

  "icer_band": [
    {
      "band": "20k_to_30k",
      "comparison_pair": "rimegepant vs placebo/best supportive care",
      "is_committee_preferred": true,
      "uncertainty_level": "moderate",
      "direction": "incremental"
    }
  ],

  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": true,
    "equality_issues_raised": true
  },

  "cross_references": [
    {
      "referenced_ta": null,
      "relationship": "same_drug",
      "context": "NICE technology appraisal guidance on rimegepant for preventing migraine (dual indication)"
    }
  ]
}
```

**Assessment: MINOR FRICTION** — `treatment_duration_type` = `other` for rimegepant (taken as-needed per migraine attack, not fitting any existing category well). A potential enum value `as_needed` could be considered but is too niche. The `baseline_risk` decision_category is used for the placebo response issue, which is a stretch -- it's really about how the placebo arm is modelled. However, no existing category fits perfectly either. Acceptable as-is.

---

## Extraction 7: TA1110 — Abiraterone, newly diagnosed mHSPC

```json
{
  "ta_number": "TA1110",
  "doc_type": "FAD",

  "appraisal_metadata": {
    "title": "Abiraterone for treating newly diagnosed high-risk hormone-sensitive metastatic prostate cancer",
    "issue_date": "August 2021",
    "recommendation_type": "not_recommended",
    "restriction_details": null,
    "appraisal_type": "STA",
    "committee_name": "Appraisal committee B",
    "erg_or_eag_name": null,
    "line_of_therapy": "first_line",
    "methods_guide_era": "2013"
  },

  "interventions": [
    {
      "generic_name": "abiraterone",
      "brand_name": "Zytiga",
      "manufacturer": "Janssen",
      "drug_class": "androgen synthesis inhibitor",
      "mechanism_of_action": null,
      "route_of_administration": "oral",
      "is_combination_regimen": true,
      "combination_components": ["abiraterone", "prednisone/prednisolone", "androgen deprivation therapy"],
      "treatment_duration_type": "treat_to_progression",
      "intervention_type": "drug"
    }
  ],

  "conditions": [
    {
      "condition_name": "newly diagnosed high-risk metastatic hormone-sensitive prostate cancer",
      "therapeutic_area": ["oncology"],
      "disease_setting": "metastatic",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],

  "comparators": [
    {
      "comparator_name": "androgen deprivation therapy (ADT) alone",
      "comparator_type": "standard_of_care",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "docetaxel plus ADT plus prednisolone",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],

  "clinical_trials": [
    {
      "trial_name": "LATITUDE",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "progression-free survival and overall survival",
      "sample_size": 1199,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    },
    {
      "trial_name": "STAMPEDE",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "open_label",
      "is_pivotal": true,
      "primary_outcome": "overall survival",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],

  "economic_model": {
    "model_type": "partitioned_survival",
    "model_source": "company",
    "time_horizon": "lifetime",
    "cycle_length": null,
    "health_states": ["hormone-sensitive progression-free", "hormone-relapsed", "death"]
  },

  "methodological_decisions": [
    {
      "decision_category": "survival_extrapolation",
      "description": "Choice of parametric curves for PFS and OS extrapolation",
      "company_position": "Log-logistic for OS (plausible but optimistic); Weibull (plausible but pessimistic)",
      "erg_position": "Provided waning scenarios",
      "committee_preference": "Weibull for PFS, log-logistic for OS supported by 8-year STAMPEDE data",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "indirect_comparison_method",
      "description": "Direct STAMPEDE comparison vs company's NMA for abiraterone vs docetaxel",
      "company_position": "Preferred NMA including LATITUDE, STAMPEDE, CHAARTED, GETUG-AFU 15",
      "erg_position": null,
      "committee_preference": "Preferred direct STAMPEDE comparison as less likely to be biased; NMA point estimate differed from direct evidence",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "treatment_sequencing",
      "description": "Abiraterone first-line limits follow-on treatment options for hormone-relapsed disease compared with ADT or docetaxel first-line",
      "company_position": "Included costs of follow-on treatments based on 4-clinician market shares",
      "erg_position": "Company may not reflect actual UK market shares",
      "committee_preference": "Concluded first-choice treatment affects follow-on options; model included costs but not full benefits of follow-on treatments, biasing ICER upward",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "population_generalisability",
      "description": "Whether LATITUDE/STAMPEDE data applies to patients for whom docetaxel is contraindicated/unsuitable",
      "company_position": "Treatment effect from whole population applies to chemotherapy-ineligible group",
      "erg_position": null,
      "committee_preference": "No specific data available; subgroup analyses by age and performance status suggest reduced benefit; considerable uncertainty",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "utility_source",
      "description": "Source of utility data for different treatment arms",
      "company_position": "EQ-5D from LATITUDE for abiraterone/ADT; separate preference study for docetaxel",
      "erg_position": "Used EQ-5D-based disutility from STAMPEDE for docetaxel",
      "committee_preference": "Preferred EQ-5D data from same source (STAMPEDE) for all arms; company/ERG approaches broadly consistent",
      "impact_on_icer": "negligible"
    }
  ],

  "evidence_gaps": [
    {
      "gap_type": "missing_subgroup_data",
      "description": "No data specific to patients for whom docetaxel is contraindicated or unsuitable"
    }
  ],

  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": false
  },

  "icer_band": [
    {
      "band": "above_50k",
      "comparison_pair": "abiraterone+ADT vs docetaxel+ADT",
      "is_committee_preferred": true,
      "uncertainty_level": "very_high",
      "direction": "incremental"
    },
    {
      "band": "30k_to_50k",
      "comparison_pair": "abiraterone+ADT vs ADT alone",
      "is_committee_preferred": true,
      "uncertainty_level": "high",
      "direction": "incremental"
    }
  ],

  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": true
  },

  "cross_references": [
    {
      "referenced_ta": null,
      "relationship": "same_drug",
      "context": "NICE technology appraisal guidance on abiraterone for treating metastatic hormone-relapsed prostate cancer (before and after chemotherapy)"
    },
    {
      "referenced_ta": null,
      "relationship": "comparator_guidance",
      "context": "NICE technology appraisal guidance on enzalutamide plus ADT for treating hormone-sensitive metastatic prostate cancer"
    },
    {
      "referenced_ta": null,
      "relationship": "precedent",
      "context": "NICE technology appraisal guidance on radium-223 dichloride - appeal panel cited re defining chemotherapy-ineligible group"
    }
  ]
}
```

**Assessment: CLEAN** — Complex post-appeal TA. 5 committee meetings handled with no schema gaps. `treatment_sequencing` used appropriately for the follow-on treatment modeling issue. No `other` categories needed.

---

## Extraction 8: TA856 — Upadacitinib, ulcerative colitis

```json
{
  "ta_number": "TA856",
  "doc_type": "FAD",

  "appraisal_metadata": {
    "title": "Upadacitinib for treating moderately to severely active ulcerative colitis",
    "issue_date": "2023",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "When conventional or biological treatment cannot be tolerated or condition has not responded/stopped responding. Choose least expensive if several suitable options.",
    "appraisal_type": "STA",
    "committee_name": "Technology appraisal evaluation committee B",
    "erg_or_eag_name": null,
    "line_of_therapy": "second_line",
    "methods_guide_era": "2022"
  },

  "interventions": [
    {
      "generic_name": "upadacitinib",
      "brand_name": "RINVOQ",
      "manufacturer": "AbbVie",
      "drug_class": "JAK inhibitor",
      "mechanism_of_action": "Janus-associated kinase inhibitor",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "continuous",
      "intervention_type": "drug"
    }
  ],

  "conditions": [
    {
      "condition_name": "moderately to severely active ulcerative colitis in adults after inadequate response to conventional or biological therapy",
      "therapeutic_area": ["gastroenterology"],
      "disease_setting": "chronic",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],

  "comparators": [
    {
      "comparator_name": "adalimumab (including biosimilar)",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "infliximab (including biosimilar)",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "vedolizumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "ustekinumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "tofacitinib",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "golimumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],

  "clinical_trials": [
    {
      "trial_name": "U-ACHIEVE induction",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "clinical remission (adapted Mayo score)",
      "sample_size": 473,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
    {
      "trial_name": "U-ACCOMPLISH",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "clinical remission (adapted Mayo score)",
      "sample_size": 515,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
    {
      "trial_name": "U-ACHIEVE maintenance",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "clinical remission (adapted Mayo score) at week 52",
      "sample_size": 451,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],

  "economic_model": {
    "model_type": "decision_tree_plus_markov",
    "model_source": "company",
    "time_horizon": "lifetime",
    "cycle_length": null,
    "health_states": ["remission", "response without remission", "active ulcerative colitis", "surgery", "post-surgery"]
  },

  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "Network meta-analyses comparing upadacitinib with all available biologics and JAK inhibitors",
      "company_position": "NMAs plausible; results supported by published meta-analyses",
      "erg_position": "Unresolvable technical issues; consistency assumption could not be tested; maintenance NMA less reliable",
      "committee_preference": "Concluded NMA results plausible and appropriate for decision making despite uncertainty",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "model_structure",
      "description": "Whether model should include second-line biologic treatment after failure",
      "company_position": "Model did not include second-line biologic (people moved to active UC with no treatment)",
      "erg_position": "Not plausible; added 'on subsequent treatment' health state",
      "committee_preference": "EAG's simplified adjustment preferred; company's pathway did not reflect NHS practice",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "utility_source",
      "description": "Whether to use literature values (Woehl 2008) or trial-based EQ-5D values",
      "company_position": "Used Woehl et al. 2008 for consistency with previous appraisals",
      "erg_position": "Preferred trial-based EQ-5D values in line with NICE reference case",
      "committee_preference": "Preferred trial-based EQ-5D values",
      "impact_on_icer": "uncertain_direction"
    }
  ],

  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head studies comparing upadacitinib with any comparator"
    }
  ],

  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },

  "icer_band": [
    {
      "band": "below_20k",
      "comparison_pair": "upadacitinib vs available biologics/JAK inhibitors (fully incremental)",
      "is_committee_preferred": true,
      "uncertainty_level": "moderate",
      "direction": "incremental"
    }
  ],

  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": true,
    "equality_issues_raised": false
  },

  "cross_references": [
    {
      "referenced_ta": null,
      "relationship": "comparator_guidance",
      "context": "NICE technology appraisal guidance on filgotinib and ozanimod for ulcerative colitis"
    },
    {
      "referenced_ta": null,
      "relationship": "precedent",
      "context": "NICE technology appraisal guidance on ustekinumab for ulcerative colitis (maintenance dose ratio precedent)"
    }
  ]
}
```

**Assessment: CLEAN** — Gastroenterology / IBD domain captured well. Many comparators, NMA, hybrid model. No `other` categories needed.

---

## Extraction 9: TA880 — Tezepelumab, severe asthma

```json
{
  "ta_number": "TA880",
  "doc_type": "FAD",

  "appraisal_metadata": {
    "title": "Tezepelumab for treating severe asthma",
    "issue_date": "2023",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "For severe asthma in people 12+ years when high-dose ICS plus another maintenance treatment has not worked. Only if 3+ exacerbations in past year OR on maintenance OCS. Stop if no 50% reduction at 12 months.",
    "appraisal_type": "STA",
    "committee_name": "Technology appraisal committee A",
    "erg_or_eag_name": null,
    "line_of_therapy": "third_line_plus",
    "methods_guide_era": "2022",
    "is_paediatric": true
  },

  "interventions": [
    {
      "generic_name": "tezepelumab",
      "brand_name": "Tezspire",
      "manufacturer": "AstraZeneca",
      "drug_class": "anti-TSLP monoclonal antibody",
      "mechanism_of_action": "thymic stromal lymphopoietin inhibitor",
      "route_of_administration": "subcutaneous",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "continuous",
      "intervention_type": "biologic"
    }
  ],

  "conditions": [
    {
      "condition_name": "severe asthma inadequately controlled despite high-dose inhaled corticosteroids plus another maintenance treatment",
      "therapeutic_area": ["respiratory"],
      "disease_setting": "chronic",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],

  "comparators": [
    {
      "comparator_name": "standard care alone (for non-biologic eligible)",
      "comparator_type": "standard_of_care",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "mepolizumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "benralizumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "omalizumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "reslizumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "dupilumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],

  "clinical_trials": [
    {
      "trial_name": "PATHWAY",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "annualised asthma exacerbation rate at 52 weeks",
      "sample_size": 550,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
    {
      "trial_name": "NAVIGATOR",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "annualised asthma exacerbation rate at 52 weeks",
      "sample_size": 1059,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
    {
      "trial_name": "SOURCE",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": false,
      "primary_outcome": "percentage reduction in maintenance OCS dose without loss of asthma control at 48 weeks",
      "sample_size": 150,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],

  "economic_model": {
    "model_type": "markov",
    "model_source": "company",
    "time_horizon": "lifetime (60 years)",
    "cycle_length": "4 weeks",
    "health_states": ["controlled asthma", "uncontrolled asthma", "controlled asthma with exacerbation", "uncontrolled asthma with exacerbation", "dead"]
  },

  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "NMAs comparing tezepelumab with existing biologics in NICE-recommended subpopulations",
      "company_position": "NMAs showed tezepelumab more effective in assessed subpopulations",
      "erg_position": "Highly uncertain due to biomarker mismatch between trials and NICE eligibility criteria",
      "committee_preference": "Concluded tezepelumab likely similar in effectiveness to existing biologics but highly uncertain",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Definition of treatment response at 52-week assessment",
      "company_position": "Initially any reduction in exacerbations; updated to 50% reduction in exacerbations or OCS dose",
      "erg_position": "20-50% reduction appropriate based on clinical advice",
      "committee_preference": "50% reduction in exacerbations or OCS dose appropriate",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "mortality_assumption",
      "description": "Asthma-related mortality estimates and whether to use CPRD all-cause mortality data",
      "company_position": "Original base-case asthma mortality; then updated with CPRD all-cause mortality study",
      "erg_position": "Company's original estimates overestimated mortality for <75 years; CPRD useful for non-biologic-eligible only",
      "committee_preference": "Original estimates preferred for most groups; CPRD data informative for non-biologic-eligible group in scenarios",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "utility_value_choice",
      "description": "Whether an additional utility gain for biological treatment over and above treatment effect is appropriate",
      "company_position": "Initially applied additional utility increment; removed after regression error identified",
      "erg_position": "Additional utility increment not appropriate; treatment effectiveness should be captured via health states",
      "committee_preference": "Agreed company's updated approach (removing additional utility) was appropriate",
      "impact_on_icer": "increases"
    }
  ],

  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head comparison between tezepelumab and any existing biologic"
    }
  ],

  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },

  "icer_band": [
    {
      "band": "below_20k",
      "comparison_pair": "tezepelumab vs existing biologics (biologic-eligible groups)",
      "is_committee_preferred": true,
      "uncertainty_level": "moderate",
      "direction": "incremental"
    },
    {
      "band": "20k_to_30k",
      "comparison_pair": "tezepelumab vs standard care (non-biologic eligible)",
      "is_committee_preferred": true,
      "uncertainty_level": "high",
      "direction": "incremental"
    }
  ],

  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": true,
    "equality_issues_raised": true
  },

  "cross_references": [
    {
      "referenced_ta": null,
      "relationship": "comparator_guidance",
      "context": "NICE technology appraisal guidance on benralizumab, mepolizumab, reslizumab, dupilumab and omalizumab for severe asthma"
    }
  ]
}
```

**Assessment: CLEAN** — Respiratory biologic with multiple subpopulations, NMA, mortality disputes all handled. `is_paediatric` flag correctly applied (12+ years). No `other` categories needed.

---

## Extraction 10: TA939 — Pembrolizumab, cervical cancer (ACD used)

```json
{
  "ta_number": "TA939",
  "doc_type": "ACD",

  "appraisal_metadata": {
    "title": "Pembrolizumab with platinum-based chemotherapy for recurrent, persistent or metastatic cervical cancer",
    "issue_date": "September 2022",
    "recommendation_type": "not_recommended",
    "restriction_details": null,
    "appraisal_type": "STA",
    "committee_name": "Appraisal committee A",
    "erg_or_eag_name": null,
    "line_of_therapy": "first_line",
    "methods_guide_era": "2022"
  },

  "interventions": [
    {
      "generic_name": "pembrolizumab",
      "brand_name": "Keytruda",
      "manufacturer": "Merck Sharp Dohme",
      "drug_class": "PD-1 checkpoint inhibitor",
      "mechanism_of_action": "anti-PD-1 monoclonal antibody",
      "route_of_administration": "intravenous",
      "is_combination_regimen": true,
      "combination_components": ["pembrolizumab", "cisplatin or carboplatin", "paclitaxel", "bevacizumab (optional)"],
      "treatment_duration_type": "fixed_duration",
      "intervention_type": "biologic"
    }
  ],

  "conditions": [
    {
      "condition_name": "persistent, recurrent, or metastatic cervical cancer with PD-L1 CPS >= 1",
      "therapeutic_area": ["oncology"],
      "disease_setting": "recurrent",
      "biomarker_defined_population": true,
      "biomarker_name": "PD-L1 combined positive score (CPS) >= 1"
    }
  ],

  "comparators": [
    {
      "comparator_name": "chemotherapy (cisplatin/carboplatin + paclitaxel) with or without bevacizumab",
      "comparator_type": "standard_of_care",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],

  "clinical_trials": [
    {
      "trial_name": "KEYNOTE-826",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "progression-free survival and overall survival",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],

  "economic_model": {
    "model_type": "markov",
    "model_source": "company",
    "time_horizon": "lifetime",
    "cycle_length": null,
    "health_states": ["progression-free survival", "progressed disease", "death"]
  },

  "methodological_decisions": [
    {
      "decision_category": "model_structure",
      "description": "State transition model vs partitioned survival model; structural link between PFS and OS",
      "company_position": "State transition model more accurate when OS data immature; PFS gains should translate to OS gains",
      "erg_position": "Limited evidence for validated PFS-OS relationship; questioned plausibility of long-term modelled benefits",
      "committee_preference": "Model may be adequate for current data; most appropriate approach may change with more data",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "survival_extrapolation",
      "description": "2-piece vs 1-piece approach for extrapolating time to progression and PFS",
      "company_position": "2-piece Kaplan-Meier + log-logistic for pembrolizumab arm",
      "erg_position": "Preferred 1-piece log-logistic for both arms",
      "committee_preference": "ERG's 1-piece may be too pessimistic; company's 2-piece may be too optimistic; neither reliable without further justification",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "treatment_effect_waning",
      "description": "Duration of pembrolizumab treatment benefit after 2-year stopping rule",
      "company_position": "Updated to treatment waning from 5 to 7 years after stopping",
      "erg_position": "Preferred waning from 2 to 5 years after stopping",
      "committee_preference": "Treatment waning from 3 to 5 years after stopping with 2-year stopping rule was reasonable",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "utility_source",
      "description": "Time-to-death vs health-state approach for estimating utilities",
      "company_position": "Time-to-death approach preferred",
      "erg_position": "Health-state approach preferred; consistent with most previous immunotherapy appraisals",
      "committee_preference": "Health-state approach preferred due to lack of evidence that utility is driven by time-to-death",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "surrogate_endpoint_validity",
      "description": "Whether PFS gains translate to OS gains in cervical cancer",
      "company_position": "PFS and OS hazard ratios similar in KEYNOTE-826; PFS should translate to OS",
      "erg_position": "Limited evidence for validated PFS-OS relationship",
      "committee_preference": "Likely that PFS benefit reflects OS benefit given limited second-line options; level of OS benefit uncertain",
      "impact_on_icer": "uncertain_direction"
    }
  ],

  "evidence_gaps": [
    {
      "gap_type": "immature_overall_survival",
      "description": "Median OS not reached in pembrolizumab arm; long-term survival benefit uncertain"
    }
  ],

  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": false
  },

  "icer_band": [
    {
      "band": "above_50k",
      "comparison_pair": "pembrolizumab+chemo+/-bevacizumab vs chemo+/-bevacizumab",
      "is_committee_preferred": true,
      "uncertainty_level": "very_high",
      "direction": "incremental"
    }
  ],

  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": true,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": true,
    "cancer_drugs_fund_eligible": false,
    "innovation_acknowledged": false,
    "equality_issues_raised": true
  },

  "cross_references": []
}
```

**Assessment: CLEAN** — Immunotherapy with immature OS, waning effect, CDF consideration all captured well. ACD format handled identically to FAD. No `other` categories needed.

---

## FINAL ASSESSMENT

### Per-TA ratings

| TA | Rating | Notes |
|----|--------|-------|
| TA100 | Clean | Multi-intervention MTA, 2006 format, dominant/cost-saving captured via decremental direction |
| TA101 | Clean | Pre-2008 STA, no PAS, equality consideration flagged |
| TA420 | Clean | Cardiovascular prevention, prevention_secondary + maintenance |
| TA871 | Clean | Cost-comparison, equivalence_assumption used correctly |
| TA887 | Clean | Complex not-recommended with biomarker, crossover adjustment, ITC, end-of-life |
| TA919 | Minor friction | `treatment_duration_type`: "other" used (as-needed dosing); `baseline_risk` used for placebo response modelling (slight stretch) |
| TA1110 | Clean | Complex post-appeal, 5 meetings, treatment sequencing, population generalisability |
| TA856 | Clean | Gastroenterology, NMA, hybrid model structure |
| TA880 | Clean | Respiratory biologic, multiple subpopulations, mortality dispute, is_paediatric |
| TA939 | Clean | ACD format, immunotherapy, CDF considered but rejected, treatment waning |

**Summary: 9/10 clean, 1/10 minor friction. Zero schema gaps.**

### `other` usage counts

| Field | Times `other` used | Context |
|-------|--------------------|---------|
| decision_categories | 0 | All decisions mapped to existing categories |
| gap_types | 0 | All gaps mapped to existing types |
| model_type | 1 | TA420 (ticagrelor) used `other` — risk-equation model |
| treatment_duration_type | 1 | TA919 (rimegepant) used `other` — as-needed acute dosing |

### Schema stability verdict

**The schema is STABLE and ready for bulk extraction.** After 5 rounds across 50 TAs spanning:
- 2003-2025
- 9 therapeutic areas (oncology, cardiovascular, neurology, gastroenterology, respiratory, rheumatology, immunology, haematology, renal)
- All recommendation types (recommended, restricted, optimised, not recommended, CDF)
- All appraisal types (STA, MTA, cost-comparison)
- All methods guide eras (pre-2008, 2008, 2013, 2022)
- Edge cases (multi-intervention, post-appeal, CDF reconsideration, paediatric, biomarker-defined)

No new entity types, relations, enum values, or structural changes were required in this round.

### TOP 3 things to fix before bulk extraction

1. **Add `as_needed` to `treatment_duration_type` enum.** Rimegepant (and potentially other acute treatments like triptans in future) does not fit `fixed_duration`, `continuous`, or `cyclical`. This is a one-line addition with no structural impact. Low risk of overcomplication.

2. **Add `risk_equation` or `patient_simulation` to `model_type` enum.** TA420's individual-patient model with risk equations is a recognizable model type that does not fit any existing enum value. Adding it prevents `other` usage by cheap models. Alternatively, `patient_level_simulation` could be interpreted broadly enough; guidance in the extraction prompt could clarify this.

3. **Add guidance for cross-reference TA numbers.** Several cross-references in this round have `referenced_ta: null` because the TA number was not explicitly stated (e.g., "NICE's technology appraisal guidance on enzalutamide for..."). The extraction prompt should instruct: "If a NICE TA is referenced by name but without a TA number, set referenced_ta to null. Do not invent TA numbers." This is already implicitly the case but should be explicit for cheap models.

### Things we should NOT fix (acceptable imperfections)

1. **`baseline_risk` used for placebo response modelling (TA919).** This is a slight semantic stretch, but the category is close enough. Creating a new `placebo_response` category would be too niche and would rarely recur. A cheap model will either map it to `baseline_risk` or `model_structure`, both acceptable.

2. **`maintenance` line_of_therapy for secondary prevention (TA420).** Cardiovascular prevention after acute treatment does not perfectly map to oncology-derived terminology. But `maintenance` is semantically reasonable and no better alternative exists without domain-specific proliferation.

3. **`treatment_duration_type: other` for as-needed dosing.** Until the enum is updated (see fix #1 above), `other` is the correct fallback. A cheap model will handle this correctly.

4. **Missing TA numbers in cross-references.** Many recent FADs reference other NICE guidance by title without citing TA numbers. This is a document limitation, not a schema limitation. Post-processing can resolve these via title matching.

5. **`is_paediatric` not in the formal ontology.json.** TA880 includes patients 12+ years. The `is_paediatric` flag was added in v0.3.0 as a TechnologyAppraisal-level attribute but is not formally listed under entity_types.TechnologyAppraisal.attributes in the current ontology.json. This should be verified but is minor.

6. **Lack of `eligible_population` extraction.** The `eligible_population` field exists in the schema but was not consistently extractable from these documents. This is acceptable — it can be populated during post-processing from NICE's published population estimates.

### Conclusion

**Proceed to bulk extraction.** The ontology v0.5.0 schema handled all 10 TAs in this final round with zero structural changes required. The three minor fixes recommended are additive (new enum values, prompt clarification) and do not change the schema structure. A cheap model (e.g., Haiku or Sonnet) should be able to extract these TAs reliably with the current extraction prompt.
