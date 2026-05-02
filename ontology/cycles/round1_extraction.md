# Round 1: Non-Cancer Diversity Extraction Test

Testing ontology v0.1 against 10 non-cancer FADs spanning 2006-2021.

---

## TA103 -- Efalizumab and etanercept for psoriasis (2006, MTA)

```json
{
  "ta_number": "TA103",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Efalizumab and etanercept for the treatment of adults with psoriasis",
    "issue_date": "August 2005",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Etanercept recommended at 25mg twice weekly only for severe psoriasis (PASI>=10 AND DLQI>10) after failure of ciclosporin, methotrexate and PUVA. Efalizumab recommended only after etanercept failure or intolerance. Both require 12-week response assessment (PASI 75 or PASI 50 + 5-point DLQI reduction).",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "Centre for Reviews and Dissemination, University of York",
    "line_of_therapy": "third_line_plus",
    "methods_guide_era": "pre_2008"
  },
  "interventions": [
    {
      "generic_name": "etanercept",
      "brand_name": "Enbrel",
      "manufacturer": "Wyeth Pharmaceuticals",
      "drug_class": "TNF inhibitor",
      "mechanism_of_action": "recombinant human TNF receptor fusion protein",
      "route_of_administration": "subcutaneous",
      "is_combination_regimen": false,
      "treatment_duration_type": "cyclical"
    },
    {
      "generic_name": "efalizumab",
      "brand_name": null,
      "manufacturer": "Serono Pharmaceuticals Ltd",
      "drug_class": "T-cell modulator",
      "mechanism_of_action": "blocks T-cell activation or migration",
      "route_of_administration": "subcutaneous",
      "is_combination_regimen": false,
      "treatment_duration_type": "continuous"
    }
  ],
  "conditions": [
    {
      "condition_name": "moderate to severe chronic plaque psoriasis in adults",
      "therapeutic_area": "dermatology",
      "disease_setting": "chronic",
      "biomarker_defined_population": false
    }
  ],
  "comparators": [
    {
      "comparator_name": "supportive care without DMARDs or biological therapies",
      "comparator_type": "best_supportive_care",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "Five efalizumab RCTs (unnamed)",
      "study_design": "RCT",
      "is_pivotal": true,
      "primary_outcome": "PASI 50, PASI 75",
      "generalisability_concern": true
    },
    {
      "trial_name": "Three etanercept RCTs (unnamed)",
      "study_design": "RCT",
      "is_pivotal": true,
      "primary_outcome": "PASI 50, PASI 75, PASI 90",
      "generalisability_concern": true
    }
  ],
  "economic_model": {
    "model_type": "decision_tree",
    "model_source": "Assessment Group (+ manufacturer models)",
    "time_horizon": "10 years",
    "health_states": ["responder", "non-responder"]
  },
  "methodological_decisions": [
    {
      "decision_category": "utility_source",
      "description": "How to map PASI/DLQI responses to EQ-5D utilities",
      "company_position": "Efalizumab manufacturer used time trade-off from 87 patients; etanercept manufacturer used DLQI-to-utility mapping",
      "erg_position": "Assessment Group mapped mean change in DLQI to EQ-5D",
      "committee_preference": "Accepted Assessment Group approach",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Whether to compare biologics against each other or supportive care",
      "company_position": "Compare against topical therapies / no systemic therapy",
      "erg_position": "Assessment Group compared all biologics and supportive care",
      "committee_preference": "Assessment Group approach comparing all options",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "population_generalisability",
      "description": "Trial inclusion did not fully reflect licensed population (psoriasis failed to respond to other treatments)",
      "company_position": "Subgroup analysis of high-need patients showed similar efficacy",
      "erg_position": null,
      "committee_preference": "Accepted that trial populations had severe psoriasis and drugs work in licensed population",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "stopping_rule",
      "description": "Response criteria and duration of treatment cycles",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "12-week assessment with PASI 75 or (PASI 50 + 5-point DLQI reduction); no re-treatment of non-responders",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Whether non-responders would require hospitalisation (21 days/year)",
      "company_position": null,
      "erg_position": "Modelled scenarios with and without hospitalisation for non-responders",
      "committee_preference": "Concluded cost effectiveness only plausible for those likely to require hospital admission",
      "impact_on_icer": "decreases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "short_follow_up",
      "description": "No RCTs longer than 12 weeks for efalizumab; limited long-term safety data for both drugs in psoriasis"
    },
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trials of etanercept vs efalizumab"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none",
    "discount_confidential": false,
    "critical_for_recommendation": false
  },
  "icer_band": {
    "band": "above_50k",
    "comparison_pair": "intermittent etanercept 25mg vs supportive care (Assessment Group base case)",
    "is_committee_preferred": false,
    "uncertainty_level": "very_high"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "severity_modifier_applied": null,
    "cancer_drugs_fund_considered": false,
    "innovation_acknowledged": false,
    "equality_issues_raised": false
  },
  "cross_references": []
}
```

**Extraction notes:** This is a pre-2008 MTA with two interventions. The ontology handles multi-intervention well. However, the ICER story is complex: base-case Assessment Group ICER was ~65k but committee concluded cost-effectiveness only in the subgroup with hospital admissions (~14k). The `icer_band` field struggles with this conditional logic. Trial names were not provided (unnamed RCTs), which is common in older MTAs.

---

## TA161 -- Osteoporosis secondary prevention (2008, MTA)

