# Ontology Proposal: NICE Technology Appraisal Knowledge Graph (Agent B)

Based on close reading of 10 FADs spanning 2003-2024 (TA70, TA276, TA310, TA467, TA612, TA810, TA891, TA903, TA959, TA1011) plus 6 scope comment files.

---

## 1. Entity Types

### 1.1 TechnologyAppraisal

The top-level entity representing a single NICE TA process and its outcome.

**Definition:** A formal NICE evaluation of a health technology, identified by its TA number, resulting in guidance (recommended, recommended with restrictions, optimised, not recommended, or recommended for CDF).

**Examples:**
- TA70: Imatinib for chronic myeloid leukaemia (2003, recommended)
- TA310: Afatinib for EGFR mutation-positive NSCLC (2014, recommended with restrictions)
- TA959: Daratumumab for systemic AL amyloidosis (2022, not recommended)

**Attributes:**
- `ta_number` (string): e.g. "TA70"
- `title` (string): full title as it appears in the document
- `issue_date` (string): month and year, e.g. "August 2003"
- `recommendation_type` (enum): "recommended" | "recommended_with_restrictions" | "optimised" | "not_recommended" | "recommended_for_cdf"
- `appraisal_type` (enum): "STA" | "MTA" | "HST" | "fast_track" | "unknown"
- `committee_name` (string): e.g. "Committee A", "Committee B", "Committee C"
- `committee_chair` (string): name of the chair
- `erg_or_eag_name` (string): name of the ERG/EAG/Assessment Group
- `is_cancer` (boolean)
- `uses_cancer_drugs_fund` (boolean)
- `end_of_life_criteria_met` (boolean)
- `severity_modifier_applied` (boolean)
- `innovation_acknowledged` (boolean)

### 1.2 Intervention

A drug, device, cell therapy, or other technology being appraised.

**Definition:** The specific health technology (or combination) under evaluation, including its brand name, generic/INN name, manufacturer, and mechanism of action.

**Examples:**
- Imatinib (Glivec, Novartis): BCR-ABL tyrosine kinase inhibitor
- Holoclar (Chiesi Farmaceutici): ex vivo expanded autologous human corneal epithelial cells containing stem cells
- Ibrutinib + venetoclax (Imbruvica + Venclyxto, Janssen-Cilag / AbbVie): BTK inhibitor + BCL-2 inhibitor

**Attributes:**
- `generic_name` (string): INN or generic name, e.g. "imatinib"
- `brand_name` (string): e.g. "Glivec"
- `manufacturer` (string): company name
- `drug_class` (string): pharmacological class, e.g. "tyrosine kinase inhibitor"
- `mechanism_of_action` (string): brief description of MOA
- `route_of_administration` (enum): "oral" | "intravenous" | "subcutaneous" | "inhaled" | "topical" | "other"
- `is_combination_regimen` (boolean)
- `combination_components` (list of strings): if combination, list the components
- `treatment_duration_type` (enum): "fixed_duration" | "treat_to_progression" | "continuous" | "cyclical" | "other"

### 1.3 Condition

The disease or clinical condition being treated.

**Definition:** The medical condition addressed by the technology, at a level of specificity matching the marketing authorisation (i.e., not just "cancer" but "EGFR mutation-positive locally advanced or metastatic NSCLC").

**Examples:**
- Philadelphia-chromosome-positive chronic myeloid leukaemia in chronic phase
- Chronic pulmonary infection caused by Pseudomonas aeruginosa in cystic fibrosis
- Hormone receptor-positive, HER2-negative, node-positive early breast cancer at high risk of recurrence

**Attributes:**
- `condition_name` (string): full name as described in the appraisal
- `therapeutic_area` (string): broad area, e.g. "oncology", "respiratory", "ophthalmology", "haematology"
- `disease_setting` (enum): "early" | "locally_advanced" | "metastatic" | "chronic" | "acute" | "adjuvant" | "neoadjuvant" | "maintenance" | "other"
- `is_orphan_or_ultra_orphan` (boolean)
- `biomarker_defined_population` (boolean): whether the population requires a specific biomarker test
- `biomarker_name` (string, optional): e.g. "Philadelphia chromosome", "EGFR mutation", "HER2"

### 1.4 Comparator

A treatment option against which the intervention is compared.

**Definition:** A specific treatment (drug, regimen, procedure, or best supportive care) used as a reference point for assessing relative clinical and cost effectiveness.

