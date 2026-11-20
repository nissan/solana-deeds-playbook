# Demo video pipeline

A deed's demo is built from a scene manifest, so one scene can be rewritten or re-voiced without redoing the rest. Direction for what the video should say is in [PLAYBOOK.md](../PLAYBOOK.md) step 6. If the owner has a video-production skill installed, read it first; it wins where it differs.

## Work outside the repository

Build each cut in a fresh directory (for example `~/Videos/deed-NN-vK.XXXXXX/`). Raw takes, models and rejected cuts stay there. Only the approved cut and its provenance are copied into `docs/evidence/video/`.

```
manifest.json     scenes, on-screen lines, narration script, voice settings
synthesize.py     manifest -> one narration WAV per scene + narration-v1.json (timings, hashes)
render.py         manifest + narration-v1.json -> renders/demo-vN.mp4 + captions/demo-vN.srt
sources/          screen takes, stills, diagrams, screenshots
validation/       contact sheet, decode log
receipts/         SHA-256 of the render and its inputs
```

## Tools

- `ffmpeg` and `ffprobe`; the Liberation Sans and Liberation Mono fonts (paths are set at the top of `render.py`).
- Python with `kokoro-onnx` and `soundfile`, and the Kokoro model and voices files. `synthesize.py` refuses model files whose SHA-256 differs from the pinned release, and refuses to overwrite existing takes. One way to run it without installing anything globally:

  ```sh
  uv run --no-project --with kokoro-onnx==0.6.1 --with soundfile==0.13.1 \
    python synthesize.py --manifest manifest.json --model-dir "$KOKORO_MODELS" --work-dir .
  python3 render.py N
  ```

- Mermaid CLI for the diagram. Keep the `.mmd` source in the repository and render it to a 1280x720 PNG used as a `still` scene.

## Manifest

Top level: `project`, `sourceCommit` (the commit the demo shows), `geometry` (1280x720 at 30 fps), `audioPolicy`, `voice` (`preset`, `language`, `speed`, `synthetic: true`, `cloned: false`) and `scenes`.

Each scene has a stable `id`, a `purpose`, a `script` (a list of sentences to speak), and a `mediaType`:

- `card`: `lines` of text, each with `text`, `size`, `y`, and optionally `x`, `color`, and `at` (seconds into the scene when the line appears). Lines with `at` are how a terminal replay is animated; lines with `x` are set in the mono font on a terminal panel.
- `still`: `selectedTake` is an image held for the length of the narration.
- `source`: `selectedTake` is a screen recording; `endStill` is held if the narration runs longer.

Write numbers and product names the way they should be spoken ("Token twenty twenty-two", "nine hundred seventy-five").

## A new cut

1. Copy the previous cut's `manifest.json`, change only the scenes that need it, and bump the cut number. To keep unchanged narration byte-identical, reuse those scenes' takes and receipt entries and synthesise only the changed scenes.
2. Render. `render.py` never overwrites a render.
3. Validate before anyone watches: full decode with no errors; duration, size, frame rate and codecs; loudness near -16 LUFS with true peak under -1 dBTP; every caption cue in bounds, non-overlapping and at most two lines; a contact sheet with a frame from every scene, early and late for animated ones; the render's SHA-256 recorded.
4. Open the exact file locally for the owner. Record the approval against the SHA-256.
5. On approval, copy the render, captions, manifest, narration receipt, scripts and contact sheet into `docs/evidence/video/` and describe them in the outcome's evidence page: what is a replay, what is a real screenshot, what is synthetic, what was not shown.

## Screen recordings and screenshots

- Record the application from the commit named in `sourceCommit`, built for production.
- A recorder emits no frames once the page stops changing; take a screenshot for the held end frame.
- Explorer screenshots are taken from the real transaction pages and cropped to the status and action rows. Confirm the signature and "finalized" are in the frame.
- No credentials, wallet secrets, notifications or private tabs in any frame.

## Upload

Uploading is a separate instruction from approving the cut. Upload the exact approved file, unlisted unless told otherwise, with the sidecar captions, the synthetic-media disclosure switched on and a description that says what is illustrated, replayed or synthetic. Wait for the platform's checks, then confirm the video plays signed out and record the URL beside the file hash.
