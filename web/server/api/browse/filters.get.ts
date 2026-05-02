export default defineEventHandler(() => {
  const db = useDb();

  const areas = db
    .prepare(
      `SELECT therapeutic_area as value, COUNT(DISTINCT tc.ta_number) as count
       FROM conditions c JOIN ta_conditions tc ON tc.condition_id = c.id
       WHERE c.therapeutic_area IS NOT NULL
       GROUP BY c.therapeutic_area ORDER BY count DESC`
    )
    .all();

  const recommendations = db
    .prepare(
      `SELECT recommendation_type as value, COUNT(*) as count
       FROM ta_resolved WHERE recommendation_type IS NOT NULL
       GROUP BY recommendation_type ORDER BY count DESC`
    )
    .all();

  const bands = db
    .prepare(
      `SELECT band as value, COUNT(*) as count
       FROM ta_icer_bands GROUP BY band ORDER BY count DESC`
    )
    .all();

  const categories = db
    .prepare(
      `SELECT decision_category as value, COUNT(*) as count
       FROM ta_methodological_decisions
       GROUP BY decision_category ORDER BY count DESC`
    )
    .all();

  return { areas, recommendations, bands, categories };
});
