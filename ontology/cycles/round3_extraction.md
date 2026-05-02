# Round 3 Extraction Test: Complex CE / Methodological Stress Test

Ontology version: 0.3.0
Tested against: 10 FADs spanning 2010--2023
Tester: Claude Opus 4.6 (round 3 refinement cycle)
Focus: methodological decision coverage, cost-effectiveness complexity, multi-comparator / sequencing TAs

---

## 1. TA187 -- Infliximab + Adalimumab for Crohn's disease (MTA, 2010)

### Abbreviated extraction

```json
{
  "ta_number": "TA187",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Infliximab (review) and adalimumab for the treatment of Crohn's disease",
    "issue_date": "February 2010",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Recommended for severe active Crohn's (CDAI >=300 or Harvey-Bradshaw >=8-9) after conventional therapy failure. Planned course of treatment until failure or 12 months, then reassessment. Treatment should start with the less expensive drug. Infliximab additionally recommended for fistulising disease and for children aged 6-17.",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "West Midlands Health Technology Assessment Collaboration",
    "line_of_therapy": "any_line",
    "eligible_population": "~60,000 UK prevalence; subset with severe active disease",
    "methods_guide_era": "2008"
  },
  "interventions": [
    {
      "generic_name": "infliximab",
      "brand_name": null,
      "manufacturer": "Schering-Plough",
      "drug_class": "TNF-alpha inhibitor",
      "mechanism_of_action": "chimeric human-murine monoclonal antibody binding TNF-alpha",
      "route_of_administration": "intravenous",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "cyclical",
      "biosimilar_available": false
    },
    {
      "generic_name": "adalimumab",
      "brand_name": null,
      "manufacturer": "Abbott Laboratories",
      "drug_class": "TNF-alpha inhibitor",
      "mechanism_of_action": "recombinant human monoclonal antibody binding TNF-alpha",
      "route_of_administration": "subcutaneous",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "cyclical",
      "biosimilar_available": false
    }
  ],
  "conditions": [{
    "condition_name": "severe active Crohn's disease",
    "therapeutic_area": ["gastroenterology"],
    "disease_setting": "chronic",
    "biomarker_defined_population": false,
    "biomarker_name": null
  }],
  "comparators": [{
    "comparator_name": "standard care (corticosteroids, immunosuppressants)",
    "comparator_type": "standard_of_care",
    "is_established_practice": true,
    "committee_preferred": true
  }],
  "clinical_trials": [
    {
      "trial_name": "ACCENT I",
      "study_design": "RCT",
      "phase": null,
      "is_pivotal": true,
      "primary_outcome": "remission rate (CDAI)",
      "sample_size": 573,
      "crossover_occurred": true,
      "crossover_adjusted": false,
      "generalisability_concern": false
    },
    {
      "trial_name": "CHARM",
      "study_design": "RCT",
      "phase": null,
      "is_pivotal": true,
      "primary_outcome": "remission at week 26 and 56",
      "sample_size": 778,
      "crossover_occurred": true,
      "crossover_adjusted": false,
      "generalisability_concern": false
    },
    {
      "trial_name": "CLASSIC I",
      "study_design": "RCT",
      "phase": null,
      "is_pivotal": true,
      "primary_outcome": "remission rate",
      "sample_size": 299,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
    {
      "trial_name": "GAIN",
      "study_design": "RCT",
      "phase": null,
      "is_pivotal": true,
      "primary_outcome": "remission rate",
      "sample_size": 325,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "multiple (company models + Assessment Group model + DSU reconciliation)",
    "time_horizon": "variable (1 year AG, lifetime Abbott)",
    "cycle_length": null,
    "health_states": ["remission", "relapse", "surgery", "post-surgery remission"]
  },
  "methodological_decisions": [
    {
      "decision_category": "baseline_risk",
      "description": "Relapse rate for patients on standard care — key driver of cost-effectiveness",
      "company_position": "Higher relapse rates from trial data (Abbott) or manufacturer-estimated rates",
      "erg_position": "Assessment Group used low relapse rate (0.59%) from Silverstein cohort",
      "committee_preference": "Agreed relapse rates should be considerably higher than AG model; DSU review found 7-14% 4-week probabilities more typical; decision informed by higher rates",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "model_structure",
      "description": "Substantial differences between manufacturer and Assessment Group model structures that could not be fully reconciled",
      "company_position": "Schering-Plough: 5-year Markov with fistula states. Abbott: lifetime horizon with CDAI-based states",
      "erg_position": "Assessment Group: 4-state Markov based on Silverstein transitions, 1-year horizon",
      "committee_preference": "Acknowledged models could not be reconciled; collective body of evidence sufficient to inform decision",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "treatment_effect_duration",
      "description": "Whether to model episodic vs maintenance (planned course) treatment",
      "company_position": "Both episodic and maintenance scenarios presented",
      "erg_position": "Assessment Group modelled both but noted episodic dominated by standard care",
      "committee_preference": "Recommended planned course of treatment for 12 months; episodic treatment not preferred due to antibody development risk and relapse concerns",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Duration of treatment and criteria for continuation beyond 12 months",
      "company_position": "Lifetime treatment assumed in Abbott model",
      "erg_position": "Limited evidence for treatment beyond 1 year",
      "committee_preference": "12-month planned course, then reassessment for ongoing active disease; trial withdrawal in stable remission; option to restart if relapse",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Uncertainty in true drug costs due to dose escalation, patient weight, vial sharing, and local discounts",
      "company_position": "Costs varied substantially depending on assumptions",
      "erg_position": "Acknowledged uncertainty over true costs",
      "committee_preference": "Choice of treatment should be based on cost; start with less expensive drug; local factors affect relative costs",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Whether infliximab and adalimumab should be compared against each other or only against standard care",
      "company_position": "Abbott argued adalimumab dominated infliximab; Schering-Plough did not present direct comparison",
      "erg_position": "No indirect comparison possible due to trial heterogeneity",
      "committee_preference": "Unable to differentiate clinically; differentiated by cost only",
      "impact_on_icer": "negligible"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trial comparing infliximab and adalimumab"
    },
    {
      "gap_type": "short_follow_up",
      "description": "Limited evidence supporting treatment beyond 1 year"
    },
    {
      "gap_type": "missing_real_world_evidence",
      "description": "Uncertain true treatment costs; dose escalation rates unclear"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },
  "icer_band": {
    "band": "not_estimable",
    "comparison_pair": "infliximab/adalimumab vs standard care",
    "is_committee_preferred": false,
    "uncertainty_level": "very_high"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },
  "cross_references": [{
    "referenced_ta": "TA40",
    "relationship": "same_drug_different_indication",
    "context": "Reviews and replaces TA40 guidance on infliximab for Crohn's disease"
  }]
}
```

### Schema stress points
- **Multi-drug MTA**: Two interventions appraised simultaneously. Ontology handles this well via array.
- **Multi-model reconciliation**: Three separate economic models (Schering-Plough, Abbott, Assessment Group) plus DSU reconciliation. The `model_source` field is insufficient -- no way to capture that multiple models existed and were partially reconciled.
- **Episodic vs maintenance vs planned course**: The treatment_duration_type enum does not have a "planned_course" value, which is the committee's preferred framing. "cyclical" is the closest but not accurate.
- **Paediatric sub-recommendation**: Infliximab recommended for children 6-17 but adalimumab is not. The ontology has `is_paediatric` but no mechanism for intervention-specific sub-recommendations.
- **Fistulising disease sub-recommendation**: Different recommendation for fistulising vs non-fistulising Crohn's. Cannot easily capture via `restriction_details` alone.
- **ICER band**: Multiple ICERs reported across different models, comparisons, relapse rate assumptions. No single "committee preferred" ICER exists. The `not_estimable` band is used but is a poor fit -- the ICERs were estimated, just radically different depending on model.

---

## 2. TA432 -- Everolimus for advanced renal cell carcinoma (CDF reconsideration, 2017)

### Abbreviated extraction

