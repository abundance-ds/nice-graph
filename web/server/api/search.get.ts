export default defineEventHandler((event) => {
  const db = useDb();
  const query = getQuery(event);
  const q = (query.q as string || "").trim();
  const docType = query.doc_type as string | undefined;
  const ta = query.ta ? parseInt(query.ta as string) : undefined;
  const limit = Math.min(parseInt(query.limit as string) || 20, 50);
  const format = query.format as string || "json";

  if (!q) throw createError({ statusCode: 400, message: "Missing query parameter 'q'" });

  const conditions = ["corpus_fts MATCH ?"];
  const params: any[] = [q];

  if (docType) {
    conditions.push("c.doc_type = ?");
    params.push(docType);
  }
  if (ta) {
    conditions.push("c.ta_number = ?");
    params.push(ta);
  }

  const where = conditions.join(" AND ");

  const rows = db
    .prepare(
      `SELECT
        c.ta_number,
        c.doc_type,
        c.filename,
        tr.title as ta_title,
        snippet(corpus_fts, 2, '>>>','<<<', '...', 40) as snippet,
        rank
      FROM corpus_fts
      JOIN corpus c ON c.id = corpus_fts.rowid
      LEFT JOIN ta_resolved tr ON tr.ta_number = c.ta_number
      WHERE ${where}
      ORDER BY rank
      LIMIT ?`
    )
    .all(...params, limit);

  if (format === "plain") {
    const lines = (rows as any[]).map(
      (r) =>
        `--- TA${r.ta_number} / ${r.doc_type} (${r.filename}) ---\n${r.snippet.replace(/>>>/g, "").replace(/<<</g, "")}\n`
    );
    setHeader(event, "Content-Type", "text/plain; charset=utf-8");
    return lines.join("\n");
  }

  return { query: q, count: (rows as any[]).length, results: rows };
});
