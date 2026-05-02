"""Phase 6: Entity resolution — normalise, deduplicate, build graph tables.

Reads extraction results from chunks table, normalises enums, deduplicates
entities across chunks within each TA, and builds typed graph tables for
downstream querying.

Usage:
    uv run python scripts/06_resolve.py

Idempotent — drops and recreates all resolved tables on each run.
"""

import json
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "nice.db"

# ─── Canonical enum values (ontology v0.5.1) ────────────────────────────────

CANONICAL_DECISION_CATEGORIES = {
    "survival_extrapolation", "treatment_effect_duration", "treatment_effect_waning",
    "indirect_comparison_method", "utility_source", "utility_value_choice",
    "surrogate_endpoint_validity", "comparator_selection", "population_generalisability",
    "subgroup_definition", "crossover_adjustment", "proportional_hazards",
    "cost_assumption", "stopping_rule", "model_structure", "treatment_sequencing",
    "carer_utility", "baseline_risk", "cure_assumption", "discount_rate",
    "mortality_assumption", "equivalence_assumption", "other",
}

CANONICAL_ICER_BANDS = {
    "below_20k", "20k_to_30k", "30k_to_50k", "50k_to_100k", "above_100k",
    "dominant", "not_estimable", "confidential",
}

CANONICAL_MODEL_TYPES = {
    "markov", "partitioned_survival", "decision_tree", "semi_markov",
    "discrete_event_simulation", "cost_minimisation", "cost_comparison",
    "cost_analysis", "decision_tree_plus_markov", "patient_level_simulation",
    "mixture_cure", "other",
}

CANONICAL_ARRANGEMENT_TYPES = {
    "simple_discount_pas", "complex_pas", "managed_access_agreement",
    "commercial_access_agreement", "free_initiation", "dose_cap", "none",
}

CANONICAL_GAP_TYPES = {
    "immature_overall_survival", "no_direct_comparison", "no_uk_data",
    "surrogate_not_validated", "missing_subgroup_data", "missing_quality_of_life_data",
    "short_follow_up", "no_comparator_data", "missing_real_world_evidence",
    "single_arm_evidence_only", "instrument_insensitivity", "other",
}

# ─── Normalisation maps ─────────────────────────────────────────────────────

DECISION_CATEGORY_EXPLICIT = {
    "treatment_duration": "treatment_effect_duration",
    "treatment_duration_type": "treatment_effect_duration",
    "treatment_duration_assumption": "treatment_effect_duration",
    "treatment_duration_choice": "treatment_effect_duration",
    "treatment_duration_selection": "treatment_effect_duration",
    "treatment_duration_waning": "treatment_effect_waning",
    "time_horizon": "model_structure",
    "population_definition": "population_generalisability",
    "adverse_event_modelling": "cost_assumption",
    "adverse_event_inclusion": "cost_assumption",
    "adverse_event_disutility": "utility_value_choice",
    "adverse_event_disutilities": "utility_value_choice",
    "adverse_event_costing": "cost_assumption",
    "adverse_events_modelling": "cost_assumption",
    "transition_probabilities": "model_structure",
    "dose_intensity": "cost_assumption",
    "discontinuation_rate": "stopping_rule",
    "discontinuation_rates": "stopping_rule",
    "treatment_discontinuation": "stopping_rule",
    "treatment_discontinuation_rates": "stopping_rule",
    "end_of_life_criteria": "other",
    "disease_progression_assumption": "mortality_assumption",
    "disease_progression": "mortality_assumption",
    "network_meta_analysis": "indirect_comparison_method",
    "network_meta_analysis_heterogeneity": "indirect_comparison_method",
    "informative_censoring": "survival_extrapolation",
    "health_state_utilities": "utility_source",
    "comparative_effectiveness": "indirect_comparison_method",
    "cycle_length": "model_structure",
    "treatment_effect_adjustment": "treatment_effect_duration",
    "probabilistic_sensitivity_analysis": "model_structure",
    "study_inclusion_criteria": "population_generalisability",
    "trial_inclusion_criteria": "population_generalisability",
    "relapse_definition": "subgroup_definition",
    "non_inferiority_margin": "surrogate_endpoint_validity",
    "dose_selection": "cost_assumption",
    "incremental_analysis": "model_structure",
    "primary_outcome_inclusion": "surrogate_endpoint_validity",
    "short_follow_up": "treatment_effect_duration",
    "chlorambucil_dose": "comparator_selection",
}