```json
{
  "ta_number": "TA161",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Alendronate, etidronate, risedronate, raloxifene, strontium ranelate and teriparatide for the secondary prevention of osteoporotic fragility fractures in postmenopausal women",
    "issue_date": "December 2010",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Complex stepped recommendations: alendronate first-line for T-score <= -2.5; risedronate/etidronate second-line with T-score/age/risk factor thresholds; strontium ranelate/raloxifene third-line with stricter thresholds; teriparatide last-line for age >= 65 with T-score <= -4.0 or T-score <= -3.5 plus >2 fractures",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "School of Health and Related Research, University of Sheffield (ScHARR)",
    "line_of_therapy": "first_line",
    "methods_guide_era": "2008"
  },
  "interventions": [
    {
      "generic_name": "alendronate",
      "brand_name": "Fosamax",
      "manufacturer": "Merck Sharp & Dohme",
      "drug_class": "bisphosphonate",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "treatment_duration_type": "continuous"
    },
    {
      "generic_name": "risedronate",
      "brand_name": "Actonel",
      "manufacturer": "Procter & Gamble UK",
      "drug_class": "bisphosphonate",
      "route_of_administration": "oral"
    },
    {
      "generic_name": "etidronate",
      "brand_name": "Didronel",
      "manufacturer": "Procter & Gamble UK",
      "drug_class": "bisphosphonate",
      "route_of_administration": "oral"
    },
    {
      "generic_name": "raloxifene",
      "brand_name": "Evista",
      "manufacturer": "Eli Lilly",
      "drug_class": "selective oestrogen receptor modulator",
      "route_of_administration": "oral"
    },
    {
      "generic_name": "strontium ranelate",
      "brand_name": "Protelos",
      "manufacturer": "Servier Laboratories",
      "drug_class": "bone metabolism agent",
      "route_of_administration": "oral"
    },
    {
      "generic_name": "teriparatide",
      "brand_name": "Forsteo",
      "manufacturer": "Eli Lilly & Company",
      "drug_class": "parathyroid hormone",
      "route_of_administration": "subcutaneous",
      "treatment_duration_type": "fixed_duration"
    }
  ],
  "conditions": [
    {
      "condition_name": "postmenopausal osteoporosis with prior fragility fracture (secondary prevention)",
      "therapeutic_area": "musculoskeletal",
      "disease_setting": "chronic",
      "biomarker_defined_population": true,
      "biomarker_name": "T-score <= -2.5 on DXA scanning"
    }
  ],
  "comparators": [
    {
      "comparator_name": "no treatment",
      "comparator_type": "no_treatment",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "Assessment Group (ScHARR)",
    "time_horizon": "10 years (morbidity) + lifetime (mortality)",
    "health_states": ["fracture-free", "vertebral fracture year", "vertebral fracture subsequent", "hip fracture year", "hip fracture subsequent", "wrist fracture", "other non-vertebral fracture", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "subgroup_definition",
      "description": "Whether strontium ranelate hip fracture efficacy should use whole trial or post-hoc high-risk subgroup (age>=74, T-score<=-2.4)",
      "company_position": "Servier argued subgroup RR of 0.64 is valid and more robust than whole-trial RR of 0.85",
      "erg_position": "DSU concluded subgroup selection was data-dependent and likely inflated; whole trial ITT analysis preferred",
      "committee_preference": "Agreed with DSU that the post-hoc subgroup RR was biased; used whole-trial data",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Impact of generic alendronate pricing on cost-effectiveness of other drugs",
      "company_position": "Various manufacturers submitted models at branded prices",
      "erg_position": "Used non-proprietary alendronate at ~54/year, making all other drugs dominated",
      "committee_preference": "Used generic alendronate as first-line benchmark",
      "impact_on_icer": "increases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "Very few head-to-head trials between the 6 drugs"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none"
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "alendronate vs no treatment",
    "is_committee_preferred": true,
    "uncertainty_level": "low"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "equality_issues_raised": false
  },
  "cross_references": []
}
```

**Extraction notes:** This is a 6-drug MTA with extraordinarily complex recommendations involving lookup tables by age/T-score/risk factors. The ontology `restriction_details` field cannot adequately represent matrix-style conditional recommendations. The `line_of_therapy` enum is inadequate -- this TA establishes a full treatment sequencing hierarchy (1st through 4th line) within one recommendation. The Court of Appeal element (post-hoc subgroup dispute for strontium ranelate) is a high-value methodological decision that the schema captures well.

---

## TA200 -- Peginterferon alfa and ribavirin for hepatitis C (2010)

```json
{
  "ta_number": "TA200",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Peginterferon alfa and ribavirin for the treatment of chronic hepatitis C (part review of TA75 and TA106)",
    "issue_date": "August 2010",
    "recommendation_type": "recommended",
    "restriction_details": "Recommended for: (1) re-treatment after non-response/relapse; (2) HIV co-infection; (3) shortened courses for rapid virological responders with low viral load",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "Southampton Health Technology Assessments Centre",
    "line_of_therapy": "any_line",
    "methods_guide_era": "2008"
  },
  "interventions": [
    {
      "generic_name": "peginterferon alfa-2a",
      "brand_name": "Pegasys",
      "manufacturer": "Roche Products",
      "drug_class": "pegylated interferon",
      "route_of_administration": "subcutaneous",
      "is_combination_regimen": true,
      "combination_components": ["peginterferon alfa-2a", "ribavirin (Copegus)"],
      "treatment_duration_type": "fixed_duration"
    },
    {
      "generic_name": "peginterferon alfa-2b",
      "brand_name": "ViraferonPeg",
      "manufacturer": "Schering-Plough",
      "drug_class": "pegylated interferon",
      "route_of_administration": "subcutaneous",
      "is_combination_regimen": true,
      "combination_components": ["peginterferon alfa-2b", "ribavirin (Rebetol)"],
      "treatment_duration_type": "fixed_duration"
    }
  ],
  "conditions": [
    {
      "condition_name": "chronic hepatitis C",
      "therapeutic_area": "infectious_disease",
      "disease_setting": "chronic",
      "biomarker_defined_population": true,
      "biomarker_name": "HCV RNA positive, genotype-stratified"
    }
  ],
  "comparators": [
    {
      "comparator_name": "best supportive care",
      "comparator_type": "best_supportive_care",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "standard duration treatment (48 or 24 weeks)",
      "comparator_type": "same_drug_different_regimen",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "Assessment Group (adapted from previous model)",
    "time_horizon": "lifetime",
    "cycle_length": "1 year",
    "health_states": ["mild hepatitis C", "moderate hepatitis C", "compensated cirrhosis", "decompensated cirrhosis", "hepatocellular carcinoma", "liver transplant", "post-SVR (3 states by disease stage at treatment)", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "other",
      "description": "Net benefit framework for shortened treatment (cost saving with QALY loss)",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "Accepted that ICERs from decreased effectiveness and decreased costs reverse the decision rule; ICERs above threshold are acceptable",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "utility_source",
      "description": "Whether age-specific utilities should apply to SVR state only or all health states",
      "company_position": "Roche applied age-specific utilities only to SVR state",
      "erg_position": "Considered this inappropriate; corrected to apply consistently",
      "committee_preference": "Agreed with Assessment Group correction",
      "impact_on_icer": "increases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_comparator_data",
      "description": "No RCTs comparing peginterferon with best supportive care for re-treatment or HIV co-infection populations"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none"
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "peginterferon + ribavirin vs best supportive care (re-treatment and co-infection)",
    "is_committee_preferred": true,
    "uncertainty_level": "low"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "equality_issues_raised": false
  },
  "cross_references": [
    {
      "referenced_ta": "TA75",
      "relationship": "same_condition",
      "context": "Part review of TA75 recommendations"
    },
    {
      "referenced_ta": "TA106",
      "relationship": "same_condition",
      "context": "Part review of TA106 recommendations for mild hepatitis C"
    }
  ]
}
```