**Examples:**
- Interferon-alpha (IFN-alpha) for CML (TA70)
- Erlotinib and gefitinib for EGFR+ NSCLC (TA310)
- Endocrine therapy alone for HR+/HER2- early breast cancer (TA810)

**Attributes:**
- `comparator_name` (string): name of the comparator
- `is_active_comparator` (boolean): vs. placebo or BSC
- `is_established_practice` (boolean): whether the committee accepted it as current standard of care
- `nice_recommended` (boolean, optional): whether NICE has previously recommended this comparator
- `relevant_nice_ta` (string, optional): if the comparator was appraised by NICE, the TA number

### 1.5 ClinicalTrial

A clinical study providing evidence for the appraisal.

**Definition:** A specific clinical trial or study cited as providing key evidence in the appraisal, identified by its name/acronym and design characteristics.

**Examples:**
- IRIS trial: phase III RCT of imatinib vs IFN-alpha + Ara-C in newly diagnosed CML (TA70)
- LUX-Lung 3: phase III open-label RCT of afatinib vs cisplatin + pemetrexed in EGFR+ NSCLC (TA310)
- GLOW: phase III open-label RCT of ibrutinib + venetoclax vs obinutuzumab + chlorambucil in untreated CLL (TA891)

**Attributes:**
- `trial_name` (string): acronym or identifier, e.g. "IRIS", "LUX-Lung 3", "monarchE"
- `study_design` (enum): "RCT" | "single_arm" | "case_series" | "observational" | "non_inferiority" | "other"
- `phase` (string): e.g. "phase III", "phase II"
- `blinding` (enum): "double_blind" | "open_label" | "single_blind" | "unknown"
- `is_pivotal` (boolean): whether this is the main study driving the appraisal decision
- `primary_outcome` (string): e.g. "progression-free survival", "overall haematological response"
- `sample_size` (integer, optional)
- `crossover_occurred` (boolean)
- `crossover_adjusted` (boolean)
- `generalisability_concern_raised` (boolean): whether the committee or ERG raised concerns about generalisability to the UK/NHS population

### 1.6 EconomicModel

The cost-effectiveness model used in the appraisal.

**Definition:** A description of the economic modelling approach used by the company or ERG/EAG to estimate the cost effectiveness of the intervention.

**Examples:**
- Markov model with 5 health states (TA70: chronic phase, accelerated phase, blast crisis, post-SCT, dead)
- Partitioned survival model with 3 states: pre-progression, post-progression, death (TA310)
- Decision tree followed by Markov model with response-stratified survival (TA959)

**Attributes:**
- `model_type` (enum): "markov" | "partitioned_survival" | "decision_tree" | "semi_markov" | "discrete_event_simulation" | "cost_minimisation" | "decision_tree_plus_markov" | "other"
- `model_source` (enum): "company" | "erg" | "assessment_group" | "both"
- `time_horizon` (string): e.g. "lifetime", "10 years", "24 weeks"
- `cycle_length` (string): e.g. "1 month", "28 days", "3 months"
- `health_states` (list of strings): names of model health states
- `perspective` (string): e.g. "NHS and PSS"
- `discount_rate_costs` (string): e.g. "3.5%"
- `discount_rate_outcomes` (string): e.g. "3.5%"

### 1.7 MethodologicalDecision

A specific methodological choice or assumption that the committee discussed, disputed, or resolved.

**Definition:** A named methodological issue in the appraisal where the committee had to choose between alternative approaches or assumptions. This is the most analytically valuable entity type for cross-TA querying.

**Examples:**
- Survival extrapolation curve choice: log-logistic vs lognormal for invasive disease-free survival (TA810)
- Treatment effect waning assumption: company assumed 8 years full effect + 19 years waning; ERG assumed 3 years full + 5 years waning (TA810)
- Proportional hazards assumption: committee concluded the assumption was violated in the mixed treatment comparison (TA310)

**Attributes:**
- `decision_category` (enum): "survival_extrapolation" | "treatment_effect_duration" | "treatment_effect_waning" | "indirect_comparison_method" | "utility_source" | "utility_value_choice" | "discount_rate" | "surrogate_endpoint_validity" | "comparator_selection" | "population_generalisability" | "subgroup_definition" | "crossover_adjustment" | "proportional_hazards" | "cost_assumption" | "stopping_rule" | "model_structure" | "other"
- `description` (string): brief description of the issue
- `company_position` (string): what the company proposed
- `erg_position` (string): what the ERG/EAG proposed
- `committee_preference` (string): what the committee preferred/concluded
- `impact_on_icer` (enum): "increases_icer" | "decreases_icer" | "uncertain_direction" | "minimal_impact" | "not_stated"