DECISION_CATEGORY_KEYWORDS = [
    (["utility", "disutility", "eq-5d", "eq5d", "hrqol"], "utility_source"),
    (["survival", "extrapolat", "kaplan", "parametric"], "survival_extrapolation"),
    (["comparator", "comparison_choice"], "comparator_selection"),
    (["crossover", "cross_over"], "crossover_adjustment"),
    (["cost", "resource", "drug_cost", "acquisition"], "cost_assumption"),
    (["discontinu", "stopping", "treatment_stop"], "stopping_rule"),
    (["waning", "wane", "effect_waning"], "treatment_effect_waning"),
    (["indirect", "network_meta", "nma", "itc", "maic"], "indirect_comparison_method"),
    (["subgroup", "sub_group"], "subgroup_definition"),
    (["model", "structure", "transition", "state_transition", "health_state"], "model_structure"),
    (["duration", "treatment_effect"], "treatment_effect_duration"),
    (["mortality", "death", "background_mortality"], "mortality_assumption"),
    (["baseline", "natural_history"], "baseline_risk"),
    (["cure", "cure_rate", "cure_fraction"], "cure_assumption"),
    (["discount", "discounting"], "discount_rate"),
    (["equivalence", "equivalent", "class_effect"], "equivalence_assumption"),
    (["proportional", "hazard", "ph_assumption"], "proportional_hazards"),
    (["population", "generalis"], "population_generalisability"),
    (["surrogate", "endpoint_validity"], "surrogate_endpoint_validity"),
    (["carer"], "carer_utility"),
    (["sequenc"], "treatment_sequencing"),
    (["adverse", "safety", "ae_", "toxicity"], "cost_assumption"),
]

ICER_BAND_MAP = {
    "below_50k": "30k_to_50k",
    "above_30k": "30k_to_50k",
    "below_30k": "20k_to_30k",
    "20k_to_50k": "30k_to_50k",
    "above_50k": "50k_to_100k",
    "dominant or below_20k": "dominant",
    "within_acceptable_range": "below_20k",
    "above_acceptable_range": "above_100k",
}

MODEL_TYPE_MAP = {
    "markov model": "markov",
    "state_transition": "markov",
    "state transition": "markov",
    "state transition model": "markov",
    "cohort": "markov",
    "cohort model": "markov",
    "semi-markov": "semi_markov",
    "semi markov": "semi_markov",
    "partitioned survival": "partitioned_survival",
    "partitioned_survival_analysis": "partitioned_survival",
    "partitioned survival analysis": "partitioned_survival",
    "discrete event simulation": "discrete_event_simulation",
    "des": "discrete_event_simulation",
    "cost-effectiveness analysis": "cost_analysis",
    "cost-utility": "cost_analysis",
    "cost-utility analysis": "cost_analysis",
    "cost utility analysis": "cost_analysis",
    "cost effectiveness analysis": "cost_analysis",
    "mixture": "mixture_cure",
    "mixture cure": "mixture_cure",
    "mixture cure model": "mixture_cure",
    "decision_tree and markov model": "decision_tree_plus_markov",
    "decision tree and markov": "decision_tree_plus_markov",
    "decision tree plus markov": "decision_tree_plus_markov",
    "patient level simulation": "patient_level_simulation",
    "individual patient simulation": "patient_level_simulation",
    "microsimulation": "patient_level_simulation",
    "individual patient-level simulation": "patient_level_simulation",
    "de novo model": None,
    "de novo": None,
    "not specified": None,
    "not explicitly stated": None,
    "not specified in this chunk": None,
    "not_specified": None,
    "not stated": None,
    "unknown": None,
    "hybrid": "other",
    "mixed": "other",
}

ARRANGEMENT_TYPE_MAP = {
    "confidential": "simple_discount_pas",
    "confidential_pas": "simple_discount_pas",
    "patient_access_scheme": "simple_discount_pas",
    "likely patient_access_scheme": "simple_discount_pas",
    "confidential discounts": "simple_discount_pas",
    "updated_pas": "simple_discount_pas",
    "confidential discount or simple_discount_pas": "simple_discount_pas",
    "commercial_access_arrangement": "commercial_access_agreement",
    "patient access schemes": "simple_discount_pas",
    "confidential discount or patient access scheme": "simple_discount_pas",
    "confidential_discount": "simple_discount_pas",
}

GAP_TYPE_IS_DECISION_CATEGORY = {
    "population_generalisability", "treatment_effect_waning",
    "surrogate_endpoint_validity", "treatment_effect_duration",
    "indirect_comparison_method",
}