```json
{
  "ta_number": "TA432",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Everolimus for advanced renal cell carcinoma after previous treatment",
    "issue_date": "2017",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Recommended within marketing authorisation only if company provides the discount agreed in the patient access scheme",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "ERG (not named)",
    "line_of_therapy": "second_line",
    "eligible_population": "<4000 in England and Wales",
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "everolimus",
    "brand_name": "Afinitor",
    "manufacturer": "Novartis Pharmaceuticals",
    "drug_class": "mTOR inhibitor",
    "mechanism_of_action": "active inhibitor of mammalian target of rapamycin (mTOR) protein",
    "route_of_administration": "oral",
    "is_combination_regimen": false,
    "combination_components": null,
    "treatment_duration_type": "treat_to_progression",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "advanced renal cell carcinoma after VEGF-targeted therapy",
    "therapeutic_area": ["oncology"],
    "disease_setting": "metastatic",
    "biomarker_defined_population": false,
    "biomarker_name": null
  }],
  "comparators": [
    {
      "comparator_name": "best supportive care",
      "comparator_type": "best_supportive_care",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "axitinib",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [{
    "trial_name": "RECORD-1",
    "study_design": "RCT",
    "phase": "phase III",
    "is_pivotal": true,
    "primary_outcome": "progression-free survival",
    "sample_size": null,
    "crossover_occurred": true,
    "crossover_adjusted": true,
    "generalisability_concern": false
  }],
  "economic_model": {
    "model_type": "markov",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": ["stable disease without adverse events", "stable disease with adverse events", "progressed disease", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "crossover_adjustment",
      "description": "81% crossover from placebo to everolimus; IPCW vs RPSFT methods",
      "company_position": "Presented both IPCW and RPSFT; preferred IPCW initially, then revised both",
      "erg_position": "RPSFT more methodologically robust (IPCW assumes no unmeasured confounders); ERG's exploratory RPSFT analysis preferred",
      "committee_preference": "Preferred RPSFT method; ERG's exploratory analysis most plausible (5.2 month OS gain more plausible than company's 8.2 months)",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "survival_extrapolation",
      "description": "Extrapolation of BSC arm OS using Weibull vs company's approach",
      "company_position": "Used mean of RPSFT cycles 5 and 6 for BSC extrapolation",
      "erg_position": "Weibull distribution more appropriate as it uses all available data",
      "committee_preference": "Agreed Weibull fitting was more appropriate",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "utility_source",
      "description": "Utility estimates not directly from RECORD-1 trial",
      "company_position": "Used utility estimates external to trial; similar values across disease states",
      "erg_position": "Larger decrement plausible for progressed disease; but one-way sensitivity showed limited impact",
      "committee_preference": "Accepted utility assumptions as acceptable despite uncertainty",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Whether to compare with axitinib (newly recommended) or BSC only",
      "company_position": "Model compared only with BSC; presented cost-minimisation vs axitinib separately",
      "erg_position": "Agreed PFS and OS similar for everolimus and axitinib; cost-minimisation appropriate",
      "committee_preference": "Accepted clinical equivalence between everolimus and axitinib; cost-minimisation analysis appropriate",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "treatment_sequencing",
      "description": "Treatment pathway changed since original TA219: axitinib and nivolumab now available after first-line TKI",
      "company_position": "Everolimus remains valuable option in changed pathway",
      "erg_position": null,
      "committee_preference": "Agreed everolimus remains valuable; treatment pathway has changed",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "immature_overall_survival",
      "description": "OS based on modelled crossover-adjusted data, not directly observed"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": [
    {
      "band": "above_50k",
      "comparison_pair": "everolimus vs BSC (original TA219, without revised PAS)",
      "is_committee_preferred": false,
      "uncertainty_level": "high"
    },
    {
      "band": "20k_to_30k",
      "comparison_pair": "everolimus vs BSC (CDF reconsideration, with revised PAS)",
      "is_committee_preferred": true,
      "uncertainty_level": "moderate"
    }
  ],
  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": true,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": true,
    "cancer_drugs_fund_eligible": true,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },
  "cross_references": [
    {
      "referenced_ta": "TA219",
      "relationship": "same_drug_different_indication",
      "context": "CDF reconsideration of the original TA219 which did not recommend everolimus"
    }
  ]
}
```

### Schema stress points
- **CDF reconsideration**: The ontology has no concept for "reconsideration" or "reappraisal". The cross_ta `SUPERSEDES` relationship is close but doesn't capture that this is a CDF-driven re-evaluation of the same drug/indication. A new relationship reason like `cdf_reconsideration` is needed.
- **Dual ICER context**: The original TA219 concluded "not recommended" (ICER ~51,700), but the CDF reconsideration concluded "recommended" (ICER <30,000 with PAS). The ontology correctly allows icer_band as array, which handles this.
- **Cost-minimisation analysis**: The model compared everolimus vs axitinib as a cost-minimisation analysis (no QALY difference). The model_type enum lacks `cost_minimisation` as a second analysis type alongside the primary Markov model.
- **Changed pathway**: The committee acknowledged the pathway has evolved (nivolumab now available). The ontology does not capture pathway evolution.

---

## 3. TA488 -- Regorafenib for GIST (3rd line, end-of-life, 2017)

### Abbreviated extraction

```json
{
  "ta_number": "TA488",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Regorafenib for previously treated unresectable or metastatic gastrointestinal stromal tumours",
    "issue_date": "October 2017",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "ECOG performance status 0 to 1 only; with PAS discount",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee D",
    "erg_or_eag_name": "ERG (not named)",
    "line_of_therapy": "third_line_plus",
    "eligible_population": null,
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "regorafenib",
    "brand_name": "Stivarga",
    "manufacturer": "Bayer",
    "drug_class": "multikinase inhibitor",
    "mechanism_of_action": null,
    "route_of_administration": "oral",
    "is_combination_regimen": false,
    "combination_components": null,
    "treatment_duration_type": "treat_to_progression",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "unresectable or metastatic gastrointestinal stromal tumours after imatinib and sunitinib",
    "therapeutic_area": ["oncology"],
    "disease_setting": "metastatic",
    "biomarker_defined_population": false,
    "biomarker_name": null
  }],
  "comparators": [{
    "comparator_name": "best supportive care",
    "comparator_type": "best_supportive_care",
    "is_established_practice": true,
    "committee_preferred": true
  }],
  "clinical_trials": [{
    "trial_name": "GRID",
    "study_design": "RCT",
    "phase": null,
    "blinding": "double-blind",
    "is_pivotal": true,
    "primary_outcome": "progression-free survival",
    "sample_size": 199,
    "crossover_occurred": true,
    "crossover_adjusted": true,
    "generalisability_concern": false
  }],
  "economic_model": {
    "model_type": "partitioned_survival",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": ["progression free", "progressed", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "crossover_adjustment",
      "description": "88% crossover from placebo to regorafenib; IPE vs RPSFT methods; with and without recensoring",
      "company_position": "Base case: IPE with recensoring (2017 data); both methods appropriate",
      "erg_position": "Both IPE and RPSFT appropriate; accepted 2017 data after initial concerns; recensoring arguments evenly balanced",
      "committee_preference": "Both RPSFT and IPE should be considered; analyses with and without recensoring should be considered",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "survival_extrapolation",
      "description": "Choice of parametric distribution for OS extrapolation -- log-logistic vs Weibull",
      "company_position": "Log-logistic: best fit to trial data",
      "erg_position": "Clinical plausibility critical; evidence for longer vs shorter tails evenly balanced",
      "committee_preference": "Weibull preferred: shorter tail more clinically plausible (very few survive 10 years at this stage)",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "other",
      "description": "Whether to include additional background mortality in model after trial period",
      "company_position": "Did not include background mortality",
      "erg_position": "Included background mortality in base case",
      "committee_preference": "Agreed background mortality adjustment appropriate; impact lower with Weibull",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "utility_source",
      "description": "Age-related utility decrements",
      "company_position": "No age-related decrements",
      "erg_position": "Applied age-related utility decrements",
      "committee_preference": "Agreed age-related decrements appropriate; limited impact",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "subgroup_definition",
      "description": "Restricting recommendation to ECOG performance status 0-1",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "Limited data for PS >=2; clinical practice would only treat PS 0-1; recommendation restricted to PS 0-1",
      "impact_on_icer": "negligible"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "immature_overall_survival",
      "description": "OS based on crossover-adjusted data with wide confidence intervals"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "30k_to_50k",
    "comparison_pair": "regorafenib vs BSC",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate"
  },
  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": true,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": true,
    "cancer_drugs_fund_eligible": true,
    "innovation_acknowledged": false,
    "equality_issues_raised": true
  },
  "cross_references": []
}
```

### Schema stress points
- **Recensoring debate**: A methodological choice (whether to apply recensoring in crossover adjustment) that does not fit existing categories. Used `crossover_adjustment` but the recensoring debate is a sub-issue.
- **Background mortality**: Using `other` for background mortality adjustment -- this is a recurrent decision in oncology TAs but has no dedicated category.
- **Data cut-off choice**: Committee debated 2015 vs 2017 data for OS estimation. This is a methodological decision about data maturity but no category covers it. Could be `other` or a new `data_cutoff` category.
- **Treatment continuation beyond progression**: Model included regorafenib costs post-progression (per trial protocol). This is an unusual treatment pattern that doesn't clearly map to existing categories.