**Extraction notes:** This is a "part review" TA, which is a relationship type not in the ontology. The comparator "same drug different regimen" (shortened vs standard duration) doesn't fit cleanly into `comparator_type`. The genotype-stratified decision-making is hard to capture -- recommendations differ by HCV genotype 1 vs 2/3 vs 4. The "net benefit framework" for cost-saving-but-less-effective scenarios is an interesting methodological decision that doesn't fit any existing category well.

---

## TA211 -- Prucalopride for constipation (2010, STA)

```json
{
  "ta_number": "TA211",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Prucalopride for the treatment of chronic constipation in women",
    "issue_date": "October 2010",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Recommended only in women who have used at least 2 laxatives from different classes at highest tolerated doses for at least 6 months without adequate relief, and invasive treatment is being considered. Discontinue if not effective after 4 weeks.",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee C",
    "erg_or_eag_name": "West Midlands Health Technology Assessment Collaboration (WMHTAC)",
    "line_of_therapy": "third_line_plus",
    "methods_guide_era": "2008"
  },
  "interventions": [
    {
      "generic_name": "prucalopride",
      "brand_name": "Resolor",
      "manufacturer": "Movetis",
      "drug_class": "selective serotonin 5-HT4 receptor agonist",
      "mechanism_of_action": "stimulates colonic motility",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "treatment_duration_type": "continuous"
    }
  ],
  "conditions": [
    {
      "condition_name": "chronic constipation in women refractory to laxatives",
      "therapeutic_area": "other",
      "disease_setting": "chronic",
      "biomarker_defined_population": false
    }
  ],
  "comparators": [
    {
      "comparator_name": "placebo plus rescue medication (bisacodyl)",
      "comparator_type": "placebo",
      "is_established_practice": false,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "PRU-INT-6",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "3 or more spontaneous complete bowel movements per week",
      "sample_size": 720
    },
    {
      "trial_name": "PRU-USA-11",
      "study_design": "RCT",
      "phase": "phase III",
      "is_pivotal": true,
      "sample_size": 628
    },
    {
      "trial_name": "PRU-USA-13",
      "study_design": "RCT",
      "phase": "phase III",
      "is_pivotal": true,
      "sample_size": 651
    },
    {
      "trial_name": "PRU-INT-12",
      "study_design": "RCT",
      "phase": "phase III",
      "is_pivotal": false,
      "primary_outcome": "3 or more spontaneous complete bowel movements per week in older women",
      "sample_size": 305
    }
  ],
  "economic_model": {
    "model_type": "decision_tree",
    "model_source": "company",
    "time_horizon": "52 weeks"
  },
  "methodological_decisions": [
    {
      "decision_category": "utility_source",
      "description": "Whether PAC-QOL/PAC-SYM mapped to EQ-5D via SF-36 is valid, or direct SF-36 data should be used",
      "company_position": "Used PAC-QOL/PAC-SYM mapped to EQ-5D via SF-36",
      "erg_position": "Concerned about mapping assumptions; noted SF-36 did not show statistically significant improvement",
      "committee_preference": "Concluded changing mapping to include SF-36 would unlikely alter results substantially",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Whether placebo plus rescue medication is appropriate comparator vs active laxatives",
      "company_position": "Placebo appropriate for laxative-refractory patients",
      "erg_position": "More appropriate comparator would be variety of oral laxatives",
      "committee_preference": "Agreed it would be difficult to define a standard laxative regimen; accepted placebo as comparator",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Whether true resource costs of chronic constipation (referrals, surgery) should be included",
      "company_position": "Conservative: excluded comparator costs",
      "erg_position": null,
      "committee_preference": "Agreed manufacturer's costs were conservative; true costs would reduce the ICER",
      "impact_on_icer": "decreases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "short_follow_up",
      "description": "Pivotal trials only 12 weeks (4 weeks for older women); long-term efficacy uncertain with >50% dropout in extension studies"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none"
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "prucalopride vs placebo plus rescue medication",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "equality_issues_raised": false
  }
}
```

**Extraction notes:** The `therapeutic_area` "other" is a fallback for gastroenterology, which is missing from the enum. The sex-restricted recommendation (women only) has no field in the schema. The comparator being placebo is awkward -- the `comparator_type` enum doesn't have a "placebo" option.

---

## TA236 -- Ticagrelor for ACS (2011, STA)

```json
{
  "ta_number": "TA236",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Ticagrelor for the treatment of acute coronary syndromes",
    "issue_date": "September 2011",
    "recommendation_type": "recommended",
    "restriction_details": "Recommended for up to 12 months in STEMI (with intended primary PCI), NSTEMI, and unstable angina (with specific risk factors)",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "Liverpool Reviews and Implementation Group (LRiG)",
    "line_of_therapy": "first_line",
    "methods_guide_era": "2008"
  },
  "interventions": [
    {
      "generic_name": "ticagrelor",
      "brand_name": "Brilique",
      "manufacturer": "AstraZeneca",
      "drug_class": "P2Y12 receptor antagonist",
      "mechanism_of_action": "oral antagonist at the P2Y12 adenosine diphosphate receptor, inhibits platelet aggregation",
      "route_of_administration": "oral",
      "is_combination_regimen": true,
      "combination_components": ["ticagrelor", "low-dose aspirin"],
      "treatment_duration_type": "fixed_duration"
    }
  ],
  "conditions": [
    {
      "condition_name": "acute coronary syndromes (STEMI, NSTEMI, unstable angina)",
      "therapeutic_area": "cardiovascular",
      "disease_setting": "acute",
      "biomarker_defined_population": false
    }
  ],
  "comparators": [
    {
      "comparator_name": "clopidogrel plus aspirin",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "PLATO",
      "study_design": "RCT",
      "phase": "phase III",
      "blinding": "double_blind",
      "is_pivotal": true,
      "primary_outcome": "time to first event (composite: MI, stroke, vascular death)",
      "sample_size": 18624,
      "generalisability_concern": true
    }
  ],
  "economic_model": {
    "model_type": "decision_tree_plus_markov",
    "model_source": "company",
    "time_horizon": "40 years (lifetime)",
    "health_states": ["non-fatal MI", "post-MI", "non-fatal stroke", "post-stroke", "death", "no further event"]
  },
  "methodological_decisions": [
    {
      "decision_category": "model_structure",
      "description": "Model did not allow patients to have multiple cardiovascular events",
      "company_position": "Simplified model structure",
      "erg_position": "Structure over-simplified; not allowing multiple events biased results",
      "committee_preference": "Agreed model oversimplified but noted this would make ICERs conservative (lower than true value if corrected)",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Resource use estimation in 1st year (combined vs separate analysis of treatment arms)",
      "company_position": "Separate health state costs for ticagrelor vs clopidogrel arms",
      "erg_position": "Combined analysis appropriate; reduced cost difference from ~371 to ~100",
      "committee_preference": "Accepted ERG adjustments",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "population_generalisability",
      "description": "Trial population younger than UK ACS population; only 281 UK patients; loading dose of clopidogrel differed from UK practice",
      "company_position": "Adjusted for age in model",
      "erg_position": "Age adjustment underestimated benefits by ~8%",
      "committee_preference": "Concluded trial broadly reflective of UK practice",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "indirect_comparison_method",
      "description": "Indirect comparison of ticagrelor vs prasugrel via PLATO and TRITON-TIMI 38",
      "company_position": "Trials not comparable; indirect comparison inappropriate",
      "erg_position": "Agreed indirect comparison unreliable",
      "committee_preference": "Concluded relative effectiveness of ticagrelor vs prasugrel was uncertain; no separate recommendation possible",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none"
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "ticagrelor plus aspirin vs clopidogrel plus aspirin",
    "is_committee_preferred": true,
    "uncertainty_level": "low"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "equality_issues_raised": false,
    "innovation_acknowledged": false
  },
  "cross_references": [
    {
      "referenced_ta": "TA182",
      "relationship": "same_condition",
      "context": "Previous NICE guidance on prasugrel for ACS with PCI"
    },
    {
      "referenced_ta": "TA152",
      "relationship": "comparator_guidance",
      "context": "Drug-eluting stents guidance on antiplatelet therapy duration"
    }
  ]
}
```