GAP_TYPE_MAP = {
    "generalisability_concern": "no_uk_data",
    "subgroup_evidence": "missing_subgroup_data",
    "post_hoc_subgroup_analyses": "missing_subgroup_data",
    "limited_clinical_evidence": "other",
    "no_utility_data": "missing_quality_of_life_data",
    "no_rct_data": "no_direct_comparison",
    "limited_utility_data": "missing_quality_of_life_data",
    "missing_biomarker_data": "missing_subgroup_data",
    "quality_of_life": "missing_quality_of_life_data",
    "data_completeness": "other",
    "lack_of_data": "other",
    "comparator_validity": "no_comparator_data",
    "indirect_comparison": "no_direct_comparison",
    "limited_evidence": "other",
    "single_device_evidence_only": "single_arm_evidence_only",
}


# ─── Normalisation functions ────────────────────────────────────────────────

norm_stats = Counter()


def normalise_decision_category(raw):
    if not raw:
        return "other"
    key = raw.lower().strip()
    if key in CANONICAL_DECISION_CATEGORIES:
        return key
    if key in DECISION_CATEGORY_EXPLICIT:
        norm_stats[f"decision: {key} -> {DECISION_CATEGORY_EXPLICIT[key]}"] += 1
        return DECISION_CATEGORY_EXPLICIT[key]
    for keywords, canonical in DECISION_CATEGORY_KEYWORDS:
        if any(kw in key for kw in keywords):
            norm_stats[f"decision: {key} -> {canonical} (keyword)"] += 1
            return canonical
    norm_stats[f"decision: {key} -> other (unmapped)"] += 1
    return "other"


def normalise_icer_band(raw):
    if not raw:
        return None
    key = raw.lower().strip()
    if key in CANONICAL_ICER_BANDS:
        return key
    if key in ICER_BAND_MAP:
        norm_stats[f"icer: {key} -> {ICER_BAND_MAP[key]}"] += 1
        return ICER_BAND_MAP[key]
    norm_stats[f"icer: {key} -> kept as-is"] += 1
    return key


def normalise_model_type(raw):
    if not raw:
        return None
    key = raw.lower().strip()
    if key in CANONICAL_MODEL_TYPES:
        return key
    if key in MODEL_TYPE_MAP:
        result = MODEL_TYPE_MAP[key]
        norm_stats[f"model: {key} -> {result}"] += 1
        return result
    norm_stats[f"model: {key} -> other (unmapped)"] += 1
    return "other"


def normalise_arrangement_type(raw):
    if not raw:
        return None
    key = raw.lower().strip()
    if key in CANONICAL_ARRANGEMENT_TYPES:
        return key
    if key in ARRANGEMENT_TYPE_MAP:
        norm_stats[f"arrangement: {key} -> {ARRANGEMENT_TYPE_MAP[key]}"] += 1
        return ARRANGEMENT_TYPE_MAP[key]
    norm_stats[f"arrangement: {key} -> kept as-is"] += 1
    return key


def normalise_gap_type(raw):
    """Returns (normalised_type, should_keep)."""
    if not raw:
        return "other", True
    key = raw.lower().strip()
    if key in GAP_TYPE_IS_DECISION_CATEGORY:
        norm_stats[f"gap: {key} -> dropped (is decision category)"] += 1
        return None, False
    if key in CANONICAL_GAP_TYPES:
        return key, True
    if key in GAP_TYPE_MAP:
        norm_stats[f"gap: {key} -> {GAP_TYPE_MAP[key]}"] += 1
        return GAP_TYPE_MAP[key], True
    norm_stats[f"gap: {key} -> other (unmapped)"] += 1
    return "other", True


def parse_ta_number(raw):
    if raw is None:
        return None
    if isinstance(raw, int):
        return raw
    s = str(raw).strip()
    m = re.match(r"[Tt][Aa]\s*(\d+)", s)
    if m:
        return int(m.group(1))
    try:
        return int(s)
    except ValueError:
        return None


# ─── Deduplication helpers ──────────────────────────────────────────────────

def dedup_key(s):
    if not s:
        return ""
    return re.sub(r"\s+", " ", s.lower().strip())


