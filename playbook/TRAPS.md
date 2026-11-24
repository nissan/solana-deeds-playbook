# Known traps

Facts that cost a retry on Deeds #1 to #5. Each was true when observed in November 2026; check before relying on one.

## Devnet

- The public devnet RPC faucet answered `410: The RPC faucet is closed on this cluster`. A provider's devnet airdrop returned HTTP 500 twice. The web faucet needs a person. Ask the owner to top up the shared payer.
- The public devnet RPC rate-limits sends (`429 Too Many Requests`) partway through a multi-transaction script. Use the owner's keyed RPC when it is available, or back off between sends.
- An RPC node's token index can trail a transfer that was just confirmed. Poll before asserting a balance.
- RPC error codes come back as `bigint` from `@solana/kit`. Comparing them to a number fails the comparison, not the transaction.
- A wallet may embed an older payment library that refuses a recipient whose main account does not exist, even for a token payment. An address that has never held SOL has none. Fund the recipient before a phone test.
- A wallet may add Compute Budget instructions to a transaction it was served, before or after the transfer. A validator of "the last instruction is the transfer" then rejects a payment that arrived. The fee on the explorer includes the priority fee those instructions set.
- A library's transfer validation may accept any amount at or above the expected one. Do not report it as an exact-amount check; read the balances for the exact amount.

## Toolchain

- A template can declare a newer Node than the deed's stack decision. Pin the decided version and make it strict (`engine-strict=true`).
- Where a version manager tracks "latest" Node, the system Node can sit ahead of the pinned one on `PATH` inside package scripts, and globally installed helper tools vanish at each Node upgrade.
- `avm install` switches the machine's default Anchor version. Switch it back afterwards and tell the owner.
- A user-level cargo `target-dir` sends build output outside the repository. Override it in the repository's `.cargo/config.toml`.
- Anchor creates `init_if_needed` accounts before it runs `has_one` and seeds checks, so a caller can see a later check's error. The transaction still reverts.
- Templates ship their own agent skill folders and advisories. Remove the former; run the package audit and patch the latter.
- A framework's development server can write its own agent-instructions file into the project on first start. Switch that off in its config, and check the tree after the first run.
- A package's newest version on the registry may be months behind its source repository, with the release workflow started by hand. Read the default branch and the open issues before porting anything.
- A framework's development server can block its page scripts for any origin but localhost. A page opened from a phone or another machine then never polls. Use a production build for other devices.
- A secret scan of the working tree flags a framework's build output, which holds generated keys. Scan the history and the tracked tree, and say which files a finding was in.

## Process

- A CI workflow that hard-codes a pinned commit keeps passing or failing on the old pin after the contract moves. Read the pin from the contract file.
- A builder writing a file the harness treats as sensitive (`.npmrc`, `.env`) stops on a permission prompt and looks busy from outside.
- A cleanup command that matches processes by pattern can match its own shell.
- A browser tab with a password manager's autofill menu open cannot be driven. Ask the owner to close the menu or do the step.
- Test libraries that simulate a browser may lack functions a UI library calls (`Element.getAnimations`). Stub only when a component needs it.
- A secret scanner's generic rule can flag a public address because the field name contains "Key". An exception scoped by file path can let real findings in those files through: scope it to the exact line shape, and test it by planting something the scanner catches without the exception.
- A process started for a check can outlive it and hold its port. Stop it by port, not by a name pattern.
- A password manager's approval prompt can time out or be dismissed. Each restart of a process that needs a secret is another prompt: start it once and leave it running.
- A form shown to the owner can return its pre-selected answers when it times out. Give no default to a question of fact, a declaration, a merge or a publication, and treat all-defaults with empty notes as unanswered.
- A feature can pass every test and every devnet run and still fail on the first RPC error, because no run met one. Inject the failure.
- A delegation tool can assign a subagent to a different model provider than the directing session, and say nothing. A repository whose checks file names one provider as the builder is then built by another. Ask every delegate for its model and provider before it edits anything.

## Video

- A screen recorder emits no frames once the page stops changing. Hold the last frame as a still.
- Burned-in captions sized for a slide cover a user interface. Keep them to two short lines at a small size, and ship a sidecar file too.
- A synthetic voice can sound stiff even when the script reads well. Listen for pauses, emphasis and the pronunciation of numbers and product names.
- A line that discloses a synthetic voice turns false the moment the owner narrates. It hides in four places: the script, a title or end card, the captions and the upload description. Remove all four together.
- When scenes are encoded separately and joined, a card that follows an animation can come out with grey blacks and dim whites: the animation was marked full range, the card was unmarked, and the joiner read the card as full range too. Mark every scene as limited range. `render.py` does; compare a corner pixel of each card if you change it.
- Asking the final join for a frame rate repeats the opening frame, so every cut lands one frame late. Let the frames pass through. Without each scene's length named in the join list, the cuts also drift by a few milliseconds per scene.
- `ffprobe`'s plain-text output can carry a trailing comma for some containers. Read frame counts from its JSON output.
- A recording made in the browser carries a second or more of silence after the last word. The voice booth cuts it; a hand-built cut would hold the picture too long.
- Caption times inside a re-voiced scene are spread over the speech, not matched to the words, and the caption text is still the script. If the owner changed the words, the caption has to be changed by hand.
- A preview that crops a video is not evidence the video is cropped. Check the file's own frame before re-rendering.
- A player that finds a caption file beside a video with the same name loads it, so a video with burned-in captions shows them twice. The file is fine; open it with sidecar loading off.
- A summary line drawn near the bottom of an animated scene sits directly above the captions and reads as a second caption.
- A block explorer page shows its summary before its token and log sections have loaded. Wait for the section you need, not for the page.
- The top of an explorer's transaction page does not show token amounts. Scroll to the token section, or the picture will not match a narration that names an amount.
- The animation script used to hang, not fail, when a clip already existed. It now skips the scene and says so; give a changed scene a new take number.
- The synthesiser refuses to write over existing takes. To add one scene, synthesise it in its own folder and add its entry and audio to the cut's narration receipt.
- A narration that says "this one" over a still gives the viewer nothing to follow. Move the picture when the words point.
- Two sentences that open with the same four words used to get the same start time in an animated scene.
- A long job in the background that prints nothing can be hung. Give it a timeout and check it.

