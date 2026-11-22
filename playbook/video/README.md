# Demo video pipeline

A deed's demo is built from a scene manifest, so one scene can be rewritten or re-voiced without redoing the rest. Direction for what the video should say is in [PLAYBOOK.md](../PLAYBOOK.md) step 6. If the owner has a video-production skill installed, read it first; it wins where it differs.

The video is made in two passes. The first is a **draft** with a synthetic reference voice, so the owner can review the picture and the words. The second replaces every scene's narration with **the owner's own recording**, made scene by scene in his voice booth: [VOICE.md](VOICE.md). Only the second is uploaded.

## Work outside the repository

Build each cut in a fresh directory (for example `~/Videos/deed-NN-vK.XXXXXX/`). Raw takes, models and rejected cuts stay there. Only the approved cut and its provenance are copied into `docs/evidence/video/`.

```
manifest.json     scenes, on-screen lines, narration script, reference voice settings
synthesize.py     manifest -> one reference WAV per scene + narration-v1.json (timings, hashes)
stage.html        the animated scenes, one <section> each (start from stage-example.html)
manifest-example.json  a small scene list showing each kind of scene
animate.cjs       stage.html + narration-v1.json -> one clip and one end still per animated scene
render.py         manifest + narration-v1.json -> renders/demo-vN.mp4 + captions/demo-vN.srt (draft)
                  with "clean": renders/demo-vN-clean.mp4, no captions, for the voice booth
sources/          screen takes, stills, diagrams, screenshots
validation/       phase stills, contact sheet, decode log
receipts/         SHA-256 of each render, and each scene's exact length in frames
```

## Tools

- `ffmpeg` and `ffprobe`; the Liberation Sans and Liberation Mono fonts (paths are set at the top of `render.py`).
- Python with `kokoro-onnx` and `soundfile`, and the Kokoro model and voices files, for the reference voice. `KOKORO_MODELS` below stands for the folder holding `kokoro-v1.0.onnx` and `voices-v1.0.bin`; the owner already has one, so ask where it is rather than downloading another. `synthesize.py` refuses model files whose SHA-256 differs from the pinned release, and refuses to overwrite existing takes. One way to run it without installing anything globally:

  ```sh
  uv run --no-project --with kokoro-onnx==0.6.1 --with soundfile==0.13.1 \
    python synthesize.py --manifest manifest.json --model-dir "$KOKORO_MODELS" --work-dir .
  PUPPETEER_DEPS=/folder/with/puppeteer node animate.cjs   # only if the cut has animated scenes
  python3 render.py N
  ```

- Node with `puppeteer` and a Chromium browser, for the animated scenes. `animate.cjs` says how it finds them.
- Mermaid for the diagram. Keep the `.mmd` source in the repository and render it to a 1280x720 PNG used as a `still` scene, or draw it into a stage section.

## Manifest

Top level: `project`, `sourceCommit` (the commit the demo shows), `geometry` (1280x720 at 30 fps), `audioPolicy`, `voice` (the reference voice: `preset`, `language`, `speed`, `synthetic: true`, `cloned: false`) and `scenes`. The scripts read only `voice` and `scenes`; the rest is the record a reader needs. `voice.synthetic: true` describes the reference voice and stays true: it is not a statement about the published narration. [manifest-example.json](manifest-example.json) shows one scene of each kind.

Each scene has a stable `id`, a `purpose`, a `script` (a list of sentences to speak), and a `mediaType`:

- `card`: `lines` of text, each with `text`, `size`, `y`, and optionally `x`, `color`, and `at` (seconds into the scene when the line appears). Lines with `at` are how a terminal replay is animated; lines with `x` are set in the mono font on a terminal panel.
- `still`: `selectedTake` is an image held for the length of the narration.
- `source`: `selectedTake` is a screen recording; `endStill` is required, and is held if the narration runs longer than the recording.
- `clip` with `"stage": true`: an animated scene. `animate.cjs` draws it from `stage.html` into `selectedTake` and writes `endStill`. Each sentence of the script starts a phase of the picture, so the drawing changes when the words do. This is how the analogy scenes are made.