def merge_records(records):
    merged = {}
    for rec in records:
        for field, value in rec.items():
            if value is None:
                continue
            existing = merged.get(field)
            if existing is None:
                merged[field] = value
            elif isinstance(value, str) and isinstance(existing, str):
                if len(value) > len(existing):
                    merged[field] = value
            elif isinstance(value, bool) and value:
                merged[field] = value
            elif isinstance(value, list) and isinstance(existing, list):
                if len(value) > len(existing):
                    merged[field] = value
    return merged


def dedup_by_key(items, key_fn):
    groups = defaultdict(list)
    for item in items:
        k = key_fn(item)
        if k is not None:
            groups[k].append(item)
    return [merge_records(group) for group in groups.values()]


# ─── Table schema ───────────────────────────────────────────────────────────

RESOLVED_TABLES = [
    "ta_resolved", "interventions", "conditions",
    "ta_interventions", "ta_conditions",
    "ta_comparators", "ta_trials", "ta_economic_models",
    "ta_methodological_decisions", "ta_evidence_gaps",
    "ta_commercial_arrangements", "ta_icer_bands",
    "ta_special_considerations", "ta_cross_references",
]


def create_tables(conn):
    for table in RESOLVED_TABLES:
        conn.execute(f"DROP TABLE IF EXISTS {table}")

    conn.executescript("""
        CREATE TABLE interventions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generic_name TEXT NOT NULL UNIQUE COLLATE NOCASE,
            brand_name TEXT,
            drug_class TEXT,
            mechanism_of_action TEXT,
            route_of_administration TEXT,
            treatment_duration_type TEXT
        );

        CREATE TABLE conditions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_name TEXT NOT NULL COLLATE NOCASE,
            therapeutic_area TEXT,
            disease_setting TEXT,
            biomarker_name TEXT
        );
        CREATE UNIQUE INDEX idx_cond_unique
            ON conditions(condition_name COLLATE NOCASE, COALESCE(disease_setting, ''));

        CREATE TABLE ta_resolved (
            ta_number INTEGER PRIMARY KEY,
            title TEXT,
            recommendation_type TEXT,
            restriction_details TEXT,
            appraisal_type TEXT,
            committee_name TEXT,
            erg_or_eag_name TEXT,
            line_of_therapy TEXT,
            issue_date TEXT
        );

        CREATE TABLE ta_interventions (
            ta_number INTEGER NOT NULL,
            intervention_id INTEGER NOT NULL REFERENCES interventions(id),
            PRIMARY KEY (ta_number, intervention_id)
        );

        CREATE TABLE ta_conditions (
            ta_number INTEGER NOT NULL,
            condition_id INTEGER NOT NULL REFERENCES conditions(id),
            PRIMARY KEY (ta_number, condition_id)
        );

        CREATE TABLE ta_comparators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ta_number INTEGER NOT NULL,
            comparator_name TEXT NOT NULL,
            comparator_type TEXT,
            is_established_practice BOOLEAN,
            committee_preferred BOOLEAN,
            UNIQUE(ta_number, comparator_name COLLATE NOCASE)
        );

        CREATE TABLE ta_trials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ta_number INTEGER NOT NULL,
            trial_name TEXT NOT NULL,
            study_design TEXT,
            phase TEXT,
            blinding TEXT,
            is_pivotal BOOLEAN,
            primary_outcome TEXT,
            sample_size INTEGER,
            crossover_occurred BOOLEAN,
            crossover_adjusted BOOLEAN,
            generalisability_concern BOOLEAN,
            UNIQUE(ta_number, trial_name COLLATE NOCASE)
        );

        CREATE TABLE ta_economic_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ta_number INTEGER NOT NULL,
            model_type TEXT,
            model_source TEXT,
            time_horizon TEXT,
            cycle_length TEXT,
            health_states TEXT
        );

        CREATE TABLE ta_methodological_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ta_number INTEGER NOT NULL,
            decision_category TEXT NOT NULL,
            description TEXT NOT NULL,
            company_position TEXT,
            erg_position TEXT,
            committee_preference TEXT,
            impact_on_icer TEXT
        );

        CREATE TABLE ta_evidence_gaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ta_number INTEGER NOT NULL,
            gap_type TEXT NOT NULL,
            description TEXT NOT NULL
        );

        CREATE TABLE ta_commercial_arrangements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ta_number INTEGER NOT NULL,
            arrangement_type TEXT,
            discount_confidential BOOLEAN,
            critical_for_recommendation BOOLEAN
        );

        CREATE TABLE ta_icer_bands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ta_number INTEGER NOT NULL,
            band TEXT NOT NULL,
            comparison_pair TEXT,
            is_committee_preferred BOOLEAN,
            uncertainty_level TEXT
        );

        CREATE TABLE ta_special_considerations (
            ta_number INTEGER PRIMARY KEY,
            end_of_life_considered BOOLEAN,
            end_of_life_met BOOLEAN,
            severity_modifier_applied BOOLEAN,
            cancer_drugs_fund_considered BOOLEAN,
            cancer_drugs_fund_eligible BOOLEAN,
            innovation_acknowledged BOOLEAN,
            equality_issues_raised BOOLEAN
        );

        CREATE TABLE ta_cross_references (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ta_number INTEGER NOT NULL,
            referenced_ta INTEGER,
            relationship TEXT,
            context TEXT,
            UNIQUE(ta_number, referenced_ta, relationship)
        );

        CREATE INDEX idx_meth_category ON ta_methodological_decisions(decision_category);
        CREATE INDEX idx_meth_ta ON ta_methodological_decisions(ta_number);
        CREATE INDEX idx_icer_band ON ta_icer_bands(band);
        CREATE INDEX idx_icer_ta ON ta_icer_bands(ta_number);
        CREATE INDEX idx_gaps_type ON ta_evidence_gaps(gap_type);
        CREATE INDEX idx_trials_ta ON ta_trials(ta_number);
        CREATE INDEX idx_comparators_ta ON ta_comparators(ta_number);
        CREATE INDEX idx_xref_ta ON ta_cross_references(ta_number);
        CREATE INDEX idx_xref_ref ON ta_cross_references(referenced_ta);
        CREATE INDEX idx_interventions_name ON interventions(generic_name COLLATE NOCASE);
        CREATE INDEX idx_conditions_name ON conditions(condition_name COLLATE NOCASE);
        CREATE INDEX idx_conditions_area ON conditions(therapeutic_area);
    """)
    conn.commit()


