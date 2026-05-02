import Anthropic from "@anthropic-ai/sdk";

const SCHEMA_DESCRIPTION = `You have access to a SQLite database of 555 NICE Technology Appraisals. Tables:

GLOBAL ENTITIES:
- interventions(id, generic_name, brand_name, drug_class, mechanism_of_action, route_of_administration, treatment_duration_type)
- conditions(id, condition_name, therapeutic_area, disease_setting, biomarker_name)

PER-TA METADATA:
- ta_resolved(ta_number PRIMARY KEY, title, recommendation_type, restriction_details, appraisal_type, committee_name, erg_or_eag_name, line_of_therapy, issue_date)

LINKS (many-to-many):
- ta_interventions(ta_number, intervention_id)
- ta_conditions(ta_number, condition_id)

PER-TA ENTITIES:
- ta_comparators(id, ta_number, comparator_name, comparator_type, is_established_practice, committee_preferred)
- ta_trials(id, ta_number, trial_name, study_design, phase, blinding, is_pivotal, primary_outcome, sample_size, crossover_occurred, crossover_adjusted, generalisability_concern)
- ta_economic_models(id, ta_number, model_type, model_source, time_horizon, cycle_length, health_states TEXT/JSON)
- ta_methodological_decisions(id, ta_number, decision_category, description, company_position, erg_position, committee_preference, impact_on_icer)
  decision_category enum: survival_extrapolation, treatment_effect_duration, treatment_effect_waning, indirect_comparison_method, utility_source, utility_value_choice, surrogate_endpoint_validity, comparator_selection, population_generalisability, subgroup_definition, crossover_adjustment, proportional_hazards, cost_assumption, stopping_rule, model_structure, treatment_sequencing, carer_utility, baseline_risk, cure_assumption, discount_rate, mortality_assumption, equivalence_assumption, other
- ta_evidence_gaps(id, ta_number, gap_type, description)
- ta_commercial_arrangements(id, ta_number, arrangement_type, discount_confidential, critical_for_recommendation)
- ta_icer_bands(id, ta_number, band, comparison_pair, is_committee_preferred, uncertainty_level)
  band enum: below_20k, 20k_to_30k, 30k_to_50k, 50k_to_100k, above_100k, dominant, not_estimable, confidential
- ta_special_considerations(ta_number, end_of_life_considered, end_of_life_met, severity_modifier_applied, cancer_drugs_fund_considered, cancer_drugs_fund_eligible, innovation_acknowledged, equality_issues_raised)
- ta_cross_references(id, ta_number, referenced_ta, relationship, context)

Drug/condition names are lowercase. Use LIKE with % for partial matching. Always include ta_number in results so you can cite specific TAs.`;

const SYSTEM_PROMPT = `You are a NICE Technology Appraisals research assistant. Answer questions by querying the database.

Rules:
- Be concise. Use markdown formatting: tables for structured data, bold for emphasis, bullet lists.
- ALWAYS cite specific TA numbers as "TA876" (not "TA 876" or "technology appraisal 876"). These become clickable links.
- Use at most 2 queries. Keep queries focused — use LIMIT 20 unless the user asks for exhaustive results.
- When listing multiple TAs, use a markdown table. Format EXACTLY like this (alignment row is required):

| TA | Drug | Finding |
|---|---|---|
| TA876 | nivolumab | Recommended with restrictions |

- Always include ta_number in your SELECT so you can cite specific TAs.
- Keep table cells concise (under 60 chars). Use separate paragraphs for longer explanations.

${SCHEMA_DESCRIPTION}`;

const TOOLS: Anthropic.Tool[] = [
  {
    name: "query_database",
    description:
      "Execute a read-only SQL query against the NICE appraisals database. Returns up to 30 rows. Use this to answer the user's question.",
    input_schema: {
      type: "object" as const,
      properties: {
        sql: {
          type: "string",
          description: "SQLite SELECT query. Must be read-only.",
        },
      },
      required: ["sql"],
    },
  },
];

const rateLimiter = {
  hits: [] as number[],
  check() {
    const now = Date.now();
    this.hits = this.hits.filter((t) => now - t < 86_400_000);
    const lastHour = this.hits.filter((t) => now - t < 3_600_000).length;
    if (lastHour >= 100) return "Rate limit exceeded (100/hour). Try again later.";
    if (this.hits.length >= 2000) return "Daily limit reached (2000/day). Try again tomorrow.";
    this.hits.push(now);
    return null;
  },
};

export default defineEventHandler(async (event) => {
  const limited = rateLimiter.check();
  if (limited) throw createError({ statusCode: 429, message: limited });

  const config = useRuntimeConfig();
  const body = await readBody(event);
  const question = body?.question;
  const history = (body?.history || []).slice(-20);
  if (!question)
    throw createError({ statusCode: 400, message: "Missing question" });

  const client = new Anthropic({ apiKey: config.anthropicApiKey });
  const db = useDb();

  setResponseHeaders(event, {
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache, no-transform",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
    "Content-Encoding": "none",
  });

  const res = event.node.res;
  res.flushHeaders();

  function send(data: any) {
    res.write(`data: ${JSON.stringify(data)}\n\n`);
    if (typeof (res as any).flush === "function") (res as any).flush();
  }

  const messages: Anthropic.MessageParam[] = [
    ...history,
    { role: "user", content: question },
  ];

  try {
    for (let turn = 0; turn < 5; turn++) {
      const stream = client.messages.stream({
        model: "claude-haiku-4-5-20251001",
        max_tokens: 4096,
        system: SYSTEM_PROMPT,
        tools: TOOLS,
        messages,
      });

      stream.on("text", (text) => {
        send({ type: "text", text });
      });

      const response = await stream.finalMessage();

      if (response.stop_reason !== "tool_use") break;

      send({ type: "status", message: "Querying database..." });

      const toolResults: Anthropic.ToolResultBlockParam[] = [];

      for (const block of response.content) {
        if (block.type === "tool_use" && block.name === "query_database") {
          const sql = (block.input as { sql: string }).sql;
          let rows: any[] = [];
          let error = "";

          try {
            if (
              /\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH)\b/i.test(
                sql
              )
            ) {
              error = "Only SELECT queries are allowed.";
            } else {
              const safeSql = /\bLIMIT\b/i.test(sql)
                ? sql
                : sql + " LIMIT 30";
              rows = db.prepare(safeSql).all();
            }
          } catch (e: any) {
            error = e.message;
          }

          send({ type: "query", sql, rows, error: error || undefined });

          const resultStr = error || JSON.stringify(rows);
          const truncated =
            resultStr.length > 12000
              ? resultStr.slice(0, 12000) +
                "\n... (truncated, " +
                rows.length +
                " total rows)"
              : resultStr;

          toolResults.push({
            type: "tool_result",
            tool_use_id: block.id,
            content: truncated,
          });
        }
      }

      messages.push({ role: "assistant", content: response.content });
      messages.push({ role: "user", content: toolResults });
    }
  } catch (e: any) {
    send({ type: "error", message: e.message || "Something went wrong" });
  }

  send({ type: "done" });
  res.end();
});
