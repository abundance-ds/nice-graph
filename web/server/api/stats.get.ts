export default defineEventHandler(() => {
  const db = useDb();
  const count = (sql: string) =>
    (db.prepare(sql).get() as { n: number }).n;

  return {
    tas: count("SELECT COUNT(DISTINCT ta_number) as n FROM corpus"),
    interventions: count("SELECT COUNT(*) as n FROM interventions"),
    conditions: count("SELECT COUNT(*) as n FROM conditions"),
    decisions: count("SELECT COUNT(*) as n FROM ta_methodological_decisions"),
    trials: count("SELECT COUNT(*) as n FROM ta_trials"),
    icers: count("SELECT COUNT(*) as n FROM ta_icer_bands"),
    comparators: count("SELECT COUNT(*) as n FROM ta_comparators"),
    crossRefs: count("SELECT COUNT(*) as n FROM ta_cross_references"),
  };
});
