import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const raw = readFileSync(join(botDir, "POST.json"), "utf8");
const data = JSON.parse(raw) as { url?: unknown };
if (
  typeof data.url !== "string" ||
  !/^https:\/\/(?:(?:www\.|mobile\.)?(?:x|twitter)\.com)\/(?:[^/]+\/status|i\/web\/status)\/\d+$/.test(
    data.url,
  )
) {
  throw new Error(`Invalid POST.json url: ${String(data.url)}`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "POST.json"), JSON.stringify({ url: data.url }) + "\n", "utf8");
