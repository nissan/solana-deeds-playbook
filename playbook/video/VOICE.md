# The owner's voice

The published video is narrated by the owner, not by a synthetic voice. The synthetic voice is a stand-in while the script and picture are being written: it lets the owner review a draft, and it is what he listens to before recording each scene. Nothing with the synthetic voice in it is uploaded or published.

Deeds #1 to #3 were first published with the synthetic voice and then redone this way. From Deed #4 on, do it this way the first time.

## What you need

- The owner's voice booth app, a small local web app in his private `voice-booth` repository. Ask where it is checked out if it is not obvious; do not clone a second copy. Its README is the reference for everything below.
- The booth's media folder and a free local port. The booth prints its media folder when it starts, and its README says how it is chosen; `<media>` below means that folder. If the default port is taken, `booth.env` beside the app sets another.
- `ffmpeg` and `ffprobe`.

Recording uses the owner's microphone. Start the booth and hand it over; never start a recording yourself.

## The steps

1. **Draft cut.** Build the cut as [README.md](README.md) describes, with the synthetic reference voice and captions burned in (`python3 render.py N`). Open it locally for the owner. He is approving the picture, the order and the words, not the voice. Revise and re-render until he is happy with those.

2. **Take the synthetic voice out of the words and the picture.** Before anything goes to the booth, check that no script line, card, caption or diagram says the narration is synthetic, and that the script is something a person would say aloud. Search each scene's `script` and card `lines` for "synthetic" and the voice engine's name. Leave the manifest's top-level `voice` block alone: it describes the reference voice. If the draft had such a line for review, remove it from the script, the card, the captions and the planned upload description together, then synthesise that scene's reference again so its captions match.

3. **Render the clean picture.** `python3 render.py N clean` writes `renders/demo-vN-clean.mp4` (no captions) and `receipts/demo-vN-clean-segments.json` (each scene's exact length in frames).

4. **Import it into the booth.** From the booth's folder:

   ```sh
   python3 import_package.py --id deed-NN --title "The Solana Deeds #NN: ..." \
       --video    CUT/renders/demo-vN-clean.mp4 \
       --manifest CUT/manifest.json \
       --narration CUT/narration-v1.json \
       --segments CUT/receipts/demo-vN-clean-segments.json
   ```

   This cuts one silent clip per scene on exact frames and copies each scene's reference audio. Audio paths in `narration-v1.json` are read relative to that file. To swap in a corrected picture or script later, run it again with `--replace`: takes and choices are kept, and it refuses if a scene that already has a take would disappear.

5. **Hand over.** Start the booth (`./start`), check all scenes list with no missing clip or reference, and tell the owner it is ready and at what address. For each scene he reads the script, hears the reference, records, compares the picture with either voice, and keeps a take. He can stop and come back; takes and choices are saved as he goes. Then he presses "Assemble the final cut".

6. **Check the cut he assembled.** It is `<media>/deed-NN/renders/deed-NN-voice-vKK.mp4`, with a `.srt` and a `.json` record beside it. Before calling it publishable:
   - The record's `reference` and `undecided` lists are empty. A cut that still uses the reference voice for any scene is a mixed cut: it presents a synthetic voice with nothing saying so, and it must not be uploaded.
   - Full decode with no errors; frame count equals the scene lengths in the record; loudness near -16 LUFS.
   - Captions: at most two lines, nothing about a synthetic voice. Inside each scene the caption times were spread over the owner's speech, not matched to his words, and the text is still the script. If he said something different, fix that scene's caption text in `<media>/deed-NN/package.json` and assemble again. A later `--replace` import rewrites that file, so make the same change in the cut's narration file too.
   - Record the file's SHA-256.

   Say plainly what you did not check (you cannot hear the take; you did not compare each caption with what was said).

7. **Approval.** The owner watches the assembled cut and approves that exact file. The approval attaches to its SHA-256. If he re-records a scene and assembles again, that is a new file and a new approval.

8. **Upload and publish** as [README.md](README.md) and [PLAYBOOK.md](../PLAYBOOK.md) step 7 describe.

9. **Evidence.** Copy the approved cut, its captions and its assembly record into `docs/evidence/video/` with the manifest and scripts that made the picture. The evidence page says the narration is the owner's own recorded voice, names the tool only as the reference used while recording, and lists what is replayed or illustrated. The owner's raw takes stay on his machine: never commit or upload them.

## Rules

- The microphone is the owner's to start, every time.
- Never present a synthetic voice as a person, and never label a person's recording as synthetic. The card, the script, the captions, the upload settings and the description must all agree with what is actually heard.
- The booth's picture box is a preview. If something looks cropped there, check the clip itself before changing the render.
- Do not edit a take, and do not assemble on the owner's behalf from choices he has not made.