## Publishing

- A video platform does not let an upload's file be replaced. A re-recorded video gets a new address, and every link to the old one has to be found and changed.
- Uploading a caption file can leave it as an unpublished draft while the page says "uploaded". Publish it, then confirm from a signed-out page that a manual track is listed beside the automatic one.
- Deleting an old upload leaves a dead link in every post that cannot be edited. Say which posts before deleting.
- One social network lets a post be edited and rewrites links into its own short form; resolve the short link to confirm where it goes. Another offers no edit after a short window; add a reply instead.
- The owner's blog shows a Mermaid block as code. Render the diagram to an image and embed that.
- The blog's link check rejects its own address written with `www.`. Use the bare host.
- A scheduling tool can be signed into a different brand's account. Check which channels it has before queueing anything, and ask if they are not the owner's.
- In a browser tab that is not in front, a click on a "Post" or menu button may do nothing. Focus the button and press Enter, then confirm on the page that it happened exactly once.
- Deleting a repository, and some account pages, ask the owner for a passkey or a wider token. That step is his.
- A post composer can scramble text inserted in one go, and can close on Escape and save what was typed as a draft. Type with keystrokes, avoid Escape, and look in drafts after any failed attempt.
- A block explorer can answer an automated link check with "too many requests" while the page loads in a browser. Report the link as unconfirmed; do not report it as checked.
- A network's mention picker can offer several organisations with the same name. If none can be confirmed, post without the mention.
- Escape closes more than a post composer: a video upload dialog closed on it too, keeping the upload as a private draft. Do not send Escape to any page with unsaved work.
- An identifier read from a screenshot can be wrong by a capital I or a lowercase l. Read addresses and IDs from the page's own text.
- A profile may not show a new post for some seconds. Check the composer and the drafts before deciding a post failed.
- One network turns "#551" in a post into a hashtag. Write "issue 551" where that matters. Another does the same to "Deed #6": write "Deed 6" there.
- A post's own page may not render in a browser tab that is not in front, or signed out. Say when a permalink was built from an ID and not read.
- A project's brand account may be run by another company, or be silent. The people who can act on a bug report are in the repository's commit history.
- A statement about someone else's issue or release can go stale between the draft and the merge. Read it again immediately before publishing.
- A typing helper can time out part-way through a long field and keep what it typed. Read the field, type the remainder, then compare the whole with the draft.
- A mention picker may not open when the `@` follows a bracket; it needs a space before it. Selecting a mention may also leave no space after it.
- An organisation's site can link its company page under another address shape ("showcase") that redirects. Search for the host, not the path.
- A web app can ignore an address typed with a chat's ID until the chat is clicked in its list. Confirm the header names the right chat and topic before typing.
- An upload form asks more than whether content is synthetic. A paid-promotion question may have no answer selected, and the answer is the owner's.
- A chat app in the browser sends on Enter. A message with a line break needs Shift+Enter, and a check after it that nothing was sent early.
- A survey frame can appear over an upload dialog's "Next" button part-way through. Dismiss it through its own button; do not click through it.
- A post composer may be a plain text area where a rich-text box was expected, and a selector written for one finds nothing in the other. Find the input by what it is, and read back what it holds by the means that input uses.

## Evaluating someone else's tool

- A host remembered from an earlier project can still answer and no longer be the vendor's. Call only addresses the vendor's current documentation names.
- A lending market can hold more than one reserve with the same ticker, and the first listed may be nearly empty and pay nothing. Look up by mint and check the size before using a rate.
- A public statistics endpoint can answer 200 with zeros while the service's "since inception" figure looks right. Compare two figures for the same thing before trusting either.
- An SDK's README can be behind its published code. When a call fails on a missing field, read the package's type declarations, not the README.
- A vendor's documentation site can be unpublished on the day it is needed. Confirm in a browser, record it, and recommend "not now" instead of guessing the API.
- A hosted service that delivers to the live network cannot be tried by an agent that may not send there. That is a finding to report, and every use of the service is the owner's step.
