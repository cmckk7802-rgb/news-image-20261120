// news-image-20261120 entry (Node 22, standard library only).
// The image is the entry.png beside this file: a front page drawn with
// Pillow that sums up Friday 20 November 2026 world news. This program
// copies it to /output/entry.png. The gate takes a whole PNG of at most
// 1 MiB and 1024 by 1024 pixels; the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

// The copy is byte-for-byte and deterministic: run it twice and the two
// outputs are identical, as the grader requires.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
