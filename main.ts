// news-image-20261121-cand-c: regenerates entry.png deterministically with
// the Python PIL build script and copies it to the output dir.
// All paths resolve from this file's own directory; no relative paths.
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const here = fileURLToPath(new URL(".", import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

// Regenerate entry.png from the build script (deterministic, no network).
execFileSync("python3", [join(here, "build_entry.py")], {
  cwd: here,
  stdio: "inherit",
  env: { ...process.env, MAKEFUN_OUTPUT_DIR: outDir },
});

const sourcePath = join(here, "entry.png");
const bytes = readFileSync(sourcePath);
if (bytes.length === 0) {
  throw new Error(`entry.png is empty (0 bytes) at ${sourcePath}`);
}
if (bytes.length > 1048576) {
  throw new Error(
    `entry.png too large: ${bytes.length} bytes exceeds 1 MiB limit (1048576 bytes)`,
  );
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), bytes);
const digest = createHash("sha256").update(bytes).digest("hex");
console.log(`entry.png sha256 ${digest} (${bytes.length} bytes)`);
