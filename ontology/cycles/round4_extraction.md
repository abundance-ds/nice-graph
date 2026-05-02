# Round 4 Extraction Test: Edge Cases (Pre-2010, Devices, JAK Inhibitors, CAR-T, Dermatology)

Ontology version: 0.4.0
Tested against: 10 FADs spanning 2002--2024
Tester: Claude Opus 4.6 (round 4 refinement cycle)
Focus: Very old document formats (2002-2005), non-pharma technologies (ECT, pacemakers), early targeted therapies, JAK inhibitors, CAR-T cell therapy, novel indications (dermatology/migraine prevention)

---

## 1. TA59 -- Electroconvulsive therapy (ECT, 2002 -- non-drug, psychiatric)

### Abbreviated extraction

```json
{
  "ta_number": "TA59",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Electroconvulsive therapy",
    "issue_date": "November 2002",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Recommended only to achieve rapid and short-term improvement of severe symptoms after adequate trial of other treatment options has proven ineffective and/or when condition is potentially life-threatening, in individuals with severe depressive illness, catatonia, or prolonged/severe manic episode. Not recommended as maintenance therapy in depressive illness. Not recommended for general management of schizophrenia.",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "School of Health and Related Research, University of Sheffield and Nuffield Institute for Health, University of Leeds",
    "line_of_therapy": null,
    "eligible_population": null,
    "methods_guide_era": "pre_2008"
  },
  "interventions": [
    {
      "generic_name": "electroconvulsive therapy",
      "brand_name": null,
      "manufacturer": null,
      "drug_class": null,
      "mechanism_of_action": "electric current induces generalised seizure activity; mechanism not fully understood",
      "route_of_administration": "other",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "cyclical",
      "biosimilar_available": null
    }
  ],
  "conditions": [
    {
      "condition_name": "severe depressive illness",
      "therapeutic_area": ["neurology_psychiatry"],
      "disease_setting": "acute",
      "biomarker_defined_population": false,
      "biomarker_name": null
    },
    {
      "condition_name": "catatonia",
      "therapeutic_area": ["neurology_psychiatry"],
      "disease_setting": "acute",
      "biomarker_defined_population": false,
      "biomarker_name": null
    },
    {
      "condition_name": "prolonged or severe manic episode",
      "therapeutic_area": ["neurology_psychiatry"],
      "disease_setting": "acute",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],
  "comparators": [
    {
      "comparator_name": "antidepressants / pharmacotherapy",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": null
    },
    {
      "comparator_name": "sham ECT",
      "comparator_type": "placebo",
      "is_established_practice": false,
      "committee_preferred": null
    }
  ],
  "clinical_trials": [],
  "economic_model": {
    "model_type": "decision_tree",
    "model_source": "Assessment Group",
    "time_horizon": "1 year",
    "cycle_length": null,
    "health_states": null
  },
  "methodological_decisions": [],
  "evidence_gaps": [
    {
      "gap_type": "short_follow_up",
      "description": "No clear evidence on longer-term benefits and risks of ECT. Evidence on cognitive impairment may be prolonged or permanent."
    },
    {
      "gap_type": "missing_quality_of_life_data",
      "description": "No study adequately captured users' views or quality of life. RCT outcome scales did not adequately capture experience of cognitive impairment."
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },
  "icer_band": {
    "band": "not_estimable",
    "comparison_pair": "ECT vs pharmacotherapy",
    "is_committee_preferred": true,
    "uncertainty_level": "very_high"
  },
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
      "referenced_ta": "TA43",
      "relationship": "same_condition",
      "context": "Guidance on newer (atypical) antipsychotic drugs for schizophrenia"
    },
    {
      "referenced_ta": "TA51",
      "relationship": "same_condition",
      "context": "Guidance on computerised cognitive behavioural therapy for anxiety and depression"
    }
  ]
}
```

### Extraction issues

1. **Non-drug intervention**: ECT does not fit `drug_class`, `mechanism_of_action`, `route_of_administration`, `biosimilar_available`, or `manufacturer`. The schema's `Intervention` entity is described as "drug, device, cell therapy, or digital health technology" -- ECT is arguably a procedure/device. Fields like `drug_class` and `biosimilar_available` are meaningless here. **ISSUE: Schema assumes pharmaceutical-like interventions.**
2. **No manufacturer / no commercial arrangement**: ECT has no manufacturer submission, no PAS, no drug cost per se -- the cost is procedural (£2475 for 6 sessions). The `CommercialArrangement` entity and price-related fields are irrelevant.
3. **Multiple conditions**: ECT is appraised across 4 conditions (depression, schizophrenia, catatonia, mania) with different recommendation outcomes per condition. The schema handles multi-condition via array, but cannot represent "recommended for condition A, not recommended for condition B" cleanly. `restriction_details` as free text handles this, but downstream querying is limited.
4. **Ethical/consent focus**: A large portion of the FAD addresses consent, Mental Health Act, advance directives -- none of which map to any schema entity. These are unique to psychiatric/involuntary treatment contexts.
5. **No named trials**: The evidence synthesis reviewed 119 RCTs via systematic review but named none. `ClinicalTrial` entity cannot capture "systematic review of N=119 RCTs".
6. **ICER**: The committee concluded ECT and pharmacotherapy are "equally cost effective" with "no consistent differences" -- the `not_estimable` band is the closest fit but not perfectly accurate. A new band `equivalent` or `comparable` might be useful.
7. **Pre-2008 format**: No numbered section 3 "Committee discussion" structure. Instead uses "4 Evidence and interpretation" with subsections. Still extractable.

---

## 2. TA64 -- Growth hormone (somatropin) in adults (2003 -- endocrine, long-term)

### Abbreviated extraction

