# The Solana Deeds playbook

The working method behind [The Solana Deeds](https://www.reddi.tech/blog/solana-b1-wallet-dashboard): twenty one-day Solana builds, each directed by one person and built by an AI coding agent, each ending in a merged build, a demo video, an article and social posts.

This repository is the master copy. Each deed repository carries a pinned copy under `docs/playbook/`, so a fresh agent session can pick a deed up from the word "begin" without the session that ran the last one.

## What is in it

| File | What it is for |
| --- | --- |
| [playbook/PLAYBOOK.md](playbook/PLAYBOOK.md) | The steps, from kickoff to retrospective |
| [playbook/briefs/](playbook/briefs/) | Brief templates for handing an outcome to a builder session |
| [playbook/video/](playbook/video/) | The demo video pipeline and its two scripts |
| [playbook/TRAPS.md](playbook/TRAPS.md) | Things that cost a retry, as observed |
| [scripts/install.py](scripts/install.py) | Copies a pinned snapshot into a deed repository, or checks one for drift |

It was written from Deeds #1 to #3 and has not yet been run by a session that did not write it. Deed #4 is its first test.

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
