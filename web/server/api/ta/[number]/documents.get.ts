import { readdirSync } from "fs";
import { resolve, basename } from "path";

export default defineEventHandler((event) => {
  const num = parseInt(getRouterParam(event, "number") || "");
  if (!num) throw createError({ statusCode: 400, message: "Invalid TA number" });

  const dataDir = resolve(process.cwd(), "..", "data", `ta${num}`);

  try {
    const files = readdirSync(dataDir);
    const docs = files
      .filter((f) => f.endsWith(".md"))
      .map((f) => {
        const name = basename(f, ".md");
        const docType = name.replace(/_\d+$/, "");
        return { filename: f, name, docType };
      })
      .sort((a, b) => {
        const order = ["FAD", "ACD", "committee_papers", "scope", "scope_comments", "evaluation_report"];
        const ai = order.indexOf(a.docType);
        const bi = order.indexOf(b.docType);
        return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
      });

    return { ta_number: num, documents: docs };
  } catch {
    return { ta_number: num, documents: [] };
  }
});