**Extraction notes:** Straightforward STA. The PLATO trial is well-named and easy to extract. The decision-tree-plus-Markov model type maps well. The `disease_setting` "acute" works here.

---

## TA303 -- Teriflunomide for MS (2014, STA)

```json
{
  "ta_number": "TA303",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Teriflunomide for treating relapsing-remitting multiple sclerosis",
    "issue_date": "November 2013",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Recommended for active RRMS (normally 2 relapses in previous 2 years) only if NOT highly active or rapidly evolving severe RRMS, and with PAS discount",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": null,
    "line_of_therapy": "first_line",
    "methods_guide_era": "2013"
  },
  "interventions": [
    {
      "generic_name": "teriflunomide",
      "brand_name": "Aubagio",
      "manufacturer": "Genzyme",
      "drug_class": "immunomodulatory disease-modifying therapy",
      "mechanism_of_action": "anti-inflammatory, blocks proliferation of stimulated lymphocytes",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "treatment_duration_type": "continuous"
    }
  ],
  "conditions": [
    {
      "condition_name": "active relapsing-remitting multiple sclerosis",
      "therapeutic_area": "neurology_psychiatry",
      "disease_setting": "chronic",
      "biomarker_defined_population": false
    }
  ],
  "comparators": [
    {
      "comparator_name": "blended comparator (beta interferons, glatiramer acetate)",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": false
    },
    {
      "comparator_name": "glatiramer acetate",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "interferon beta-1a (Rebif-44)",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "TEMSO",
      "study_design": "RCT",
      "phase": "phase III",
      "is_pivotal": true,
      "primary_outcome": "annualised relapse rate",
      "sample_size": 1088
    },
    {
      "trial_name": "TOWER",
      "study_design": "RCT",
      "phase": "phase III",
      "is_pivotal": true,
      "primary_outcome": "annualised relapse rate",
      "sample_size": 1169
    },
    {
      "trial_name": "TENERE",
      "study_design": "RCT",
      "phase": "phase III",
      "is_pivotal": false,
      "primary_outcome": "time to failure (relapse or discontinuation)",
      "sample_size": 324
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "company",
    "time_horizon": "lifetime (50 years)",
    "cycle_length": "1 year",
    "health_states": ["RRMS EDSS 0-7 (8 states)", "SPMS EDSS 0-9 (10 states)", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "Whether to use post-2000 MTC (base case) or all-years MTC or adjusted all-years MTC",
      "company_position": "Post-2000 MTC preferred (changes in diagnostic criteria)",
      "erg_position": "Post-2000 MTC excluded key placebo-controlled trials; all-years MTC with baseline relapse rate covariate preferred",
      "committee_preference": "Accepted adjusted all-years MTC as most appropriate",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "comparator_selection",
      "description": "Whether blended comparator or individual comparators should be used",
      "company_position": "Blended comparator based on UK market share",
      "erg_position": "Blended comparator inappropriate; masks individual treatment effects",
      "committee_preference": "Agreed individual comparisons more appropriate",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "treatment_effect_waning",
      "description": "Whether treatment effect wanes over time",
      "company_position": "Initially assumed constant effect; revised to 75% at 2 years, 50% at 5 years",
      "erg_position": null,
      "committee_preference": "Accepted treatment waning in revised base case",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "utility_source",
      "description": "Whether to use Orme et al. survey data or TEMSO trial EQ-5D data",
      "company_position": "Used Orme et al. (lower utilities)",
      "erg_position": "Preferred TEMSO trial data with Orme et al. increments for high EDSS states",
      "committee_preference": "Accepted ERG preferred approach",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "missing_subgroup_data",
      "description": "Very small subgroups for highly active and rapidly evolving severe RRMS from TEMSO (n=11 and n=33)"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "teriflunomide vs glatiramer acetate (with PAS)",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "equality_issues_raised": false
  },
  "cross_references": [
    {
      "referenced_ta": "TA32",
      "relationship": "same_condition",
      "context": "Beta interferon and glatiramer acetate for MS"
    },
    {
      "referenced_ta": "TA127",
      "relationship": "same_condition",
      "context": "Natalizumab for highly active RRMS"
    },
    {
      "referenced_ta": "TA254",
      "relationship": "same_condition",
      "context": "Fingolimod for highly active RRMS"
    }
  ]
}
```

**Extraction notes:** Complex MTC (mixed treatment comparison) methodological decisions are well captured. The "blended comparator" concept is unusual and hard to classify under `comparator_type`. The 20-state Markov model (EDSS 0-9 x RRMS/SPMS) is captured in a simplified way. The restriction "only if NOT highly active" is a negative restriction which is unusual.

---

## TA341 -- Apixaban for DVT/PE (2015, STA)

