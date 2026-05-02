# Ontology Proposal for NICE Technology Appraisal Knowledge Graph

**Agent A -- Exploration Cycle**
**Based on reading 10 FADs (TA92, TA178, TA249, TA400, TA540, TA733, TA854, TA877, TA943, TA1027) and 8 scope comment files**

---

## 1. Entity Types

### 1.1 TechnologyAppraisal
**Definition:** A single NICE technology appraisal, identified by its TA number. This is the root entity from which most relations originate. It represents the full decision process including scoping, evidence review, committee deliberation, and final recommendation.

**Examples:**
- TA249: Dabigatran etexilate for the prevention of stroke and systemic embolism in atrial fibrillation (2012, recommended)
- TA854: Esketamine nasal spray for treatment-resistant depression (2022, not recommended)
- TA1027: Tebentafusp for treating advanced uveal melanoma (2025, not recommended)

**Key attributes:**
- `ta_number` (string): e.g. "TA249"
- `title` (string): full title
- `year` (integer): year of FAD publication
- `appraisal_type` (enum): STA | MTA | HST
- `recommendation` (enum): recommended | recommended_with_restrictions | recommended_for_CDF | recommended_only_in_research | not_recommended
- `committee` (string): e.g. "Committee A"
- `chair` (string): name of committee chair
- `review_date` (string): scheduled review date if mentioned

### 1.2 Technology
**Definition:** The intervention being appraised. May be a pharmaceutical drug, biologic, medical device, or digital health technology. A single TA may appraise multiple technologies (e.g., TA178 appraised bevacizumab, sorafenib, sunitinib, and temsirolimus together).

**Examples:**
- Dabigatran etexilate (Pradaxa, Boehringer Ingelheim) -- oral anticoagulant, thrombin inhibitor
- Nivolumab + ipilimumab (Opdivo + Yervoy, Bristol-Myers Squibb) -- checkpoint inhibitor combination
- HealOzone (KaVo) -- ozone-delivering medical device for dental caries
- Hybrid closed loop systems (multiple manufacturers) -- insulin pump + CGM + algorithm

**Key attributes:**
- `generic_name` (string)
- `brand_name` (string)
- `manufacturer` (string)
- `technology_type` (enum): small_molecule | biologic | biosimilar | device | digital_health | combination_regimen
- `mechanism_of_action` (string): free text, e.g. "PD-1 checkpoint inhibitor"
- `route_of_administration` (enum): oral | intravenous | subcutaneous | nasal | topical | implanted | other
- `is_combination` (boolean): whether this is a combination regimen

### 1.3 Condition
**Definition:** The disease, condition, or clinical context for which the technology is appraised. Expressed in terms of the specific indication, not just the broad disease category.

**Examples:**
- Non-valvular atrial fibrillation (for stroke prevention) -- TA249
- Advanced (unresectable or metastatic) melanoma -- TA400
- Treatment-resistant depression (not responded to >=2 antidepressants) -- TA854
- Type 1 diabetes (blood glucose management) -- TA943

**Key attributes:**
- `condition_name` (string)
- `icd_code` (string, optional)
- `disease_area` (enum): oncology | cardiovascular | neurology_psychiatry | metabolic_endocrine | renal | respiratory | musculoskeletal | dental | ophthalmology | dermatology | infectious_disease | haematology | other
- `severity` (string, optional): e.g., "advanced/metastatic", "treatment-resistant"
- `rarity` (enum): common | uncommon | rare | ultra_rare

### 1.4 Comparator
**Definition:** A treatment or strategy against which the technology is compared in the clinical and cost-effectiveness evidence. May be an active drug, best supportive care, placebo, or watchful waiting. Crucially, the committee often disputes which comparator is most relevant.

**Examples:**
- Warfarin (dose-adjusted) -- comparator for dabigatran in TA249
- Pembrolizumab -- deemed most relevant comparator for nivolumab+ipilimumab in TA400 even though not in scope
- Best supportive care -- comparator for sorafenib 2nd-line in TA178
- Investigator's choice (pembrolizumab 82%, ipilimumab 13%, dacarbazine 6%) -- TA1027

