// Draws the animated scenes of manifest.json from stage.html, timed to narration-v1.json.
//
//   node animate.cjs --preview        stills of each phase only, into validation/
//   node animate.cjs [--scene=ID]     each scene's clip to its selectedTake, and its last
//                                     drawing to its endStill
//
// An animated scene is a manifest scene with "stage": true, "mediaType": "clip", a
// "selectedTake" such as "renders/s02-analogy-take-1.mp4" and an "endStill" such as
// "validation/s02-analogy-late.png". stage.html holds one <section id="SCENE ID"> per scene
// and a function frame(id, t, hits) that draws the scene at t seconds; hits[i] is when the
// i-th sentence of the scene's script starts, so the picture changes when the words do.
// stage-example.html is a worked example.
//
// Run from the cut's folder. PUPPETEER_DEPS names a folder whose node_modules has puppeteer;
// CHROMIUM names the browser binary (default /usr/bin/chromium).
const { readFile, mkdir } = require('node:fs/promises');
const { spawn } = require('node:child_process');
const { once } = require('node:events');
const { resolve, dirname } = require('node:path');
const { pathToFileURL } = require('node:url');
const { createRequire } = require('node:module');
if (!process.env.PUPPETEER_DEPS) { console.error('Set PUPPETEER_DEPS to a folder whose node_modules has puppeteer.'); process.exit(1); }
const puppeteer = createRequire(resolve(process.env.PUPPETEER_DEPS, 'package.json'))('puppeteer');

async function main() {
  const preview = process.argv.includes('--preview');
  const specs = JSON.parse(await readFile('manifest.json', 'utf8')).scenes.filter(s => s.stage);
  for (const dir of ['validation', ...specs.flatMap(s => [dirname(s.selectedTake), dirname(s.endStill)])]) await mkdir(dir, { recursive: true });
  const only = process.argv.find(a => a.startsWith('--scene='))?.slice(8);
  const receipt = JSON.parse(await readFile('narration-v1.json', 'utf8'));
  const browser = await puppeteer.launch({ executablePath: process.env.CHROMIUM || '/usr/bin/chromium', headless: true, args: ['--disable-gpu', '--disable-dev-shm-usage'] });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
    await page.goto(pathToFileURL(resolve('stage.html')).href);
    await page.evaluate(() => document.fonts.ready);
    for (const scene of specs) {
      if (only && scene.id !== only) continue;
      const entry = receipt.scenes.find(item => item.id === scene.id);
      const hits = scene.script.map(s => {
        const prefix = s.split(' ').slice(0, 4).join(' ');
        const cue = entry.captions.find(c => c.text.replaceAll('\n', ' ').startsWith(prefix));
        if (!cue) throw new Error(`Missing caption timing: ${prefix}`);
        return cue.start;
      });
      const picture = t => page.evaluate((id, t, hits) => frame(id, t, hits), scene.id, t, hits);
      await picture(entry.durationSeconds);
      await page.screenshot({ path: scene.endStill });
      for (const [i, h] of hits.entries()) { await picture(Math.min(h + 6, (hits[i + 1] ?? entry.durationSeconds) - 0.15)); await page.screenshot({ path: `validation/${scene.id}-p${i}.png` }); }
      if (preview) { console.log(scene.id, hits.join(', ')); continue; }
      const frames = Math.ceil((entry.durationSeconds + .32) * 15);
      // -n: an existing take is never overwritten; give a changed scene a new take number.
      const clip = spawn('ffmpeg', ['-v', 'error', '-n', '-f', 'image2pipe', '-framerate', '15', '-c:v', 'mjpeg', '-i', 'pipe:0', '-vf', 'fps=30', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', scene.selectedTake], { stdio: ['pipe', 'ignore', 'inherit'] });
      const exited = once(clip, 'exit');
      for (let n = 0; n < frames; n++) {
        await picture(n / 15);
        const jpeg = await page.screenshot({ type: 'jpeg', quality: 92 });
        if (!clip.stdin.write(jpeg)) await once(clip.stdin, 'drain');
      }
      clip.stdin.end();
      const [status] = await exited;
      if (status !== 0) throw new Error(`Encoder failed in ${scene.id}`);
      console.log(`${scene.id}: ${frames} drawings; phase changes at ${hits.join(', ')}s`);
    }
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