```json
{
  "ta_number": "TA341",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Apixaban for the treatment and secondary prevention of deep vein thrombosis and/or pulmonary embolism",
    "issue_date": "February 2015",
    "recommendation_type": "recommended",
    "restriction_details": "Recommended within its marketing authorisation as an option for treating and preventing recurrent DVT and PE in adults",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee",
    "erg_or_eag_name": "Liverpool Reviews and Implementation Group",
    "line_of_therapy": "first_line",
    "methods_guide_era": "2013"
  },
  "interventions": [
    {
      "generic_name": "apixaban",
      "brand_name": "Eliquis",
      "manufacturer": "Bristol-Myers Squibb and Pfizer",
      "drug_class": "direct oral anticoagulant (factor Xa inhibitor)",
      "mechanism_of_action": "directly inhibits factor Xa, inhibiting thrombin formation",
      "route_of_administration": "oral",
      "is_combination_regimen": false,
      "treatment_duration_type": "continuous"
    }
  ],
  "conditions": [
    {
      "condition_name": "deep vein thrombosis and/or pulmonary embolism (treatment and secondary prevention)",
      "therapeutic_area": "cardiovascular",
      "disease_setting": "acute",
      "biomarker_defined_population": false
    }
  ],
  "comparators": [
    {
      "comparator_name": "enoxaparin/warfarin",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "rivaroxaban",
      "comparator_type": "active_drug",
      "is_established_practice": true
    },
    {
      "comparator_name": "dabigatran etexilate",
      "comparator_type": "active_drug",
      "is_established_practice": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "AMPLIFY",
      "study_design": "non_inferiority",
      "is_pivotal": true,
      "primary_outcome": "recurrent symptomatic VTE or VTE-related death (non-inferiority)",
      "sample_size": 5395,
      "generalisability_concern": true
    },
    {
      "trial_name": "AMPLIFY-EXT",
      "study_design": "RCT",
      "is_pivotal": true,
      "primary_outcome": "symptomatic recurrent VTE or all-cause death",
      "sample_size": 2482
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "company",
    "time_horizon": "lifetime (to age 100)",
    "cycle_length": "3 months",
    "health_states": ["DVT index", "PE index", "recurrent DVT", "recurrent PE", "intracranial bleed", "non-intracranial major bleed", "clinically relevant non-major bleed", "CTEPH", "PTS", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "Whether NMA2 (secondary prevention) was appropriate given heterogeneous trial follow-up periods",
      "company_position": "NMA results valid; different periods do not substantially affect results",
      "erg_position": "NMA2 inappropriate due to very different follow-up (6 to 37 months); only direct evidence from AMPLIFY-EXT reliable",
      "committee_preference": "Agreed NMA results should be interpreted with caution; could not differentiate between DOACs for bleeding",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "cost_assumption",
      "description": "INR monitoring costs for warfarin",
      "company_position": "6 visits in first 3 months, 3 per quarter thereafter",
      "erg_position": "Values within range of previous appraisals",
      "committee_preference": "Accepted as within range; noted no agreed values established",
      "impact_on_icer": "decreases"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No head-to-head trials comparing apixaban with rivaroxaban or dabigatran"
    },
    {
      "gap_type": "missing_subgroup_data",
      "description": "Insufficient data for people with active cancer"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none"
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "apixaban vs enoxaparin/warfarin",
    "is_committee_preferred": true,
    "uncertainty_level": "low"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "equality_issues_raised": false
  },
  "cross_references": [
    {
      "referenced_ta": "TA327",
      "relationship": "same_condition",
      "context": "Dabigatran for treatment and secondary prevention of DVT/PE"
    },
    {
      "referenced_ta": "TA287",
      "relationship": "same_condition",
      "context": "Rivaroxaban for treating PE"
    },
    {
      "referenced_ta": "TA261",
      "relationship": "same_condition",
      "context": "Rivaroxaban for treatment of DVT"
    }
  ]
}
```

**Extraction notes:** Non-inferiority study design not well served by `study_design` enum (needs `non_inferiority` option). The dual-purpose (treatment AND secondary prevention) creates ambiguity for `disease_setting` -- is it "acute" or "chronic"? Both apply. The manufacturer field "Bristol-Myers Squibb and Pfizer" (joint venture) is fine as a string.

---

## TA455 -- Biologics for psoriasis in children (2017, MTA)

```json
{
  "ta_number": "TA455",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Adalimumab, etanercept and ustekinumab for treating plaque psoriasis in children and young people",
    "issue_date": "June 2017",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Adalimumab (age>=4), etanercept (age>=6), ustekinumab (age>=12) all recommended for severe psoriasis (PASI>=10) after failure of standard systemic therapy. Stopping rules: etanercept at 12 weeks, adalimumab/ustekinumab at 16 weeks if no PASI 75. Start with cheapest biosimilar option.",
    "appraisal_type": "MTA",
    "committee_name": "Appraisal Committee B",
    "erg_or_eag_name": "Assessment Group (not named in document)",
    "line_of_therapy": "third_line_plus",
    "methods_guide_era": "2013"
  },
  "interventions": [
    {
      "generic_name": "adalimumab",
      "brand_name": "Humira",
      "manufacturer": "AbbVie",
      "drug_class": "TNF-alpha inhibitor",
      "route_of_administration": "subcutaneous"
    },
    {
      "generic_name": "etanercept",
      "brand_name": "Enbrel",
      "manufacturer": "Pfizer",
      "drug_class": "TNF-alpha inhibitor",
      "route_of_administration": "subcutaneous"
    },
    {
      "generic_name": "ustekinumab",
      "brand_name": "Stelara",
      "manufacturer": "Janssen",
      "drug_class": "interleukin inhibitor (IL-12/IL-23)",
      "route_of_administration": "subcutaneous"
    }
  ],
  "conditions": [
    {
      "condition_name": "severe chronic plaque psoriasis in children and young people",
      "therapeutic_area": "dermatology",
      "disease_setting": "chronic",
      "biomarker_defined_population": false
    }
  ],
  "comparators": [
    {
      "comparator_name": "best supportive care (non-biological systemic treatment)",
      "comparator_type": "best_supportive_care",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "methotrexate",
      "comparator_type": "active_drug",
      "is_established_practice": true
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "Assessment Group",
    "time_horizon": "6-14 years (until age 18)",
    "health_states": ["trial period", "continued use", "best supportive care", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "utility_source",
      "description": "Whether children's quality of life gains should use mapped paediatric data or adult utility values",
      "company_position": null,
      "erg_position": "Mapped PedsQL to EQ-5D-Y; resulted in lower utility gains than adults",
      "committee_preference": "Concluded it is implausible that children benefit less than adults; applied most optimistic adult utility gains",
      "impact_on_icer": "decreases"
    },
    {
      "decision_category": "cost_assumption",
      "description": "Number of hospitalisation days with best supportive care (0 vs 6.49 bed days/year)",
      "company_position": "6.49 bed days per year (from Fonia et al.)",
      "erg_position": "0 days (based on clinical expert advice)",
      "committee_preference": "Concluded likely value between 0 and 6.49; this had important effect on ICER",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "other",
      "description": "Whether fully incremental analysis or pairwise comparison with BSC is appropriate for decision-making",
      "company_position": null,
      "erg_position": null,
      "committee_preference": "Concluded pairwise comparison with BSC more appropriate because incremental analysis would create age-based differential recommendations (equality concern) and incremental QALYs were highly uncertain",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No common comparator in paediatric trials; NMA required adult data with adjustments"
    },
    {
      "gap_type": "missing_quality_of_life_data",
      "description": "No EQ-5D-Y data collected in trials; mapping from PedsQL uncertain"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "none"
  },
  "icer_band": {
    "band": "20k_to_30k",
    "comparison_pair": "each biologic vs best supportive care",
    "is_committee_preferred": true,
    "uncertainty_level": "high"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "equality_issues_raised": true,
    "innovation_acknowledged": false
  },
  "cross_references": [
    {
      "referenced_ta": "TA103",
      "relationship": "same_drug_different_indication",
      "context": "Adult psoriasis guidance for etanercept and adalimumab"
    }
  ]
}
```

