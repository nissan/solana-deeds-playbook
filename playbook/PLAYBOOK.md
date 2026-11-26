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

**Deed numbers.** The twenty challenges are numbered in the order they are done, as the owner set on 23 November 2026: B1 to B5 are Deeds #1 to #5, M1 to M8 are #6 to #13, and A1 to A7 are #14 to #20. Each repository carries its own number: the `deed` field at the top of `planning/graph.json`, and the opening lines of `AGENTS.md` and `README.md`. Use that number in the journal's file name, the video and article titles and the posts. If the three places disagree, stop and ask.

## 1. When the owner says "begin"

1. Read `AGENTS.md`, `README.md`, `docs/SECURITY.md`, `docs/DECISIONS.md`, `docs/ROUTING.md`, `docs/agent-settings/CHECKS.md`, `planning/graph.json` and the first open outcome issue.
2. Check the starting state: default branch clean, no open pull requests, the last hosted run on `main` green. If the outcome's acceptance is already met on `main`, say so with the evidence and move to the next outcome.
3. Check this copy is current. `docs/playbook/import.json` names the master commit it was copied from; compare it with `gh api repos/nissan/solana-deeds-playbook/commits/main -q .sha`. If the copy is behind, tell the owner before building and ask whether to refresh first. A refresh is `python3 scripts/install.py apply` run from a clean clone of the master, taken through this repository's own pull-request flow; never edit the copy by hand. A deed already under way keeps the copy it started with unless the owner says otherwise.
4. Record intake before any edit: append a receipt to `planning/intake.json` mapping each ask to an issue, with the SHA-256 of the issue body as read back from the forge, then run `python3 scripts/intake.py --base FULL_BASE_SHA --live`. The live check needs a token: `GITHUB_TOKEN=$(gh auth token)`. Without it a private repository answers 404.
5. Work in one worktree per outcome, on a branch named for the outcome (`b4-001-toolchain`). Keep the main clone on `main`. The owner keeps deed clones together in one projects folder; ask where if it is not obvious, and do not invent a second location.
6. Start the build journal (step 5) with the kickoff entry.
7. Say which builder will do the work. `docs/agent-settings/CHECKS.md` names who builds and who reviews. If the named builder cannot be started, stop and say so; never switch provider silently.

## 2. Giving an outcome to a builder

A long outcome goes to a separate builder session with a written brief, so the directing session stays free and the work survives a restart. The owner may instead have the directing session build an outcome itself. That is his choice: ask, and do not assume either way. Deed #4 was built in the directing session.

1. Check capacity first, by the rule in the owner's fleet policy. Unknown capacity is a stop, not a free slot.

   **Check who the builder will be before the brief goes out.** `docs/agent-settings/CHECKS.md` names the kind of session that builds. A delegation tool can hand the work to another provider without saying so. Ask the delegate to state its model and provider first; if it is not the named builder, do not delegate that repository. A delegate that finds itself in the wrong repository stops and reports. Added after three planning pull requests in M7 were written by a session the repository does not name as its builder.
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

**A follow-up for the same builder.** When the owner's decision changes the work after a handoff, send it to the session that did the work, so it keeps what it read: `claude --bg --resume <session-id> ... -- "$(cat followup.md)"`, with the session id from `claude agents --json`. Write the follow-up as a file beside the brief. It starts with the owner's decision in his words, tells the builder to record that decision in the intake file before any other edit, and ends by asking for the handoff to be rewritten. Keep a copy of the old handoff so a rewritten one can be told from an unchanged one.

**A tool outside the allowed list.** A builder may reach for a tool it was not started with, a browser-automation tool for screenshots for example, and stop on a prompt for each call. Read the whole request, approve a single use only if the brief already covers what it does, and never choose "don't ask again". In the next brief either allow the tool on purpose or tell the builder not to use it and to say what it could not do. Tell every builder where temporary files go: the system temporary directory, never the harness's own state folder, which the harness treats as sensitive. Added after Deed #1's follow-up outcomes, where builders stopped five times on permission prompts: once for a log saved in the harness's folder and four times for a browser tool.

**When a dependency lags.** If a published package is too old for the rest of the stack, read its source repository's default branch, its release workflow and its open issues before deciding the package is the problem; the work may be done and unreleased. If an unpublished build is the answer, show that it can be rebuilt byte for byte from a named upstream commit, commit the build with a script that does that, and have CI run the script. Put the choice to the owner with that evidence, not before it.

