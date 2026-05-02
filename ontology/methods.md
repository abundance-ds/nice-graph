# Ontology Development — Methods

## Objective

Develop a stable knowledge graph ontology for ~900 NICE Technology Appraisals that captures structured, queryable information for HEOR researchers, pharma companies, and health policy analysts. The ontology must be:
- Rich enough to answer cross-TA questions about methodological decisions, stakeholder arguments, and appraisal outcomes
- Simple enough for a cheap AI model (Haiku/Flash Lite) to extract reliably from 3-page markdown chunks
- Grounded in what's actually in the documents, not theoretical HTA frameworks

## Approach: Emergent ontology via iterative extraction

Rather than defining the ontology top-down from domain expertise, we let it emerge from the documents through multiple rounds of AI-assisted exploration and refinement. This avoids the common failure mode of HTA ontologies: overly academic schemas that don't match the messy reality of appraisal documents.

### Phase 1: Independent exploration (2 agents, 20 TAs)

Two Opus agents each receive 10 different NICE TAs (FADs + scope comments where available) spanning:
- **Eras:** 2003–2025 (document format and committee reasoning style evolve significantly)
- **Therapeutic areas:** Oncology, rare disease, chronic conditions, devices, mental health, infectious disease
- **Decision types:** Recommended, not recommended, managed access, CDF, optimised

Each agent independently:
1. Reads all 10 documents
2. Proposes entity types with definitions and examples from the documents
3. Proposes relation types with definitions and examples
4. Identifies what should NOT be extracted (and why)
5. Proposes a structured extraction format suitable for a cheap model

The agents receive no seed ontology — they work from the raw documents only.

### Phase 2: Convergence analysis and v0.1

We compare the two independent proposals:
- **Strong convergence** (both agents propose similar types) → high confidence, include in v0.1
- **Partial convergence** (same concept, different framing) → merge, clarify definitions
- **Divergence** (one agent proposes something the other doesn't) → evaluate against documents, decide
- **Unique insights** → consider adding if well-evidenced

Output: `ontology.json` v0.1 + `extraction_prompt.md` v0.1

### Phase 3: Iterative refinement (5+ rounds)

Each round:
1. Select 10 new TAs (not used in previous rounds) — deliberately include edge cases
2. An Opus agent receives the current ontology + extraction prompt + 10 new documents
3. Agent attempts extraction using the schema, producing structured JSON triplets
4. Agent also critiques the schema: what doesn't fit? What's missing? What's ambiguous?
5. We review extracted triplets for: garbage (hallucinated/wrong), gaps (important facts missed), inconsistency (same fact tagged differently)
6. Update ontology and extraction prompt based on findings

Each round's inputs, outputs, and schema changes are logged in `ontology/cycles/`.

### Phase 4: Convergence assessment

After 5+ rounds, we evaluate:
- **Schema stability:** Are entity/relation types still changing between rounds?
- **Extraction consistency:** Does the same type of fact get tagged the same way across different documents?
- **Coverage:** Are important facts in documents captured by the schema?
- **Precision:** Are extracted triplets correct? (target: >85%)
- **Cheap-model readiness:** Is the schema simple enough for Haiku/Flash Lite?

If stable → freeze as v1.0 and proceed to bulk tagging.
If not → additional rounds targeting weak areas.

## TA Selection Strategy

### Initial exploration (20 TAs)

| Group | TAs | Rationale |
|-------|-----|-----------|
| Agent A | TA92, TA178, TA249, TA400, TA540, TA733, TA854, TA877, TA943, TA1027 | Broad therapeutic diversity: dental, renal cancer, anticoagulant, melanoma, lymphoma, cholesterol, depression, CKD, diabetes device, uveal melanoma |
| Agent B | TA70, TA276, TA310, TA467, TA612, TA810, TA891, TA903, TA959, TA1011 | Decision/complexity diversity: CML (early), cystic fibrosis, NSCLC, stem cell therapy, breast cancer (rejected), breast cancer (CDK inhibitor), CLL combo, prostate combo, amyloidosis (rare), VHL (ultra-rare) |

### Refinement rounds (10 new TAs per round, 50+ total)

Selection criteria evolve based on findings:
- Round 1-2: Fill gaps in therapeutic area and era coverage
- Round 3-4: Stress-test weak schema areas (complex methodological disputes, multi-indication TAs)
- Round 5+: Edge cases (very old TAs, terminated appraisals, appeals, managed access agreements)

## Document types used

| Document | Role in ontology development |
|----------|------------------------------|
| FAD (Final Appraisal Document) | Primary source. Contains decision, reasoning, methodological choices, key uncertainties. |
| Scope comments + responses | Stakeholder arguments, NICE responses. Tests the stakeholder comment extraction schema. |
| ACD (Appraisal Consultation Document) | Not used for ontology (similar to FAD but draft). May be added if temporal tracking is needed later. |
| Committee papers / ERG reports | Not used initially (too long for exploration context). Ontology designed to work on these based on FAD patterns. |

## Quality metrics

- **Precision:** % of extracted triplets that are factually correct and correctly typed (target: >85%)
- **Recall:** Qualitative assessment — are the most important facts in each document captured?
- **Schema compliance:** % of extractions that parse correctly against the JSON schema
- **Cross-TA consistency:** Same entity type used consistently across different TAs and eras
- **Cheap-model transferability:** Quality drop when moving from Opus to Haiku/Flash Lite (target: <15% precision drop)

## Outputs

- `ontology/ontology.json` — Entity types, relation types, definitions, examples
- `ontology/extraction_prompt.md` — Prompt template for bulk extraction
- `ontology/cycles/` — Raw outputs and change logs from each development round
- `ontology/methods.md` — This document