**Extraction notes:** The equality issue (PASI underestimating severity in darker skin) is well captured. The paediatric-specific challenges (mapping child QoL instruments, carer disutility) are methodological decisions not well categorised by existing decision_categories. "Carer disutility" is a missing concept. The time horizon "until age 18" is unusual and not captured well.

---

## TA694 -- Bempedoic acid for cholesterol (2021, STA)

```json
{
  "ta_number": "TA694",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Bempedoic acid with ezetimibe for treating primary hypercholesterolaemia or mixed dyslipidaemia",
    "issue_date": "March 2021",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Recommended only if: statins contraindicated or not tolerated; ezetimibe alone insufficient; company provides commercial arrangement",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee C",
    "erg_or_eag_name": null,
    "line_of_therapy": "third_line_plus",
    "methods_guide_era": "2013"
  },
  "interventions": [
    {
      "generic_name": "bempedoic acid",
      "brand_name": "Nilemdo",
      "manufacturer": "Daiichi Sankyo",
      "drug_class": "ACL inhibitor (cholesterol synthesis inhibitor)",
      "mechanism_of_action": "inhibits cholesterol synthesis in liver; inactive in skeletal muscle (unlike statins)",
      "route_of_administration": "oral",
      "is_combination_regimen": true,
      "combination_components": ["bempedoic acid", "ezetimibe"],
      "treatment_duration_type": "continuous"
    }
  ],
  "conditions": [
    {
      "condition_name": "primary hypercholesterolaemia (heterozygous familial and non-familial) or mixed dyslipidaemia",
      "therapeutic_area": "cardiovascular",
      "disease_setting": "chronic",
      "biomarker_defined_population": true,
      "biomarker_name": "LDL-C levels (thresholds vary by population)"
    }
  ],
  "comparators": [
    {
      "comparator_name": "ezetimibe alone",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "alirocumab or evolocumab",
      "comparator_type": "active_drug",
      "is_established_practice": true
    }
  ],
  "economic_model": {
    "model_type": "markov",
    "model_source": "company",
    "time_horizon": "lifetime"
  },
  "methodological_decisions": [
    {
      "decision_category": "indirect_comparison_method",
      "description": "Network meta-analyses had high clinical and statistical heterogeneity; multiple iterations required",
      "company_position": "Broad network including all relevant trials",
      "erg_position": "Restricted network to trials where all patients had ezetimibe at baseline; updated ERG NMA preferred",
      "committee_preference": "ERG's updated NMA (restricted to ezetimibe-at-baseline patients) preferred and most suitable",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "surrogate_endpoint_validity",
      "description": "Whether LDL-C reduction validly predicts cardiovascular outcomes for bempedoic acid",
      "company_position": "Used Cholesterol Treatment Trialist Collaboration meta-analysis relationship (from statin data)",
      "erg_position": null,
      "committee_preference": "Accepted LDL-C to CV outcome link but would have liked direct cardiovascular outcomes evidence",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "treatment_effect_waning",
      "description": "Whether 12-week LDL-C reduction is maintained long-term",
      "company_position": "12-week effect maintained throughout model",
      "erg_position": "Possible slight waning beyond 12 weeks in some trials, but unclear if same waning occurs with comparators",
      "committee_preference": "Concluded uncertainty in long-term treatment effect",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "subgroup_definition",
      "description": "Whether subgroup analyses by HeFH and CV risk status were valid",
      "company_position": "Assumed common treatment effect across subgroups",
      "erg_position": "CLEAR trials not designed for these subgroup analyses; underpowered",
      "committee_preference": "Concluded subgroup analyses insufficient; cannot assume common treatment effect",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "surrogate_not_validated",
      "description": "No direct cardiovascular outcomes data for bempedoic acid; reliance on LDL-C as surrogate"
    },
    {
      "gap_type": "missing_subgroup_data",
      "description": "Cannot appropriately do subgroup analyses by HeFH and CV risk status due to trial limitations"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "commercial_access_agreement",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "bempedoic acid + ezetimibe vs ezetimibe alone (population 2a, with CAA)",
    "is_committee_preferred": true,
    "uncertainty_level": "high"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "equality_issues_raised": false
  },
  "cross_references": []
}
```

**Extraction notes:** The "population 2a / 2b" labelling used in the document is a population segmentation not captured by the schema. The cost-saving + QALY-loss analysis for population 2b (where threshold logic reverses) is methodologically interesting but hard to standardise. The iterative NMA refinement process (multiple rounds of committee-ERG exchange) is common in modern TAs but the schema only captures the final outcome.

---

## TA719 -- Secukinumab for nr-axSpA (2021, STA)