**Pins taken from an earlier deed.** A set of versions that an earlier deed proved together is a starting point, not the answer. Before adopting it, read what devnet and mainnet run (`getVersion`) and the newest stable release of each tool, and try the newest set in a scratch copy outside the repository. In Deed #8 the first pins ran the tests on a runtime a major version behind devnet; the owner asked, and the newest set built and passed first time.

**When someone else's tool is proposed for a deed.** Whether a protocol, SDK or hosted service belongs in a deed is settled by an evaluation, not an opinion. Use the `third-party-evaluation` skill (source: `nissan/Work`, `skills/third-party-evaluation/`): read the outcome first; send documentation research to a delegate that runs nothing; keep the probe with the session that holds the keys, in a throwaway folder outside every repository, going from install beside the deed's pins to a devnet run only as far as the deed's rules allow; write one page that leads with the recommendation and says what was run, what was read and what was not tried; and add a proposal the owner decides. Change no outcome before he does. Eight evaluation pages were written this way in the week of Deed #5: two led to stretch outcomes, one changed a toolchain, one confirmed a pin, and four were declined or deferred.

## 3. Review and merge

1. Tell the owner what was built, what was checked, and every open risk the builder listed. Recommend which risks to fix before merge and which to list as limitations. Beside each limitation, write what would remove it and roughly what that costs; if the cost is small, remove it now. In Deed #4 a limit recorded as accepted ("only the 20 newest transactions are searched") was the first thing a reader of the public source asked about, a day later.
2. The owner decides. A fix requested at review gets a test that fails before the fix and passes after.

   **Before asking for the merge**, added after Deed #5's second outcome merged with a fault in it:
   - For code that reads the chain because something told it to (a webhook, a poll, a retry), test what it does when that read fails. If the script that proves a feature needed a retry to get through rate limits, ask the same question of the server.
   - Run the deed's one-command reproduction from a fresh clone of the merge candidate. The run in step 8 comes after the merge, and found the fault ten minutes too late.
3. Merge only on the owner's instruction, only the exact reviewed head (`gh pr merge N --merge --match-head-commit SHA`), with a merge commit. If another pull request merges first and this one then conflicts, resolving the conflict moves its head: read the checks on the new head and ask for the owner's word again.
4. Watch the hosted run on `main` after the merge. A failure there is fixed before new work starts.
5. Bring the record up to date in the same sitting, through the repository's pull-request flow. A status line written before the merge ("in a draft pull request", "Open: owner merge") is false the moment the merge lands, and nothing flags it. In Deed #1 five outcomes still said so days later and took two extra pull requests to correct.
   - **Status line:** "Merged on main by pull request #N as SHA on DATE, with hosted CI green on main. Delivered: … Open: …". Keep every fact that is still true; verify the merge commit and the run before writing them.
   - **Readiness:** when the owner confirms the scenarios, and only then, set it to "Ready (scenarios confirmed by the owner on DATE)" and quote his words in the intake receipt. A confirmation covers the scenarios as written at a named commit. Check that the generated page stops calling them drafts; a repository whose `plan.py` renders the draft sentence unconditionally needs that fixed first.
   - **Sync the issue** from the regenerated mirror, and first compare the live text with the mirror on `main`. If they differ, the live text came from somewhere else, an unmerged branch for example: save it and find out where from before overwriting it.
   - **Close the issue** only on the owner's instruction, after the hosted run on `main` passes for the commit the closing comment cites. Read the comment in full before posting it, whoever drafted it, and check every path it names exists on `main`.

Scenarios written by an agent stay "Draft" until the owner confirms them. Building to draft scenarios is allowed; calling them accepted is not.

**When a hosted check fails on the pull request.** Read which test failed and why before proposing anything. If every failure is a timeout and the failing test changes from run to run, the tests share something slow: compare the branch's pass rate with `main`'s, counted from the run list, and look for a network read the change added to. Raising a time limit or a wait treats the symptom. In Deed #1's follow-up two rounds went to time limits while three of six runs failed on three different tests; the cause was a test network that fetched from a free public endpoint, and saving those accounts in the repository fixed it. A product setting changed to get a test environment through is a change for users: say so, and put it back when the environment is fixed another way.