### 1.8 CommercialArrangement

The pricing or access arrangement under which the technology is made available.

**Definition:** Any patient access scheme, commercial access agreement, managed access agreement, or other pricing arrangement between the manufacturer and the NHS.

**Examples:**
- Simple discount PAS for afatinib (TA310): confidential discount at point of purchase
- Managed access agreement for belzutifan (TA1011) via Cancer Drugs Fund with data collection requirements
- No PAS: tobramycin DPI at list price was not cost effective; PAS made it dominant (TA276)

**Attributes:**
- `arrangement_type` (enum): "simple_discount_pas" | "complex_pas" | "managed_access_agreement" | "commercial_access_agreement" | "none" | "other"
- `discount_confidential` (boolean)
- `was_critical_for_recommendation` (boolean): whether the PAS/arrangement was necessary for the positive recommendation

### 1.9 ICERBand

The committee's assessment of where the ICER falls relative to NICE willingness-to-pay thresholds.

**Definition:** A categorical representation of the ICER range as assessed by the committee, avoiding specific numerical values.

**Examples:**
- TA70: Imatinib vs IFN-alpha approximately GBP26,000/QALY -- "below_30k"
- TA310: Most plausible ICER could not be estimated; cost comparison used -- "not_estimable"
- TA959: All ICERs above the acceptable range -- "above_50k"

**Attributes:**
- `icer_band` (enum): "below_20k" | "20k_to_30k" | "30k_to_50k" | "above_50k" | "dominant" | "not_estimable" | "confidential"
- `comparison_pair` (string): what intervention vs what comparator
- `is_committee_preferred` (boolean): whether this reflects the committee's preferred assumptions
- `uncertainty_level` (enum): "low" | "moderate" | "high" | "very_high"

---

## 2. Relation Types

### 2.1 APPRAISES

**Definition:** Links a TechnologyAppraisal to the Intervention it evaluates.

**Example:** TA310 APPRAISES afatinib

### 2.2 TREATS

**Definition:** Links an Intervention to the Condition it is indicated for in this appraisal.

**Example:** Imatinib TREATS Philadelphia-chromosome-positive CML in chronic phase

### 2.3 COMPARED_WITH

**Definition:** Links an Intervention to a Comparator in the context of a specific TA. Directional: the intervention is compared with the comparator.

**Example:** Afatinib COMPARED_WITH erlotinib (TA310)

### 2.4 EVIDENCED_BY

**Definition:** Links a TechnologyAppraisal to a ClinicalTrial that provides key evidence.

**Example:** TA810 EVIDENCED_BY monarchE

### 2.5 USES_MODEL

**Definition:** Links a TechnologyAppraisal to the EconomicModel(s) considered.

**Example:** TA903 USES_MODEL partitioned survival model (3-state)

### 2.6 RAISES_ISSUE

**Definition:** Links a TechnologyAppraisal to a MethodologicalDecision that was debated.

**Example:** TA810 RAISES_ISSUE treatment effect waning (company: 8yr full + 19yr waning; ERG: 3yr full + 5yr waning)

### 2.7 HAS_ARRANGEMENT

**Definition:** Links a TechnologyAppraisal (or Intervention) to a CommercialArrangement.

**Example:** TA310 HAS_ARRANGEMENT simple discount PAS

### 2.8 PRODUCES_ICER

**Definition:** Links a TechnologyAppraisal to an ICERBand, representing the committee's view on cost effectiveness.

**Example:** TA959 PRODUCES_ICER above_50k (committee preferred assumptions)

### 2.9 SUPERSEDES / REFERENCES

**Definition:** Links one TechnologyAppraisal to another. SUPERSEDES means the new TA replaces older guidance. REFERENCES means the TA cites reasoning or precedent from another TA.

**Examples:**
- TA70 SUPERSEDES TA50 (imatinib second-line CML)
- TA810 (abemaciclib) REFERENCES TA612 (neratinib) for treatment waning assumptions
- TA903 (darolutamide) REFERENCES TA741 (apalutamide) for docetaxel disutility

### 2.10 SUBMITTED_BY

**Definition:** Links a TechnologyAppraisal to the manufacturer/sponsor who submitted the evidence.

