export default defineEventHandler((event) => {
  const db = useDb();
  const query = getQuery(event);

  const area = query.area as string | undefined;
  const recommendation = query.recommendation as string | undefined;
  const band = query.band as string | undefined;
  const category = query.category as string | undefined;
  const drug = query.drug as string | undefined;
  const search = query.search as string | undefined;
  const page = Math.max(1, parseInt(query.page as string) || 1);
  const limit = 50;
  const offset = (page - 1) * limit;

  const conditions: string[] = [];
  const params: any[] = [];

  if (area) {
    conditions.push(
      "tr.ta_number IN (SELECT tc.ta_number FROM ta_conditions tc JOIN conditions c ON c.id = tc.condition_id WHERE c.therapeutic_area = ?)"
    );
    params.push(area);
  }
  if (recommendation) {
    conditions.push("tr.recommendation_type = ?");
    params.push(recommendation);
  }
  if (band) {
    conditions.push(
      "tr.ta_number IN (SELECT ta_number FROM ta_icer_bands WHERE band = ?)"
    );
    params.push(band);
  }
  if (category) {
    conditions.push(
      "tr.ta_number IN (SELECT ta_number FROM ta_methodological_decisions WHERE decision_category = ?)"
    );
    params.push(category);
  }
  if (drug) {
    conditions.push(
      "tr.ta_number IN (SELECT ti.ta_number FROM ta_interventions ti JOIN interventions i ON i.id = ti.intervention_id WHERE i.generic_name LIKE ?)"
    );
    params.push(`%${drug}%`);
  }
  if (search) {
    conditions.push("tr.title LIKE ?");
    params.push(`%${search}%`);
  }

  const where = conditions.length
    ? "WHERE " + conditions.join(" AND ")
    : "";

  const total = (
    db.prepare(`SELECT COUNT(*) as n FROM ta_resolved tr ${where}`).get(
      ...params
    ) as { n: number }
  ).n;

  const rows = db
    .prepare(
      `
    SELECT
      tr.ta_number,
      tr.title,
      tr.recommendation_type,
      tr.appraisal_type,
      tr.line_of_therapy,
      GROUP_CONCAT(DISTINCT i.generic_name) as drugs,
      GROUP_CONCAT(DISTINCT c.therapeutic_area) as areas,
      (SELECT band FROM ta_icer_bands WHERE ta_number = tr.ta_number LIMIT 1) as icer_band,
      (SELECT COUNT(*) FROM ta_methodological_decisions WHERE ta_number = tr.ta_number) as decision_count
    FROM ta_resolved tr
    LEFT JOIN ta_interventions ti ON ti.ta_number = tr.ta_number
    LEFT JOIN interventions i ON i.id = ti.intervention_id
    LEFT JOIN ta_conditions tc ON tc.ta_number = tr.ta_number
    LEFT JOIN conditions c ON c.id = tc.condition_id
    ${where}
    GROUP BY tr.ta_number
    ORDER BY tr.ta_number DESC
    LIMIT ? OFFSET ?
  `
    )
    .all(...params, limit, offset);

  return { rows, total, page, pages: Math.ceil(total / limit) };
});