# ─── Per-TA resolution ──────────────────────────────────────────────────────

def resolve_ta(ta_number, chunk_results):
    all_metadata = []
    all_interventions = []
    all_conditions = []
    all_comparators = []
    all_trials = []
    all_models = []
    all_decisions = []
    all_gaps = []
    all_arrangements = []
    all_icers = []
    all_special = []
    all_xrefs = []

    for data in chunk_results:
        if data.get("no_relevant_content"):
            continue

        meta = data.get("appraisal_metadata")
        if meta and isinstance(meta, dict):
            all_metadata.append(meta)

        for item in data.get("interventions", []):
            if isinstance(item, dict) and item.get("generic_name"):
                item["generic_name"] = item["generic_name"].lower().strip()
                all_interventions.append(item)

        for item in data.get("conditions", []):
            if isinstance(item, dict) and item.get("condition_name"):
                item["condition_name"] = item["condition_name"].lower().strip()
                all_conditions.append(item)

        for item in data.get("comparators", []):
            if isinstance(item, dict) and item.get("comparator_name"):
                item["comparator_name"] = item["comparator_name"].lower().strip()
                all_comparators.append(item)

        for item in data.get("clinical_trials", []):
            if isinstance(item, dict) and item.get("trial_name"):
                all_trials.append(item)

        model = data.get("economic_model")
        if model and isinstance(model, dict) and any(v for v in model.values() if v):
            if model.get("model_type"):
                model["model_type"] = normalise_model_type(model["model_type"])
            all_models.append(model)

        for item in data.get("methodological_decisions", []):
            if isinstance(item, dict) and item.get("decision_category"):
                item["decision_category"] = normalise_decision_category(
                    item["decision_category"]
                )
                all_decisions.append(item)

        for item in data.get("evidence_gaps", []):
            if isinstance(item, dict) and item.get("gap_type"):
                normalised, keep = normalise_gap_type(item["gap_type"])
                if keep and normalised:
                    item["gap_type"] = normalised
                    all_gaps.append(item)

        arr = data.get("commercial_arrangement")
        if arr and isinstance(arr, dict):
            if arr.get("arrangement_type"):
                arr["arrangement_type"] = normalise_arrangement_type(
                    arr["arrangement_type"]
                )
            all_arrangements.append(arr)

        icer = data.get("icer_band")
        if icer and isinstance(icer, dict) and icer.get("band"):
            icer["band"] = normalise_icer_band(icer["band"])
            all_icers.append(icer)

        special = data.get("special_considerations")
        if special and isinstance(special, dict):
            all_special.append(special)

        for item in data.get("cross_references", []):
            if isinstance(item, dict) and item.get("relationship"):
                item["referenced_ta"] = parse_ta_number(item.get("referenced_ta"))
                all_xrefs.append(item)

    # Deduplicate within TA
    metadata = merge_records(all_metadata) if all_metadata else {}

    interventions = dedup_by_key(
        all_interventions, lambda i: dedup_key(i.get("generic_name", ""))
    )
    conditions = dedup_by_key(
        all_conditions,
        lambda c: (
            dedup_key(c.get("condition_name", "")),
            dedup_key(c.get("disease_setting", "")),
        ),
    )
    comparators = dedup_by_key(
        all_comparators, lambda c: dedup_key(c.get("comparator_name", ""))
    )
    trials = dedup_by_key(
        all_trials, lambda t: dedup_key(t.get("trial_name", ""))
    )

    # Economic models: merge by source
    if all_models:
        models = dedup_by_key(
            all_models, lambda m: dedup_key(m.get("model_source", "unknown"))
        )
    else:
        models = []

    # Methodological decisions: dedup by (category, first 80 chars of description)
    decisions = dedup_by_key(
        all_decisions,
        lambda d: (
            d.get("decision_category", "other"),
            dedup_key(d.get("description", ""))[:80],
        ),
    )

    gaps = dedup_by_key(
        all_gaps,
        lambda g: (
            g.get("gap_type", "other"),
            dedup_key(g.get("description", ""))[:80],
        ),
    )

    arrangement = merge_records(all_arrangements) if all_arrangements else None

    icers = dedup_by_key(
        all_icers,
        lambda i: (i.get("band", ""), dedup_key(i.get("comparison_pair", ""))),
    )

    # Special considerations: OR all booleans
    special = {}
    for s in all_special:
        for field, value in s.items():
            if isinstance(value, bool):
                special[field] = special.get(field, False) or value

    xrefs = dedup_by_key(
        all_xrefs,
        lambda x: (x.get("referenced_ta"), dedup_key(x.get("relationship", ""))),
    )

    return {
        "metadata": metadata,
        "interventions": interventions,
        "conditions": conditions,
        "comparators": comparators,
        "trials": trials,
        "economic_models": models,
        "decisions": decisions,
        "gaps": gaps,
        "arrangement": arrangement,
        "icers": icers,
        "special": special,
        "cross_references": xrefs,
    }