---

## 4. TA512 -- Tivozanib for advanced RCC (1st line, crowded comparator space, 2018)

### Abbreviated extraction

```json
{
  "ta_number": "TA512",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Tivozanib for treating advanced renal cell carcinoma",
    "issue_date": "February 2018",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "First-line only (no previous treatment); with PAS discount",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee B",
    "erg_or_eag_name": "ERG (not named)",
    "line_of_therapy": "first_line",
    "eligible_population": null,
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "tivozanib",
    "brand_name": "Fotivda",
    "manufacturer": "EUSA Pharma",
    "drug_class": "VEGFR tyrosine kinase inhibitor",
    "mechanism_of_action": "targets 3 vascular endothelial growth factor receptors",
    "route_of_administration": "oral",
    "is_combination_regimen": false,
    "combination_components": null,
    "treatment_duration_type": "treat_to_progression",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "advanced renal cell carcinoma, untreated",
    "therapeutic_area": ["oncology"],
    "disease_setting": "metastatic",
    "biomarker_defined_population": false,
    "biomarker_name": null
  }],
  "comparators": [
    {
      "comparator_name": "pazopanib",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "sunitinib",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [{
    "trial_name": "TIVO-1",
    "study_design": "RCT",
    "phase": null,
    "blinding": "open_label",
    "is_pivotal": true,
    "primary_outcome": "progression-free survival",
    "sample_size": 517,
    "crossover_occurred": true,
    "crossover_adjusted": true,
    "generalisability_concern": true
  }],
  "economic_model": {
    "model_type": "partitioned_survival",
    "model_source": "company",
    "time_horizon": "10 years",
    "cycle_length": null,
    "health_states": ["pre-progression", "post-progression", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "comparator_selection",
      "description": "Pivotal trial comparator (sorafenib) not used in NHS; indirect comparison needed to relevant comparators",
      "company_position": "Used network meta-analysis to compare with pazopanib and sunitinib via sorafenib link",
      "erg_position": "Agreed on network structure (4 trials) but different fractional polynomial selections",
      "committee_preference": "Neither company's nor ERG's NMA results considered plausible or robust; at best tivozanib similar to sunitinib/pazopanib",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "indirect_comparison_method",
      "description": "Fractional polynomial network meta-analysis -- curve selection had large impact on results",
      "company_position": "Used fractional polynomials because PH assumption violated; selected curves giving tivozanib favourable OS vs sunitinib",
      "erg_position": "Used different fractional polynomial curves prioritising clinical plausibility; results showed tivozanib less effective",
      "committee_preference": "Neither set of results plausible; ERG's PFS estimate (6.1 months) unrealistically low vs trial (12.7 months); choice of curve had large impact",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "crossover_adjustment",
      "description": "62.6% crossover in TIVO-1 from sorafenib to tivozanib; IPCW and RPSFT methods used",
      "company_position": "IPCW preferred (full population, showed similar OS); RPSFT done on untreated subgroup",
      "erg_position": "RPSFT preferred; RPSFT results showed tivozanib had lower OS than sorafenib",
      "committee_preference": "Both methods had limitations; at best tivozanib similar to sorafenib for OS",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "proportional_hazards",
      "description": "PH assumption did not hold for PFS in TIVO-1 -- motivated use of fractional polynomials",
      "company_position": "Acknowledged PH violation; used fractional polynomials",
      "erg_position": "Agreed PH assumption violated",
      "committee_preference": "Agreed PH violated; fractional polynomial approach accepted but results implausible",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "population_generalisability",
      "description": "88% of TIVO-1 patients from Central/Eastern Europe; may have poorer access to subsequent therapies",
      "company_position": "Baseline characteristics broadly similar",
      "erg_position": null,
      "committee_preference": "Concerned about generalisability; shorter survival times in TIVO-1 may partly reflect geography",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "treatment_sequencing",
      "description": "Model included subsequent therapies (axitinib, everolimus, nivolumab, BSC) but only costs not benefits",
      "company_position": "60% axitinib, 40% BSC; axitinib for rest of life; costs not discounted; no benefits modelled",
      "erg_position": "50% axitinib, 10% everolimus, 30% nivolumab, 10% BSC; costs discounted; no benefits modelled",
      "committee_preference": "ERG assumptions better reflect current pathway; concerned that both excluded subsequent therapy benefits on OS",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Relative dose intensity: whether to model intended dose (100%) or actual delivered dose",
      "company_position": "100% dose intensity for all treatments",
      "erg_position": "94% for tivozanib, 86% for pazopanib and sunitinib (from trial and prior appraisals)",
      "committee_preference": "Likely between 100% and ERG estimates, closer to ERG; including RDI makes tivozanib less cost effective",
      "impact_on_icer": "increases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No direct trial comparing tivozanib with pazopanib or sunitinib"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "tivozanib vs pazopanib/sunitinib (less costly, less effective -- reversed ICER)",
    "is_committee_preferred": true,
    "uncertainty_level": "very_high"
  },
  "special_considerations": {
    "end_of_life_considered": true,
    "end_of_life_met": false,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },
  "cross_references": []
}
```

### Schema stress points
- **Reversed ICER (less costly, less effective)**: The ontology has no concept for a "south-west quadrant" ICER where the technology is cheaper but less effective. The icer_band values and decision logic are implicitly "more effective, more costly" (north-east quadrant). A reversed ICER of >30,000 saved per QALY lost is a fundamentally different decision framework. This needs representation -- perhaps a `direction` field (incremental vs decremental) on icer_band.
- **Fractional polynomial NMA**: Neither company nor ERG results deemed plausible. This is a deeper failure of evidence than the existing gap types capture. A gap_type like `unreliable_indirect_comparison` would help.
- **Subsequent therapy benefits not modelled**: Both company and ERG included costs of subsequent treatments but not health benefits. This is a common shortcoming in oncology models. `treatment_sequencing` captures the debate but the specific issue of "costs without benefits" is a structural model bias.

---

## 5. TA563 -- Abemaciclib + AI for HR+ breast cancer (1st line CDK inhibitor, 2019)

### Abbreviated extraction

