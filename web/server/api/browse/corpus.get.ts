export default defineEventHandler(() => {
  const db = useDb();

  const rows = db
    .prepare(
      `SELECT c.ta_number, tr.title, c.filename, c.doc_type, c.page_count
       FROM corpus c
       LEFT JOIN ta_resolved tr ON tr.ta_number = c.ta_number
       ORDER BY c.ta_number DESC, c.doc_type`
    )
    .all() as {
    ta_number: number;
    title: string | null;
    filename: string;
    doc_type: string;
    page_count: number;
  }[];

  const grouped: Record<
    number,
    { ta_number: number; title: string | null; documents: { filename: string; doc_type: string; page_count: number }[] }
  > = {};

  for (const row of rows) {
    if (!grouped[row.ta_number]) {
      grouped[row.ta_number] = {
        ta_number: row.ta_number,
        title: row.title,
        documents: [],
      };
    }
    grouped[row.ta_number].documents.push({
      filename: row.filename,
      doc_type: row.doc_type,
      page_count: row.page_count,
    });
  }

  return Object.values(grouped);
});