**Measure on the final commit.** Decide how many hosted runs will be read and what ends the round before the first one, and bind both to the final commit. Push nothing after it: a commit that only records a passing run starts a new run on a head nobody has measured. Run links go in the pull request description and an issue comment.

**"Continue" after a merge means the next planned outcome**, added after Deed #6. Before starting the demo video, list every planned outcome that is not yet built and either build it or ask. In Deed #6 the builder went to the video with two outcomes unbuilt and the owner had to stop it.

## 4. Working on devnet

- Devnet, a local validator or a mainnet fork only. Never mainnet.
- One owner-funded devnet payer is shared across deeds. Its keypair file lives outside every repository and is named by `DEVNET_PAYER_KEYPAIR`. Read it by path; never print, copy or commit it. Check its balance before and after and report both.
- Scripts refuse to sign unless the RPC's genesis hash is devnet's.
- Agree a spend cap with the owner before a deployment. A program deployment costs rent in proportion to its size; pass a `--max-len` close to the binary size.
- Print each signature and its explorer link before sending, wait for `finalized`, and read the result back from the chain. If a send is interrupted, reconcile by signature; do not resend blindly.
- Prove a rejection with a signed simulation, not a failed transaction: assert the named error and that the accounts did not change.
- Save one real run's console output to `docs/evidence/`. The demo video replays it.
- Do not ask the faucet from code. See [TRAPS.md](TRAPS.md).
- For a test from the owner's phone: run a production server, not the development one; make sure the recipient's main account and token account exist; open the page from another device the way he will. Ask him to try an unhappy path with his own hands at least once. Deeds #4 and #5 both found their most useful faults that way.

**When a deed needs mainnet.** Some deeds only work against mainnet. The agent still never signs there and never holds a mainnet key. The owner makes the transaction from his own wallet; the agent starts the application, records the screen if he wants footage, and afterwards reads the transaction back from the chain at `finalized` and compares it with what the application showed. Keep a read-only reproduction script that does that read-back.

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

Checks added after Deed #4, where the owner caught each of these himself:

- **Words against picture.** Before a draft is shown, go through the script. For every claim the narration makes about what is on screen, look at the frame at that moment and confirm it shows the thing named.
- **Words against time.** Lay each scene's narration timing against its screen clip. If the picture reaches a point after the words do, re-time the clip.
- **Re-time to his take.** After the owner records, re-time animated scenes to his recording. The reference voice reads slower than he does, so a scene timed to it runs on after he stops.
- **Room for captions.** Leave the bottom of the frame empty in screen scenes. Draw no summary line where captions go: it reads as a second caption.
- **Screen takes.** The owner drives and the agent records. Say beforehand what a full-screen recording will show. Raw takes stay outside the repository; scenes are cropped to the page.

  **One driver, named first.** Before the recorder starts, say who drives the page (the owner by hand, or the agent through the browser relay at his request) and who starts and stops the recorder. Capture the tab, not the screen, where the host allows it. In Deed #7 a whole-screen recording ran while each side waited for the other to drive, and nothing in it was usable.
- **Covering a secret.** Cover it for its whole time on screen with a margin, then check by OCR over every frame of the clip and by eye at both edges of the cover.
- **One fault, every scene.** When one scene has a fault, look for the same fault in every scene before rendering again.

Checks added after Deed #5:

- **Numbers from the source.** Before a number goes into the script, read it from the screenshot or the chain it will be shown beside. A fee on an explorer page is the base fee plus whatever priority fee the wallet added.
- **Explain a term the first time it is said.** A unit or a name that appears on screen (lamports, priority fee) gets one plain sentence before it is used.
- **When the words point, the picture points.** "This one" and "here" need a zoom, an outline or a move at that moment. A still that contains the thing is not enough if the viewer cannot tell which thing is meant.
- **Bound every long job.** Give a render, a synthesis or a recording a timeout and look at it. A job that has printed nothing for longer than the last one took is not working.
- **Adding a scene after recording has started.** Synthesise and draw only that scene, show that every other scene's narration, clip and length is unchanged, then swap the picture into the booth with `--replace`. [video/README.md](video/README.md) has the steps.
- **Listen by transcription.** After the owner assembles, transcribe the cut locally with word times. Compare his words with the captions, place the captions on his words, and compare his timing with each timed change in the picture. [video/VOICE.md](video/VOICE.md) has the steps.
- **Captions on his words: overlap and order.** After placing captions on the owner's words, check that no two cues overlap and that they are in order, at scene edges especially. Length and line count do not show it. Use `video/place_captions.py`: it ends each scene's last cue on that scene's own last matched word and inside the scene, so a cue cannot run into the next scene. Placing captions by other means, a scene's last cue can take its end from the next scene's first word, said early inside the scene's window; in Deed #7, whose pinned copy predated the script, four cues did. Clamp each scene's last cue to end before the next scene's first cue starts, then check again. Before the video step, check that the deed's pinned copy has the scripts the video step names; refresh it first if not.
- **No pre-selected answer about what he said.** When the transcriber's word is in doubt, ask him on a form with nothing pre-selected. A form can return its defaults when it times out; an answer that is all defaults with empty notes is unanswered until he confirms it. The same goes for any declaration, merge or publication.