**Key attributes:**
- `comparator_name` (string)
- `comparator_type` (enum): active_drug | best_supportive_care | placebo | standard_of_care_mix | watchful_waiting | no_treatment
- `committee_preferred` (boolean): whether the committee considered this the most relevant comparator
- `in_scope` (boolean): whether the comparator was in the original scope

### 1.5 ClinicalTrial
**Definition:** A specific clinical trial cited as key evidence in the appraisal. Identified by name or registry number.

**Examples:**
- RE-LY (NCT00262600): non-inferiority RCT, dabigatran vs warfarin, n=18113 -- TA249
- CheckMate-067: 3-arm RCT, nivolumab+ipilimumab vs nivolumab vs ipilimumab, advanced melanoma -- TA400
- KEYNOTE-087: single-arm, pembrolizumab in relapsed/refractory classical Hodgkin lymphoma -- TA540
- FIDELIO-DKD: phase 3, double-blind, finerenone vs placebo + standard care, CKD + T2D, n>5000 -- TA877

**Key attributes:**
- `trial_name` (string)
- `trial_design` (enum): RCT_superiority | RCT_non_inferiority | single_arm | randomised_discontinuation | observational | expanded_access
- `blinding` (enum): open_label | single_blind | double_blind | not_reported
- `sample_size` (integer, optional)
- `primary_endpoint` (string)
- `is_pivotal` (boolean): whether this was the key trial for the appraisal

### 1.6 EconomicModel
**Definition:** The cost-effectiveness model used in the appraisal. Captures model structure and key methodological choices. One TA typically has a company model and may have an ERG/Assessment Group alternative.

**Examples:**
- Markov model with 3 disability levels + death (TA249 dabigatran, manufacturer)
- Partitioned survival model with 3 states: PFS, progressed disease, death (TA1027, TA400)
- State-transition model with 5 states: MDE, response, remission, recovery, death (TA854 esketamine)
- Cohort-level state-transition Markov model with CKD stages + CV sub-models (TA877 finerenone)

**Key attributes:**
- `model_type` (enum): markov_cohort | partitioned_survival | decision_tree | microsimulation | patient_level_simulation | mixed
- `health_states` (list of strings): e.g. ["progression_free", "progressed_disease", "death"]
- `time_horizon` (string): e.g. "lifetime", "20 years", "5 years"
- `cycle_length` (string): e.g. "3 months", "4 months", "1 week"
- `perspective` (enum): NHS_PSS | societal
- `discount_rate` (string): e.g. "3.5%"
- `source` (enum): company | ERG | assessment_group | DSU

### 1.7 UtilitySource
**Definition:** The source used to derive health-state utility values in the economic model. This is a recurrent area of committee scrutiny.

**Examples:**
- EQ-5D sub-study of RE-LY trial (TA249) -- used for baseline utility in AF
- Utility values from TA358 (tolvaptan for ADPKD) reused for CKD stages in TA877
- Time-to-death utilities derived from TA357 (pembrolizumab for melanoma), applied in TA1027
- MADRS-mapped EQ-5D-5L from TRANSFORM-2 (TA854)

**Key attributes:**
- `instrument` (enum): EQ_5D_3L | EQ_5D_5L | HUI3 | SF_6D | VAS | TTO | SG | other
- `derivation` (enum): trial_direct | trial_mapped | literature | vignette | expert_opinion
- `mapping_method` (string, optional): e.g. "EQ-5D-5L mapped to 3L"
- `previous_ta_source` (string, optional): if reusing utilities from a prior TA
- `committee_accepted` (boolean)

### 1.8 PatientAccessScheme
**Definition:** A commercial arrangement between the company and NHS/Department of Health that modifies the effective price. Includes simple discounts, dose caps, free initial supply, and complex outcomes-based schemes.

**Examples:**
- Simple discount on ipilimumab list price (TA400) -- commercial in confidence
- First pack of sorafenib free to NHS (TA178)
- Bevacizumab: rebate after 10g per patient per year + free IFN-alpha when co-administered (TA178)
- Commercial access agreement for inclisiran (TA733) -- discount size confidential

**Key attributes:**
- `scheme_type` (enum): simple_discount | dose_cap | free_initiation | outcomes_based | commercial_access_agreement
- `confidential` (boolean)
- `applied_to_which_drug` (string)

