export default defineEventHandler((event) => {
  const db = useDb();
  const num = parseInt(getRouterParam(event, "number") || "");
  if (!num) throw createError({ statusCode: 400, message: "Invalid TA number" });

  const meta = db
    .prepare("SELECT * FROM ta_resolved WHERE ta_number = ?")
    .get(num);
  if (!meta)
    throw createError({ statusCode: 404, message: `TA${num} not found` });

  const interventions = db
    .prepare(
      `SELECT i.* FROM interventions i
       JOIN ta_interventions ti ON ti.intervention_id = i.id
       WHERE ti.ta_number = ?`
    )
    .all(num);

  const conditions = db
    .prepare(
      `SELECT c.* FROM conditions c
       JOIN ta_conditions tc ON tc.condition_id = c.id
       WHERE tc.ta_number = ?`
    )
    .all(num);

  const comparators = db
    .prepare("SELECT * FROM ta_comparators WHERE ta_number = ?")
    .all(num);

  const trials = db
    .prepare("SELECT * FROM ta_trials WHERE ta_number = ?")
    .all(num);

  const models = db
    .prepare("SELECT * FROM ta_economic_models WHERE ta_number = ?")
    .all(num);

  const decisions = db
    .prepare(
      `SELECT * FROM ta_methodological_decisions
       WHERE ta_number = ? ORDER BY decision_category`
    )
    .all(num);

  const gaps = db
    .prepare("SELECT * FROM ta_evidence_gaps WHERE ta_number = ?")
    .all(num);

  const arrangement = db
    .prepare("SELECT * FROM ta_commercial_arrangements WHERE ta_number = ?")
    .get(num);

  const icers = db
    .prepare("SELECT * FROM ta_icer_bands WHERE ta_number = ?")
    .all(num);

  const special = db
    .prepare("SELECT * FROM ta_special_considerations WHERE ta_number = ?")
    .get(num);

  const crossRefs = db
    .prepare(
      `SELECT xr.*, tr.title as ref_title
       FROM ta_cross_references xr
       LEFT JOIN ta_resolved tr ON tr.ta_number = xr.referenced_ta
       WHERE xr.ta_number = ?`
    )
    .all(num);

  return {
    meta,
    interventions,
    conditions,
    comparators,
    trials,
    models,
    decisions,
    gaps,
    arrangement,
    icers,
    special,
    crossRefs,
  };
});