```json
{
  "ta_number": "TA563",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Abemaciclib with an aromatase inhibitor for previously untreated, hormone receptor-positive, HER2-negative, locally advanced or metastatic breast cancer",
    "issue_date": "January 2019",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Within marketing authorisation as first endocrine-based therapy; only with commercial arrangement",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee A",
    "erg_or_eag_name": "ERG (not named)",
    "line_of_therapy": "first_line",
    "eligible_population": null,
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "abemaciclib",
    "brand_name": "Verzenios",
    "manufacturer": "Eli Lilly",
    "drug_class": "CDK 4/6 inhibitor",
    "mechanism_of_action": "cyclin-dependent kinase 4 and 6 inhibitor",
    "route_of_administration": "oral",
    "is_combination_regimen": true,
    "combination_components": ["abemaciclib", "aromatase inhibitor (letrozole or anastrozole)"],
    "treatment_duration_type": "treat_to_progression",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "HR-positive, HER2-negative locally advanced or metastatic breast cancer",
    "therapeutic_area": ["oncology"],
    "disease_setting": "metastatic",
    "biomarker_defined_population": true,
    "biomarker_name": "HR-positive, HER2-negative"
  }],
  "comparators": [
    {
      "comparator_name": "palbociclib with aromatase inhibitor",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "ribociclib with aromatase inhibitor",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [{
    "trial_name": "MONARCH 3",
    "study_design": "RCT",
    "phase": "phase III",
    "blinding": "double_blind",
    "is_pivotal": true,
    "primary_outcome": "progression-free survival",
    "sample_size": 493,
    "crossover_occurred": false,
    "crossover_adjusted": null,
    "generalisability_concern": false
  }],
  "economic_model": {
    "model_type": "other",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": ["progression-free survival 1st line", "post-progression 1st line", "progression-free survival 2nd line", "post-progression 2nd line", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "other",
      "description": "Class effect assumption: whether abemaciclib, palbociclib and ribociclib have equivalent clinical effectiveness",
      "company_position": "NMA showed similar efficacy; class effect supported",
      "erg_position": "Agreed no large differences; NMA has limitations (PH assumption may not hold, OS immature)",
      "committee_preference": "Concluded appropriate to consider CDK 4/6 inhibitors as a class; cost-comparison approach preferred over full CEA",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Time on treatment differed substantially across CDK 4/6 inhibitors -- unexplained",
      "company_position": "Used MONARCH 3 for abemaciclib, SPC data for comparators; large difference unexplained",
      "erg_position": "Questioned plausibility of large differences in treatment duration given similar PFS",
      "committee_preference": "No reason to expect a difference; assumed same treatment duration for all 3 CDK 4/6 inhibitors",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "model_structure",
      "description": "State-transition model with 'fixed pay-off' submodel for second-line treatment -- differs from previous CDK 4/6 inhibitor appraisals",
      "company_position": "Novel approach explicitly modelling second-line to reduce OS uncertainty",
      "erg_position": "New approach with similarities to ribociclib model but not identical",
      "committee_preference": "Acknowledged difference from previous appraisals; preferred ERG's approach to PFS, pre-progression death, 2nd line utility, and 2nd line OS extrapolation",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "indirect_comparison_method",
      "description": "Network meta-analyses comparing 3 CDK 4/6 inhibitors",
      "company_position": "NMA of 18 studies showed similar treatment effects for all 3 CDK 4/6 inhibitors",
      "erg_position": "Agreed; but noted PH assumption may not hold; heterogeneity across trials; OS immature in 3/4 trials",
      "committee_preference": "No real difference in efficacy shown; results plausible despite limitations",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "survival_extrapolation",
      "description": "Overall survival on second-line treatment -- choice of trial data and parametric distribution",
      "company_position": "Used MONARCH 2 (exponential) and CONFIRM (Weibull) together",
      "erg_position": "Preferred MONARCH 2 only (Gompertz distribution)",
      "committee_preference": "Preferred ERG's approach",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trial comparing abemaciclib with palbociclib or ribociclib"
    },
    {
      "gap_type": "immature_overall_survival",
      "description": "OS data from MONARCH 3 immature; final analysis not available"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "confidential",
    "comparison_pair": "abemaciclib vs palbociclib/ribociclib (cost-comparison)",
    "is_committee_preferred": true,
    "uncertainty_level": "low"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },
  "cross_references": []
}
```

### Schema stress points
- **Class effect / cost-comparison**: The committee concluded that a cost-comparison approach was preferred because clinical equivalence was assumed. The model_type enum does not include `cost_comparison`. This is increasingly common (also seen in TA888).
- **"Class effect" decision**: The decision that 3 drugs have equivalent clinical effect is not well captured by any existing category. Used `other` but this is a distinct, important decision type. Proposed new category: `class_effect_assumption`.
- **"Fixed pay-off" submodel**: A novel model structure explicitly modelling second-line treatment within the economic model. The model_type `other` is used because no enum value captures this.

---

## 6. TA671 -- Mepolizumab for severe eosinophilic asthma (2016)

### Note on data

The FAD.md file for TA671 contains only the equality impact assessment form, not the substantive FAD. Extraction is based on the committee papers/pre-meeting briefing (ACD.md) and is therefore less detailed than for other TAs.

### Abbreviated extraction

```json
{
  "ta_number": "TA671",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Mepolizumab for treating severe refractory eosinophilic asthma",
    "issue_date": "November 2016",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Severe refractory eosinophilic asthma in adults; blood eosinophil threshold required; continuation criteria based on exacerbation rate reduction",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "School of Health and Related Research (ScHARR)",
    "line_of_therapy": "any_line",
    "eligible_population": null,
    "methods_guide_era": "2013"
  },
  "interventions": [{
    "generic_name": "mepolizumab",
    "brand_name": null,
    "manufacturer": "GlaxoSmithKline",
    "drug_class": "anti-IL-5 monoclonal antibody",
    "mechanism_of_action": "binds interleukin-5 to reduce eosinophil levels",
    "route_of_administration": "subcutaneous",
    "is_combination_regimen": false,
    "combination_components": null,
    "treatment_duration_type": "continuous",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "severe refractory eosinophilic asthma",
    "therapeutic_area": ["respiratory"],
    "disease_setting": "chronic",
    "biomarker_defined_population": true,
    "biomarker_name": "blood eosinophil count"
  }],
  "comparators": [
    {
      "comparator_name": "best standard care (without biological treatment)",
      "comparator_type": "standard_of_care",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "omalizumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "MENSA",
      "study_design": "RCT",
      "phase": "phase III",
      "is_pivotal": true,
      "primary_outcome": "exacerbation rate",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": null
  },
  "methodological_decisions": [
    {
      "decision_category": "subgroup_definition",
      "description": "Blood eosinophil count threshold for treatment eligibility -- 150 vs 300 cells/microlitre",
      "company_position": ">=150 cells/microlitre at initiation; >=4 exacerbations or on maintenance OCS",
      "erg_position": ">=300 cells/microlitre in previous 12 months more suitable",
      "committee_preference": null,
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "treatment_effect_duration",
      "description": "Assumption about treatment duration in model: 10 years vs lifetime",
      "company_position": "10-year treatment duration",
      "erg_position": "Lifetime treatment duration more reflective of clinical practice",
      "committee_preference": null,
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "utility_source",
      "description": "EQ-5D from trials vs mapping from SGRQ; duration of exacerbation utility decrements",
      "company_position": "Mapped from SGRQ",
      "erg_position": "EQ-5D directly from trials more appropriate",
      "committee_preference": null,
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Continuation criteria: treatment continued unless exacerbation rate worsened",
      "company_position": "Continue unless worsened vs previous year",
      "erg_position": null,
      "committee_preference": null,
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "other",
      "description": "Asthma-related mortality source: Watson study vs Roberts study with narrower age bands",
      "company_position": "Watson study (age bands 18-44 and 45+, constant rate for 45+)",
      "erg_position": "Roberts study (narrower age bands including 65+) preferable",
      "committee_preference": null,
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "confidential",
    "comparison_pair": "mepolizumab vs standard care",
    "is_committee_preferred": null,
    "uncertainty_level": "high"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },
  "cross_references": []
}
```

### Schema stress points
- **Incomplete FAD data**: The FAD file only contained the equality impact assessment. This is a real-world data quality issue that extraction pipelines must handle.
- **Asthma-related mortality source**: The choice of mortality data source is a recurrent methodological issue in chronic disease models. Used `other` but this is common enough (also seen in TA880) to potentially warrant its own category: `mortality_source` or `background_mortality`.
- **Biomarker threshold as treatment restriction**: The decision about eosinophil count threshold is both a subgroup definition and a stopping rule. It has aspects of both.

---

## 7. TA828 -- Ozanimod for ulcerative colitis (oral vs biologic, 2022)

### Abbreviated extraction

```json
{
  "ta_number": "TA828",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Ozanimod for treating moderately to severely active ulcerative colitis",
    "issue_date": "July 2022",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "After conventional treatment failure if infliximab not suitable; or after biological treatment failure; with commercial arrangement",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee A",
    "erg_or_eag_name": "ERG (not named)",
    "line_of_therapy": "second_line",
    "eligible_population": null,
    "methods_guide_era": "2022"
  },
  "interventions": [{
    "generic_name": "ozanimod",
    "brand_name": "Zeposia",
    "manufacturer": "Celgene (Bristol Myers Squibb)",
    "drug_class": "sphingosine 1-phosphate receptor modulator",
    "mechanism_of_action": "S1P receptor modulator; decreases circulating lymphocytes to reduce inflammation",
    "route_of_administration": "oral",
    "is_combination_regimen": false,
    "combination_components": null,
    "treatment_duration_type": "continuous",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "moderately to severely active ulcerative colitis",
    "therapeutic_area": ["gastroenterology"],
    "disease_setting": "chronic",
    "biomarker_defined_population": false,
    "biomarker_name": null
  }],
  "comparators": [
    {
      "comparator_name": "infliximab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "adalimumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "golimumab",
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
    }
  ],
  "clinical_trials": [{
    "trial_name": "TRUENORTH",
    "study_design": "RCT",
    "phase": "phase III",
    "blinding": "double_blind",
    "is_pivotal": true,
    "primary_outcome": "clinical remission at week 10 (induction) and week 52 (maintenance)",
    "sample_size": 1012,
    "crossover_occurred": false,
    "crossover_adjusted": null,
    "generalisability_concern": false
  }],
  "economic_model": {
    "model_type": "markov",
    "model_source": "company",
    "time_horizon": "lifetime",
    "cycle_length": "2 weeks",
    "health_states": ["remission", "response without remission", "active ulcerative colitis"]
  },
  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "NMA of 25 trials stratified by TNF-alpha inhibitor experience and treatment phase",
      "company_position": "Random effects ordinal model with probit link; assessed baseline placebo risk from representative UK trials",
      "erg_position": "Approach broadly appropriate but uncertainty about best source for baseline placebo risk",
      "committee_preference": "Revised NMA approach suboptimal for baseline placebo risk but overall appropriate for decision making",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "baseline_risk",
      "description": "Estimating baseline placebo risk in the NMA from single trials considered representative of UK practice",
      "company_position": "Used single UK-representative trials to estimate baseline placebo risk",
      "erg_position": "Uncertain whether most suitable evidence source was used",
      "committee_preference": "Suboptimal but accepted; company tried but failed to identify better sources",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Whether to split the analysis by TNF-alpha inhibitor experience",
      "company_position": "Divided population into TNF-naive and TNF-experienced subgroups",
      "erg_position": null,
      "committee_preference": "Agreed stratification by TNF-alpha inhibitor experience was appropriate",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "other",
      "description": "Best supportive care transition probabilities: whether TNF-experienced data should inform TNF-naive subgroup in post-active treatment phase",
      "company_position": "Used TNF-experienced data for TNF-naive subgroup (reasoning: patients in post-active phase have already had TNF)",
      "erg_position": "Subgroup-specific data should inform transition probabilities",
      "committee_preference": "Preferred subgroup-specific data; modest ICER difference",
      "impact_on_icer": "negligible"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trials comparing ozanimod with any active comparator"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "confidential",
    "comparison_pair": "ozanimod vs multiple comparators",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },
  "cross_references": []
}
```