```json
{
  "ta_number": "TA64",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Human growth hormone (somatropin) in adults with growth hormone deficiency",
    "issue_date": "April 2003",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Recommended only if: (1) severe GH deficiency (peak GH <9 mU/litre on ITT), (2) QoL-AGHDA score >=11, and (3) receiving treatment for other pituitary hormone deficiencies. Must be reassessed at 9 months; discontinued if QoL improvement <7 points. Childhood-onset patients should stop GH at completion of linear growth, re-test, and restart only if biochemically deficient until peak bone mass (~25 years).",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "Southampton Health Technology Assessment Centre / School of Health and Related Research (ScHARR), University of Sheffield",
    "line_of_therapy": null,
    "eligible_population": "~12,600 adults with GH deficiency in England and Wales; ~1,180 estimated eligible for continuous treatment",
    "methods_guide_era": "pre_2008"
  },
  "interventions": [
    {
      "generic_name": "somatropin",
      "brand_name": "Genotropin / Humatrope / Norditropin / Saizen",
      "manufacturer": "Pharmacia / Lilly / Novo Nordisk / Serono",
      "drug_class": "recombinant human growth hormone",
      "mechanism_of_action": "replacement of deficient growth hormone",
      "route_of_administration": "subcutaneous",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "continuous",
      "biosimilar_available": false
    }
  ],
  "conditions": [
    {
      "condition_name": "adult growth hormone deficiency",
      "therapeutic_area": ["metabolic_endocrine"],
      "disease_setting": "chronic",
      "biomarker_defined_population": true,
      "biomarker_name": "peak GH response <9 mU/litre on insulin tolerance test"
    }
  ],
  "comparators": [
    {
      "comparator_name": "no GH treatment",
      "comparator_type": "no_treatment",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [],
  "economic_model": {
    "model_type": "other",
    "model_source": "mixed (Assessment Group cost analysis + manufacturer submissions)",
    "time_horizon": "lifetime",
    "cycle_length": null,
    "health_states": null
  },
  "methodological_decisions": [
    {
      "decision_category": "utility_source",
      "description": "Which QoL instrument best captures the effect of GH treatment -- NHP, QoL-AGHDA, QLS-H, or EQ-5D",
      "company_position": "KIMS observational data using QoL-AGHDA with regression-mapped utilities",
      "erg_position": "RCT evidence insufficient to estimate utility gain; observational data overestimates treatment effect",
      "committee_preference": "QoL-AGHDA is the best available tool; minimum 7-point improvement needed for cost-effectiveness",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "subgroup_definition",
      "description": "Baseline QoL-AGHDA score threshold for identifying patients who benefit sufficiently",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "Baseline QoL-AGHDA score of at least 11 needed; improvement of at least 7 points required to justify cost-effectiveness",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Whether GH treatment should be continued indefinitely or reassessed",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "9-month trial period (3 months dose titration + 6 months therapeutic trial); discontinue if <7 point QoL-AGHDA improvement",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "mortality_assumption",
      "description": "Whether GH deficiency independently affects overall mortality beyond cardiovascular risk and bone mineral density",
      "company_position": "GH deficiency increases SMR; GH replacement may reduce mortality",
      "erg_position": "Observational SMR data not adjusted for confounders; causality unclear",
      "committee_preference": "Uncertain impact on mortality; best available evidence from observational studies already included in CE estimates",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "other",
      "description": "RCT evidence insufficient to prove QoL benefit of GH -- many studies poor quality, patients had relatively normal baseline QoL, and dosage regimens differed from current practice."
    },
    {
      "gap_type": "surrogate_not_validated",
      "description": "Relationship between GH deficiency, cardiovascular risk factors, bone mineral density, and mortality not clearly established."
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },
  "icer_band": {
    "band": "30k_to_50k",
    "comparison_pair": "somatropin vs no treatment",
    "is_committee_preferred": true,
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
  "cross_references": [
    {
      "referenced_ta": "TA42",
      "relationship": "same_drug",
      "context": "Guidance on human growth hormone in children with growth failure"
    }
  ]
}
```

### Extraction issues

1. **Multiple manufacturers / brands**: Four manufacturers making essentially the same product. The schema's `Intervention` entity with single `brand_name` / `manufacturer` fields does not cleanly handle MTA with 4 equivalent products. Workaround: concatenate with " / " but this is lossy.
2. **QoL-based stopping rule**: The recommendation hinges on a disease-specific QoL instrument score threshold (QoL-AGHDA >=11 to start, >=7 improvement to continue). This is a highly specific restriction type not seen in modern TAs. The `restriction_details` free text captures it, but there is no structured field for "QoL-instrument-based eligibility."
3. **Childhood-to-adult transition**: The guidance covers a transitional period (childhood-onset GH deficiency into adulthood) that is conceptually distinct from the adult-onset indication. The schema has `is_paediatric` flag but not a "transitional" concept.
4. **Cost analysis vs cost-effectiveness**: The Assessment Group explicitly stated they could not estimate utility gain from RCTs, so the Wessex report was a cost analysis only. The `EconomicModel` entity's `model_type` has no `cost_analysis` option. Used `other`.
5. **Pre-2008 document structure**: Extractable without difficulty.

---

## 3. TA75 -- Interferon alfa (pegylated and non-pegylated) and ribavirin for chronic hepatitis C (2004)

### Abbreviated extraction

```json
{
  "ta_number": "TA75",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Interferon alfa (pegylated and non-pegylated) and ribavirin for the treatment of chronic hepatitis C",
    "issue_date": "November 2003",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Peginterferon alfa + ribavirin combination recommended for moderate-to-severe CHC aged >=18. Genotype 2/3: treat 24 weeks. Genotype 1/4/5/6: treat 12 weeks then viral load test; continue to 48 weeks only if >=2-log viral load reduction. For ribavirin-intolerant: peginterferon monotherapy for 48 weeks with 12-week viral load test. Not recommended for prior peginterferon combination failures, <18 years, or post-transplant (experimental only).",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "Southampton Health Technology Assessment Centre (SHTAC)",
    "line_of_therapy": "first_line",
    "eligible_population": "~2000 treated per year; estimated prevalence 50,000-500,000",
    "methods_guide_era": "pre_2008"
  },
  "interventions": [
    {
      "generic_name": "peginterferon alfa-2a",
      "brand_name": "Pegasys",
      "manufacturer": "Roche Products Ltd",
      "drug_class": "pegylated interferon",
      "mechanism_of_action": "antiviral, alters host-cell metabolism",
      "route_of_administration": "subcutaneous",
      "is_combination_regimen": true,
      "combination_components": ["peginterferon alfa-2a", "ribavirin"],
      "treatment_duration_type": "fixed_duration",
      "biosimilar_available": false
    },
    {
      "generic_name": "peginterferon alfa-2b",
      "brand_name": "ViraferonPeg",
      "manufacturer": "Schering-Plough Ltd",
      "drug_class": "pegylated interferon",
      "mechanism_of_action": "antiviral, alters host-cell metabolism",
      "route_of_administration": "subcutaneous",
      "is_combination_regimen": true,
      "combination_components": ["peginterferon alfa-2b", "ribavirin"],
      "treatment_duration_type": "fixed_duration",
      "biosimilar_available": false
    }
  ],
  "conditions": [
    {
      "condition_name": "moderate to severe chronic hepatitis C",
      "therapeutic_area": ["infectious_disease"],
      "disease_setting": "chronic",
      "biomarker_defined_population": true,
      "biomarker_name": "HCV genotype (1, 2/3, 4/5/6)"
    }
  ],
  "comparators": [
    {
      "comparator_name": "interferon alfa + ribavirin combination therapy",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "interferon alfa monotherapy",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": false
    }
  ],
  "clinical_trials": [],
  "economic_model": {
    "model_type": "markov",
    "model_source": "Assessment Report",
    "time_horizon": "30 years",
    "cycle_length": null,
    "health_states": null
  },
  "methodological_decisions": [
    {
      "decision_category": "subgroup_definition",
      "description": "Whether treatment duration and monitoring should differ by HCV genotype",
      "company_position": null,
      "erg_position": "SVRs much lower for genotype 1 vs 2/3; genotype-differentiated treatment duration is cost-effective",
      "committee_preference": "Genotype 2/3: 24 weeks. Genotype 1/4/5/6: 12-week viral load test then conditional 48-week treatment.",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Whether 12-week viral load testing should be used to stop treatment early for non-responders",
      "company_position": null,
      "erg_position": "Non-responders at 12 weeks have <2% SVR chance; continuing costs ~£227,000/QALY",
      "committee_preference": "12-week viral load testing for genotype 1+ combination therapy and all monotherapy patients; stop if <2-log reduction",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "equivalence_assumption",
      "description": "Whether peginterferon alfa-2a and alfa-2b can be considered equivalent",
      "company_position": null,
      "erg_position": "No head-to-head trials; treatments may be different but pooled results similar",
      "committee_preference": "Insufficient evidence to recommend one over the other; both should be available",
      "impact_on_icer": "negligible"
    }
  ],
  "evidence_gaps": [],
  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "peginterferon alfa combination vs interferon alfa combination (genotype 1, 48 weeks)",
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
  "cross_references": [
    {
      "referenced_ta": "TA14",
      "relationship": "comparator_guidance",
      "context": "Previous NICE guidance on ribavirin and interferon alpha for hepatitis C (being superseded)"
    }
  ]
}
```