Checks added after Deed #6:

- **One sentence per scene.** The owner's test: can someone who hears the scene once say what its point is? Apply it to every scene before the reference is synthesised. A scene that is a list of incidents fails it; so does a line kept because the writer liked it.
- **Fixable faults before the script.** Before a scene says something is still wrong, ask the owner whether it should be fixed first. A video that ends on a fault the deed could have closed reads as unfinished, and the scene has to be rewritten after he has recorded around it.
- **An address on a card must already answer.** Any address drawn into the picture is requested signed out before the cut is handed over. The source address on a closing card is the public repository's (step 8), so settle its name before the card is drawn; a private repository's address is a dead link for every viewer. In Deed #6 both closing cards named the private repository and were caught after the owner had recorded and assembled both parts.

Checks added after Deed #7:

- **Who "you" is, when the subject is money.** A scene or sentence that tells the viewer whether to move, keep or spend money says who the viewer is (the person using the tool, not a trader or an investor) and that it is arithmetic, not financial advice. In Deed #7 the owner stopped recording at the advice scene because he could not tell what his role was in it.

Checks added after Deed #8:

- **Fixable faults: ask before the first cut is drawn.** The check above says to ask before a scene says something is still wrong. Ask when the fault is found, not with the draft. In Deed #8 the question came with cut 1; the owner chose the fix, and seven of thirteen scenes were redone.
- **A name on screen is said and explained, wherever it appears.** A name in a diagram box or a replayed terminal line counts as much as one in the narration. In Deed #8 a service's name was on screen in two scenes and the narration only described it; the owner caught it.
- **Ask how each name is said.** Before the reference voice is synthesised, list the product and project names in the script and ask the owner how he says each. The reference voice and the transcriber will both get an unusual name wrong.
- **Known small fixes come before the request for approval.** Do not ask "approve this file, or shall I change X?": a yes to both approves a file that no longer exists. Make the change, then ask for approval of the result by its hash.

## 7. Article and social posts

Order: video approved and uploaded, then the article live, then the social posts, each on the owner's explicit instruction.

**Write the whole order out.** When reporting where the release stands, list every remaining step in this order, the upload included, even when the owner has asked about only one of them. In Deed #7 a report that said "public source, then article and posts" left the upload out, and the owner had to ask for it.

1. Draft from the journal, the evidence pages and the receipts. Every number, date and named claim must trace to one of them; mark anything unsourced instead of smoothing it over.
2. Use the owner's writing-style skill first, then the humaniser skill, then check that the second pass did not strip the voice. Run each as its own pass and write down what it changed; reading a skill and writing "to" it is not using it. If a pass changed nothing, say that. Text the agent itself drafted in the target style is recorded as "written to the style", not as a pass, and a pass record lists only changes that were made. If either skill is missing, say so rather than imitating it. For every first-person sentence, check who actually did the thing: the owner, the agent, or both.
3. Carry the analogy from the video into the article. Explain the concept before the mechanics. Keep the series name and number in the title, and link the previous deed.
4. Social posts open on a hook a reader can picture, not a summary. Keep the series hashtag the owner uses. Follow the continuity of the earlier posts in the series, except where this playbook says otherwise. Before handing a draft over, apply everything already on file for it: both links, the series hashtag, and the accounts to tag. Open each profile before tagging it. If a mention picker offers look-alike accounts, tag nobody and say so. Count the post's weighted length against the network's limit before handing it over.

   **Looking for an organisation's account.** List every link on its own site that contains the network's host, on more than one page, before saying it has none: a company page can sit under an address shape a search for the usual one misses. Where a mention replaces a name in a sentence, write the sentence around the mention in the draft, since the mention shows the page's full name.

   **A disclosure goes where the claim goes.** If the owner has an interest in something a post argues for (a grant, a sponsor, a holding) and a short post has no room to say so, ask him before posting whether it goes in a reply. Do not report the gap afterwards.

   **Start the tag list yourself.** When a deed builds on, or reports a fault in, someone else's project, find who to tell without being asked. The people who can act are the maintainers: read the repository's recent commits, take the handles from their own profiles, and confirm each on the network. A brand account may be run by another company or be silent. Check a hashtag by reading its newest posts; a popular one may carry only bots. File the list in `docs/evidence/` with how each entry was checked.
