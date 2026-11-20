/**
 * Copy the pre-rendered infographic (entry.png) into the make.fun
 * output directory. Standard library only, no network access.
 *
 * The image itself is produced by generate_image.py; this script only
 * places the finished file where the harness expects it.
 */

import { copyFile, mkdir, stat } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out");
const target = join(outDir, "entry.png");

await mkdir(outDir, { recursive: true });
await copyFile(source, target);
const info = await stat(target);
console.log(`copied ${source} -> ${target} (${info.size} bytes)`);
