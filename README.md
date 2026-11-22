# The Solana Deeds playbook

The working method behind [The Solana Deeds](https://www.reddi.tech/blog/solana-b1-wallet-dashboard): twenty one-day Solana builds, each directed by one person and built by an AI coding agent, each ending in a merged build, a demo video, an article and social posts.

This repository is the master copy. Each deed repository carries a pinned copy under `docs/playbook/`, so a fresh agent session can pick a deed up from the word "begin" without the session that ran the last one.

## What is in it

| File | What it is for |
| --- | --- |
| [playbook/PLAYBOOK.md](playbook/PLAYBOOK.md) | The steps, from kickoff to retrospective |
| [playbook/briefs/](playbook/briefs/) | Brief templates for handing an outcome to a builder session |
| [playbook/video/](playbook/video/) | The demo video pipeline, its scripts, and [how the owner's own narration replaces the draft's synthetic voice](playbook/video/VOICE.md) before anything is published |
| [playbook/TRAPS.md](playbook/TRAPS.md) | Things that cost a retry, as observed |
| [scripts/install.py](scripts/install.py) | Copies a pinned snapshot into a deed repository, or checks one for drift |

It was written from Deeds #1 to #3, then revised after their three videos were re-recorded in the owner's voice and republished. Deed #4 was its first run by a session that did not write it. That session got from "begin" to three merged outcomes without correction, but the owner had to correct the video and the publishing seven times; the playbook was revised again from that retrospective. Deed #5 was the first run of those revised checks. Three of them caught a fault before anything was posted, and two did not hold: a narrated scene passed "words against picture" though a viewer could not tell which of two things was meant, and an Escape keystroke closed a dialog in an application the trap did not name. The owner still raised eight things before the agent acted on them, and four messages went out under his name before he had read them. The playbook was revised again from that retrospective, and those revisions have not yet been run by a fresh session.

## What it is not

It grants no authority. Merging, publishing, spending, credentials and repository settings stay with the person directing the work, under each repository's own contract. It names where secrets live by role only and holds none. It does not install an agent, a scheduler or a fleet policy.

## Installing a copy

```sh
python3 scripts/install.py apply /path/to/deed-repository
python3 scripts/install.py check /path/to/deed-repository
```

`apply` writes `docs/playbook/` with an `import.json` naming this repository's commit and each file's SHA-256, and adds one managed section to the target's `AGENTS.md`. Review and commit the result in the target through its own pull-request flow.

## Changing it

Change the master, never a copy. The retrospective at the end of each deed is where changes are proposed.

## Licence

MIT. See [LICENSE](LICENSE). The video scripts use a local Kokoro model (Apache-2.0) through kokoro-onnx (MIT); neither is redistributed here.