5. Put review copies in the owner's Obsidian vault (`~/Documents/Obsidian Vault`), in a new folder named `Solana Deed N review.XXXXXX` (as `mktemp -d` makes it), with each file named for what it is ("Blog article.md", "X post.md", "Review notes.md"), and open the review notes in Obsidian. Revise in place there. Name the folder in the deed's release record, so the next deed copies the place and not only the media folder. In Deed #7 the drafts went to a folder under `~/Videos`, copied from Deed #6's release record, which named that folder and not the vault. The article's draft includes its picture and the picture's alt text, with the place it goes marked: a picture added after approval is unapproved.
6. Publish the article through the site repository's own pull-request flow and wait for its checks. Build it locally first; the site has its own link and claim checks (see [TRAPS.md](TRAPS.md)). In the minute before the merge, read again every statement the article makes about the outside world: an issue's status, a release, a count. Read the live page back and confirm every link before posting anything that points to it. Read it with a request that follows redirects: the site sends its bare host to `www.`, and a request that does not follow sees a redirect, not the page.
7. Post from the owner's signed-in accounts only when told to. If the scheduling tool he names is signed into a different account or lacks his channels, stop and ask rather than posting somewhere else. Link both the article and the video. Type one character and confirm it landed, then type the rest with keystrokes, compare what the composer holds with the draft, and only then post. After any failed attempt, check what was posted and what was saved as a draft before trying again. Read each post back after it is sent, check there is exactly one, and record the permalinks. A profile may not show a new post for some seconds; look at the composer and the drafts before concluding it failed.

   **Everything under his name is shown to him first.** That includes a video's title and description, a comment on someone else's issue and the community message, not only the article and the posts. Put them in the review folder with the other drafts.
8. Upload the video the owner narrated and approved, unlisted unless told otherwise, with published captions, then confirm it plays signed out. The platform's declarations are his to make: see the upload checklist. [video/README.md](video/README.md) has the upload checklist and what to do when a video that is already linked has to be replaced.
9. Share the release where the owner's community gathers. Each earlier deed went to a chat group as one short message: a two-sentence hook and the link to the social post. Find the previous deed's message there, match its shape, send one, and read it back. This step was missed for Deed #3 and had to be asked for; it belongs in the same instruction as the social posts.
10. After publishing, bring the repository's own record up to date through its pull-request flow: README and evidence page name the cut that is live, its visibility and its address.
11. **A second release for the same deed.** Its posts are new pieces, not edits of the first release's, and they link the same public source. When it makes a statement in an earlier article untrue ("this isn't built"), add a dated forward link to that article in the same step, and leave the original sentence as written.
12. **A deed released in two parts from the start.** When the owner asks for two short videos and one article: each video has its own length limit and its own title and description, and each description links the other part. The article links both. Upload both unlisted, publish the article with the first part, and make the second part public at its own release with its own new posts. Tell the owner that the article's link lets a reader watch the second part before its release.
13. **A fix upstream can be its own post.** When a fault the deed reported is fixed by the project's maintainers, tell the owner and offer a one-off post about it, separate from the release posts. Keep it to what the record shows: when it was reported, when the fix merged, and whether the fix names the cause the report gave.

## 8. Public source

The private repository's history holds the build journal and issue discussion. Do not change its visibility.

