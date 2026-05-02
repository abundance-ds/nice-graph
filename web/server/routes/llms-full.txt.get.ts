export default defineEventHandler((event) => {
  const db = useDb();

  const tas = db
    .prepare(
      `SELECT DISTINCT c.ta_number, tr.title, COUNT(*) as doc_count, SUM(c.page_count) as total_pages
       FROM corpus c
       LEFT JOIN ta_resolved tr ON tr.ta_number = c.ta_number
       GROUP BY c.ta_number
       ORDER BY c.ta_number`
    )
    .all() as {
    ta_number: number;
    title: string | null;
    doc_count: number;
    total_pages: number;
  }[];

  const totalDocs = tas.reduce((s, t) => s + t.doc_count, 0);
  const totalPages = tas.reduce((s, t) => s + t.total_pages, 0);

  let text = `# NICE Technology Appraisals — Full Corpus Index
# ${tas.length} TAs, ${totalDocs.toLocaleString()} documents, ${totalPages.toLocaleString()} pages
#
# For API guide and project overview, see /llms.txt
#
# Endpoints:
#   /api/corpus/ta{N}/         — document index for a TA
#   /api/corpus/ta{N}/{doc}.md — raw document text
#   /api/search?q={query}&format=plain — full-text search

`;

  for (const ta of tas) {
    const title = ta.title || "Untitled";
    text += `- TA${ta.ta_number}: ${title} (${ta.doc_count} docs, ${ta.total_pages}p) -> /api/corpus/ta${ta.ta_number}/\n`;
  }

  setHeader(event, "Content-Type", "text/plain; charset=utf-8");
  return text;
});
