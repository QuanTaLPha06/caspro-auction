import * as mupdf          from 'mupdf';
import { createClient }   from '@supabase/supabase-js';
import fs                from 'fs';
import path              from 'path';
import { fileURLToPath } from 'url';
import { spawnSync }     from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT      = path.resolve(__dirname, '..');

// ── Config ───────────────────────────────────────────────────────────────────
const SUPABASE_URL  = process.env.VITE_SUPABASE_URL  || 'https://fvtphepaneyyokaqmtvw.supabase.co';
const SUPABASE_KEY  = process.env.SUPABASE_SERVICE_ROLE_KEY 
                   || process.env.VITE_SUPABASE_SERVICE_ROLE_KEY 
                   || process.env.VITE_SUPABASE_ANON_KEY 
                   || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ2dHBoZXBhbmV5eW9rYXFtdHZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyNDE4NDMsImV4cCI6MjEwMjgxNzg0M30.F5J0aWAlEzIsp2i_9Q_7q8XrlZsxB5TrKjQxTVHTDKA';
const POSSIBLE_PDFS = [
  path.join(__dirname, 'IPL_Auction_Deck_2026.pptx.pptx.pdf'),
  path.join(__dirname, 'IPL_Auction_Deck_2026 (1).pdf'),
  path.join(__dirname, 'IPL_Auction_Deck_2026.pdf'),
];
const PDF_PATH      = POSSIBLE_PDFS.find(p => fs.existsSync(p)) || POSSIBLE_PDFS[0];
const MAP_PATH      = path.join(__dirname, 'page_map.json');
const PLAYERS_JSON  = path.join(ROOT, 'players.json');
const BUCKET        = 'player-slides';
const LOCAL_OUT_DIR = path.join(ROOT, 'public', 'slides');

// ── CLI flags ─────────────────────────────────────────────────────────────────
const AUTO       = process.argv.includes('--auto');
const DRY_RUN    = process.argv.includes('--dry');
const SAVE_LOCAL = process.argv.includes('--local'); // saves directly to public/slides/{player_id}.jpg
const SKIP       = parseInt(process.argv.find(a => a.startsWith('--skip='))?.split('=')[1] ?? '0', 10);
const ONLY_PAGE  = process.argv.find(a => a.startsWith('--page='))?.split('=')[1];
const BATCH_SIZE = 30; // WASM heap stays safely below memory limit in 30-page chunks

const FROM_ARG   = process.argv.find(a => a.startsWith('--from='))?.split('=')[1];
const TO_ARG     = process.argv.find(a => a.startsWith('--to='))?.split('=')[1];
const IS_WORKER  = process.argv.includes('--worker');

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  if (!fs.existsSync(PDF_PATH)) {
    console.error(`\n❌  PDF not found: ${PDF_PATH}\n`);
    process.exit(1);
  }

  // Build page → player_id map
  let pageMap;
  if (AUTO) {
    const players = JSON.parse(fs.readFileSync(PLAYERS_JSON, 'utf8'));
    pageMap = players.map((p, i) => ({
      page:      i + 1 + SKIP,
      player_id: String(p.id),
    }));
  } else {
    if (!fs.existsSync(MAP_PATH)) {
      console.error(`\n❌  page_map.json not found.\n    Create scripts/page_map.json or run with --auto\n`);
      process.exit(1);
    }
    pageMap = JSON.parse(fs.readFileSync(MAP_PATH, 'utf8'));
  }

  // ── Master Orchestrator (spawns clean subprocesses per batch) ─────────────
  if (!IS_WORKER && !ONLY_PAGE) {
    console.log(`\n📄  Loading PDF: ${path.basename(PDF_PATH)}`);
    console.log(`🗺   Total slides to process: ${pageMap.length} (in batches of ${BATCH_SIZE})`);
    if (DRY_RUN) console.log(`🔍  DRY RUN MODE — no uploads will occur`);
    console.log('');

    for (let start = 0; start < pageMap.length; start += BATCH_SIZE) {
      const end = Math.min(start + BATCH_SIZE - 1, pageMap.length - 1);
      const args = [
        ...process.argv.slice(2),
        '--worker',
        `--from=${start}`,
        `--to=${end}`
      ];

      const res = spawnSync(process.execPath, [fileURLToPath(import.meta.url), ...args], {
        stdio: 'inherit',
        env: process.env,
      });

      if (res.status !== 0) {
        console.error(`\n⚠️  Batch ${start}-${end} failed with exit code ${res.status}`);
      }
    }

    console.log(`\n✨  All batches finished! Check Supabase Storage bucket "${BUCKET}".\n`);
    return;
  }

  // ── Worker Execution (handles a slice of items) ───────────────────────────
  const startIdx = FROM_ARG ? parseInt(FROM_ARG, 10) : 0;
  const endIdx   = TO_ARG   ? parseInt(TO_ARG, 10)   : pageMap.length - 1;
  const slice    = pageMap.slice(startIdx, endIdx + 1);

  const pdfBytes = fs.readFileSync(PDF_PATH);
  const doc = mupdf.Document.openDocument(pdfBytes, 'application/pdf');
  const totalPages = doc.countPages();
  const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

  for (let i = 0; i < slice.length; i++) {
    const item = slice[i];
    const globalIdx = startIdx + i;
    const { page, player_id } = item;
    const label = `[${globalIdx + 1}/${pageMap.length}] Page ${page} → ${player_id}.jpg`;
    process.stdout.write(`  ${label} … `);

    if (page > totalPages || page < 1) {
      process.stdout.write(`⚠️  SKIP (page out of range)\n`);
      continue;
    }

    try {
      const pngBuf = renderPage(doc, page);

      if (DRY_RUN) {
        process.stdout.write(`✅  (${(pngBuf.length / 1024).toFixed(0)} KB)\n`);
        continue;
      }

      if (SAVE_LOCAL) {
        if (!fs.existsSync(LOCAL_OUT_DIR)) fs.mkdirSync(LOCAL_OUT_DIR, { recursive: true });
        const filePath = path.join(LOCAL_OUT_DIR, `${player_id}.jpg`);
        fs.writeFileSync(filePath, pngBuf);
        process.stdout.write(`✅  (saved local ${(pngBuf.length / 1024).toFixed(0)} KB)\n`);
        continue;
      }

      const { error } = await supabase.storage
        .from(BUCKET)
        .upload(`${player_id}.jpg`, pngBuf, {
          contentType: 'image/png',
          upsert:      true,
        });

      if (error) throw error;
      process.stdout.write(`✅  (${(pngBuf.length / 1024).toFixed(0)} KB)\n`);
    } catch (err) {
      process.stdout.write(`❌  ${err.message}\n`);
    }
  }
}

// ── Render a single PDF page to PNG buffer ──────────────────────────────────
function renderPage(doc, pageNum) {
  const page   = doc.loadPage(pageNum - 1);
  const matrix = mupdf.Matrix.scale(1.5, 1.5);
  const bbox   = mupdf.Rect.transform(page.getBounds(), matrix);
  const pixmap = new mupdf.Pixmap(mupdf.ColorSpace.DeviceRGB, bbox, false);
  pixmap.clear(255);

  const device = new mupdf.DrawDevice(matrix, pixmap);
  page.run(device, mupdf.Matrix.identity);
  device.close();

  const pngBytes = pixmap.asPNG();
  return Buffer.from(pngBytes);
}

main().catch(e => { console.error('\n💥', e); process.exit(1); });