### Schema stress points
- **Many comparators (6+)**: The ontology handles this fine via array, but the ICER band entity is awkward when there are 6+ pairwise comparisons, many confidential.
- **Conditional positioning**: Ozanimod is recommended ONLY IF infliximab not suitable (in TNF-naive) or after biologic failure. This conditional/hierarchical positioning is more complex than `restriction_details` captures. The recommendation is essentially "second-best after infliximab" in one subgroup and "one of several options" in another.
- **Induction + maintenance phases**: The model structure captures both induction and maintenance phases with different transition probabilities. The health_states array doesn't distinguish these phases. This is also seen in Crohn's disease models.
- **Treatment pathway complexity**: UC has highly individualised treatment with numerous sequencing options. The ontology captures comparators as a flat list but doesn't capture the tree structure of "if X fails, then Y or Z."

---

## 8. TA880 -- Tezepelumab for severe asthma (biologic add-on, 2023)

### Abbreviated extraction

```json
{
  "ta_number": "TA880",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Tezepelumab for treating severe asthma",
    "issue_date": "2023",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Add-on in severe asthma (12+), high-dose ICS + another maintenance treatment, with >=3 exacerbations/year or on maintenance OCS; stopping rule at 12 months (50% reduction); with commercial arrangement",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee A",
    "erg_or_eag_name": "EAG (not named)",
    "line_of_therapy": "any_line",
    "eligible_population": null,
    "methods_guide_era": "2022"
  },
  "interventions": [{
    "generic_name": "tezepelumab",
    "brand_name": "Tezspire",
    "manufacturer": "AstraZeneca",
    "drug_class": "anti-TSLP monoclonal antibody",
    "mechanism_of_action": "blocks thymic stromal lymphopoietin (TSLP); effective across asthma phenotypes regardless of biomarker profiles",
    "route_of_administration": "subcutaneous",
    "is_combination_regimen": false,
    "combination_components": null,
    "treatment_duration_type": "continuous",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "severe asthma inadequately controlled despite high-dose ICS plus another maintenance treatment",
    "therapeutic_area": ["respiratory"],
    "disease_setting": "chronic",
    "biomarker_defined_population": false,
    "biomarker_name": null
  }],
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
    },
    {
      "comparator_name": "omalizumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "NAVIGATOR",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "annualised asthma exacerbation rate at 52 weeks",
      "sample_size": 1059,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
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
      "trial_name": "SOURCE",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "percentage reduction in maintenance OCS dose",
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
    "health_states": ["controlled asthma", "uncontrolled asthma", "controlled asthma with exacerbation", "uncontrolled asthma with exacerbation", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "NMAs for multiple outcomes across biomarker-defined subpopulations; biomarkers in trials did not match NICE-recommended subpopulations",
      "company_position": "Series of NMAs comparing tezepelumab with other biologics in NICE-recommended subpopulations; updated base case uses eosinophil >=300 for anti-IL-5 comparisons",
      "erg_position": "NMA results uncertain; biomarker mismatches unresolvable; preferred eosinophil >=150 for dupilumab comparison",
      "committee_preference": "NMAs highly uncertain but company had explored uncertainty; tezepelumab likely similar effectiveness to other biologics",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Treatment response definition and 52-week stopping rule",
      "company_position": "Initially: any reduction = response; updated: 50% reduction in exacerbations (no mOCS) or 50% reduction in mOCS dose",
      "erg_position": "Company's original definition not clinically meaningful; 20-50% reduction appropriate",
      "committee_preference": "50% reduction appropriate; company's updated definition (50% exacerbation OR 50% mOCS) accepted as clinically meaningful",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "other",
      "description": "Asthma-related mortality: company's original estimates vs CPRD real-world data vs other sources",
      "company_position": "Original: deaths only through exacerbations; updated: CPRD-based multiplier for non-biologic eligible group",
      "erg_position": "CPRD analysis well done but applied too broadly; also, calibrating exacerbation mortality to all-cause mortality may overestimate",
      "committee_preference": "Company's original base-case mortality preferred; CPRD informative only for non-biologic eligible group as scenario",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "model_structure",
      "description": "Modelling exacerbations as controlled vs uncontrolled health states; transition restrictions",
      "company_position": "Prohibited transitions from controlled-to-uncontrolled-with-exacerbation and vice versa",
      "erg_position": "Inappropriate restriction; clinical opinion says exacerbations can happen from any state",
      "committee_preference": "Company's approach acceptable for decision making (consistent with previous appraisals)",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "other",
      "description": "ACQ-6 score cut-off for defining controlled vs uncontrolled asthma: 1.0 vs 1.5",
      "company_position": "1.5 cut-off (in line with previous NICE appraisals: dupilumab, benralizumab, reslizumab)",
      "erg_position": "Preferred 1.0 based on Juniper et al. study",
      "committee_preference": "1.5 cut-off appropriate (consistent with previous appraisals; Juniper study population included mild asthma)",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "utility_value_choice",
      "description": "Whether to apply additional utility increment for biological treatment above health-state utilities",
      "company_position": "Initially included biologic-specific utility gain; updated base case removed it after correcting regression error",
      "erg_position": "Additional utility increment not appropriate; treatment benefit should be reflected in health states",
      "committee_preference": "Agreed removal of additional utility gain was appropriate",
      "impact_on_icer": "increases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trial comparing tezepelumab with any existing biologic"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "tezepelumab vs other biologics (biologic-eligible subgroups)",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },
  "cross_references": []
}
```

### Schema stress points
- **Biomarker subgroup complexity**: The appraisal considers multiple overlapping subpopulations defined by biomarker eligibility for different existing treatments. The ontology captures `biomarker_defined_population` as boolean + name, but this TA has 5+ overlapping biomarker-defined subpopulations each with different comparators and ICERs.
- **Non-biologic-eligible population**: A key subgroup is people who CANNOT have existing biologics. This "defined-by-ineligibility" population is a novel concept not well captured.
- **Multiple ICER contexts**: ICERs differ across subpopulations (biologic-eligible vs non-biologic-eligible). The icer_band entity captures one comparison pair at a time, so multiple entries needed.
- **Precedent-based decisions**: Committee explicitly references previous appraisals (benralizumab, omalizumab) to justify modelling choices (ACQ-6 cut-off, transition structure). The cross_references relationship types don't include `precedent_for_modelling_choices`.
- **Asthma mortality source**: Recurrent "other" category -- same issue as TA671.

---

## 9. TA888 -- Risankizumab for Crohn's disease (biologic, sequential, 2023)

### Abbreviated extraction