Write numbers and product names the way they should be spoken ("Token twenty twenty-two", "nine hundred seventy-five"). The owner will read this script aloud, so write sentences a person would say, and write nothing about the voice being synthetic: the script, the cards and the captions all end up in the published video.

Ids are letters, digits, `-` and `_` only. Once the owner has recorded a scene, keep its id: his takes are filed under it.

## A new cut

1. Copy the previous cut's `manifest.json`, change only the scenes that need it, and bump the cut number. To keep unchanged narration byte-identical, reuse those scenes' takes and receipt entries and synthesise only the changed scenes.
2. Render. `render.py` never overwrites a render.
3. Validate before anyone watches: full decode with no errors; duration, size, frame rate and codecs; loudness near -16 LUFS with true peak under -1 dBTP; every caption cue in bounds, non-overlapping and at most two lines; a contact sheet with a frame from every scene, early and late for animated ones; the cards all the same darkness (see [TRAPS.md](../TRAPS.md)); the render's SHA-256 recorded.
4. Open the exact file locally for the owner. At the draft stage he approves the picture and the words. Then follow [VOICE.md](VOICE.md); the approval that counts for publishing is the one he gives the cut assembled with his own voice, recorded against its SHA-256.
5. On that approval, copy the approved cut, its captions and assembly record, the manifest, narration receipt, scripts, stage and contact sheet into `docs/evidence/video/` and describe them in the outcome's evidence page: whose voice it is, what is a replay, what is a real screenshot, what is illustrated, what was not shown.

## Adding or changing one scene after the owner has started recording

His takes are filed under scene ids, and a scene he has recorded must not change length or words under him.

1. Add the scene to `manifest.json` with a new id, or give a changed scene a new take number. Leave every other scene's entry alone.
2. `synthesize.py` refuses to write over existing takes. Synthesise only the new scene: copy the manifest with just that scene into a new folder, run the synthesiser there, then copy its audio files beside the others and insert its entry into `narration-v1.json` at the scene's place. Keep a copy of the receipt from before.
3. Draw only that scene: `node animate.cjs --scene=ID`. Clips that exist are left as they are.
4. Render a new numbered cut and its clean copy. Compare the two segment files: no existing scene's frame count may differ, unless that scene's picture is the thing being changed.
5. Compare the narration receipt with the copy from before: no existing scene's entry may differ.
6. Import into the booth with `--replace`, then confirm his choices and every take file are unchanged.

## Screen recordings and screenshots

- Record the application from the commit named in `sourceCommit`, built for production.
- A recorder emits no frames once the page stops changing; take a screenshot for the held end frame.
- Explorer screenshots are taken from the real transaction pages and cropped to the status and action rows. Confirm the signature and "finalized" are in the frame.
- No credentials, wallet secrets, notifications or private tabs in any frame.

## Upload

Uploading is a separate instruction from approving the cut. Upload the exact approved file, narrated by the owner, with a description that says who narrates and what is illustrated or replayed.

- **Visibility:** unlisted unless told otherwise. Ask before the article goes out whether it should be public.
- **Altered or synthetic content:** answer for what is in the file. With the owner's own voice and plainly illustrated scenes the answer is no. If any synthetic voice remained, the answer would be yes, and the cut should not be going up at all (see [VOICE.md](VOICE.md)).
- **Captions:** upload the sidecar file with timing, then publish it. Uploading alone leaves a draft. Confirm from a signed-out page that a manual caption track is listed.
- Wait for the platform's checks, confirm the video plays signed out, and record the URL beside the file hash.
- **Replacing a video that is already linked:** the platform gives a new upload a new address. Update every place that links the old one (article, public source README, evidence page, posts that can be edited) and add a reply where a post cannot be edited. Delete the old upload only on the owner's instruction, and tell him which posts will be left with a dead link.