# ─── Global entity management ──────────────────────────────────────────────


class EntityRegistry:
    def __init__(self, conn):
        self.conn = conn

    def get_or_create_intervention(self, data):
        name = data.get("generic_name", "").strip()
        if not name:
            return None

        row = self.conn.execute(
            "SELECT id FROM interventions WHERE generic_name = ? COLLATE NOCASE",
            (name,),
        ).fetchone()

        if row:
            iid = row[0]
            for field in [
                "brand_name", "drug_class", "mechanism_of_action",
                "route_of_administration", "treatment_duration_type",
            ]:
                val = data.get(field)
                if val:
                    self.conn.execute(
                        f"UPDATE interventions SET {field} = COALESCE({field}, ?) WHERE id = ?",
                        (val, iid),
                    )
            return iid

        cur = self.conn.execute(
            """INSERT INTO interventions
               (generic_name, brand_name, drug_class, mechanism_of_action,
                route_of_administration, treatment_duration_type)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                name, data.get("brand_name"), data.get("drug_class"),
                data.get("mechanism_of_action"), data.get("route_of_administration"),
                data.get("treatment_duration_type"),
            ),
        )
        return cur.lastrowid

    def get_or_create_condition(self, data):
        name = data.get("condition_name", "").strip()
        if not name:
            return None
        setting = data.get("disease_setting") or None

        row = self.conn.execute(
            """SELECT id FROM conditions
               WHERE condition_name = ? COLLATE NOCASE
               AND COALESCE(disease_setting, '') = COALESCE(?, '')""",
            (name, setting or ""),
        ).fetchone()

        if row:
            cid = row[0]
            for field in ["therapeutic_area", "biomarker_name"]:
                val = data.get(field)
                if val:
                    self.conn.execute(
                        f"UPDATE conditions SET {field} = COALESCE({field}, ?) WHERE id = ?",
                        (val, cid),
                    )
            return cid

        cur = self.conn.execute(
            """INSERT INTO conditions
               (condition_name, therapeutic_area, disease_setting, biomarker_name)
               VALUES (?, ?, ?, ?)""",
            (name, data.get("therapeutic_area"), setting, data.get("biomarker_name")),
        )
        return cur.lastrowid


# ─── Insertion ──────────────────────────────────────────────────────────────


def insert_resolved(conn, ta_number, resolved, registry):
    meta = resolved["metadata"]
    if meta:
        conn.execute(
            """INSERT OR REPLACE INTO ta_resolved
               (ta_number, title, recommendation_type, restriction_details,
                appraisal_type, committee_name, erg_or_eag_name,
                line_of_therapy, issue_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                ta_number, meta.get("title"), meta.get("recommendation_type"),
                meta.get("restriction_details"), meta.get("appraisal_type"),
                meta.get("committee_name"), meta.get("erg_or_eag_name"),
                meta.get("line_of_therapy"), meta.get("issue_date"),
            ),
        )

    for intv in resolved["interventions"]:
        iid = registry.get_or_create_intervention(intv)
        if iid:
            conn.execute(
                "INSERT OR IGNORE INTO ta_interventions VALUES (?, ?)",
                (ta_number, iid),
            )

    for cond in resolved["conditions"]:
        cid = registry.get_or_create_condition(cond)
        if cid:
            conn.execute(
                "INSERT OR IGNORE INTO ta_conditions VALUES (?, ?)",
                (ta_number, cid),
            )

    for comp in resolved["comparators"]:
        conn.execute(
            """INSERT OR IGNORE INTO ta_comparators
               (ta_number, comparator_name, comparator_type,
                is_established_practice, committee_preferred)
               VALUES (?, ?, ?, ?, ?)""",
            (
                ta_number, comp.get("comparator_name"), comp.get("comparator_type"),
                comp.get("is_established_practice"), comp.get("committee_preferred"),
            ),
        )

    for trial in resolved["trials"]:
        conn.execute(
            """INSERT OR IGNORE INTO ta_trials
               (ta_number, trial_name, study_design, phase, blinding, is_pivotal,
                primary_outcome, sample_size, crossover_occurred,
                crossover_adjusted, generalisability_concern)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                ta_number, trial.get("trial_name"), trial.get("study_design"),
                trial.get("phase"), trial.get("blinding"), trial.get("is_pivotal"),
                trial.get("primary_outcome"), trial.get("sample_size"),
                trial.get("crossover_occurred"), trial.get("crossover_adjusted"),
                trial.get("generalisability_concern"),
            ),
        )

    for model in resolved["economic_models"]:
        hs = model.get("health_states")
        if isinstance(hs, list):
            hs = json.dumps(hs)
        conn.execute(
            """INSERT INTO ta_economic_models
               (ta_number, model_type, model_source, time_horizon,
                cycle_length, health_states)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                ta_number, model.get("model_type"), model.get("model_source"),
                model.get("time_horizon"), model.get("cycle_length"), hs,
            ),
        )

    for dec in resolved["decisions"]:
        conn.execute(
            """INSERT INTO ta_methodological_decisions
               (ta_number, decision_category, description, company_position,
                erg_position, committee_preference, impact_on_icer)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                ta_number, dec.get("decision_category"), dec.get("description"),
                dec.get("company_position"), dec.get("erg_position"),
                dec.get("committee_preference"), dec.get("impact_on_icer"),
            ),
        )

    for gap in resolved["gaps"]:
        conn.execute(
            "INSERT INTO ta_evidence_gaps (ta_number, gap_type, description) VALUES (?, ?, ?)",
            (ta_number, gap.get("gap_type"), gap.get("description")),
        )

    arr = resolved["arrangement"]
    if arr:
        conn.execute(
            """INSERT INTO ta_commercial_arrangements
               (ta_number, arrangement_type, discount_confidential,
                critical_for_recommendation)
               VALUES (?, ?, ?, ?)""",
            (
                ta_number, arr.get("arrangement_type"),
                arr.get("discount_confidential"), arr.get("critical_for_recommendation"),
            ),
        )

    for icer in resolved["icers"]:
        conn.execute(
            """INSERT INTO ta_icer_bands
               (ta_number, band, comparison_pair, is_committee_preferred,
                uncertainty_level)
               VALUES (?, ?, ?, ?, ?)""",
            (
                ta_number, icer.get("band"), icer.get("comparison_pair"),
                icer.get("is_committee_preferred"), icer.get("uncertainty_level"),
            ),
        )

    special = resolved["special"]
    if special:
        conn.execute(
            """INSERT OR REPLACE INTO ta_special_considerations
               (ta_number, end_of_life_considered, end_of_life_met,
                severity_modifier_applied, cancer_drugs_fund_considered,
                cancer_drugs_fund_eligible, innovation_acknowledged,
                equality_issues_raised)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                ta_number,
                special.get("end_of_life_considered"),
                special.get("end_of_life_met"),
                special.get("severity_modifier_applied"),
                special.get("cancer_drugs_fund_considered"),
                special.get("cancer_drugs_fund_eligible"),
                special.get("innovation_acknowledged"),
                special.get("equality_issues_raised"),
            ),
        )

    for xref in resolved["cross_references"]:
        conn.execute(
            """INSERT OR IGNORE INTO ta_cross_references
               (ta_number, referenced_ta, relationship, context)
               VALUES (?, ?, ?, ?)""",
            (
                ta_number, xref.get("referenced_ta"),
                xref.get("relationship"), xref.get("context"),
            ),
        )