```json
{
  "ta_number": "TA888",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Risankizumab for previously treated moderately to severely active Crohn's disease",
    "issue_date": "April 2023",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "After biological treatment failure/intolerance OR if TNF-alpha inhibitors unsuitable; use the least expensive if multiple suitable options; with commercial arrangement",
    "appraisal_type": "STA",
    "committee_name": "Evaluation Committee A",
    "erg_or_eag_name": "EAG (not named)",
    "line_of_therapy": "second_line",
    "eligible_population": null,
    "methods_guide_era": "2022"
  },
  "interventions": [{
    "generic_name": "risankizumab",
    "brand_name": "Skyrizi",
    "manufacturer": "AbbVie",
    "drug_class": "anti-IL-23 monoclonal antibody",
    "mechanism_of_action": "selectively binds interleukin-23 p19 subunit",
    "route_of_administration": "subcutaneous",
    "is_combination_regimen": false,
    "combination_components": null,
    "treatment_duration_type": "continuous",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "moderately to severely active Crohn's disease",
    "therapeutic_area": ["gastroenterology"],
    "disease_setting": "chronic",
    "biomarker_defined_population": false,
    "biomarker_name": null
  }],
  "comparators": [
    {
      "comparator_name": "adalimumab (including biosimilars)",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "infliximab (including biosimilars)",
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
      "comparator_name": "vedolizumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "ADVANCE",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "clinical remission (CDAI <150) and endoscopic response (SES-CD)",
      "sample_size": 931,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
    {
      "trial_name": "MOTIVATE",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "clinical remission and endoscopic response",
      "sample_size": 618,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
    {
      "trial_name": "FORTIFY",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "clinical remission and endoscopic response",
      "sample_size": 542,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],
  "economic_model": {
    "model_type": "decision_tree_plus_markov",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": ["remission (CDAI <150)", "mild disease (CDAI 150-220)", "moderate to severe disease (CDAI 220-600)", "surgery"]
  },
  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "NMA approach: split vs single network, fixed vs random effects, risk difference vs risk ratio, temporal effect adjustment",
      "company_position": "Split network (risankizumab+ustekinumab vs adalimumab+infliximab+vedolizumab); fixed effects; risk difference",
      "erg_position": "Single network preferred; random effects preferred; temporal effect adjustment needed; risk ratios more informative",
      "committee_preference": "EAG approach preferred (single network, random effects, temporal adjustment, risk ratios); relative effectiveness highly uncertain with either approach",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "other",
      "description": "Clinical equivalence assumption: whether evidence sufficient to support cost-comparison approach",
      "company_position": "Updated NMAs show similar effectiveness; cost comparison appropriate",
      "erg_position": "NMAs do not support equivalent effectiveness; point estimates for adalimumab, infliximab, ustekinumab below 1 (favouring comparator) vs risankizumab",
      "committee_preference": "Only enough certainty that risankizumab has at least equivalent benefits to vedolizumab; not confident of equivalence to TNF-alpha inhibitors or ustekinumab",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "model_structure",
      "description": "Cost-utility model does not reflect treatment pathway: assumes only 1 biologic then conventional care",
      "company_position": "Structure consistent with previous NICE Crohn's appraisals",
      "erg_position": "Does not reflect current clinical pathway (multiple sequential biologics used)",
      "committee_preference": "Model not suitable for decision making because it does not allow multiple biological treatments; EAG's 20-year treatment duration more appropriate than company's 1-year",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Treatment duration: 1-year (company), 20-year (EAG), or 10-year (cost-comparison model)",
      "company_position": "1-year maximum treatment duration (consistent with previous Crohn's appraisals)",
      "erg_position": "20-year duration more reflective of clinical practice; 1-year does not reflect lifelong nature of disease",
      "committee_preference": "1-year too short; 20-year more appropriate for cost-utility; in cost-comparison, 10-year used but shorter may be appropriate",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Dose escalation assumptions: proportion of patients on high-dose maintenance for various comparators",
      "company_position": "50% adalimumab, 40% infliximab, 92.5% ustekinumab, 30% IV vedolizumab on high dose",
      "erg_position": null,
      "committee_preference": "Assumptions were similar to clinical practice observations",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "cost_assumption",
      "description": "IV vs SC administration split: 50% IV and 50% SC for infliximab and vedolizumab",
      "company_position": "50/50 split",
      "erg_position": null,
      "committee_preference": "Accepted as reflecting clinical practice",
      "impact_on_icer": "negligible"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trial comparing risankizumab with any biologic comparator"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "confidential",
    "comparison_pair": "risankizumab vs vedolizumab (cost-comparison, cost-saving)",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate"
  },
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
      "referenced_ta": "TA187",
      "relationship": "same_condition",
      "context": "Previous NICE guidance on infliximab and adalimumab for Crohn's disease"
    }
  ]
}
```

### Schema stress points
- **Cost-comparison as primary analysis**: The committee rejected the cost-utility model entirely and based its decision on a cost-comparison model. The ontology has no clean way to capture this -- the model_type and icer_band structures assume cost-utility analysis.
- **Model rejection**: The committee explicitly stated the cost-utility model was "not suitable for decision making". The ontology has no field for capturing model rejection.
- **Sequential biologic treatment**: The fundamental critique of the cost-utility model was that it did not allow sequential biological treatments. This is a treatment_sequencing issue but deeper than the current category describes -- it's about whether the model structure can capture the real-world treatment pathway.
- **Temporal effect in NMA**: The committee required adjustment for a temporal effect in placebo remission rates across trials. This is a distinct NMA methodology issue not captured by existing categories.
- **Evaluation Committee vs Appraisal Committee**: By 2023, NICE uses "Evaluation Committee" terminology. The ontology notes this in design_notes but extraction should capture the raw term.

---

## 10. TA898 -- Dabrafenib + Trametinib for BRAF+ NSCLC (biomarker, combo, 2023)

### Abbreviated extraction

```json
{
  "ta_number": "TA898",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Dabrafenib plus trametinib for treating BRAF V600 mutation-positive advanced non-small-cell lung cancer",
    "issue_date": "May 2023",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "First-line treatment of advanced stage only; with commercial arrangement",
    "appraisal_type": "STA",
    "committee_name": "Evaluation Committee D",
    "erg_or_eag_name": "EAG (not named)",
    "line_of_therapy": "first_line",
    "eligible_population": "Very small (~1-3% of lung cancers have BRAF; ~half are V600)",
    "methods_guide_era": "2022"
  },
  "interventions": [{
    "generic_name": "dabrafenib plus trametinib",
    "brand_name": "Tafinlar + Mekinist",
    "manufacturer": "Novartis",
    "drug_class": "BRAF inhibitor + MEK inhibitor",
    "mechanism_of_action": "BRAF V600 kinase inhibitor + MEK1/MEK2 inhibitor combination",
    "route_of_administration": "oral",
    "is_combination_regimen": true,
    "combination_components": ["dabrafenib", "trametinib"],
    "treatment_duration_type": "treat_to_progression",
    "biosimilar_available": false
  }],
  "conditions": [{
    "condition_name": "BRAF V600 mutation-positive advanced non-small-cell lung cancer",
    "therapeutic_area": ["oncology"],
    "disease_setting": "metastatic",
    "biomarker_defined_population": true,
    "biomarker_name": "BRAF V600 mutation"
  }],
  "comparators": [{
    "comparator_name": "pembrolizumab plus platinum chemotherapy",
    "comparator_type": "active_drug",
    "is_established_practice": true,
    "committee_preferred": true
  }],
  "clinical_trials": [{
    "trial_name": "BRF113928",
    "study_design": "single_arm",
    "phase": null,
    "blinding": null,
    "is_pivotal": true,
    "primary_outcome": "overall response rate",
    "sample_size": 36,
    "crossover_occurred": false,
    "crossover_adjusted": null,
    "generalisability_concern": true
  }],
  "economic_model": {
    "model_type": "partitioned_survival",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": ["progression free", "progressed disease", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "Matching-adjusted indirect comparison (MAIC) with KEYNOTE-189 for comparator arm, with single-arm trial for intervention",
      "company_position": "MAIC adjusting BRF113928 (n=36) to match KEYNOTE-189 population; presented multiple evidence sources (FLATIRON, clinical equivalence assumption, KEYNOTE-189 naive comparison)",
      "erg_position": "MAIC results uncertain due to small sample size, unanchored comparison, and lack of common comparator; presented 2 base cases (MAIC and naive comparison)",
      "committee_preference": "MAIC accepted as preferred despite limitations; sensitivity MAIC (fewer covariates, larger effective sample) preferred over base-case MAIC",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "other",
      "description": "Evidence source for comparator arm: FLATIRON real-world database vs KEYNOTE-189 RCT vs clinical equivalence assumption",
      "company_position": "Explored multiple sources; FLATIRON subpopulation small with limited follow-up",
      "erg_position": "KEYNOTE-189 more appropriate than FLATIRON despite not being BRAF-specific population",
      "committee_preference": "KEYNOTE-189 preferred as evidence source; BRAF mutation not strong prognostic factor for immunotherapy outcomes",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "other",
      "description": "Prognostic value of BRAF V600 mutation status for immunotherapy outcomes",
      "company_position": "Did not provide strong evidence either way",
      "erg_position": null,
      "committee_preference": "No strong evidence BRAF is a strong prognostic factor; mixed evidence",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "utility_value_choice",
      "description": "Disutility for intravenous infusion (for pembrolizumab comparator)",
      "company_position": "Applied 0.023 per cycle decrement for IV infusion; later modified to apply only in infusion cycles",
      "erg_position": "Decrement too high (double that for pneumonia hospitalisation); not from EQ-5D; should be removed or reduced",
      "committee_preference": "Preferred not to include explicit IV disutility in base case; noted as potential uncaptured benefit of oral therapy qualitatively",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Whether to include BRAF V600 mutation testing costs in model",
      "company_position": "Not included: test is routine practice",
      "erg_position": "Questioned whether routine without NICE recommendation",
      "committee_preference": "Agreed testing is routine and costs should not be included (per NICE methodology)",
      "impact_on_icer": "negligible"
    },
    {
      "decision_category": "discount_rate",
      "description": "Discrete annual discounting vs continuous discounting from model outset",
      "company_position": "Discrete discounting from start of year 2",
      "erg_position": "Continuous discounting from outset (more frequently used in prior NICE models)",
      "committee_preference": "Continuous discounting preferred; small impact on results",
      "impact_on_icer": "negligible"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No RCT comparing dabrafenib+trametinib with pembrolizumab+chemotherapy in BRAF V600+ NSCLC"
    },
    {
      "gap_type": "other",
      "description": "Very small single-arm trial (n=36 first-line); no cost-effectiveness evidence for second-line use"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "confidential",
    "comparison_pair": "dabrafenib+trametinib vs pembrolizumab+chemo",
    "is_committee_preferred": true,
    "uncertainty_level": "high"
  },
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
      "referenced_ta": "TA789",
      "relationship": "precedent",
      "context": "Tepotinib MAIC covariates used as precedent for MAIC methodology"
    },
    {
      "referenced_ta": "TA653",
      "relationship": "precedent",
      "context": "Osimertinib MAIC covariates used as precedent"
    },
    {
      "referenced_ta": "TA628",
      "relationship": "precedent",
      "context": "Lorlatinib MAIC covariates used as precedent"
    }
  ]
}
```

