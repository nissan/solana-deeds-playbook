# The Solana Deeds playbook

How one deed goes from "begin" to a merged build, a demo video, an article and social posts. Written from Deeds #1 to #3, and revised after their videos were re-recorded in the owner's own voice and republished. It is for a fresh agent session with no memory of earlier deeds, and for the person directing it.

This folder is a pinned copy. The master is `nissan/solana-deeds-playbook`; do not edit the copy. If a step here is wrong, finish the deed, then propose the change to the master in the retrospective (step 9).

## What wins when rules disagree

1. The owner's instruction in the current session.
2. This repository's `AGENTS.md`, `docs/SECURITY.md`, `docs/DECISIONS.md` and the outcome issues.
3. The delivery kit (`docs/agent-settings/`, `docs/delivery/`).
4. This playbook.

The playbook gives no authority. Merging, publishing, spending, changing repository settings and anything with credentials still need the owner each time, as the repository contract says.

## The shape of a deed

A deed repository starts as a plan: three or four outcome issues and no product code.

| Outcome | What it is | Brief to use |
| --- | --- | --- |
| `-001` | Pinned toolchain and an empty scaffold that builds and runs one test | [briefs/01-scaffold.md](briefs/01-scaffold.md) |
| `-002` | The core user outcome, sized for one day | [briefs/02-core.md](briefs/02-core.md) |
| `-003` | Reviewer proof: README, reproduction, secret scan, demo | [briefs/03-reviewer-proof.md](briefs/03-reviewer-proof.md) |
| `-004` | Stretch outcome, only after the core is merged | [briefs/04-stretch.md](briefs/04-stretch.md) |

After the outcomes: demo video, drafted with a reference voice and then narrated by the owner (step 6), article and social posts (step 7), public source (step 8), retrospective (step 9).

## 1. When the owner says "begin"

1. Read `AGENTS.md`, `README.md`, `docs/SECURITY.md`, `docs/DECISIONS.md`, `docs/ROUTING.md`, `docs/agent-settings/CHECKS.md`, `planning/graph.json` and the first open outcome issue.
2. Check the starting state: default branch clean, no open pull requests, the last hosted run on `main` green. If the outcome's acceptance is already met on `main`, say so with the evidence and move to the next outcome.
3. Record intake before any edit: append a receipt to `planning/intake.json` mapping each ask to an issue, with the SHA-256 of the issue body as read back from the forge, then run `python3 scripts/intake.py --base FULL_BASE_SHA --live`. The live check needs a token: `GITHUB_TOKEN=$(gh auth token)`. Without it a private repository answers 404.
4. Work in one worktree per outcome, on a branch named for the outcome (`b4-001-toolchain`). Keep the main clone on `main`. The owner keeps deed clones together in one projects folder; ask where if it is not obvious, and do not invent a second location.
5. Start the build journal (step 5) with the kickoff entry.
6. Say which builder will do the work. `docs/agent-settings/CHECKS.md` names who builds and who reviews. If the named builder cannot be started, stop and say so; never switch provider silently.

## 2. Giving an outcome to a builder

A long outcome goes to a separate builder session with a written brief, so the directing session stays free and the work survives a restart.

1. Check capacity first, by the rule in the owner's fleet policy. Unknown capacity is a stop, not a free slot.
2. Fill in the brief template for the outcome type. Every `[BRACKET]` is re-derived for this deed; nothing is carried over from an earlier deed.
3. Save the brief outside the repository (for example `~/.local/state/<outcome>/brief.md`) and tell the builder to finish by writing `handoff.md` beside it.
4. Start the builder in the outcome's worktree. With Claude Code:

   ```sh
   claude --bg -n <outcome-branch> --model <model> --effort <effort> \
     --permission-mode acceptEdits --allowedTools Bash Edit Write Read Glob Grep \
     -- "$(cat ~/.local/state/<outcome>/brief.md)"
   ```

   Model and effort come from `docs/ROUTING.md` and the fleet policy, not from this file. A new worktree needs its workspace trust prompt accepted once; that is the owner's consent to give, so ask the first time.
5. Watch it. `claude agents --json` shows `busy`, `idle`, or `waiting` with a reason. A builder that is `waiting` on a permission prompt is stalled, not working: read the prompt, and approve only what the brief already allows.
6. When the handoff arrives, check it against the forge yourself: the pull request head matches the handoff's commit, and the hosted checks on that commit passed. Report what you verified separately from what the builder claims.
7. Stop the finished session so it does not hold a slot.

## 3. Review and merge

1. Tell the owner what was built, what was checked, and every open risk the builder listed. Recommend which risks to fix before merge and which to list as limitations.
2. The owner decides. A fix requested at review gets a test that fails before the fix and passes after.
3. Merge only on the owner's instruction, only the exact reviewed head (`gh pr merge N --merge --match-head-commit SHA`), with a merge commit.
4. Watch the hosted run on `main` after the merge. A failure there is fixed before new work starts.
5. Update the outcome's status line in `planning/graph.json`, regenerate the mirrors, and sync the issue body from the mirror.

Scenarios written by an agent stay "Draft" until the owner confirms them. Building to draft scenarios is allowed; calling them accepted is not.

## 4. Working on devnet

