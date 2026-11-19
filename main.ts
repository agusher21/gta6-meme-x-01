// gta6-meme-x-01 entry: the program hands the grader the post's address.
//
// The post itself is the entry. The house reads it from X — its first
// picture, then its text — and an AI judge compares posts two at a time.
// Nothing this program writes about the post is judged, so all it has to
// do is copy POST.json from the repository root into /output.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
try {
  copyFileSync(join(botDir, "POST.json"), join(outDir, "POST.json"));
} catch (err) {
  console.error(`could not copy POST.json out of ${botDir}: ${(err as Error).message}`);
  process.exit(1);
}