### 1.9 CommitteeDecisionFactor
**Definition:** A specific methodological or evidentiary issue that the committee explicitly deliberated on and that influenced the recommendation. These are the "pivot points" of the appraisal.

**Examples:**
- "INR monitoring cost estimate drives cost-effectiveness" (TA249)
- "2-year stopping rule not clinically justified" (TA1027)
- "Post-progression survival modelling biggest driver of CE" (TA400)
- "Excluding people with suicidal ideation limits generalisability to NHS" (TA854)
- "RECIST criteria may not capture tebentafusp benefit -- PFS not sensitive measure" (TA1027)
- "Treatment-dependent vs treatment-independent disability/mortality after stroke" (TA249)

**Key attributes:**
- `factor_type` (enum): clinical_uncertainty | model_structure | parameter_choice | generalisability | comparator_relevance | subgroup_validity | treatment_duration | stopping_rule | extrapolation_choice | cost_estimate | utility_estimate | treatment_waning | crossover_adjustment | end_of_life | innovation | equality
- `description` (string): concise free-text description
- `direction` (enum): favours_technology | favours_comparator | uncertain | neutral
- `resolved` (boolean): whether the committee reached a clear conclusion

### 1.10 EvidenceGap
**Definition:** An explicit gap in the evidence that the committee highlighted, often leading to research recommendations or CDF entry.

**Examples:**
- "No direct comparison of inclisiran with ezetimibe, alirocumab, or evolocumab" (TA733)
- "Overall survival data from CheckMate-067 immature" (TA400)
- "No long-term cardiovascular outcomes data for inclisiran" (TA733)
- "No UK recruitment in TRANSFORM-2 and SUSTAIN-1 trials" (TA854)
- "No evidence for effectiveness of immunotherapies in uveal melanoma" (TA1027)

**Key attributes:**
- `gap_type` (enum): immature_OS | no_direct_comparison | no_UK_data | surrogate_not_validated | missing_subgroup | missing_QoL | short_follow_up | no_comparator_data
- `description` (string)
- `recommended_research` (string, optional): what NICE recommended to address the gap

### 1.11 EndOfLifeCriteria
**Definition:** Whether and how the end-of-life (EOL) criteria were applied. Requires: life expectancy <24 months with current treatment, and extension >= 3 months.

**Examples:**
- Met: TA540 pembrolizumab Hodgkin lymphoma, TA1027 tebentafusp (met but ICER still too high)
- Not formally considered: TA400 nivolumab+ipilimumab (cost-effective without EOL)
- Met but contested: TA178 sorafenib/temsirolimus (met EOL criteria but ICERs still too high)
- Not applicable: TA249 dabigatran, TA733 inclisiran, TA877 finerenone

**Key attributes:**
- `applied` (boolean)
- `life_expectancy_met` (enum): yes | no | uncertain
- `extension_met` (enum): yes | no | uncertain
- `outcome` (enum): criteria_met | criteria_not_met | not_considered | not_applicable

### 1.12 CancerDrugsFund
**Definition:** Whether the technology was considered for or recommended through the Cancer Drugs Fund, including what data collection was proposed.

**Examples:**
- TA540: pembrolizumab recommended in CDF for population 2 (transplant-ineligible)
- TA1027: tebentafusp considered for CDF but ICER too high, not recommended
- Most non-oncology TAs: not applicable

**Key attributes:**
- `considered` (boolean)
- `recommended_for_CDF` (boolean)
- `data_collection_proposed` (list of strings)
- `data_collection_end_date` (string, optional)

---

## 2. Relation Types

### 2.1 APPRAISES
**Definition:** Links a TechnologyAppraisal to the Technology being appraised.
**Example:** TA249 --APPRAISES--> Dabigatran etexilate

### 2.2 INDICATED_FOR
**Definition:** Links a Technology to the Condition it is indicated for in this appraisal context.
**Example:** Dabigatran --INDICATED_FOR--> Non-valvular atrial fibrillation (stroke prevention)

### 2.3 COMPARED_WITH
**Definition:** Links a TechnologyAppraisal to a Comparator. Includes whether this was the committee-preferred comparator.
**Example:** TA400 --COMPARED_WITH {committee_preferred: true}--> Pembrolizumab
**Example:** TA1027 --COMPARED_WITH {in_scope: true}--> Dacarbazine