1. Export an allowlist of files from the merged commit into a new single-commit repository: source, tests, lock files, licence, toolchain pins and a README written for the public.
2. Scan the snapshot and its history for secrets, private paths and private repository links, and for the owner's own identifiers: a wallet address used as a test fixture is not a secret, but it is his. Put any such finding to him before publishing.
3. Fix a finding in the private repository through its pull-request flow, then rebuild the snapshot from the merged commit, so the public source stays byte-identical to a commit that passed the hosted checks. Compare blob ids to prove it.
4. Build and test from a fresh clone of the snapshot before publishing it, and run the deed's reproduction from that clone.
5. Show the owner the README written for the public before publishing: it goes out under his name, like a video description. Then publish, and confirm from an anonymous clone that it holds the one commit and that the private repository is still private.
6. Only then link it from the article and posts, and remove any sentence that says the source is private.
7. **A later fix goes on top as one commit** (the owner's decision, 26 November 2026). When a merged fix has to reach a snapshot that is already public, add one commit that carries exactly the files the fix changed, taken from the new merged commit, and update the README's snapshot line. Do not rebuild and replace the history: links to the repository keep working and a reader can see what changed. Steps 2 to 5 apply again: scan the tree and the history, prove every source file identical to the merged commit, test from a fresh clone, and show the owner the README's changed lines before the push. In Deed #4 the README changes went out before he saw them.

## 9. Retrospective

At the end of the deed, write down what should change: a step in this playbook that was wrong or missing, a trap worth recording, a correction the owner had to make twice. Propose playbook changes to the master repository and put durable lessons where the owner keeps them. Do not edit this pinned copy.

**Close the records first.** The session that made the release does this before the retrospective, while it still knows what happened. A release is not finished until all of these are true on the default branch, and the retrospective says each was checked:

1. Every outcome's status in `planning/graph.json` says what was merged, by which pull request and merge commit, and what was left unshown. None still reads "Queued" or "not started" for work that is merged.
2. Every readiness line says whether the owner confirmed the scenarios, with the date. If he has not, ask; do not leave "Draft" on a published deed without saying so.
3. A release record names the published file by its SHA-256, the owner's approval of that file in his words, and each public address with the date it went out: video, article, posts, public source.
4. No evidence page still says "nothing has been made public" without the date that was true.
5. Each delivered outcome's issue is synced from its page and closed with the pull request, merge commit and status. An outcome that was not built stays open and says so.

Read each outcome's whole status before closing its issue; a list cut short hides the one that was never built. A repair made later by another session can only record what it can read that day.

Added on 26 November 2026. Deed #2 had been public for six days while its plan said the work was not started, all four issues were open, and no record existed of the narrated cut, its hash or the owner's approval. Deed #3's stretch outcome was nearly closed as delivered from a shortened listing; it had never been built.

## 10. After the release: replies and fixes

Publishing is not the end. Someone may reply with a fault, and they may be right.

1. In the days after a release, read the replies and mentions on each post as a whole before answering any, so related follow-ups are found together. Open each thread and read beneath the account's own last reply: in Deed #4 the notification list showed neither of two follow-ups. Work that another session or the owner has already answered is reported, not picked up; look for an existing answer from the account under the question before typing one.
2. Check an outside report against the code and the interface it relies on before drafting a reply, and say in the reply what was confirmed. Check any remedy it proposes the same way, and say plainly when the interface does not offer it. If the owner remembers the design differently from the report, read the code before agreeing with either, then check what the video and the article say.
3. A reply goes out under the owner's name: show him the text first, each time. "Post it" for a reply he has not seen is a request for the draft. Count the length with a tool when you quote it.
4. Build the fix as its own outcome: intake receipt, issue, scenarios, a test that fails on the old code, a builder the repository allows, a pull request, the owner's merge. Record which new tests fail before the fix and which pass on both sides.
5. Say "fixed" in public only after the hosted run on `main` passes for the merge commit. When the reader can only see the public source, refresh it first (item 6), so the reply is true where they can look. Then post one follow-up reply, read it back, and record its address. Prefer that single reply to a promise followed by a confirmation: show the owner its wording alongside the pull request.
6. Bring the public copies into line: refresh the public source from the merged commit (step 8, proving it identical again), and update the article by step 7, item 11: a dated section or forward link, with the original sentence left as written.
7. If a suggestion would change what a user sees, state the rule you intend to build back to the owner before building it, label it as your reading in the issue, and name the case it does not cover.

Added after Deed #1, where one reader's replies led to five follow-up outcomes in two days.
