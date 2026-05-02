"""Tool definitions for NICE TA extraction via Anthropic tool use."""

TOOLS = [
    {
        "name": "report_no_content",
        "description": "Call this when the chunk contains no extractable appraisal information — e.g. appendices, committee member lists, implementation sections, tables of numbers, administrative boilerplate, or blank pages.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "extract_appraisal_data",
        "description": "Extract structured appraisal data from a NICE Technology Appraisal chunk. Only extract what is explicitly stated. Use suggested enum values where they fit, but use a short descriptive string if none fit. A normalisation pass will follow.",
        "input_schema": {
            "type": "object",
            "properties": {
                "appraisal_metadata": {
                    "type": "object",
                    "description": "Top-level appraisal facts. Only fill fields found in this chunk.",
                    "properties": {
                        "title": {"type": "string", "description": "Full title of the appraisal"},
                        "issue_date": {"type": "string", "description": "Month and year, e.g. 'August 2023'"},
                        "recommendation_type": {"type": "string", "description": "E.g. recommended, recommended_with_restrictions, optimised, not_recommended, recommended_for_cdf"},
                        "restriction_details": {"type": "string", "description": "Details of any restrictions on the recommendation"},
                        "appraisal_type": {"type": "string", "description": "E.g. STA, MTA, HST, fast_track"},
                        "committee_name": {"type": "string"},
                        "erg_or_eag_name": {"type": "string"},
                        "line_of_therapy": {"type": "string", "description": "E.g. first_line, second_line, third_line_plus, adjuvant, maintenance"},
                    },
                },
                "interventions": {
                    "type": "array",
                    "description": "Drugs/technologies being appraised",
                    "items": {
                        "type": "object",
                        "properties": {
                            "generic_name": {"type": "string"},
                            "brand_name": {"type": "string"},
                            "manufacturer": {"type": "string"},
                            "drug_class": {"type": "string"},
                            "mechanism_of_action": {"type": "string"},
                            "route_of_administration": {"type": "string"},
                            "is_combination_regimen": {"type": "boolean"},
                            "combination_components": {"type": "array", "items": {"type": "string"}},
                            "treatment_duration_type": {"type": "string", "description": "E.g. fixed_duration, treat_to_progression, continuous, cyclical, single_administration, as_needed"},
                        },
                        "required": ["generic_name"],
                    },
                },
                "conditions": {
                    "type": "array",
                    "description": "Diseases/conditions targeted",
                    "items": {
                        "type": "object",
                        "properties": {
                            "condition_name": {"type": "string"},
                            "therapeutic_area": {"type": "string", "description": "E.g. oncology, haematology, cardiovascular, neurology_psychiatry, metabolic_endocrine, renal, respiratory, rheumatology, gastroenterology, dermatology, ophthalmology"},
                            "disease_setting": {"type": "string", "description": "E.g. early, locally_advanced, metastatic, chronic, acute, adjuvant, maintenance, relapsed_refractory, prevention_secondary"},
                            "biomarker_defined_population": {"type": "boolean"},
                            "biomarker_name": {"type": "string"},
                        },
                        "required": ["condition_name"],
                    },
                },
                "comparators": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "comparator_name": {"type": "string"},
                            "comparator_type": {"type": "string", "description": "E.g. active_drug, placebo, best_supportive_care, no_treatment, standard_of_care"},
                            "is_established_practice": {"type": "boolean"},
                            "committee_preferred": {"type": "boolean"},
                        },
                        "required": ["comparator_name"],
                    },
                },
                "clinical_trials": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "trial_name": {"type": "string"},
                            "study_design": {"type": "string", "description": "E.g. RCT, single_arm, observational, non_inferiority"},
                            "phase": {"type": "string"},
                            "blinding": {"type": "string", "description": "E.g. double_blind, open_label, single_blind"},
                            "is_pivotal": {"type": "boolean"},
                            "primary_outcome": {"type": "string"},
                            "sample_size": {"type": "integer"},
                            "crossover_occurred": {"type": "boolean"},
                            "crossover_adjusted": {"type": "boolean"},
                            "generalisability_concern": {"type": "boolean"},
                        },
                        "required": ["trial_name"],
                    },
                },
                "economic_model": {
                    "type": "object",
                    "properties": {
                        "model_type": {"type": "string", "description": "E.g. markov, partitioned_survival, decision_tree, cost_comparison, mixture_cure, patient_level_simulation"},
                        "model_source": {"type": "string", "description": "E.g. company, erg, assessment_group"},
                        "time_horizon": {"type": "string"},
                        "cycle_length": {"type": "string"},
                        "health_states": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "methodological_decisions": {
                    "type": "array",
                    "description": "HIGHEST VALUE TARGET. Extract when the text describes a disagreement between company and ERG, or a committee conclusion about a modelling assumption.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "decision_category": {
                                "type": "string",
                                "description": "E.g. survival_extrapolation, treatment_effect_waning, indirect_comparison_method, utility_source, comparator_selection, population_generalisability, crossover_adjustment, cost_assumption, stopping_rule, model_structure, treatment_sequencing, cure_assumption, mortality_assumption, equivalence_assumption, or any short descriptive string",
                            },
                            "description": {"type": "string", "description": "Brief description of the issue"},
                            "company_position": {"type": "string"},
                            "erg_position": {"type": "string"},
                            "committee_preference": {"type": "string"},
                            "impact_on_icer": {"type": "string", "description": "E.g. increases, decreases, uncertain_direction, negligible"},
                        },
                        "required": ["decision_category", "description"],
                    },
                },
                "evidence_gaps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "gap_type": {"type": "string", "description": "E.g. immature_overall_survival, no_direct_comparison, no_uk_data, surrogate_not_validated, short_follow_up, single_arm_evidence_only"},
                            "description": {"type": "string"},
                        },
                        "required": ["gap_type", "description"],
                    },
                },
                "commercial_arrangement": {
                    "type": "object",
                    "properties": {
                        "arrangement_type": {"type": "string", "description": "E.g. simple_discount_pas, complex_pas, managed_access_agreement, commercial_access_agreement, none"},
                        "discount_confidential": {"type": "boolean"},
                        "critical_for_recommendation": {"type": "boolean"},
                    },
                },
                "icer_band": {
                    "type": "object",
                    "description": "Committee's preferred ICER range. below_20k / 20k_to_30k / 30k_to_50k / 50k_to_100k / above_100k / dominant / not_estimable / confidential",
                    "properties": {
                        "band": {"type": "string"},
                        "comparison_pair": {"type": "string", "description": "E.g. 'afatinib vs erlotinib'"},
                        "is_committee_preferred": {"type": "boolean"},
                        "uncertainty_level": {"type": "string", "description": "E.g. low, moderate, high, very_high"},
                    },
                },
                "special_considerations": {
                    "type": "object",
                    "properties": {
                        "end_of_life_considered": {"type": "boolean"},
                        "end_of_life_met": {"type": "boolean"},
                        "severity_modifier_applied": {"type": "boolean"},
                        "cancer_drugs_fund_considered": {"type": "boolean"},
                        "cancer_drugs_fund_eligible": {"type": "boolean"},
                        "innovation_acknowledged": {"type": "boolean"},
                        "equality_issues_raised": {"type": "boolean"},
                    },
                },
                "cross_references": {
                    "type": "array",
                    "description": "References to other NICE TAs. Do not guess TA numbers — set to null if only referenced by title.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "referenced_ta": {"type": "string", "description": "E.g. 'TA192'. Null if number not stated."},
                            "relationship": {"type": "string", "description": "E.g. precedent, utility_reuse, comparator_guidance, same_condition, same_drug, cdf_reconsideration"},
                            "context": {"type": "string"},
                        },
                        "required": ["relationship"],
                    },
                },
            },
        },
    },
]