```json
{
  "ta_number": "TA719",
  "doc_type": "FAD",
  "appraisal_metadata": {
    "title": "Secukinumab for treating non-radiographic axial spondyloarthritis",
    "issue_date": "May 2021",
    "recommendation_type": "recommended_with_restrictions",
    "restriction_details": "Recommended only if: TNF-alpha inhibitors are not suitable or have not controlled condition well enough; with PAS discount. Response assessment at 16 weeks (BASDAI reduction >=50% or >=2 units AND spinal pain VAS reduction >=2cm)",
    "appraisal_type": "STA",
    "committee_name": "Appraisal Committee A",
    "erg_or_eag_name": null,
    "line_of_therapy": "second_line",
    "methods_guide_era": "2013"
  },
  "interventions": [
    {
      "generic_name": "secukinumab",
      "brand_name": "Cosentyx",
      "manufacturer": "Novartis",
      "drug_class": "interleukin-17A inhibitor",
      "mechanism_of_action": "monoclonal antibody targeting IL-17A",
      "route_of_administration": "subcutaneous",
      "is_combination_regimen": false,
      "treatment_duration_type": "continuous"
    }
  ],
  "conditions": [
    {
      "condition_name": "active non-radiographic axial spondyloarthritis with objective signs of inflammation",
      "therapeutic_area": "musculoskeletal",
      "disease_setting": "chronic",
      "biomarker_defined_population": true,
      "biomarker_name": "elevated CRP or MRI evidence of inflammation"
    }
  ],
  "comparators": [
    {
      "comparator_name": "TNF-alpha inhibitors as a class (adalimumab biosimilar cheapest)",
      "comparator_type": "active_drug",
      "is_established_practice": true,
      "committee_preferred": true
    },
    {
      "comparator_name": "conventional care (NSAIDs and physical therapies)",
      "comparator_type": "best_supportive_care",
      "is_established_practice": true,
      "committee_preferred": true
    }
  ],
  "clinical_trials": [
    {
      "trial_name": "PREVENT",
      "study_design": "RCT",
      "is_pivotal": true,
      "primary_outcome": "ASAS 40 response at week 16",
      "sample_size": 371,
      "generalisability_concern": true
    }
  ],
  "economic_model": {
    "model_type": "decision_tree_plus_markov",
    "model_source": "company",
    "time_horizon": "lifetime",
    "health_states": ["induction/trial period", "biologic treatment", "conventional care", "death"]
  },
  "methodological_decisions": [
    {
      "decision_category": "comparator_selection",
      "description": "Whether to use average TNF-alpha inhibitor costs or cheapest biosimilar (adalimumab)",
      "company_position": "Used weighted average TNF-alpha inhibitor costs from market share data",
      "erg_position": "Adalimumab biosimilar costs most appropriate for first-line TNF-alpha inhibitor",
      "committee_preference": "Agreed adalimumab biosimilar costs best represent first-line TNF-alpha inhibitor costs",
      "impact_on_icer": "increases"
    },
    {
      "decision_category": "indirect_comparison_method",
      "description": "NMA results uncertain; cannot exclude possibility secukinumab less effective than TNF-alpha inhibitors",
      "company_position": "Clinical efficacy not expected to differ substantially from TNF-alpha inhibitors",
      "erg_position": "NMA appropriate but too few trials to check consistency or estimate heterogeneity",
      "committee_preference": "Concluded NMA results uncertain; cannot exclude secukinumab being less effective",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "other",
      "description": "Whether to use common or conditional baselines (response-conditional baseline BASDAI/BASFI)",
      "company_position": "Conditional baselines (responders have different baseline characteristics)",
      "erg_position": "Common baselines preferred (consistent with previous NICE appraisals)",
      "committee_preference": "Concluded this was an area of substantial uncertainty",
      "impact_on_icer": "uncertain_direction"
    },
    {
      "decision_category": "treatment_sequencing",
      "description": "Whether to model further biologic treatment after first-line failure",
      "company_position": "Base case: no further biologic after failure (conventional care only)",
      "erg_position": "Sequence model better reflects pathway (secukinumab then TNF vs TNF then TNF)",
      "committee_preference": "Concluded sequence model better reflects treatment pathway but relies on common baselines",
      "impact_on_icer": "uncertain_direction"
    }
  ],
  "evidence_gaps": [
    {
      "gap_type": "no_direct_comparison",
      "description": "No trials directly comparing secukinumab with TNF-alpha inhibitors for nr-axSpA"
    },
    {
      "gap_type": "missing_subgroup_data",
      "description": "Less than 10% of PREVENT had prior TNF-alpha inhibitor; limited data for most likely NHS use population"
    }
  ],
  "commercial_arrangement": {
    "arrangement_type": "simple_discount_pas",
    "discount_confidential": true,
    "critical_for_recommendation": true
  },
  "icer_band": {
    "band": "below_20k",
    "comparison_pair": "secukinumab vs conventional care (with PAS)",
    "is_committee_preferred": true,
    "uncertainty_level": "moderate"
  },
  "special_considerations": {
    "end_of_life_considered": false,
    "equality_issues_raised": true,
    "innovation_acknowledged": false
  },
  "cross_references": [
    {
      "referenced_ta": null,
      "relationship": "same_condition",
      "context": "NICE technology appraisal guidance on TNF-alpha inhibitors for nr-axSpA (number not specified in document)"
    },
    {
      "referenced_ta": null,
      "relationship": "same_drug_different_indication",
      "context": "NICE technology appraisal guidance on secukinumab for active ankylosing spondylitis"
    }
  ]
}
```

**Extraction notes:** The biosimilar competition dynamic (adalimumab biosimilar being cheapest, driving cost comparisons) is increasingly common in modern TAs but has no dedicated schema concept. The "same_drug_different_indication" relationship is useful but TA numbers were not specified in the document. The equality issue here is about BASDAI/VAS questionnaire accessibility, not PASI skin colour.

---

## Schema Critique

### What worked well

1. **Core entity structure is sound.** The TechnologyAppraisal -> Intervention -> Condition -> Comparator chain maps naturally to every document. The 1:N relationship for multi-intervention TAs (TA103, TA161, TA455) works correctly.

2. **MethodologicalDecision is the most valuable entity.** Every single TA had 2-5 extractable methodological disputes. The `company_position` / `erg_position` / `committee_preference` triple captures the core deliberation pattern. This is the entity that makes the knowledge graph differentiated from a simple catalogue.

3. **decision_categories cover ~85% of cases.** Categories like `comparator_selection`, `indirect_comparison_method`, `utility_source`, `cost_assumption`, `treatment_effect_waning`, `stopping_rule`, `model_structure`, and `treatment_sequencing` were all used across these 10 TAs. This validates the taxonomy.

4. **EvidenceGap entity is useful.** `no_direct_comparison`, `short_follow_up`, `missing_subgroup_data`, and `surrogate_not_validated` were all used. These directly predict recommendation uncertainty.

5. **Cross-references work well.** Older TAs reference newer ones, and the `relationship` field (same_condition, same_drug_different_indication, comparator_guidance) differentiates the reason usefully.

6. **icer_band as categorical works.** Avoiding specific numbers and using bands is feasible. The `below_20k` and `20k_to_30k` bands were the most common for recommended technologies.

### What was MISSING from the schema

1. **`therapeutic_area` enum is missing several areas.** Needed: `gastroenterology` (TA211 constipation, TA200 hepatitis C liver disease), `rheumatology` (TA719 could be musculoskeletal but spondyloarthritis is typically rheumatology). The current `infectious_disease` covers hepatitis C but feels wrong since it's really about liver disease management.

2. **`comparator_type` enum is missing values.** Needed: `placebo`, `best_supportive_care`, `no_treatment`, `same_drug_different_regimen` (TA200 shortened vs standard duration). Currently the enum isn't even defined in the ontology -- it's left implicit.

