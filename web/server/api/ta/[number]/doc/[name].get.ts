import { readFileSync } from "fs";
import { resolve } from "path";

export default defineEventHandler((event) => {
  const num = parseInt(getRouterParam(event, "number") || "");
  const name = getRouterParam(event, "name") || "";
  if (!num || !name)
    throw createError({ statusCode: 400, message: "Invalid parameters" });

  if (name.includes("..") || name.includes("/"))
    throw createError({ statusCode: 400, message: "Invalid document name" });

  const filePath = resolve(process.cwd(), "..", "data", `ta${num}`, `${name}.md`);

  try {
    const content = readFileSync(filePath, "utf-8");
    return { ta_number: num, name, content };
  } catch {
    throw createError({
      statusCode: 404,
      message: `Document ${name} not found for TA${num}`,
    });
  }
});