### Extraction issues

1. **Very long document** (41 pages): Dense clinical detail. The pre-2008 format includes extended sections on clinical need, trial results with percentages, and specific dosing guidance. Extraction is straightforward but the document is much longer than modern FADs.
2. **Genotype-stratified recommendations**: The recommendation differs by HCV genotype with different treatment durations. This is analogous to biomarker-defined subgroups but uses viral genotype rather than patient biomarker. The `biomarker_name` field is being stretched to cover "HCV genotype."
3. **Multiple ICER bands**: The document presents ICERs for many comparison pairs (genotype 1 vs 2/3, 24 vs 48 weeks, monotherapy vs combination). The schema allows `icer_band` as an array but the number of distinct ICERs in this TA is unusually high (8+ comparisons in Table 1 and Table 2). Only the most decision-relevant one is extracted.
4. **Supersedes prior guidance**: Explicit reference to TA14. The `SUPERSEDES` relation works well here.
5. **Re-treatment populations**: The document distinguishes first-treatment, monotherapy-failure re-treatment, and combination-failure re-treatment populations with different cost-effectiveness. The schema does not have a structured way to represent multiple treatment-history-defined populations within a single TA.

---

## 4. TA86 -- Imatinib for unresectable/metastatic GIST (2004 -- early targeted therapy)

### Abbreviated extraction

```json
{
  "ta_number": "TA86",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Imatinib for the treatment of unresectable and/or metastatic gastro-intestinal stromal tumours",
    "issue_date": "August 2004",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Imatinib 400 mg/day recommended as first-line for KIT (CD117)-positive unresectable/metastatic GIST. Continue only if response achieved within 12 weeks (SWOG criteria). Reassess every 12 weeks. Dose escalation NOT recommended for progressive disease.",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "West Midlands Health Technology Collaboration",
    "line_of_therapy": "first_line",
    "eligible_population": "80-240 new cases/year in England and Wales",
    "methods_guide_era": "pre_2008"
  },
  "interventions": [
    {
      "generic_name": "imatinib",
      "brand_name": "Glivec",
      "manufacturer": "Novartis",
      "drug_class": "tyrosine kinase inhibitor",
      "mechanism_of_action": "selectively inhibits c-KIT receptor tyrosine kinase to block uncontrolled cell proliferation",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "treat_to_progression",
      "biosimilar_available": false
    }
  ],
  "conditions": [
    {
      "condition_name": "KIT (CD117)-positive unresectable and/or metastatic gastro-intestinal stromal tumour",
      "therapeutic_area": ["oncology"],
      "disease_setting": "metastatic",
      "biomarker_defined_population": true,
      "biomarker_name": "KIT (CD117) positive"
    }
  ],
  "comparators": [
    {
      "comparator_name": "best supportive care",
      "comparator_type": "best_supportive_care",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "CSTI571-B2222",
      "study_design": "single_arm",
      "phase": "phase II",
      "blinding": null,
      "is_pivotal": true,
      "primary_outcome": "tumour response (SWOG criteria)",
      "sample_size": 147,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "NICE Decision Support Unit (DSU)",
    "time_horizon": "10 years",
    "cycle_length": null,
    "health_states": ["progressive disease", "responding to imatinib", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "model_structure",
      "description": "Whether patients should start in the responding or progressive health state in the model",
      "company_position": "All patients respond immediately to imatinib",
      "erg_position": "Overestimates benefit; modified model with both survival and time-to-failure curves",
      "committee_preference": "DSU model in which all patients begin in progressive phase is most appropriate",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "survival_extrapolation",
      "description": "Method of extrapolating trial and cohort data to 10-year time horizon",
      "company_position": "Exponential curves assuming constant hazard",
      "erg_position": null,
      "committee_preference": "DSU model not assuming constant hazard, using all available data, is most appropriate",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Whether imatinib dose should be escalated to 600 mg/day after progressive disease on 400 mg/day",
      "company_position": "Dose escalation may benefit some patients",
      "erg_position": "Limited evidence, short follow-up, not randomised",
      "committee_preference": "Dose escalation not cost effective; not recommended",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Which patients from the historical cohort study should be used as control group",
      "company_position": "Selected patients who never received imatinib",
      "erg_position": "All patients censored at time imatinib became available",
      "committee_preference": "Censored data least prone to bias and best estimate of untreated prognosis",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "single_arm_evidence_only",
      "description": "No RCTs comparing imatinib with best supportive care; pivotal study was uncontrolled phase II."
    },
    {
      "gap_type": "immature_overall_survival",
      "description": "Median survival not yet reached after 31 months follow-up."
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },
  "icer_band": {
    "band": "30k_to_50k",
    "comparison_pair": "imatinib 400 mg/day vs best supportive care",
    "is_committee_preferred": true,
    "uncertainty_level": "high",
    "direction": "incremental"
  },
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
      "referenced_ta": "TA70",
      "relationship": "same_drug",
      "context": "Guidance on imatinib for chronic myeloid leukaemia"
    }
  ]
}
```

### Extraction issues

1. **Historical controls instead of RCTs**: The cost-effectiveness analysis relies entirely on an unpublished historical cohort study for the comparator arm. The `ClinicalTrial` entity with `study_design` enum does not have a `historical_cohort` option. Used `single_arm` for the pivotal study but the comparator evidence is not extractable as a ClinicalTrial.
2. **DSU model**: The NICE Decision Support Unit developed a separate model, distinct from both the company and ERG models. This is unusual; `model_source` currently has company/ERG but "DSU" is a valid distinct source.
3. **Pre-CDF era**: Despite being oncology with uncertain OS data, the Cancer Drugs Fund did not exist in 2004. The recommendation went ahead on the basis of clinical need and plausible ICER. This contrasts with modern TAs where the same evidence profile would lead to CDF entry.
4. **Early targeted therapy**: One of the earliest TKI appraisals. The schema handles this well.

---

## 5. TA88 -- Dual-chamber pacemakers for symptomatic bradycardia (2005 -- device, non-pharma)

### Abbreviated extraction