- Devnet, a local validator or a mainnet fork only. Never mainnet.
- One owner-funded devnet payer is shared across deeds. Its keypair file lives outside every repository and is named by `DEVNET_PAYER_KEYPAIR`. Read it by path; never print, copy or commit it. Check its balance before and after and report both.
- Scripts refuse to sign unless the RPC's genesis hash is devnet's.
- Agree a spend cap with the owner before a deployment. A program deployment costs rent in proportion to its size; pass a `--max-len` close to the binary size.
- Print each signature and its explorer link before sending, wait for `finalized`, and read the result back from the chain. If a send is interrupted, reconcile by signature; do not resend blindly.
- Prove a rejection with a signed simulation, not a failed transaction: assert the named error and that the accounts did not change.
- Save one real run's console output to `docs/evidence/`. The demo video replays it.
- Do not ask the faucet from code. See [TRAPS.md](TRAPS.md).

## 5. The build journal

Start it at kickoff and add to it as things happen, not at the end. It is what the article is written from.

- One private file per deed, `docs/evidence/deed-NN-journal.md`. Record the request, what changed, why, and the commit or check that proves it.
- Record failures and corrections with the same care as successes: the rejected video cut, the check that caught a real bug, the thing that had to be asked twice. These are the story.
- Sanitised decisions only. No credentials, no raw chat, no private browser state. The raw session stays local.
- Commit often, in small commits whose messages say why.

## 6. The demo video

Read [video/README.md](video/README.md) for the pipeline and [video/VOICE.md](video/VOICE.md) for the owner's narration. The direction below is what the owner asked for across Deeds #1 to #3; apply it from the first cut.

The video is made in two passes. A **draft** with a synthetic reference voice gets the picture and the words right. Then **the owner records every scene himself** in his voice booth and assembles the cut that is published. The synthetic voice is never published.

1. **Goal first.** The opening card and first spoken line say what the deed builds and what outcome we want. Do not open on a puzzle the viewer has no context for.
2. **Teach before showing.** Assume a curious beginner. Explain the accounts or concepts the deed depends on before the walkthrough, at roughly a ten-to-fifteen-year-old's level. Say what a thing is before using its name.
3. **One concrete analogy, with its own animated scene.** Find a real-world story that makes the mechanism obvious and stays true to how the chain behaves, then lead back to the real flow. Check the analogy against the protocol: if it would teach something false, change the analogy. Draw it as an animated scene near the start, where each sentence changes the picture. A script of feature statements over screen footage is not enough: Deed #1 was redone for that reason.
4. **A diagram.** A Mermaid flow of the transactions and accounts, rendered into the video, with the source kept in the repository for the article.
5. **Proof on screen.** Animated replays of the saved terminal output, labelled as replays, and real block-explorer screenshots of the finalised transactions. Never present a replay as live footage. Real addresses and amounts in an illustration come from the run; anything made up is labelled as an example or drawn without figures.
6. **Say why a tool was chosen** when the deed made a choice a learner would wonder about, and when the alternative would be the better pick.
7. **Honest labels.** The published video is the owner's voice, so nothing in it says the narration is synthetic: not the script, not a card, not a caption, not the description. A draft is never published, and a cut with any scene still in the reference voice is not publishable. Test wallets and fixtures are named as such.
8. **Write the narration to be spoken by a person.** Run it through the writing skills (step 7) before synthesising the reference. Read it aloud once: glossary sentences and stiff phrasing are the usual faults.
9. **Draft review.** Open each draft cut locally for the owner. Number the cuts and never overwrite one. He approves the picture and the words.
10. **The owner's voice.** Follow [video/VOICE.md](video/VOICE.md): render the clean picture, load it into the voice booth, hand over, and check the cut he assembles. He records; you never start the microphone. His approval of that assembled file, by its SHA-256, is the one that allows upload.

## 7. Article and social posts

Order: video approved and uploaded, then the article live, then the social posts, each on the owner's explicit instruction.

1. Draft from the journal, the evidence pages and the receipts. Every number, date and named claim must trace to one of them; mark anything unsourced instead of smoothing it over.
2. Use the owner's writing-style skill first, then the humaniser skill, then check that the second pass did not strip the voice. If either skill is missing, say so rather than imitating it.
3. Carry the analogy from the video into the article. Explain the concept before the mechanics. Keep the series name and number in the title, and link the previous deed.
4. Social posts open on a hook a reader can picture, not a summary. Keep the series hashtag the owner uses. Follow the continuity of the earlier posts in the series.
5. Put review copies where the owner reads drafts and open them there. Revise in place.
6. Publish the article through the site repository's own pull-request flow and wait for its checks. Build it locally first; the site has its own link and claim checks (see [TRAPS.md](TRAPS.md)). Read the live page back and confirm every link before posting anything that points to it.
7. Post from the owner's signed-in accounts only when told to. If the scheduling tool he names is signed into a different account or lacks his channels, stop and ask rather than posting somewhere else. Link both the article and the video. Read each post back after it is sent, check there is exactly one, and record the permalinks.
8. Upload the video the owner narrated and approved, unlisted unless told otherwise, with published captions, then confirm it plays signed out. [video/README.md](video/README.md) has the upload checklist and what to do when a video that is already linked has to be replaced.
9. After publishing, bring the repository's own record up to date through its pull-request flow: README and evidence page name the cut that is live, its visibility and its address.

## 8. Public source

The private repository's history holds the build journal and issue discussion. Do not change its visibility.

1. Export an allowlist of files from the merged commit into a new single-commit repository: source, tests, lock files, licence, toolchain pins and a README written for the public.
2. Scan the snapshot and its history for secrets, private paths and private repository links.
3. Build and test from the snapshot before publishing it.
4. Only then link it from the article and posts.

## 9. Retrospective

At the end of the deed, write down what should change: a step in this playbook that was wrong or missing, a trap worth recording, a correction the owner had to make twice. Propose playbook changes to the master repository and put durable lessons where the owner keeps them. Do not edit this pinned copy.