# ─── Main ───────────────────────────────────────────────────────────────────


def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    print("Loading extraction results...")
    rows = conn.execute("""
        SELECT ta_number, result FROM chunks
        WHERE doc_type='FAD' AND status='done' AND result IS NOT NULL
    """).fetchall()

    chunks_by_ta = defaultdict(list)
    parse_errors = 0
    for ta_number, result_str in rows:
        try:
            data = json.loads(result_str)
            chunks_by_ta[ta_number].append(data)
        except (json.JSONDecodeError, TypeError):
            parse_errors += 1

    print(f"  {len(rows)} chunks, {len(chunks_by_ta)} TAs, {parse_errors} parse errors")

    print("Creating graph tables...")
    create_tables(conn)

    print("Resolving entities...")
    registry = EntityRegistry(conn)
    stats = Counter()

    for ta_number in sorted(chunks_by_ta):
        resolved = resolve_ta(ta_number, chunks_by_ta[ta_number])
        insert_resolved(conn, ta_number, resolved, registry)

        stats["tas"] += 1
        stats["interventions"] += len(resolved["interventions"])
        stats["conditions"] += len(resolved["conditions"])
        stats["comparators"] += len(resolved["comparators"])
        stats["trials"] += len(resolved["trials"])
        stats["models"] += len(resolved["economic_models"])
        stats["decisions"] += len(resolved["decisions"])
        stats["gaps"] += len(resolved["gaps"])
        stats["arrangements"] += 1 if resolved["arrangement"] else 0
        stats["icers"] += len(resolved["icers"])
        stats["xrefs"] += len(resolved["cross_references"])

    conn.commit()

    # Summary
    global_interventions = conn.execute("SELECT COUNT(*) FROM interventions").fetchone()[0]
    global_conditions = conn.execute("SELECT COUNT(*) FROM conditions").fetchone()[0]

    print(f"\n{'='*55}")
    print(f" Entity resolution complete")
    print(f"{'='*55}")
    print(f"  TAs resolved:              {stats['tas']:>6}")
    print(f"  Global interventions:      {global_interventions:>6}")
    print(f"  Global conditions:         {global_conditions:>6}")
    print(f"  TA-intervention links:     {stats['interventions']:>6}")
    print(f"  TA-condition links:        {stats['conditions']:>6}")
    print(f"  Comparators:               {stats['comparators']:>6}")
    print(f"  Clinical trials:           {stats['trials']:>6}")
    print(f"  Economic models:           {stats['models']:>6}")
    print(f"  Methodological decisions:  {stats['decisions']:>6}")
    print(f"  Evidence gaps:             {stats['gaps']:>6}")
    print(f"  Commercial arrangements:   {stats['arrangements']:>6}")
    print(f"  ICER bands:                {stats['icers']:>6}")
    print(f"  Cross-references:          {stats['xrefs']:>6}")

    print(f"\nDecision categories:")
    for cat, n in conn.execute(
        """SELECT decision_category, COUNT(*) FROM ta_methodological_decisions
           GROUP BY decision_category ORDER BY COUNT(*) DESC"""
    ).fetchall():
        print(f"  {cat:35s} {n:5d}")

    print(f"\nICER bands:")
    for band, n in conn.execute(
        "SELECT band, COUNT(*) FROM ta_icer_bands GROUP BY band ORDER BY COUNT(*) DESC"
    ).fetchall():
        print(f"  {band:25s} {n:5d}")

    print(f"\nTop normalisation actions:")
    for action, n in norm_stats.most_common(20):
        print(f"  [{n:>4}x] {action}")

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
