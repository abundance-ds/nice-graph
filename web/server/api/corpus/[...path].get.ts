import { readFileSync, readdirSync } from "fs";
import { resolve } from "path";

export default defineEventHandler((event) => {
  const path = getRouterParam(event, "path") || "";
  const query = getQuery(event);

  if (path.includes(".."))
    throw createError({ statusCode: 400, message: "Invalid path" });

  // TA folder index: /api/corpus/ta876/ or /api/corpus/ta876
  const folderMatch = path.match(/^ta(\d+)\/?$/);
  if (folderMatch) {
    return serveFolderIndex(event, parseInt(folderMatch[1]));
  }

  // Document file: /api/corpus/ta876/FAD.md
  const fileMatch = path.match(/^ta(\d+)\/(.+)$/);
  if (!fileMatch)
    throw createError({
      statusCode: 400,
      message: "Use /api/corpus/ta{N}/ or /api/corpus/ta{N}/{document}.md",
    });

  const [, taNum, docName] = fileMatch;
  const fileName = docName.endsWith(".md") ? docName : `${docName}.md`;
  const filePath = resolve(process.cwd(), "..", "data", `ta${taNum}`, fileName);

  try {
    const content = readFileSync(filePath, "utf-8");
    setHeader(event, "Content-Type", "text/plain; charset=utf-8");

    if (query.download === "true") {
      setHeader(
        event,
        "Content-Disposition",
        `attachment; filename="ta${taNum}_${fileName}"`
      );
    }

    return content;
  } catch {
    throw createError({
      statusCode: 404,
      message: `Not found: ta${taNum}/${fileName}`,
    });
  }
});

function serveFolderIndex(event: any, taNum: number) {
  const db = useDb();
  const dataDir = resolve(process.cwd(), "..", "data", `ta${taNum}`);

  const meta = db
    .prepare("SELECT title FROM ta_resolved WHERE ta_number = ?")
    .get(taNum) as { title: string } | undefined;

  const title = meta?.title || `Technology Appraisal ${taNum}`;

  let files: string[];
  try {
    files = readdirSync(dataDir).filter((f) => f.endsWith(".md")).sort();
  } catch {
    throw createError({ statusCode: 404, message: `TA${taNum} not found` });
  }

  const docLabels: Record<string, string> = {
    FAD: "Final Appraisal Document",
    ACD: "Appraisal Consultation Document",
    committee_papers: "Committee Papers",
    scope: "Scope",
    scope_comments: "Scope Consultation Comments",
    evaluation_report: "Evaluation Report",
  };

  let md = `# TA${taNum} — ${title}\n\n## Documents\n\n`;

  for (const f of files) {
    const name = f.replace(".md", "");
    const base = name.replace(/_\d+$/, "");
    const label = docLabels[base] || name.replace(/_/g, " ");

    const row = db
      .prepare(
        "SELECT page_count FROM corpus WHERE ta_number = ? AND filename = ?"
      )
      .get(taNum, f) as { page_count: number } | undefined;

    const pages = row?.page_count ? ` (${row.page_count} pages)` : "";
    md += `- [${label}](${f})${pages}\n`;
  }

  setHeader(event, "Content-Type", "text/plain; charset=utf-8");
  return md;
}