**Example:** TA310 SUBMITTED_BY Boehringer Ingelheim

### 2.11 INVOLVES_BIOMARKER

**Definition:** Links a Condition (in the context of a TA) to the biomarker required for patient selection.

**Example:** EGFR mutation-positive NSCLC INVOLVES_BIOMARKER EGFR-TK mutation testing

---

## 3. Proposed JSON Extraction Schema

This schema is designed for a cheap model to fill in per 3-page chunk. Fields that cannot be determined from the chunk should be set to `null`. The model should only extract what is explicitly stated.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NICE TA Chunk Extraction",
  "type": "object",
  "properties": {
    "chunk_id": {
      "type": "string",
      "description": "Identifier for this chunk, e.g. 'ta310_pages_1_3'"
    },
    "ta_number": {
      "type": ["string", "null"],
      "description": "TA number if identifiable, e.g. 'TA310'"
    },

    "appraisal_metadata": {
      "type": ["object", "null"],
      "description": "Top-level appraisal facts, fill only if found in this chunk",
      "properties": {
        "title": { "type": ["string", "null"] },
        "issue_date": { "type": ["string", "null"] },
        "recommendation_type": {
          "type": ["string", "null"],
          "enum": ["recommended", "recommended_with_restrictions", "optimised", "not_recommended", "recommended_for_cdf", null]
        },
        "appraisal_type": {
          "type": ["string", "null"],
          "enum": ["STA", "MTA", "HST", "fast_track", "unknown", null]
        },
        "committee_chair": { "type": ["string", "null"] },
        "committee_name": { "type": ["string", "null"] },
        "erg_or_eag_name": { "type": ["string", "null"] }
      }
    },

    "interventions": {
      "type": "array",
      "description": "Drugs/technologies mentioned as the appraised intervention",
      "items": {
        "type": "object",
        "properties": {
          "generic_name": { "type": "string" },
          "brand_name": { "type": ["string", "null"] },
          "manufacturer": { "type": ["string", "null"] },
          "drug_class": { "type": ["string", "null"] },
          "route_of_administration": {
            "type": ["string", "null"],
            "enum": ["oral", "intravenous", "subcutaneous", "inhaled", "topical", "other", null]
          },
          "is_combination_regimen": { "type": ["boolean", "null"] },
          "combination_components": {
            "type": ["array", "null"],
            "items": { "type": "string" }
          },
          "treatment_duration_type": {
            "type": ["string", "null"],
            "enum": ["fixed_duration", "treat_to_progression", "continuous", "cyclical", "other", null]
          }
        },
        "required": ["generic_name"]
      }
    },

    "conditions": {
      "type": "array",
      "description": "Diseases/conditions mentioned as the target of the appraisal",
      "items": {
        "type": "object",
        "properties": {
          "condition_name": { "type": "string" },
          "therapeutic_area": { "type": ["string", "null"] },
          "disease_setting": {
            "type": ["string", "null"],
            "enum": ["early", "locally_advanced", "metastatic", "chronic", "acute", "adjuvant", "neoadjuvant", "maintenance", "other", null]
          },
          "biomarker_defined_population": { "type": ["boolean", "null"] },
          "biomarker_name": { "type": ["string", "null"] }
        },
        "required": ["condition_name"]
      }
    },

    "comparators": {
      "type": "array",
      "description": "Treatments the intervention is compared against",
      "items": {
        "type": "object",
        "properties": {
          "comparator_name": { "type": "string" },
          "is_active_comparator": { "type": ["boolean", "null"] },
          "is_established_practice": { "type": ["boolean", "null"] }
        },
        "required": ["comparator_name"]
      }
    },

    "clinical_trials": {
      "type": "array",
      "description": "Named trials or studies cited in this chunk",
      "items": {
        "type": "object",
        "properties": {
          "trial_name": { "type": "string" },
          "study_design": {
            "type": ["string", "null"],
            "enum": ["RCT", "single_arm", "case_series", "observational", "non_inferiority", "other", null]
          },
          "phase": { "type": ["string", "null"] },
          "blinding": {
            "type": ["string", "null"],
            "enum": ["double_blind", "open_label", "single_blind", "unknown", null]
          },
          "is_pivotal": { "type": ["boolean", "null"] },
          "primary_outcome": { "type": ["string", "null"] },
          "sample_size": { "type": ["integer", "null"] },
          "crossover_occurred": { "type": ["boolean", "null"] },
          "generalisability_concern_raised": { "type": ["boolean", "null"] }
        },
        "required": ["trial_name"]
      }
    },

    "economic_model": {
      "type": ["object", "null"],
      "description": "Economic model details if described in this chunk",
      "properties": {
        "model_type": {
          "type": ["string", "null"],
          "enum": ["markov", "partitioned_survival", "decision_tree", "semi_markov", "discrete_event_simulation", "cost_minimisation", "decision_tree_plus_markov", "other", null]
        },
        "model_source": {
          "type": ["string", "null"],
          "enum": ["company", "erg", "assessment_group", "both", null]
        },
        "time_horizon": { "type": ["string", "null"] },
        "cycle_length": { "type": ["string", "null"] },
        "health_states": {
          "type": ["array", "null"],
          "items": { "type": "string" }
        },
        "discount_rate_costs": { "type": ["string", "null"] },
        "discount_rate_outcomes": { "type": ["string", "null"] }
      }
    },

    "methodological_decisions": {
      "type": "array",
      "description": "Specific methodological issues discussed in this chunk",
      "items": {
        "type": "object",
        "properties": {
          "decision_category": {
            "type": "string",
            "enum": [
              "survival_extrapolation",
              "treatment_effect_duration",
              "treatment_effect_waning",
              "indirect_comparison_method",
              "utility_source",
              "utility_value_choice",
              "discount_rate",
              "surrogate_endpoint_validity",
              "comparator_selection",
              "population_generalisability",
              "subgroup_definition",
              "crossover_adjustment",
              "proportional_hazards",
              "cost_assumption",
              "stopping_rule",
              "model_structure",
              "other"
            ]
          },
          "description": { "type": "string" },
          "company_position": { "type": ["string", "null"] },
          "erg_position": { "type": ["string", "null"] },
          "committee_preference": { "type": ["string", "null"] },
          "impact_on_icer": {
            "type": ["string", "null"],
            "enum": ["increases_icer", "decreases_icer", "uncertain_direction", "minimal_impact", "not_stated", null]
          }
        },
        "required": ["decision_category", "description"]
      }
    },

    "commercial_arrangement": {
      "type": ["object", "null"],
      "description": "PAS or commercial arrangement details if mentioned in this chunk",
      "properties": {
        "arrangement_type": {
          "type": ["string", "null"],
          "enum": ["simple_discount_pas", "complex_pas", "managed_access_agreement", "commercial_access_agreement", "none", "other", null]
        },
        "discount_confidential": { "type": ["boolean", "null"] },
        "was_critical_for_recommendation": { "type": ["boolean", "null"] }
        }
    },

    "icer_band": {
      "type": ["object", "null"],
      "description": "ICER range if mentioned in this chunk",
      "properties": {
        "band": {
          "type": ["string", "null"],
          "enum": ["below_20k", "20k_to_30k", "30k_to_50k", "above_50k", "dominant", "not_estimable", "confidential", null]
        },
        "comparison_pair": { "type": ["string", "null"] },
        "is_committee_preferred": { "type": ["boolean", "null"] },
        "uncertainty_level": {
          "type": ["string", "null"],
          "enum": ["low", "moderate", "high", "very_high", null]
        }
      }
    },

    "cross_references": {
      "type": "array",
      "description": "References to other NICE TAs or guidelines",
      "items": {
        "type": "object",
        "properties": {
          "referenced_ta": { "type": "string", "description": "TA number or guideline ID, e.g. 'TA192', 'NG101'" },
          "relationship": {
            "type": "string",
            "enum": ["supersedes", "references_for_precedent", "same_condition", "same_drug_different_indication", "comparator_guidance"]
          },
          "context": { "type": ["string", "null"], "description": "Why is this TA referenced?" }
        },
        "required": ["referenced_ta", "relationship"]
      }
    },

    "special_considerations": {
      "type": ["object", "null"],
      "description": "Special NICE framework considerations",
      "properties": {
        "end_of_life_criteria_considered": { "type": ["boolean", "null"] },
        "end_of_life_criteria_met": { "type": ["boolean", "null"] },
        "severity_modifier_applied": { "type": ["boolean", "null"] },
        "innovation_acknowledged": { "type": ["boolean", "null"] },
        "equality_issues_raised": { "type": ["boolean", "null"] },
        "equality_issue_description": { "type": ["string", "null"] },
        "cancer_drugs_fund_considered": { "type": ["boolean", "null"] },
        "cancer_drugs_fund_eligible": { "type": ["boolean", "null"] }
      }
    }
  },
  "required": ["chunk_id"]
}
```

### Extraction Instructions for Cheap Models

When processing a 3-page chunk:

1. **Only extract what is explicitly stated.** Never infer. If a field is not mentioned, set it to `null`.
2. **Interventions and comparators**: Extract the specific names as they appear. Do not normalise drug names across chunks -- a deduplication pass will follow.
3. **Methodological decisions**: This is the highest-value extraction target. When the text describes a disagreement between company and ERG, or a committee conclusion about a modelling assumption, extract it. Look for phrases like "the committee concluded", "the ERG preferred", "the company assumed", "the committee agreed".
4. **ICER band**: Only extract if the text gives enough information to categorise. If the text says "the ICERs were within the range NICE considers acceptable" that maps to "below_30k". If it says "above the range NICE considers acceptable" that maps to "above_50k". If results are confidential and no characterisation is given, use "confidential".
5. **Cross references**: When the text mentions another NICE TA (e.g., "NICE technology appraisal guidance 192"), extract the TA number and the reason for referencing.
6. **Do not extract**: committee member lists, implementation/audit details, appendix content listing consultees, specific numerical results (hazard ratios, p-values, costs), long direct quotes.

---

## 4. What NOT to Extract (and Why)

### 4.1 Specific numerical values (ICERs, costs, QALYs, hazard ratios)

**Reason:** These are (a) frequently redacted as commercial-in-confidence, (b) context-dependent (which model run? which sensitivity analysis?), (c) hard for cheap models to extract accurately, and (d) not useful for cross-TA pattern queries. The categorical ICER band captures the decision-relevant information.

### 4.2 Committee member rosters and affiliations

**Reason:** These change every 3 years, appear in appendices, and are not analytically useful for cross-TA research. The chair name is retained because it indicates which era/committee culture was active.

### 4.3 Implementation logistics and NHS compliance timelines

**Reason:** These sections (e.g., "Section 7(6) of the NICE Constitution and Functions Regulations 2013 requires...") are boilerplate that is identical across all TAs from a given period. Zero informational value.

### 4.4 Full adverse event profiles

**Reason:** These are better sourced from SmPCs and clinical trial registries. What matters for the knowledge graph is whether adverse events were a significant committee concern or affected the recommendation, which is captured under MethodologicalDecision or as a note.

### 4.5 Patient and public involvement statements (verbatim)

**Reason:** The sentiment is captured through structured fields (e.g., innovation_acknowledged, equality_issues_raised). The specific testimony is too unstructured and variable for reliable extraction.

### 4.6 Detailed sensitivity analysis numerical results

**Reason:** There can be dozens of sensitivity analyses per TA, each with different parameter variations. These are not reliably extractable and not useful for cross-TA patterns. The key information (which parameters drove cost effectiveness) is captured under MethodologicalDecision.

### 4.7 Trial recruitment details and country-by-country breakdown

**Reason:** The key information (generalisability concerns) is captured as a boolean on the trial entity. Whether trial site X was in country Y is too granular.

---

## 5. Surprising Patterns / Things a Naive Ontology Designer Would Miss

### 5.1 The document format and vocabulary change dramatically over time

TA70 (2003) uses "Appraisal Committee", "Assessment Group", "Assessment Report", and has no structured summary table. TA310 (2014) introduces the tabular summary of key conclusions. TA612 (2019) introduces the "technical engagement" process. TA891 (2023) uses "evaluation committee" and "external assessment group (EAG)" instead of "appraisal committee" and "evidence review group (ERG)". TA1011 (2024) is a Managed Access Agreement rather than a traditional FAD. The ontology must be vocabulary-agnostic: "ERG" = "EAG" = "Assessment Group"; "appraisal committee" = "evaluation committee".

**Implication:** Extraction prompts must provide a normalisation map, or use a post-processing step to align terminology across eras.

### 5.2 The "recommendation type" is far more nuanced than recommended/not recommended

Many TAs are "recommended with restrictions" but the nature of the restrictions varies enormously:
- Restriction to a biomarker-defined subgroup (TA310: EGFR mutation-positive only)
- Restriction requiring prior treatment (TA612: after adjuvant trastuzumab)
- Restriction to one eye only (TA467: Holoclar for 1 eye)
- Restriction conditional on a PAS (nearly universal from ~2010 onwards)
- Restriction to a risk-defined subgroup not requiring a test (TA810: 4+ positive nodes OR 1-3 nodes with grade 3/tumour 5cm+)
- Recommendation via Cancer Drugs Fund with data collection (TA1011)

A simple enum is insufficient. The `recommendation_type` field should be supplemented by extracting the specific conditions as free text.

### 5.3 Treatment effect waning is a recurring flashpoint that is cross-referenced across TAs

TA810 (abemaciclib 2022) explicitly references TA612 (neratinib 2019) for its waning assumptions. TA903 (darolutamide 2023) references TA741 (apalutamide) and other prostate cancer TAs. This creates a citation network of methodological precedent that is extremely valuable for pharma companies. The `REFERENCES` relation and `cross_references` in the schema must capture these.

### 5.4 The committee often cannot estimate a "most plausible ICER"

A naive designer would assume every TA produces an ICER. In reality:
- TA310 (afatinib): "a most plausible ICER could not be estimated" because the model was deemed unreliable
- TA612 (neratinib): ICERs are entirely confidential
- TA467 (Holoclar): ICERs vary enormously by comparator (dominant vs. GBP69,000/QALY depending on which comparator)

The `not_estimable` and `confidential` categories in the ICER band are essential, as is linking the ICER to a specific comparison pair.

### 5.5 Non-cancer TAs have fundamentally different structures

TA276 (cystic fibrosis) and TA467 (Holoclar, ophthalmology) differ from the oncology TAs in:
- No end-of-life consideration
- No Cancer Drugs Fund pathway
- Different primary outcomes (FEV1% predicted rather than PFS/OS; transplant success rather than tumour response)
- Cost-effectiveness arguments based on cost savings from reduced treatment burden (nebuliser time) or avoided exacerbations, not survival gains
- The south-west quadrant of the cost-effectiveness plane (less effective but cheaper) arises in TA276, which requires different decision logic than the usual north-east quadrant

The ontology must not be oncology-centric. The `disease_setting` enum and `primary_outcome` on trials should accommodate non-cancer contexts.

### 5.6 The comparator is often the most contested element of the appraisal

In several TAs, the committee spends more time arguing about the correct comparator than about the clinical evidence:
- TA70: IFN-alpha vs hydroxyurea as comparator -- the ICER vs HU was GBP87,000/QALY but the committee accepted IFN-alpha as the relevant comparator (GBP26,000/QALY)
- TA276: Colistimethate sodium DPI was compared with nebulised tobramycin but the committee said the correct comparator should be nebulised colistimethate sodium, for which no trial existed
- TA891: Whether venetoclax+obinutuzumab (only available via CDF) should be a comparator

The `comparator_selection` category in MethodologicalDecision and the `is_established_practice` attribute on Comparator capture this.

### 5.7 Innovation and "uncaptured benefits" are used to justify ICERs above the usual threshold

TA467 (Holoclar): "Given the patient need and innovative nature of the treatment, the committee agreed that it would pragmatically accept this as a demonstration of cost effectiveness" despite ICERs of GBP30-42k/QALY against the nearest comparator. The committee was willing to accept higher ICERs because Holoclar was the first stem cell medicine.

This is captured via `innovation_acknowledged` and should be extractable. But the degree to which innovation influenced the acceptability threshold is qualitative and hard to standardise.

### 5.8 Surrogate endpoint validity is a make-or-break issue for several TAs

- TA70: Whether cytogenetic response predicts survival in CML
- TA959: Whether haematological response predicts overall survival in AL amyloidosis (committee concluded confounding was not adequately addressed, contributing to rejection)
- TA810: Whether invasive disease-free survival is a valid surrogate for overall survival in early breast cancer

This pattern occurs when OS data is immature, which is increasingly common as trials are submitted earlier. The `surrogate_endpoint_validity` category captures this explicitly.

### 5.9 The same TA can contain multiple recommendation types for subgroups

TA467 recommends Holoclar for one eye (routine commissioning) but only in the context of research for two eyes. TA276 recommends tobramycin DPI for one subgroup and colistimethate sodium DPI for a narrower subgroup with different conditions. This means the TechnologyAppraisal entity may need to link to multiple recommendation outcomes.

### 5.10 Managed Access Agreements are an entirely different document type

TA1011 (belzutifan) was not a traditional FAD -- it was a Managed Access Agreement with a data collection arrangement. These contain information about ongoing data collection timelines, Blueteq eligibility criteria, and SACT dataset requirements that are absent from standard FADs. The ontology should flag `uses_cancer_drugs_fund = true` and `arrangement_type = managed_access_agreement` but should not try to capture all the operational detail of the MAA.

---

## 6. Open Questions / Areas of Uncertainty

### 6.1 How to handle the evolving NICE process terminology

Pre-2013: "National Institute for Clinical Excellence", "Assessment Group", "Assessment Report"
2013-2022: "National Institute for Health and Care Excellence", "ERG", "Evidence Review Group"
2022+: "EAG" (External Assessment Group), "evaluation committee", "final draft guidance" instead of "final appraisal determination"

**Decision needed:** Should we normalise all terms to the latest vocabulary at extraction time, or preserve the original and normalise in post-processing? I recommend post-processing normalisation so the cheap model does not need era-specific instructions.

### 6.2 Granularity of condition entities

Should "HR+/HER2-/node-positive early breast cancer at high risk of recurrence" and "HR+/HER2+ early breast cancer" be separate condition entities, or should they share a parent entity "early breast cancer" with subtype attributes? The former is simpler for extraction; the latter enables richer queries ("show me all TAs for breast cancer").

**Recommendation:** Use a flat condition entity matching the specific marketing authorisation population, then have a separate `therapeutic_area` tag for broad grouping. Hierarchical condition ontologies (like ICD-10 or MeSH) can be linked in a second pass.

### 6.3 How many methodological decisions per TA to target

Some TAs raise 3-4 key methodological issues; TA276 and TA959 raise 10+. Should we cap the number? Uncapped extraction risks the cheap model hallucinating decisions. Capping risks missing important ones.

**Recommendation:** No cap, but instruct the model to only extract decisions where the text explicitly describes a disagreement or a committee conclusion. This naturally limits to the 3-8 most prominent issues per TA.

### 6.4 Whether to model "the ERG" as an entity

The ERG/EAG plays a critical role: its preferred ICER is often what the committee adopts. But the ERG is typically named only once per TA (e.g., "Liverpool Reviews and Implementation Group"). Is it worth tracking?

**Recommendation:** Yes, as an attribute on TechnologyAppraisal rather than a standalone entity. This allows queries like "which TAs used ScHARR as the assessment group?" without the overhead of a separate entity.

### 6.5 Handling confidential information

Many modern TAs redact: exact PAS discount, exact ICERs with discounts applied, comparator PAS details, some HR values from indirect comparisons. The extraction model will encounter "XXXX" and "[commercial in confidence]" placeholders.

**Recommendation:** The schema already handles this via null values and the "confidential" ICER band. Instruct the model: "If a value is described as commercial in confidence or redacted, set the field to null and note `discount_confidential: true` where applicable."

### 6.6 Scope comments as a separate extraction target

Scope comments contain information not in the FAD: which patient groups lobbied for the appraisal, what comparators were contested before the formal process began, and what outcome measures the manufacturer suggested. These are structured differently (table with Section/Consultee/Comment/Action columns).

**Recommendation:** Create a separate, simpler extraction schema for scope comments with fields: `consultee_name`, `consultee_type` (manufacturer/patient_group/professional_body/other), `section` (population/comparators/outcomes/etc), `comment_summary`, and `nice_action`. This is secondary to the FAD extraction.

### 6.7 Whether "treatment pathway position" deserves its own entity

Several TAs carefully describe where the intervention sits in the treatment pathway (first-line, second-line, adjuvant, extended adjuvant, maintenance). This is partially captured by `disease_setting` on the Condition entity but deserves richer modelling.

**Recommendation:** Add a `line_of_therapy` attribute to the TechnologyAppraisal or Intervention entity with values: "first_line", "second_line", "third_line_plus", "adjuvant", "neoadjuvant", "extended_adjuvant", "maintenance", "any_line". This enables queries like "show me all TAs for first-line treatments in CLL."

### 6.8 Indirect comparison methods as a high-value extraction target

The method used for indirect comparisons (NMA, MAIC, ITC, STC, none) is a key methodological choice that pharma companies need to track. The committee's acceptance or rejection of the indirect comparison method often determines the outcome.

**Recommendation:** The `indirect_comparison_method` category under MethodologicalDecision should capture this, with the `description` field specifying the method type (fixed-effects NMA, random-effects NMA, anchored MAIC, unanchored MAIC, Bucher ITC, simulated treatment comparison, etc.).