```json
{
  "ta_number": "TA88",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Dual-chamber pacemakers for symptomatic bradycardia due to sick sinus syndrome and/or atrioventricular block",
    "issue_date": "October 2004",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Dual-chamber pacing recommended for symptomatic bradycardia due to SSS, AVB, or combination, except: (1) SSS without impaired AV conduction (use single-chamber atrial pacing), (2) AVB with continuous atrial fibrillation (use single-chamber ventricular pacing), (3) AVB when patient-specific factors favour single-chamber ventricular pacing.",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "Peninsula Technology Assessment Group",
    "line_of_therapy": null,
    "eligible_population": "~26,000 pacemakers implanted/year in UK; ~60% dual-chamber in 2003",
    "methods_guide_era": "pre_2008"
  },
  "interventions": [
    {
      "generic_name": "dual-chamber pacemaker (DDD/DDDR)",
      "brand_name": null,
      "manufacturer": "Biotronik / ELA Medical / Guidant / Medtronic / Sorin Biomedica / St Jude Medical",
      "drug_class": null,
      "mechanism_of_action": "electrical stimulation of both right atrium and ventricle to maintain AV synchrony",
      "route_of_administration": "implanted",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "continuous",
      "biosimilar_available": null
    }
  ],
  "conditions": [
    {
      "condition_name": "symptomatic bradycardia due to sick sinus syndrome and/or atrioventricular block",
      "therapeutic_area": ["cardiovascular"],
      "disease_setting": "chronic",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],
  "comparators": [
    {
      "comparator_name": "single-chamber ventricular pacemaker (VVI/VVIR)",
      "comparator_type": "same_drug_different_regimen",
      "is_established_practice": true,
      "committee_preferred": false
    },
    {
      "comparator_name": "single-chamber atrial pacemaker (AAI/AAIR)",
      "comparator_type": "same_drug_different_regimen",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "MOST",
      "study_design": "RCT",
      "phase": null,
      "blinding": null,
      "is_pivotal": true,
      "primary_outcome": "mortality, stroke, atrial fibrillation, quality of life",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    },
    {
      "trial_name": "CTOPP",
      "study_design": "RCT",
      "phase": null,
      "is_pivotal": true,
      "primary_outcome": "mortality, stroke, atrial fibrillation",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    },
    {
      "trial_name": "PASE",
      "study_design": "RCT",
      "phase": null,
      "is_pivotal": true,
      "primary_outcome": "quality of life",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
    {
      "trial_name": "UKPACE",
      "study_design": "RCT",
      "phase": null,
      "is_pivotal": true,
      "primary_outcome": "mortality, atrial fibrillation, QoL",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "Assessment Group",
    "time_horizon": "10 years",
    "cycle_length": "1 month",
    "health_states": ["post-operative complications", "well with pacemaker", "atrial fibrillation", "heart failure", "stroke", "mild pacemaker syndrome", "severe pacemaker syndrome", "generator expiry", "upgrade to dual-chamber", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "utility_value_choice",
      "description": "Disutility associated with mild pacemaker syndrome, which is a key driver of cost-effectiveness",
      "company_position": null,
      "erg_position": "Mild pacemaker syndrome utility 0.80 (not resolving) vs 0.925 for well-with-pacemaker",
      "committee_preference": "Disutility may be overestimated; but dual-chamber pacing is cost-effective even with conservative assumptions",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Whether to use market price (discounted) or list price for pacemaker devices",
      "company_position": "Market price (lower)",
      "erg_position": "Used UKPACE survey aggregate acquisition costs",
      "committee_preference": "Considered both market and list prices; dual-chamber pacing cost-effective at market price, ICER up to £34,000 at maximum list price",
      "impact_on_icer": "increases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "other",
      "description": "RCT evidence from patients with mean age 73-80 may not be applicable to younger patients."
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "dual-chamber vs single-chamber ventricular pacing (AVB, market price, 10 years)",
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

### Extraction issues

1. **Device appraisal**: Like ECT, `drug_class`, `biosimilar_available` are meaningless. The `route_of_administration: "implanted"` works well -- this value was added in the schema.
2. **Multiple device manufacturers (6)**: Same issue as TA64 with multiple brands.
3. **Comparator type**: Comparing dual-chamber vs single-chamber pacemakers. Used `same_drug_different_regimen` but this is a stretch -- they are different device types, not different regimens of the same drug. **ISSUE: Need `same_class_different_variant` or `device_comparison` comparator type.**
4. **Device pricing structure**: Pacemaker costs are hardware + lead + implantation procedure costs, fundamentally different from drug pricing. The `CommercialArrangement` entity is irrelevant.
5. **Complex health-state model**: The Markov model has 10 health states, which is unusually rich for the schema's `health_states` array field. Works fine.

---

## 6. TA856 -- Upadacitinib for moderately to severely active ulcerative colitis (2023 -- JAK inhibitor)

### Abbreviated extraction

```json
{
  "ta_number": "TA856",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Upadacitinib for treating moderately to severely active ulcerative colitis",
    "issue_date": "2023",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Recommended within marketing authorisation when conventional or biological treatment cannot be tolerated or disease has not responded well enough, with commercial arrangement. Choose most appropriate treatment after discussion; if one of a range of suitable options, choose least expensive.",
    "appraisal_type": "STA",
    "committee_name": "Technology appraisal evaluation committee B",
    "erg_or_eag_name": "EAG (external assessment group)",
    "line_of_therapy": "any_line",
    "eligible_population": null,
    "methods_guide_era": "2022"
  },
  "interventions": [
    {
      "generic_name": "upadacitinib",
      "brand_name": "RINVOQ",
      "manufacturer": "AbbVie",
      "drug_class": "Janus-associated kinase (JAK) inhibitor",
      "mechanism_of_action": "JAK inhibitor",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "continuous",
      "biosimilar_available": false
    }
  ],
  "conditions": [
    {
      "condition_name": "moderately to severely active ulcerative colitis",
      "therapeutic_area": ["gastroenterology", "immunology"],
      "disease_setting": "chronic",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],
  "comparators": [
    {
      "comparator_name": "adalimumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": null
    },
    {
      "comparator_name": "golimumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": null
    },
    {
      "comparator_name": "infliximab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": null
    },
    {
      "comparator_name": "tofacitinib",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": null
    },
    {
      "comparator_name": "ustekinumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": null
    },
    {
      "comparator_name": "vedolizumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": null
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "U-ACHIEVE",
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
    "time_horizon": null,
    "cycle_length": null,
    "health_states": ["remission", "response without remission", "active ulcerative colitis", "surgery", "post-surgery"]
  },
  "methodological_decisions": [
    {
      "decision_category": "model_structure",
      "description": "Whether the model should include a second-line biologic therapy health state after first-line treatment failure",
      "company_position": "No second-line treatment after failure; people move to 'active ulcerative colitis' with no drug treatment",
      "erg_position": "Not plausible; people would get surgery within 12 months or other drug treatments. Added 'on subsequent treatment' health state.",
      "committee_preference": "EAG's simplified adjustment preferred; neither model truly reflects NHS practice but EAG's is closer",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "utility_source",
      "description": "Whether to use trial-based EQ-5D data or values from Woehl et al. 2008",
      "company_position": "Woehl et al. 2008 (real-world) consistent with previous UC appraisals",
      "erg_position": "Trial EQ-5D data preferred per NICE reference case; mostly higher utility values",
      "committee_preference": "Trial-based utility estimates preferred",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "indirect_comparison_method",
      "description": "Network meta-analyses comparing upadacitinib with biologics and tofacitinib",
      "company_position": "NMA results plausible; upadacitinib at least as effective as comparators",
      "erg_position": "Unresolvable technical issues; maintenance-phase results less reliable",
      "committee_preference": "NMA results plausible and appropriate for decision making",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head studies comparing upadacitinib with biologics or tofacitinib; relies on network meta-analysis."
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "upadacitinib vs existing NICE-recommended treatments",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": true,
    "equality_issues_raised": false
  },
  "cross_references": []
}
```

### Extraction issues

1. **Modern format**: Clean, well-structured. Extraction is smooth.
2. **Many comparators (6)**: The schema handles this well via array.
3. **Biologic-naive vs biologic-experienced subgroups**: The company's subgroup definitions (biologic-naive/experienced) map to `subgroup_definition` methodological decision but also affect comparator selection. The schema does not have a structured field for "treatment-history subgroups."
4. **Evolving treatment landscape**: The committee acknowledges treatments recommended since the evaluation (filgotinib, ozanimod) were not included. This is a common modern issue but the schema has no field for "acknowledged but excluded comparators."

---

## 7. TA906 -- Rimegepant for preventing migraine (2023 -- neurology)

### Abbreviated extraction

```json
{
  "ta_number": "TA906",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Rimegepant for preventing migraine",
    "issue_date": "May 2023",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Recommended for preventing episodic migraine in adults with >=4 and <15 attacks/month, only after >=3 preventative treatments have failed. Stop after 12 weeks if migraine frequency does not reduce by >=50%. Choose least expensive option if multiple suitable treatments.",
    "appraisal_type": "STA",
    "committee_name": "Technology appraisal committee D",
    "erg_or_eag_name": "ERG (external review group)",
    "line_of_therapy": "third_line_plus",
    "eligible_population": null,
    "methods_guide_era": "2022"
  },
  "interventions": [
    {
      "generic_name": "rimegepant",
      "brand_name": "Vydura",
      "manufacturer": "Pfizer",
      "drug_class": "calcitonin gene-related peptide (CGRP) receptor antagonist",
      "mechanism_of_action": "CGRP receptor antagonist (gepant)",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "continuous",
      "biosimilar_available": false
    }
  ],
  "conditions": [
    {
      "condition_name": "episodic migraine (>=4 and <15 attacks/month) after >=3 preventative treatments have failed",
      "therapeutic_area": ["neurology_psychiatry"],
      "disease_setting": "prevention_secondary",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],
  "comparators": [
    {
      "comparator_name": "erenumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": null
    },
    {
      "comparator_name": "fremanezumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": null
    },
    {
      "comparator_name": "galcanezumab",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": null
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "BHV3000-305",
      "study_design": "RCT",
      "phase": "phase 2/3",
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "change in mean monthly migraine days (last 4 weeks of 12-week treatment)",
      "sample_size": 741,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    }
  ],
  "economic_model": {
    "model_type": "decision_tree_plus_markov",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": ["on treatment (responding)", "stopped treatment"]
  },
  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "NMA of rimegepant vs CGRP monoclonal antibodies using 14 trials",
      "company_position": "NMA results plausible; rimegepant as effective as comparators",
      "erg_position": "NMA uncertain due to trial limitations (BHV3000-305 excluded treatment-refractory patients; populations/methods differ across trials)",
      "committee_preference": "NMA limitations unresolvable but suitable for decision making; rimegepant likely similar to or less effective than comparators",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "population_generalisability",
      "description": "Clinical trial excluded the most relevant population (treatment-refractory after >=3 prior treatments)",
      "company_position": "Unresolvable; no data on how prior treatment failure affects rimegepant efficacy",
      "erg_position": "Evidence uncertain; refractory migraine harder to treat",
      "committee_preference": "Noted uncertainty; factored into decision making",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "utility_source",
      "description": "EQ-5D derived via mapping from Migraine Specific Questionnaire; baseline utility difference between arms",
      "company_position": "Used MSQ-mapped EQ-5D",
      "erg_position": "Include baseline EQ-5D as covariate to eliminate non-trivial baseline difference between arms",
      "committee_preference": "Baseline mapped EQ-5D values for each arm should be the same; agreed with ERG approach",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Whether rimegepant healthcare resource use costs should be from primary or secondary care perspective",
      "company_position": "Primary care approach (GP visits)",
      "erg_position": "Secondary care approach (specialist neurologist) preferred",
      "committee_preference": "Rimegepant most likely started by specialist; specialist costs included alongside primary care costs",
      "impact_on_icer": "increases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trial comparing rimegepant with erenumab, fremanezumab, or galcanezumab."
    },
    {
      "gap_type": "other",
      "description": "Key clinical trial excluded population most relevant to positioning (patients who failed >=3 prior preventative treatments)."
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "rimegepant vs erenumab/fremanezumab/galcanezumab",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate",
    "direction": "decremental"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": true,
    "equality_issues_raised": true
  },
  "cross_references": []
}
```

### Extraction issues

1. **South-west quadrant ICER**: Rimegepant is less expensive and less effective than comparators. The schema's `direction: "decremental"` captures this. Net health benefit analysis was used instead of standard ICER. This is an edge case the schema handles via the `direction` field added in v0.4.
2. **Narrower than licence positioning**: The company positioned rimegepant narrower than its marketing authorisation (after >=3 treatments vs licence for >=4 attacks/month regardless of prior treatment). This positioning choice affects the entire appraisal but the schema has no field for "company-proposed restriction vs MA."
3. **Dual indication drug**: Rimegepant has both acute treatment and prevention indications being evaluated separately. Cross-reference to ID1539 but no TA number assigned yet.
4. **Disease_setting**: Used `prevention_secondary` for migraine prevention. This maps reasonably well.

---

## 8. TA926 -- Baricitinib for severe alopecia areata (2023 -- dermatology, novel indication, NOT recommended)

### Abbreviated extraction

```json
{
  "ta_number": "TA926",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Baricitinib for treating severe alopecia areata",
    "issue_date": "May 2023",
    "recommendation_type": "not_recommended",
    "restriction_details": null,
    "appraisal_type": "STA",
    "committee_name": "Technology appraisal committee A",
    "erg_or_eag_name": "EAG (evidence assessment group)",
    "line_of_therapy": null,
    "eligible_population": null,
    "methods_guide_era": "2022"
  },
  "interventions": [
    {
      "generic_name": "baricitinib",
      "brand_name": "Olumiant",
      "manufacturer": "Eli Lilly and Company",
      "drug_class": "Janus-associated kinase (JAK) inhibitor",
      "mechanism_of_action": "JAK inhibitor",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "continuous",
      "biosimilar_available": false
    }
  ],
  "conditions": [
    {
      "condition_name": "severe alopecia areata",
      "therapeutic_area": ["dermatology"],
      "disease_setting": "chronic",
      "biomarker_defined_population": false,
      "biomarker_name": null
    }
  ],
  "comparators": [
    {
      "comparator_name": "no active treatment (best supportive care including wigs, topical corticosteroids, off-label immunosuppressants)",
      "comparator_type": "best_supportive_care",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "BRAVE-AA1",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "SALT score of 20 or less at week 36",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    },
    {
      "trial_name": "BRAVE-AA2",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "SALT score of 20 or less at week 36",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "company",
    "time_horizon": "lifetime",
    "cycle_length": "4 weeks",
    "health_states": ["induction", "maintenance", "best supportive care", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "utility_source",
      "description": "Whether to use EQ-5D-5L data from BRAVE trials or Adelphi real-world study",
      "company_position": "Adelphi study EQ-5D preferred; only 1 in 5 had full health scores vs ~half in BRAVE trials",
      "erg_position": "BRAVE trial EQ-5D preferred per NICE reference case; within-person changes more appropriate",
      "committee_preference": "True values likely between BRAVE and Adelphi; agreed to consider a range",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Whether best supportive care or specific off-label treatments should be the comparator",
      "company_position": "No active treatment (basket of treatments in BSC)",
      "erg_position": "BSC composition uncertain but no active treatment comparator acceptable",
      "committee_preference": "No active treatment as comparator acceptable; would have liked analyses with immunosuppressants but accepted BSC",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Whether proportion of patients having BSC differs between baricitinib and no-treatment arms after non-response, and duration of BSC medicines",
      "company_position": "People who had baricitinib are less likely to have BSC after non-response; 10-year limit on BSC medicines",
      "erg_position": "No evidence for differential BSC use; assumed no one has BSC medicines after non-response",
      "committee_preference": "Same proportion in both arms; 10-year time horizon for BSC medicines; considered range of scenarios",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "other",
      "description": "EQ-5D-5L may not capture quality-of-life impact of alopecia areata; half of trial patients reported full health at baseline despite severe condition",
      "company_position": "EQ-5D may underestimate QoL impact; Adelphi study more plausible",
      "erg_position": "BRAVE trial baseline scores consistent with other studies; may underestimate QALY gains",
      "committee_preference": "Acknowledged profound psychosocial impact not shown in EQ-5D-5L scores; may be insensitivity of instrument or trial population differences",
      "impact_on_icer": "increases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "missing_quality_of_life_data",
      "description": "EQ-5D-5L may not be sensitive to changes in QoL in alopecia areata. ~Half of people with severe disease reported full health at baseline. No clinically meaningful improvement in EQ-5D, HADS, or SF-36 with treatment."
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": false
  },
  "icer_band": {
    "band": "above_50k",
    "comparison_pair": "baricitinib vs no active treatment",
    "is_committee_preferred": true,
    "uncertainty_level": "very_high"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "cancer_drugs_fund_eligible": null,
    "innovation_acknowledged": true,
    "equality_issues_raised": true
  },
  "cross_references": []
}
```

### Extraction issues

1. **EQ-5D insensitivity**: A central issue is that the EQ-5D may not capture QoL impact of a cosmetic/psychosocial condition. The `missing_quality_of_life_data` gap type captures this partially, but the issue is more nuanced -- it is about instrument validity rather than missing data. **POTENTIAL NEW GAP_TYPE: `instrument_insensitivity` or `outcome_measure_validity`.**
2. **Dermatology / cosmetic-adjacent condition**: Alopecia areata is not life-threatening and the primary benefit is psychosocial. The schema's `special_considerations` and `severity_modifier` fields do not have a structured way to express "condition impact is primarily psychosocial." The committee acknowledged baricitinib as innovative but still did not recommend.
3. **Best supportive care composition**: BSC is a basket of mostly off-label treatments including wigs and mental health services. The composition and duration of BSC is itself a major methodological dispute. This is well captured by `cost_assumption` and `comparator_selection` decision categories.
4. **Not recommended + managed access also rejected**: The committee considered and rejected both routine commissioning and managed access. The schema's `recommendation_type: "not_recommended"` captures this, but there is no field for "managed_access_considered_and_rejected."

---

## 9. TA962 -- Olaparib for maintenance treatment of BRCA mutation-positive advanced ovarian cancer (2019/2024 -- CDF, maintenance oncology)

### Abbreviated extraction

```json
{
  "ta_number": "TA962",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Olaparib for maintenance treatment of BRCA mutation-positive advanced ovarian, fallopian tube or peritoneal cancer after response to first-line platinum-based chemotherapy",
    "issue_date": "July 2019",
    "recommendation_type": "recommended_for_cdf",
    "restriction_details": "Recommended for CDF use for maintenance of BRCA1/2 mutation-positive, advanced (FIGO stages 3 and 4) high-grade epithelial ovarian/fallopian tube/peritoneal cancer after response to first-line platinum-based chemotherapy. Conditions in managed access agreement must be followed.",
    "appraisal_type": "STA",
    "committee_name": "Appraisal committee A",
    "erg_or_eag_name": "ERG (evidence review group)",
    "line_of_therapy": "maintenance",
    "eligible_population": null,
    "methods_guide_era": "2013"
  },
  "interventions": [
    {
      "generic_name": "olaparib",
      "brand_name": "Lynparza",
      "manufacturer": "AstraZeneca",
      "drug_class": "PARP inhibitor",
      "mechanism_of_action": "poly-ADP-ribose polymerase inhibition",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "fixed_duration",
      "biosimilar_available": false
    }
  ],
  "conditions": [
    {
      "condition_name": "BRCA mutation-positive advanced (FIGO 3-4) high-grade epithelial ovarian, fallopian tube or primary peritoneal cancer after response to first-line platinum-based chemotherapy",
      "therapeutic_area": ["oncology"],
      "disease_setting": "maintenance",
      "biomarker_defined_population": true,
      "biomarker_name": "BRCA1/2 mutation (germline and/or somatic)"
    }
  ],
  "comparators": [
    {
      "comparator_name": "routine surveillance (no active maintenance treatment)",
      "comparator_type": "no_treatment",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "SOLO-1",
      "study_design": "RCT",
      "phase": null,
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "progression-free survival",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": true
    }
  ],
  "economic_model": {
    "model_type": "partitioned_survival",
    "model_source": "company",
    "time_horizon": null,
    "cycle_length": null,
    "health_states": ["progression-free", "progressed disease (post-first-line)", "progressed disease (post-second-line / PFS-2)", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "survival_extrapolation",
      "description": "How to model overall survival given immature data -- company used PFS-2 as surrogate instead of directly fitting OS data",
      "company_position": "OS data too immature for direct extrapolation; PFS-2 used as surrogate for OS",
      "erg_position": "Not using available OS data from the trial is a major weakness; model may overestimate survival gain",
      "committee_preference": "Acknowledged PFS-2 as indicator of prolonged benefit but model predictions should reflect trial OS data; OS modelling is extremely uncertain",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "cure_assumption",
      "description": "Whether olaparib can cure some patients -- model predicts ~20% alive at 20 years in olaparib arm vs ~18% with routine surveillance",
      "company_position": "~20% cure rate plausible based on Study 19 long-term data showing 10% disease-free at 10 years",
      "erg_position": "No OS benefit demonstrated in SOLO-1; cure assumption speculative",
      "committee_preference": "Cure is possible and the 20% estimate is plausible, but no OS benefit yet demonstrated",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Treatment duration capped at 2 years per marketing authorisation unless residual disease",
      "company_position": "10% continue beyond 2 years (per SOLO-1)",
      "erg_position": null,
      "committee_preference": "~15% in UK practice may continue beyond 2 years; introduces cost uncertainty",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "treatment_sequencing",
      "description": "Whether subsequent PARP inhibitor use after olaparib failure changes cost-effectiveness",
      "company_position": "SOLO-1 trial data reflects current practice for subsequent PARP inhibitor use",
      "erg_position": "Model cannot test different assumptions about subsequent PARP inhibitor use; clinical pathway evolving",
      "committee_preference": "Subsequent PARP inhibitor use in trial is reasonable reflection of current practice but pathway uncertainty exists",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "discount_rate",
      "description": "Whether 1.5% discount rate for costs and benefits should apply",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "Reference case 3.5% discount rates should be applied; criteria for 1.5% not met",
      "impact_on_icer": "increases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "immature_overall_survival",
      "description": "Overall survival at 21% maturity; small non-significant benefit; median not reached in either arm (HR 0.95, 95% CI 0.60-1.53)."
    },
    {
      "gap_type": "surrogate_not_validated",
      "description": "Relationship between PFS-2 and OS not established. PFS improvement may not translate proportionally to OS benefit."
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "managed_access_agreement",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "olaparib vs routine surveillance",
    "is_committee_preferred": false,
    "uncertainty_level": "very_high"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": true,
    "cancer_drugs_fund_eligible": true,
    "innovation_acknowledged": true,
    "equality_issues_raised": false
  },
  "cross_references": [
    {
      "referenced_ta": "TA381",
      "relationship": "same_drug",
      "context": "Olaparib capsules recommended after >=3 lines of platinum-based chemotherapy"
    }
  ]
}
```

### Extraction issues

1. **CDF entry with uncertain ICER**: The company's base-case ICER is £17,480 (below_20k) but the committee considers it highly uncertain and possibly much higher. The `is_committee_preferred: false` flag and `uncertainty_level: "very_high"` capture this tension, but the schema cannot express "company says below_20k but committee thinks it could be above_50k."
2. **Study 19 as external validation**: The committee references Study 19 (olaparib in relapsed ovarian cancer) to support long-term cure assumptions. This cross-study reasoning is important but not captured as a formal cross-reference since Study 19 is a clinical trial, not a TA.
3. **Edinburgh Ovarian Cancer Database**: External real-world data used to validate the model. The schema has no entity for real-world evidence databases.
4. **Treatment duration**: 2-year fixed duration with ~15% continuing beyond -- the `treatment_duration_type: "fixed_duration"` captures the modal case but the 15% exception is important.
5. **Evolving pathway**: PARP inhibitor placement in the ovarian cancer pathway was actively changing at time of appraisal. The schema captures this as treatment_sequencing uncertainty.

---

## 10. TA975 -- Tisagenlecleucel for relapsed/refractory B-cell ALL in people aged up to 25 years (2018 -- CAR-T, paediatric)

### Abbreviated extraction

**NOTE**: The FAD.md file for TA975 contains the Cancer Drugs Fund Managed Access Agreement and Data Collection Arrangement, not a standard Final Appraisal Document. This is itself an edge case -- some early CDF appraisals were published with the MAA rather than a conventional FAD. The extraction below is based on available content.

```json
{
  "ta_number": "TA975",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Tisagenlecleucel for treating relapsed or refractory B-cell acute lymphoblastic leukaemia in people aged up to 25 years",
    "issue_date": "November 2018",
    "recommendation_type": "recommended_for_cdf",
    "restriction_details": "Recommended within CDF for relapsed/refractory B-cell ALL in people aged up to 25 years. Requires JACIE accreditation for Immune Effector Cell therapy, Novartis quality assurance, NHS England service specification compliance. Application via National CAR T Clinical Panel. Detailed eligibility criteria including: 2nd+ bone marrow relapse, any relapse post-transplant, primary/secondary refractory disease, Philadelphia-positive ALL failing 2 TKIs. Must have flow cytometry detectable ALL with CD19 positivity.",
    "appraisal_type": "STA",
    "committee_name": null,
    "erg_or_eag_name": null,
    "line_of_therapy": "third_line_plus",
    "eligible_population": "25-30 new patients per year",
    "methods_guide_era": "2013"
  },
  "interventions": [
    {
      "generic_name": "tisagenlecleucel",
      "brand_name": "Kymriah",
      "manufacturer": "Novartis Pharmaceuticals Ltd",
      "drug_class": "CAR-T cell therapy",
      "mechanism_of_action": "autologous anti-CD19 chimeric antigen receptor T-cell immunotherapy",
      "route_of_administration": "intravenous",
      "is_combination_regimen": false,
      "combination_components": null,
      "treatment_duration_type": "single_administration",
      "biosimilar_available": false
    }
  ],
  "conditions": [
    {
      "condition_name": "relapsed or refractory B-cell acute lymphoblastic leukaemia",
      "therapeutic_area": ["haematology"],
      "disease_setting": "relapsed_refractory",
      "biomarker_defined_population": true,
      "biomarker_name": "CD19 positivity"
    }
  ],
  "comparators": [],
  "clinical_trials": [
    {
      "trial_name": "ELIANA",
      "study_design": "single_arm",
      "phase": "phase II",
      "blinding": null,
      "is_pivotal": true,
      "primary_outcome": "overall survival",
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
    {
      "trial_name": "ENSIGN",
      "study_design": "single_arm",
      "phase": null,
      "is_pivotal": false,
      "primary_outcome": null,
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    },
    {
      "trial_name": "B2101J",
      "study_design": "single_arm",
      "phase": null,
      "is_pivotal": false,
      "primary_outcome": null,
      "sample_size": null,
      "crossover_occurred": false,
      "crossover_adjusted": null,
      "generalisability_concern": false
    }
  ],
  "economic_model": null,
  "methodological_decisions": [],
  "evidence_gaps": [
    {
      "gap_type": "immature_overall_survival",
      "description": "Data does not fully support the curative nature of tisagenlecleucel."
    },
    {
      "gap_type": "other",
      "description": "Rate of subsequent stem cell transplant uncertain. Duration of IV immunoglobulin treatment for B-cell aplasia unknown."
    },
    {
      "gap_type": "single_arm_evidence_only",
      "description": "All pivotal evidence from single-arm studies (ELIANA, ENSIGN, B2101J)."
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "managed_access_agreement",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": null,
  "special_considerations": {
    "end_of_life_considered": false,
    "end_of_life_met": null,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": true,
    "cancer_drugs_fund_eligible": true,
    "innovation_acknowledged": true,
    "equality_issues_raised": false
  },
  "cross_references": []
}
```

### Extraction issues

1. **Document is MAA, not standard FAD**: The file contains the Managed Access Agreement and Data Collection Arrangement, not the full committee deliberation. Many fields cannot be populated (economic model, methodological decisions, ICER band, comparators). This is a **major schema gap** -- the schema assumes all FADs have the same structure, but CDF MAA documents are substantially different.
2. **CAR-T cell therapy**: The `treatment_duration_type: "single_administration"` works perfectly for CAR-T (added in v0.3). The `drug_class` field is being used for "CAR-T cell therapy" which is not a drug class in the traditional sense.
3. **Paediatric/young adult population (up to 25 years)**: The schema's `is_paediatric` flag (added in v0.3) is relevant but this is a paediatric-and-young-adult population, not purely paediatric.
4. **Complex eligibility criteria**: The MAA contains extremely detailed eligibility criteria (JACIE accreditation, National CAR T Clinical Panel, specific relapse/refractory definitions, Philadelphia-positive criteria). This level of detail is captured in `restriction_details` but is far more complex than typical restrictions.
5. **Infrastructure requirements**: The recommendation requires accredited treatment centres, phased implementation, national clinical panel prioritisation. None of this maps to any schema entity. **POTENTIAL NEW ENTITY: `InfrastructureRequirement` for advanced therapies.**
6. **Missing comparators**: The MAA document does not name formal comparators. In the full FAD (not available here), these would likely include blinatumumab and clofarabine-based regimens.

---

## Critique and Convergence Assessment

### A. Pre-2010 documents vs modern documents

**The schema handles pre-2010 documents reasonably well despite significant structural differences.**

Key differences in pre-2010 FADs:
- **Format**: "National Institute for Clinical Excellence" (not "Health and Care Excellence"). Sections use "Evidence and interpretation" rather than "Committee discussion." Documents include extensive appendices (committee members, sources, audit criteria).
- **No structured methodological decision sections**: Older FADs embed committee reasoning in flowing text rather than discrete numbered paragraphs. Extraction requires more interpretation.
- **No PAS/commercial arrangements**: Pre-2010 documents rarely mention discounts; drug costs are discussed at BNF list price.
- **No CDF, no end-of-life criteria, no severity modifier**: These frameworks did not exist. The `special_considerations` fields correctly default to false/null.
- **Assessment Groups vs ERGs**: Pre-2010 uses "Assessment Group" or "Assessment Report" rather than ERG/EAG. The schema's `design_notes.terminology_normalisation` accounts for this.
- **Multiple manufacturers**: MTAs (TA64, TA75) frequently appraise multiple equivalent products from different manufacturers. The single-manufacturer `Intervention` entity is awkward.

**Verdict: The schema flexes adequately for pre-2010 documents.** The `methods_guide_era: "pre_2008"` flag correctly signals the different framework. No structural changes are needed, though some fields are systematically null (commercial arrangements, special considerations).

### B. Non-pharmaceutical technologies (ECT, pacemakers)

These expose the most significant schema weakness. The `Intervention` entity was designed around pharmaceuticals:
- `drug_class`, `biosimilar_available`, `route_of_administration` are meaningless for procedures (ECT) and awkward for devices (pacemakers)
- `CommercialArrangement` is irrelevant (no manufacturer PAS for ECT; pacemaker procurement discounts are fundamentally different)
- Device comparisons (dual vs single-chamber pacemaker) do not fit `comparator_type` well

**Recommendation**: Consider adding `intervention_type` enum: `drug | biologic | device | procedure | cell_therapy | digital_health`. This would allow downstream consumers to filter out irrelevant fields. This is a minor structural addition, not a fundamental redesign.

### C. NEW issues identified in Round 4

| Issue | New? | Severity | Proposed fix |
|-------|------|----------|-------------|
| Non-drug interventions need `intervention_type` field | **NEW** | Medium | Add enum to `Intervention` entity |
| `comparator_type` missing `device_comparison` | **NEW** | Low | Add to enum |
| EQ-5D instrument insensitivity as a gap type | **NEW** | Low | Add `instrument_insensitivity` to `gap_types` |
| MAA documents structurally different from FADs | **NEW** | Medium | Add `doc_type` enum: `FAD`, `ACD`, `MAA`, `DCA` |
| Multiple manufacturers in MTA | Previously noted | Low | Accept as limitation; concatenate in field |
| QoL-instrument-based eligibility criteria | **NEW** | Low | Capture in `restriction_details` free text |
| Infrastructure requirements for ATMPs | **NEW** | Low | Out of scope for v0.5; note for future |
| `model_type` missing `cost_analysis` | **NEW** | Low | Add to enum |
| Company-proposed restriction narrower than MA | Partially new | Low | Capture in `restriction_details` free text |

### D. Is the schema stabilising?

**Yes, the schema is clearly stabilising.** Evidence:

1. **Core entity structure is stable**: All 10 TAs were extractable using the existing entity types. No new entity types are needed. The 8 entity types (TechnologyAppraisal, Intervention, Condition, Comparator, ClinicalTrial, EconomicModel, MethodologicalDecision, EvidenceGap) plus CommercialArrangement cover the full range from 2002 to 2024.

2. **Decision categories are comprehensive**: Across these 10 very diverse TAs, the decision categories used were: `survival_extrapolation`, `treatment_effect_duration`, `indirect_comparison_method`, `utility_source`, `utility_value_choice`, `comparator_selection`, `population_generalisability`, `subgroup_definition`, `stopping_rule`, `model_structure`, `treatment_sequencing`, `cost_assumption`, `cure_assumption`, `discount_rate`, `mortality_assumption`, `equivalence_assumption`, and `other`. Only 1 of 40+ methodological decisions required `other` (EQ-5D insensitivity in alopecia areata), and this could be addressed by a narrow addition to `gap_types` rather than a new decision category.

3. **New issues are minor enums, not structural**: Round 4 issues are primarily about adding values to existing enums (`intervention_type`, `cost_analysis` model type, `instrument_insensitivity` gap type) rather than adding new entities or relationships.

4. **Diminishing returns**: Rounds 1-2 required adding multiple new decision categories, disease settings, therapeutic areas, and model types. Round 3 added 3 decision categories and 2 gap types. Round 4 identifies 0 new decision categories and suggests 1 new gap type and 2-3 enum values. The rate of new findings is clearly declining.

### E. Estimated `other` category usage after Round 4 refinements

Across the 40 TAs tested in rounds 1-4:
- **decision_category `other`**: ~3-5% of all methodological decisions would use `other` after adding `instrument_insensitivity` to gap_types. The main remaining `other` cases are highly idiosyncratic disputes (e.g., consent procedures in ECT, wig provision in alopecia areata) that do not warrant dedicated categories.
- **gap_type `other`**: ~5-8% of evidence gaps. Remaining `other` gaps include: trial exclusion of relevant population (rimegepant), infrastructure/implementation concerns (CAR-T), and condition-specific measurement issues.
- **therapeutic_area `other`**: 0% -- all 10 TAs map to existing values. The dermatology addition in v0.4 was prescient.
- **disease_setting `other`**: 0% -- the expanded enum covers all cases.

**Overall `other` estimate: ~5% of categorical assignments**, down from ~20-25% at v0.1. This is approaching an acceptable floor for a general-purpose ontology.

### F. Summary of recommendations for v0.5

1. **Add `intervention_type` enum** to `Intervention` entity: `drug | biologic | device | procedure | cell_therapy | digital_health`
2. **Add `cost_analysis` to `model_type` enum** (for early TAs where QALY estimation was not possible)
3. **Add `instrument_insensitivity` to `gap_types` enum** (for cases where EQ-5D or other instruments may not capture condition impact)
4. **Add `device_comparison` to `comparator_type` enum** (for device-vs-device TAs)
5. **Add `MAA` and `DCA` to doc_type options** in extraction prompt (to flag when source document is not a standard FAD)
6. **No new entity types or relationships needed** -- the schema is structurally complete for the NICE TA corpus

The schema is converging. A v0.5 incorporating these minor additions would likely handle the full ~1000 TA corpus with <5% `other` usage.