### Schema stress points
- **Single-arm trial as primary evidence**: The ontology's ClinicalTrial entity handles this well with `study_design: "single_arm"`, but the very small sample size (n=36) and the decision to use MAIC with an external control represent a distinct evidence paradigm.
- **COVID-19 interim access**: Dabrafenib+trametinib was available during COVID-19 as interim treatment. This is a regulatory/access pathway not captured in the ontology.
- **Unanchored MAIC**: A specific type of indirect comparison that assumes all effect modifiers identified. The `indirect_comparison_method` category captures this but "unanchored MAIC" is methodologically distinct from standard NMA and should perhaps be a separate value.
- **Oral vs IV preference**: The committee considered IV disutility qualitatively but not quantitatively. This treatment preference/convenience factor is increasingly important in NICE decisions but has no dedicated place in the ontology.
- **Route of administration as methodological dispute**: The decision about whether to model IV disutility is a utility_value_choice issue but also touches on broader mode-of-administration preferences. This cross-cuts multiple categories.
- **Biomarker testing costs**: Whether companion diagnostic testing costs should be included is a recurring question in biomarker-defined populations. Used `cost_assumption` but this is common enough to warrant recognition.

---

## COMPREHENSIVE CRITIQUE

### A. Decision Categories Assessment

#### Categories that worked well across all 10 TAs

1. **crossover_adjustment** -- Extensively tested in TA432, TA488, TA512. The category cleanly captures the IPCW vs RPSFT debate which is one of the most common methodological disputes in oncology. Performed well.

2. **survival_extrapolation** -- Tested in TA432, TA488. Choice of parametric distribution (Weibull vs log-logistic etc.) is a recurrent, well-defined decision. The category works.

3. **comparator_selection** -- Tested heavily in TA187, TA432, TA512, TA828. Works well for capturing which comparator is relevant. However, the distinction between "which comparator to compare against" and "the structure of comparisons" (head-to-head vs network) bleeds into `indirect_comparison_method`.

4. **indirect_comparison_method** -- Heavily used in TA512, TA563, TA828, TA880, TA888, TA898. Works well. The category captures NMA, MAIC, and ITC disputes. However, it's becoming overloaded: the category must hold NMA methodology choices (fixed vs random effects, risk ratio vs risk difference, temporal adjustment), MAIC methodology (anchored vs unanchored, covariate selection), and fractional polynomial choices. These are very different types of decisions.

5. **stopping_rule** -- Tested in TA187, TA671, TA880, TA888. Works well for treatment duration caps and response-based continuation criteria.

6. **cost_assumption** -- Heavily used across all TAs. Works as a catch-all for drug costs, dose intensity, administration routes, testing costs. But its breadth reduces its analytical value.

#### Categories that were underused or not needed

1. **treatment_effect_waning** -- Not triggered in any of these 10 TAs. This is surprising; it may be more relevant to curative-intent / immunotherapy TAs.

2. **cure_assumption** -- Not triggered. Expected for haematology/CAR-T, not in this round's selection.

3. **carer_utility** -- Not triggered. Expected for paediatric/dementia TAs.

4. **proportional_hazards** -- Only triggered in TA512. Often a sub-issue within indirect_comparison_method rather than a standalone decision.

#### Categories that were stretched or used as "other"

The `other` category was used 11 times across 10 TAs. This is too frequent -- it indicates systematic gaps. Here are the recurring patterns:

1. **Background/general population mortality** (TA488, TA671, TA880): Whether and how to include non-disease-specific mortality. Used in at least 3 TAs.
   - **Proposed new category: `mortality_assumption`**
   - Definition: "Disputes about disease-specific vs all-cause mortality rates, background mortality adjustments, or data sources for mortality estimation."

2. **Clinical equivalence / class effect assumption** (TA563, TA888): Whether drugs can be assumed clinically equivalent to justify cost-comparison.
   - **Proposed new category: `equivalence_assumption`**
   - Definition: "Whether the technology and its comparator(s) can be assumed to have equivalent clinical effectiveness, justifying a cost-comparison approach."

3. **Evidence source for comparator arm** (TA898): When there's no head-to-head trial and the comparator's effectiveness must come from external data sources (different trial, real-world database, assumption of equivalence).
   - This partly overlaps with `indirect_comparison_method` but is distinct: it's about which data to use, not which statistical method to apply. Could be folded into a broadened `indirect_comparison_method` definition or kept as a sub-issue.

4. **Asthma control status cut-off** (TA880): A disease-specific threshold that defines health states in the model. This is a `model_structure` sub-issue.

5. **Temporal effect adjustment in NMA** (TA888): A methodological refinement specific to networks where placebo rates change over time. This is an `indirect_comparison_method` sub-issue.

6. **Prognostic value of biomarker** (TA898): Whether a biomarker (BRAF V600) is prognostic for treatment outcomes. This is a `population_generalisability` sub-issue.

#### Summary of proposed new categories

| New category | Occurrences in round 3 | Definition |
|---|---|---|
| `mortality_assumption` | 3 (TA488, TA671, TA880) | Disputes about mortality data source, background mortality adjustments, or disease-specific vs all-cause mortality |
| `equivalence_assumption` | 2 (TA563, TA888) | Whether clinical equivalence between treatments can be assumed, justifying cost-comparison |

Two proposed categories. Both are recurring and analytically important.

### B. Structural Schema Issues

#### 1. ICER directionality: South-west quadrant

TA512 (tivozanib) is cheaper but less effective than comparators. The ICER is in the "south-west quadrant" -- savings per QALY lost. The icer_band framework implicitly assumes the north-east quadrant (cost per QALY gained). A `direction` field is needed:

```json
"icer_band": {
  "band": "...",
  "direction": "incremental | decremental",
  ...
}
```

Where `decremental` means "cost saving per QALY lost" (the acceptability logic is reversed).

#### 2. Cost-comparison analysis