### 2.4 CITES_TRIAL
**Definition:** Links a TechnologyAppraisal to a ClinicalTrial that provided key evidence.
**Example:** TA249 --CITES_TRIAL {role: "pivotal"}--> RE-LY
**Example:** TA400 --CITES_TRIAL {role: "pivotal"}--> CheckMate-067

### 2.5 USES_MODEL
**Definition:** Links a TechnologyAppraisal to the EconomicModel used.
**Example:** TA877 --USES_MODEL {source: "company"}--> Markov CKD state-transition model

### 2.6 USES_UTILITY_FROM
**Definition:** Links an EconomicModel to its UtilitySource.
**Example:** TA877 model --USES_UTILITY_FROM--> TA358 (tolvaptan ADPKD utilities)

### 2.7 HAS_PAS
**Definition:** Links a TechnologyAppraisal to a PatientAccessScheme.
**Example:** TA400 --HAS_PAS--> Simple discount on ipilimumab

### 2.8 HAS_DECISION_FACTOR
**Definition:** Links a TechnologyAppraisal to a CommitteeDecisionFactor.
**Example:** TA854 --HAS_DECISION_FACTOR--> "Excluding suicidal ideation limits NHS generalisability"

### 2.9 HAS_EVIDENCE_GAP
**Definition:** Links a TechnologyAppraisal to an EvidenceGap.
**Example:** TA733 --HAS_EVIDENCE_GAP--> "No long-term cardiovascular outcomes data"

### 2.10 APPLIES_EOL
**Definition:** Links a TechnologyAppraisal to an EndOfLifeCriteria assessment.
**Example:** TA1027 --APPLIES_EOL--> {criteria_met: true, outcome: "met but ICER too high"}

### 2.11 REFERENCES_TA
**Definition:** Links one TechnologyAppraisal to another that is referenced (e.g., for precedent on utility values, comparator pricing, or methodological decisions).
**Example:** TA877 --REFERENCES_TA {reason: "utility values for CKD stages"}--> TA358
**Example:** TA540 --REFERENCES_TA {reason: "nivolumab cost-effectiveness comparison"}--> TA462

### 2.12 SUPERSEDES_IN_PATHWAY
**Definition:** Links a Technology to another Technology it has replaced or largely superseded in clinical practice, as described by clinical experts.
**Example:** Pembrolizumab/Nivolumab --SUPERSEDES_IN_PATHWAY--> Ipilimumab monotherapy (in first-line melanoma, per TA400 clinical expert testimony)

### 2.13 CONSIDERED_FOR_CDF
**Definition:** Links a TechnologyAppraisal to a CancerDrugsFund assessment.
**Example:** TA540 --CONSIDERED_FOR_CDF--> {recommended: true, population: "population 2"}

---

## 3. Proposed JSON Extraction Schema