3. **No concept for population restrictions by demographics.** TA211 is restricted to women only. TA161 is restricted to postmenopausal women. TA455 has age-specific recommendations (4+, 6+, 12+). There's no `eligible_population` field to capture sex, age range, or other demographic restrictions.

4. **No concept for treatment sequencing within a single TA.** TA161 establishes a 4-tier hierarchy (alendronate -> risedronate/etidronate -> raloxifene/strontium ranelate -> teriparatide). TA455 establishes 2nd-line and 3rd-line positioning. TA719 positions secukinumab after TNF-alpha inhibitors. The `line_of_therapy` field captures only one value per TA, but many TAs define a full pathway.

5. **No concept for response criteria / stopping rules as structured data.** Multiple TAs (TA103, TA455, TA719) define specific stopping rules (PASI 75 at 12/16 weeks; BASDAI reduction at 16 weeks). These are currently buried in `restriction_details` as free text. A structured `response_criteria` entity with `assessment_timepoint`, `response_measure`, `response_threshold` fields would enable powerful cross-TA queries.

6. **No concept for "part review" or "update" relationship.** TA200 is a part review of TA75 and TA106. This is different from SUPERSEDES. It's more like "AMENDS_PARTIALLY".

7. **No field for biosimilar availability.** TA455 and TA719 both discuss biosimilar competition as a key cost driver. A flag or field for `biosimilar_available` on Intervention would be useful.

8. **Carer disutility / carer QoL.** TA455 explicitly discusses carer disutility for children with psoriasis. The schema has no way to capture this.

### What was AMBIGUOUS

1. **`disease_setting` enum doesn't fit non-cancer conditions well.** "metastatic", "locally_advanced", "adjuvant", "neoadjuvant", "extended_adjuvant", "maintenance" are all oncology terms. For the 10 non-cancer TAs, almost everything falls into "chronic" or "acute". The enum needs general medical options like `prevention_primary`, `prevention_secondary`, `relapsing_remitting`, `treatment_and_prevention`.

2. **`line_of_therapy` is ambiguous for multi-line TAs.** TA161 recommends 6 drugs across 4 lines. TA303 is first-line for "active" RRMS but NOT for "highly active" RRMS. TA719 is second-line (after TNF-alpha inhibitor failure) for the recommended population. Should `line_of_therapy` capture the recommended position or the full scope?

3. **`recommendation_type` "optimised" is unclear.** None of these 10 used it. Is it the same as "recommended_with_restrictions"? In practice, NICE uses "optimised" for the post-2022 methods era. Suggest adding a definition.

4. **`impact_on_icer` values are not clearly defined.** The extraction prompt shows `uncertain_direction` but the ontology doesn't define allowed values. Suggest formalising: `increases`, `decreases`, `uncertain_direction`, `negligible`.

5. **When is `is_combination_regimen` true?** Ticagrelor + aspirin is a combination (TA236). Peginterferon + ribavirin is a combination (TA200). But bempedoic acid + ezetimibe (TA694) -- the FDC is a combination, but is it a "regimen"? The line between a single product and a combination regimen blurs with fixed-dose combinations.

### What was REDUNDANT or never used

1. **`severity_modifier_applied`** -- never applicable to any of these 10 (only applies to post-2022 methods). Still worth keeping for future TAs.

2. **`cancer_drugs_fund_considered` / `cancer_drugs_fund_eligible`** -- correctly never triggered for this non-cancer set. Not redundant, just not applicable to this test set.

3. **`crossover_occurred` / `crossover_adjusted` on ClinicalTrial** -- never relevant in these 10. These are cancer-specific (survival endpoint trials). Not redundant for oncology.

4. **`blinding` on ClinicalTrial** -- extractable in maybe 3 of 10 TAs (PLATO, prucalopride trials). Most older MTAs don't discuss blinding in the FAD text. Low extraction yield.

### What would Haiku struggle with

1. **Multi-intervention MTAs.** TA161 (6 drugs) and TA455 (3 drugs) require extracting separate interventions and understanding their relative positioning. A cheap model might merge them or miss some.

2. **Distinguishing company vs ERG vs committee positions.** The prompt captures these as a triple, but the text interleaves them across paragraphs. Haiku would likely confuse who said what, especially in TA303 where there are 3 different MTC analyses.

3. **Conditional ICER interpretation.** TA103: the "base case" ICER is ~65k but the "relevant subgroup" ICER is ~14k. TA694: population 2a has a positive ICER, population 2b has a negative ICER (cost-saving, QALY-losing). Mapping these to `icer_band` requires nuanced understanding.

4. **Cross-reference extraction.** Older documents reference TAs by description ("NICE technology appraisal guidance on TNF-alpha inhibitors") without giving the TA number. Haiku would need to either infer the number or leave it null.

5. **The "other" decision_category.** Three TAs required "other" for novel methodological decisions: net benefit framework (TA200), fully incremental vs pairwise (TA455), common vs conditional baselines (TA719). A cheap model might force these into wrong categories.

6. **Free-text `restriction_details`.** Extracting the precise restriction wording requires careful reading. TA161's matrix-style recommendation (lookup tables by age/T-score/risk factors) is particularly hard to summarise.

### Specific proposed changes

**Add to enums:**
- `therapeutic_area`: add `gastroenterology`, `rheumatology`, `immunology`
- `disease_setting`: add `prevention_secondary`, `relapsing_remitting`, `treatment_and_prevention`
- `comparator_type` (new enum): `["active_drug", "placebo", "best_supportive_care", "no_treatment", "same_drug_different_regimen", "standard_of_care"]`
- `study_design`: add `non_inferiority` to existing list
- `impact_on_icer` (new enum): `["increases", "decreases", "uncertain_direction", "negligible"]`

**Add fields:**
- `TechnologyAppraisal.eligible_population`: free text for demographic restrictions (sex, age range)
- `TechnologyAppraisal.supersedes_partially`: list of TA numbers partially updated
- `Intervention.biosimilar_available`: boolean
- New entity `ResponseCriteria`: `{ assessment_timepoint, response_measure, response_threshold, action_if_not_met }`

**Add decision_categories:**
- `net_benefit_framework` -- for cost-saving-but-less-effective analyses
- `carer_utility` -- for paediatric/dependent populations
- `baseline_characteristics` -- for common vs conditional baseline disputes
- `network_heterogeneity` -- broader than `indirect_comparison_method`, for NMA quality/restriction debates

**Modify:**
- `line_of_therapy` should allow multiple values (array) to capture recommended position AND alternative positions within the same TA
- `cross_references.relationship` should add `partially_updates` value

**Remove:** Nothing. Every field was usable in at least some TAs.