TAs 563 and 888 both used cost-comparison as the primary analysis (not cost-utility). The ontology needs:
- A `model_type` enum value: `cost_comparison`
- Or a separate field `analysis_approach` with values `cost_utility`, `cost_comparison`, `cost_minimisation`

This is distinct from model_type (which describes the simulation structure) -- a cost-comparison analysis doesn't necessarily use a Markov or PSM.

#### 3. CDF reconsideration

TA432 is a CDF reconsideration. The cross_ta relationship needs a new reason value: `cdf_reconsideration`. The existing `SUPERSEDES` relationship doesn't capture that the same drug/indication was re-evaluated under new commercial terms.

#### 4. Multi-model situations

TA187 had three separate economic models (from two companies + the assessment group) plus a DSU reconciliation. The `model_source` field cannot capture this. Options:
- Make `model_source` an array
- Add a `model_reconciliation` boolean/description field
- Accept that `model_source: "multiple"` is sufficient

#### 5. Treatment pathway / conditional positioning

TA828 (ozanimod) has a recommendation that is conditional on infliximab not being suitable. The ontology captures `restriction_details` as freetext, which works but is not queryable. For cross-TA analysis of treatment positioning, a structured field like `positioning_constraints` would help:

```json
"positioning_constraints": [
  {"condition": "infliximab_not_suitable", "population": "TNF-naive"},
  {"condition": "biologic_failure", "population": "TNF-experienced"}
]
```

This is complex to generalise, however, and may be better left as freetext.

#### 6. Induction + maintenance phases

TAs 828, 888, and 880 all have models with distinct induction and maintenance phases. The `health_states` field does not capture this phase structure. A `model_phases` array could help:

```json
"model_phases": ["induction", "maintenance"]
```

But this may be over-engineering for the extraction use case.

### C. Consistency of Category Usage

The following categories showed inconsistent usage across TAs:

1. **baseline_risk vs model_structure**: In TA187, the dispute about relapse rates was categorised as `baseline_risk`. In TA828, the dispute about baseline placebo risk in the NMA was also `baseline_risk`. But the TA880 dispute about mortality estimates was categorised as `other`. These are conceptually related (what background/natural history rates to use) but were categorised differently. The proposed `mortality_assumption` category would help.

2. **comparator_selection vs treatment_sequencing**: In TA512, the question of subsequent therapy costs (without benefits) was categorised as `treatment_sequencing`. In TA828, the question of which comparator is relevant at each pathway position was categorised as `comparator_selection`. There's a genuine continuum here -- choosing which comparators to include overlaps with modelling subsequent treatment. The distinction should be:
   - `comparator_selection`: Which drugs to compare the intervention against head-to-head
   - `treatment_sequencing`: How subsequent treatments after the index treatment are modelled (including costs and benefits)

3. **cost_assumption**: Used for very different things -- drug costs (TA187), dose intensity (TA512), testing costs (TA898), dose escalation (TA888), IV vs SC split (TA888). The category is too broad. However, splitting it further (e.g. `dose_intensity`, `testing_costs`, `administration_costs`) would create too many categories for the marginal gain.

### D. What Would Haiku Struggle With?

Based on this round's documents, here are specific challenges for a smaller model:

1. **TA187 (multi-model reconciliation)**: The three-model situation with DSU reconciliation requires understanding that the committee could not pick a "best" model but used the collective evidence. Haiku may try to extract a single model structure and miss the meta-level decision.

2. **TA512 (reversed ICER)**: The "less costly, less effective" ICER with reversed decision logic is conceptually non-obvious. Haiku may not flag the directionality and may mis-categorise the ICER band.

3. **TA563 (class effect leading to cost-comparison)**: The chain of reasoning -- NMA shows no difference -> class effect assumed -> cost-comparison preferred over full CEA -- requires multi-step inference. Haiku may extract the NMA result and the cost-comparison result separately without linking them.

4. **TA880 (biomarker subgroup complexity)**: The multiple overlapping subpopulations (biologic-eligible, non-biologic-eligible, eosinophil >=300, >=150, FeNO+, etc.) with different comparators and ICERs for each would be challenging. Haiku may conflate subgroup results.

5. **TA888 (model rejection)**: The committee rejected the primary economic model and based its decision on a secondary cost-comparison model. Haiku may extract from the rejected model and present those results as the committee's preferred analysis.

6. **TA898 (multiple evidence sources for single comparison)**: Four different evidence sources for the comparator (FLATIRON, KEYNOTE-189, clinical equivalence, MAIC) with the committee preferring one. Haiku may struggle to track which source the committee ultimately selected.

7. **TA671 (wrong document)**: The FAD.md file contains only the equality impact assessment. Haiku might not recognise that it lacks the substantive content and may try to extract from the equality form, producing a mostly-null extraction.

8. **General: confidential results**: Many TAs (TA828, TA880, TA888, TA898) redact key results. Haiku needs to correctly set fields to `confidential` rather than guessing or leaving null.

### E. Specific Proposed Changes for v0.4.0

#### New decision_categories (add 2)

```json
"mortality_assumption",
"equivalence_assumption"
```

Definitions:

| Category | When to use |
|---|---|
| mortality_assumption | Disputes about disease-specific vs all-cause mortality, background mortality adjustments, mortality data sources, or age-specific mortality rates |
| equivalence_assumption | Whether the technology and its comparator(s) can be assumed clinically equivalent, justifying cost-comparison or cost-minimisation analysis |

#### New model_type values (add 1)

```json
"cost_comparison"
```

This reflects the increasingly common situation where the committee rejects a full cost-utility analysis and uses a cost-comparison approach.

#### New icer_band field

```json
"direction": "incremental | decremental"
```

Where `incremental` = standard (more costly, more effective), `decremental` = south-west quadrant (less costly, less effective). Default: `incremental`.

#### New cross_ta relationship reasons (add 1)

Add `cdf_reconsideration` to the existing list:
```json
"REFERENCES": "... reason: precedent, utility_reuse, comparator_guidance, same_condition, same_drug, cdf_reconsideration"
```

Or use `SUPERSEDES` with a qualifier. Either way, the CDF reconsideration pattern needs representation.

#### New gap_type (add 1)

```json
"single_arm_evidence_only"
```

For situations like TA898 where the only evidence for the intervention comes from a single-arm trial with no randomised comparator.

#### Minor additions

- `treatment_duration_type` enum: add `planned_course` for TA187-style fixed-period-then-reassess treatment.
- Consider adding `model_rejected` boolean to EconomicModel entity for TA888-style situations.
- Consider `analysis_approach` field: `cost_utility | cost_comparison | cost_minimisation` as distinct from model_type.

### F. Summary Table

| TA | Key stress test | Schema adequate? | Changes needed? |
|---|---|---|---|
| TA187 | Multi-drug MTA, multi-model, planned course treatment | Partial | planned_course enum, multi-model representation |
| TA432 | CDF reconsideration, changed pathway | Partial | cdf_reconsideration relationship |
| TA488 | End-of-life, recensoring, background mortality | Good | mortality_assumption category |
| TA512 | Reversed ICER, implausible NMA, subsequent therapy costs/benefits | Poor | ICER direction field critical |
| TA563 | Class effect, cost-comparison, novel model structure | Poor | equivalence_assumption category, cost_comparison model_type |
| TA671 | Incomplete data file | N/A (data issue) | -- |
| TA828 | 6+ comparators, conditional positioning, induction/maintenance | Good | Minor: positioning constraints |
| TA880 | Biomarker subgroups, multiple biologics, mortality source | Good | mortality_assumption category |
| TA888 | Model rejection, cost-comparison, sequential biologics | Poor | cost_comparison type, model_rejected flag |
| TA898 | Single-arm trial, MAIC, biomarker testing costs, oral vs IV | Partial | single_arm_evidence_only gap type |

### G. Convergence Assessment

The ontology is maturing well. Rounds 1 and 2 added foundational entity types and decision categories. This round identified:
- 2 new decision categories needed (down from 4 in round 1 and 2 in round 2)
- 1 critical structural addition (ICER direction)
- 2 important but non-blocking additions (cost_comparison model_type, equivalence_assumption)
- Several minor enum additions

The rate of new issues is declining. The main remaining gaps are in handling:
1. Non-standard analysis approaches (cost-comparison, cost-minimisation)
2. Complex treatment pathway structures (sequential biologics, conditional positioning)
3. The increasing prevalence of indirect comparisons via MAIC (not just NMA)

These are addressable with the proposed v0.4.0 changes. A round 4 focused on HSTs and devices would test the remaining untested corners of the schema.