This schema is designed for a cheap model (Haiku/Flash Lite) to fill in when processing a 3-page chunk of a FAD. Not all fields will be populated from every chunk. The model should output `null` for fields where no relevant information appears in the chunk.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "chunk_metadata": {
      "type": "object",
      "properties": {
        "ta_number": { "type": "string", "description": "e.g. TA249" },
        "page_range": { "type": "string", "description": "e.g. 1-3" },
        "section_type": {
          "type": "string",
          "enum": ["guidance", "technology_description", "clinical_need", "clinical_effectiveness", "cost_effectiveness", "committee_discussion", "implementation", "appendix", "other"]
        }
      },
      "required": ["ta_number"]
    },

    "technology": {
      "type": ["object", "null"],
      "properties": {
        "generic_name": { "type": "string" },
        "brand_name": { "type": ["string", "null"] },
        "manufacturer": { "type": ["string", "null"] },
        "technology_type": {
          "type": "string",
          "enum": ["small_molecule", "biologic", "biosimilar", "device", "digital_health", "combination_regimen"]
        },
        "mechanism_of_action": { "type": ["string", "null"] },
        "route_of_administration": {
          "type": "string",
          "enum": ["oral", "intravenous", "subcutaneous", "nasal", "topical", "implanted", "other"]
        }
      }
    },

    "condition": {
      "type": ["object", "null"],
      "properties": {
        "condition_name": { "type": "string" },
        "disease_area": {
          "type": "string",
          "enum": ["oncology", "cardiovascular", "neurology_psychiatry", "metabolic_endocrine", "renal", "respiratory", "musculoskeletal", "dental", "ophthalmology", "dermatology", "infectious_disease", "haematology", "other"]
        },
        "severity": { "type": ["string", "null"] },
        "rarity": {
          "type": "string",
          "enum": ["common", "uncommon", "rare", "ultra_rare"]
        }
      }
    },

    "recommendation": {
      "type": ["object", "null"],
      "properties": {
        "decision": {
          "type": "string",
          "enum": ["recommended", "recommended_with_restrictions", "recommended_for_CDF", "recommended_only_in_research", "not_recommended"]
        },
        "restriction_details": { "type": ["string", "null"] },
        "icer_band": {
          "type": ["string", "null"],
          "enum": ["below_20k", "20k_to_30k", "30k_to_50k", "above_50k", "not_reported", null],
          "description": "Committee's preferred/most plausible ICER range"
        },
        "year": { "type": ["integer", "null"] }
      }
    },

    "comparators": {
      "type": ["array", "null"],
      "items": {
        "type": "object",
        "properties": {
          "comparator_name": { "type": "string" },
          "comparator_type": {
            "type": "string",
            "enum": ["active_drug", "best_supportive_care", "placebo", "standard_of_care_mix", "watchful_waiting", "no_treatment"]
          },
          "committee_preferred": { "type": "boolean" },
          "in_scope": { "type": "boolean" }
        },
        "required": ["comparator_name"]
      }
    },

    "clinical_trials": {
      "type": ["array", "null"],
      "items": {
        "type": "object",
        "properties": {
          "trial_name": { "type": "string" },
          "trial_design": {
            "type": "string",
            "enum": ["RCT_superiority", "RCT_non_inferiority", "single_arm", "randomised_discontinuation", "observational", "expanded_access"]
          },
          "blinding": {
            "type": "string",
            "enum": ["open_label", "single_blind", "double_blind", "not_reported"]
          },
          "sample_size": { "type": ["integer", "null"] },
          "primary_endpoint": { "type": ["string", "null"] },
          "is_pivotal": { "type": "boolean" }
        },
        "required": ["trial_name"]
      }
    },

    "economic_model": {
      "type": ["object", "null"],
      "properties": {
        "model_type": {
          "type": "string",
          "enum": ["markov_cohort", "partitioned_survival", "decision_tree", "microsimulation", "patient_level_simulation", "mixed"]
        },
        "health_states": {
          "type": ["array", "null"],
          "items": { "type": "string" }
        },
        "time_horizon": { "type": ["string", "null"] },
        "cycle_length": { "type": ["string", "null"] },
        "source": {
          "type": "string",
          "enum": ["company", "ERG", "assessment_group", "DSU"]
        }
      }
    },

    "utility_sources": {
      "type": ["array", "null"],
      "items": {
        "type": "object",
        "properties": {
          "instrument": {
            "type": "string",
            "enum": ["EQ_5D_3L", "EQ_5D_5L", "HUI3", "SF_6D", "VAS", "TTO", "SG", "other"]
          },
          "derivation": {
            "type": "string",
            "enum": ["trial_direct", "trial_mapped", "literature", "vignette", "expert_opinion"]
          },
          "source_description": { "type": ["string", "null"] },
          "from_previous_ta": { "type": ["string", "null"] },
          "committee_accepted": { "type": ["boolean", "null"] }
        }
      }
    },

    "patient_access_scheme": {
      "type": ["object", "null"],
      "properties": {
        "scheme_type": {
          "type": "string",
          "enum": ["simple_discount", "dose_cap", "free_initiation", "outcomes_based", "commercial_access_agreement"]
        },
        "confidential": { "type": "boolean" },
        "applied_to": { "type": ["string", "null"] }
      }
    },

    "decision_factors": {
      "type": ["array", "null"],
      "items": {
        "type": "object",
        "properties": {
          "factor_type": {
            "type": "string",
            "enum": ["clinical_uncertainty", "model_structure", "parameter_choice", "generalisability", "comparator_relevance", "subgroup_validity", "treatment_duration", "stopping_rule", "extrapolation_choice", "cost_estimate", "utility_estimate", "treatment_waning", "crossover_adjustment", "end_of_life", "innovation", "equality"]
          },
          "description": { "type": "string" },
          "direction": {
            "type": "string",
            "enum": ["favours_technology", "favours_comparator", "uncertain", "neutral"]
          }
        },
        "required": ["factor_type", "description"]
      }
    },

    "evidence_gaps": {
      "type": ["array", "null"],
      "items": {
        "type": "object",
        "properties": {
          "gap_type": {
            "type": "string",
            "enum": ["immature_OS", "no_direct_comparison", "no_UK_data", "surrogate_not_validated", "missing_subgroup", "missing_QoL", "short_follow_up", "no_comparator_data"]
          },
          "description": { "type": "string" }
        },
        "required": ["gap_type", "description"]
      }
    },

    "end_of_life": {
      "type": ["object", "null"],
      "properties": {
        "applied": { "type": "boolean" },
        "life_expectancy_met": {
          "type": "string",
          "enum": ["yes", "no", "uncertain"]
        },
        "extension_met": {
          "type": "string",
          "enum": ["yes", "no", "uncertain"]
        },
        "outcome": {
          "type": "string",
          "enum": ["criteria_met", "criteria_not_met", "not_considered", "not_applicable"]
        }
      }
    },

    "cancer_drugs_fund": {
      "type": ["object", "null"],
      "properties": {
        "considered": { "type": "boolean" },
        "recommended": { "type": "boolean" },
        "data_to_collect": {
          "type": ["array", "null"],
          "items": { "type": "string" }
        }
      }
    },

    "referenced_tas": {
      "type": ["array", "null"],
      "items": {
        "type": "object",
        "properties": {
          "ta_number": { "type": "string" },
          "reason": { "type": "string" }
        }
      }
    },

    "survival_extrapolation": {
      "type": ["object", "null"],
      "properties": {
        "method": {
          "type": "string",
          "enum": ["weibull", "log_logistic", "log_normal", "gompertz", "exponential", "generalised_gamma", "spline", "piecewise", "kaplan_meier_with_tail", "other"]
        },
        "company_preferred": { "type": ["string", "null"] },
        "erg_preferred": { "type": ["string", "null"] },
        "committee_preferred": { "type": ["string", "null"] },
        "is_key_driver": { "type": ["boolean", "null"] }
      }
    },

    "innovation": {
      "type": ["object", "null"],
      "properties": {
        "considered_innovative": { "type": "boolean" },
        "step_change_claimed": { "type": "boolean" },
        "uncaptured_benefits": { "type": "boolean", "description": "Whether committee identified benefits not in QALY" },
        "description": { "type": ["string", "null"] }
      }
    }
  }
}
```

---

## 4. What NOT to Extract (with Reasoning)

### 4.1 Specific numerical results (ICERs, QALYs, costs)
**Do not extract:** exact ICER values (e.g., "£18,900 per QALY gained"), exact QALY gains, exact costs, exact hazard ratios.
**Why:** (1) Many are commercially confidential and redacted. (2) They change across scenarios and sensitivity analyses -- extracting one number without full context is misleading. (3) Numerical precision requires human verification. (4) A cheap model will hallucinate numbers. **Exception:** We DO capture the committee's preferred ICER *band* (below 20k, 20-30k, 30-50k, above 50k) as this is a categorical judgement.

### 4.2 Appendix content (committee member lists, consultee lists)
**Do not extract:** Names of individual committee members, lists of consultee organisations, project team members.
**Why:** This is administrative metadata that adds bulk without analytical value. Committee chairs are captured at the TA level. Organisational participation could be a separate database if needed.

### 4.3 Detailed clinical trial results
**Do not extract:** Specific efficacy numbers (median PFS/OS, response rates, hazard ratios with CIs), subgroup forest plots, adverse event rates.
**Why:** These are better captured from structured clinical trial registries (ClinicalTrials.gov) and are too numerous and context-dependent for reliable extraction from prose. What matters for cross-TA queries is the *design* and *committee's interpretation* of the trial, not the raw numbers.

### 4.4 Page-level formatting artefacts
**Do not extract:** Page numbers, headers/footers, "Final Healozone FAD for consultation 030605.doc", repeated title lines, redacted picture placeholders.
**Why:** These are OCR/conversion artefacts with no semantic value.

### 4.5 Dosage and pharmacokinetic details
**Do not extract:** Specific dosing regimens (e.g., "150 mg twice daily"), pharmacokinetic parameters, drug interaction lists, contraindication details.
**Why:** This information is better sourced from SPCs/BNF and changes over time. The ontology focuses on HTA decision reasoning, not clinical pharmacology.

### 4.6 Implementation and audit details
**Do not extract:** NHS implementation timelines, costing templates, audit tools, Welsh Assembly Minister directions.
**Why:** Boilerplate text that is essentially identical across TAs and has no analytical value for cross-TA comparison.

---

## 5. Surprising Patterns / Things a Naive Ontology Designer Would Miss

### 5.1 The comparator is frequently disputed and often changes during the appraisal
A naive designer would model the comparator as a simple attribute. In reality, it is one of the most contested aspects. In TA400, the scope included ipilimumab but the committee concluded pembrolizumab was the "most clinically relevant" comparator -- even though the company didn't submit that comparison initially. In TA854, the company positioned esketamine against placebo+oral antidepressant, but the committee argued augmentation therapy was the real-world comparator. The ontology must allow multiple comparators per TA with explicit `committee_preferred` and `in_scope` flags.

### 5.2 Older TAs (pre-2010) have fundamentally different structures
TA92 (2005) has no structured "committee discussion" section -- it interleaves evidence with committee consideration. It uses "Assessment Group" rather than "ERG". The numbering schemes differ. TA178 (2009) appraises 4 drugs simultaneously across multiple treatment lines. Any extraction system must handle these structural variations gracefully. The schema should not require fields that only exist in post-2016 documents.

### 5.3 Cross-referencing between TAs is a critical feature
Committees routinely reference decisions from other TAs. TA877 reuses utility values from TA358. TA540 explicitly compares its cost-effectiveness with TA462 (nivolumab for Hodgkin lymphoma). TA400 notes that its review should coincide with reviews of TA268, TA319, TA357, TA366. TA854 references TA for vortioxetine for utility comparisons. These cross-references encode a "precedent network" that would be extremely valuable for pharma companies preparing submissions.

### 5.4 The "stopping rule" and "treatment duration" issue is pervasive and underappreciated
Virtually every oncology TA and many others (esketamine, inclisiran, finerenone) involve debate about how long treatment continues. Companies often propose 2-year caps. Committees reject or accept these based on clinical evidence (or lack thereof). This interacts directly with costs and drives the ICER substantially. In TA1027, removing the 2-year stopping rule was a major post-consultation change. This must be a first-class decision factor, not buried in free text.

### 5.5 The "ICER band" concept needs nuance for end-of-life cases
When end-of-life criteria are met, the acceptable ICER threshold shifts from £20-30k to up to £50k. In TA1027, the committee explicitly stated the threshold was £50,000 for end-of-life and found the ICER above this. In TA178, even meeting end-of-life criteria was insufficient because ICERs were >£60k. The schema needs to capture both the applicable threshold AND whether the ICER was above/below it.

### 5.6 Medical devices and digital health technologies create different evidence challenges
TA92 (HealOzone) and TA943 (hybrid closed loop) face entirely different evidence requirements than pharmaceuticals. Device appraisals contend with: lack of blinding possibility, rapid technology iteration, user competence requirements, and implementation costs. The ontology should accommodate these without forcing device-specific fields into every record.

### 5.7 The "company vs ERG preferred" assumptions pattern is universal
In every TA from ~2010 onward, there is a structured tension: the company presents assumptions (model type, survival curves, utility values, costs) and the ERG/assessment group proposes alternatives. The committee then picks a preferred set. This "assumption negotiation" is the core of HTA decision-making. The `survival_extrapolation` entity captures one aspect, but this pattern extends to utility values, treatment waning, resource use, and more.

### 5.8 Cancer Drugs Fund has specific procedural implications that changed over time
The CDF was introduced in 2016 with reformed processes. TA540 (2018) uses the "reformed CDF" pathway, which includes managed access agreements and specified data collection. Earlier oncology TAs (TA178, TA400) predate the reformed CDF. This temporal evolution means the same term "Cancer Drugs Fund" has different procedural meanings across TAs.

### 5.9 Equality issues are formulaic but occasionally substantive
Most TAs conclude "no equality issues." But some (TA943 HCL diabetes) identify real issues: ethnic minority access to technology, socioeconomic barriers, learning difficulties. TA854 (esketamine) identifies geographic access as a potential equality concern. The scope comments reveal that equality arguments are occasionally used strategically by companies (e.g., tebentafusp arguing for HST pathway due to rarity).

### 5.10 Surrogate endpoint validation is a recurring cross-cutting theme
Inclisiran (TA733) uses LDL-C reduction as a surrogate for cardiovascular events, referencing the CTT meta-analysis. Finerenone (TA877) uses a composite renal endpoint. Oncology TAs frequently debate PFS vs OS. The committee's acceptance or rejection of surrogates is a high-value queryable pattern: "In which TAs has NICE accepted LDL-C as a surrogate for CV events?"

---

## 6. Open Questions / Areas of Uncertainty in the Schema

### 6.1 How to handle multi-indication TAs?
TA178 appraises 4 drugs across 6 treatment strategy questions. Should this be modeled as one TechnologyAppraisal with four Technologies and six sub-appraisals? Or six separate records sharing a TA number? The current schema assumes 1:many TA-to-Technology, but the decision logic is per-strategy, not per-TA.

### 6.2 How granular should CommitteeDecisionFactors be?
TA854 (esketamine) has approximately 30 distinct deliberative points. TA92 (HealOzone) has perhaps 5. Should we aim for a fixed number per TA, or allow unlimited extraction? Too many dilutes signal; too few misses key reasoning. Proposal: cap at 10 most significant factors per TA.

### 6.3 Should we model the timeline of committee deliberation?
Several TAs (TA249, TA540, TA854, TA877, TA1027) had multiple committee meetings with evolving positions. The company revised its model between meetings. Should we capture this temporal evolution, or just the final position? **Proposed:** Only capture the final position, but note the number of committee meetings as a complexity indicator.

### 6.4 How to handle confidential (CIC/AIC) information?
Many ICERs, PAS discounts, and some clinical data are redacted. The schema should gracefully handle `null` for these. But should we flag that a value was confidential (and therefore exists but is hidden) vs truly absent? **Proposed:** Add an optional `is_confidential` flag where relevant.

### 6.5 Treatment pathway position vs line of therapy
The concept of "line of therapy" works for oncology but not well for depression (TA854), cholesterol (TA733), CKD (TA877), or dental caries (TA92). A more general concept is "position in treatment pathway" which might be: first-line, second-line, add-on, alternative, last-resort, or specific-subgroup. This needs careful enumeration.

### 6.6 Should the schema capture the company's clinical positioning vs the committee's?
In TA854, the company initially positioned esketamine for the full marketing authorisation population, then narrowed to 3+ treatments subgroup, then to 3+ treatments + augmentation. The committee's final judgement may differ from the company's positioning. Both are valuable for understanding the negotiation. **Proposed:** Capture `company_positioning` and `committee_conclusion` separately.

### 6.7 How to handle the scope comments data?
Scope comments are structurally different (tabular comment-response pairs) and contain different information (stakeholder concerns, definitional debates). They could be extracted as separate entities linked to the TA, or integrated into the CommitteeDecisionFactor framework. **Proposed:** Create a lightweight `ScopeComment` entity with `stakeholder`, `topic`, and `NICE_response` fields, linked to the TA. Extract only if the scope comment is referenced in the FAD itself.

### 6.8 Temporal evolution of NICE methods
NICE's methods guide changed significantly between 2004, 2008, 2013, and 2022. The 2022 methods manual introduces "severity modifier" replacing end-of-life criteria. TA1027 explicitly notes that if re-reviewed under the new methods, end-of-life criteria would not apply. Should the schema capture which methods guide was applicable? **Proposed:** Yes, add `methods_guide_version` to TechnologyAppraisal (enum: pre_2008 | 2008 | 2013 | 2022).
