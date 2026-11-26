# Parts every brief shares

Every `[BRACKET]` is re-derived for this deed and outcome. Delete this heading and paste the parts into the brief.

## Opening

You are the builder for outcome [ID] of [OWNER/REPO] ("The Solana Deeds #[N]", [ONE-LINE DESCRIPTION]). Work only in this worktree: [WORKTREE PATH], branch [BRANCH], base [FULL BASE SHA]. Do not edit the main clone at [MAIN CLONE PATH].

Read first: AGENTS.md, README.md, docs/SECURITY.md, docs/DECISIONS.md, docs/agent-settings/CHECKS.md, DELIVERY-PRACTICES.md and CHAT-INTAKE.md, docs/issues/[ID].md, planning/graph.json, planning/intake.json, docs/playbook/PLAYBOOK.md and TRAPS.md[, AND EARLIER HANDOFFS: PATHS]. Live issue: [ISSUE URL] (body SHA-256 [HASH]). Its scenarios are agent-written drafts unless the issue says the owner confirmed them: build to them, say in the pull request that they are unreviewed, do not mark them confirmed.

## Housekeeping

- planning/intake.json has receipt [RECEIPT ID] with owned_paths; add any further path you must touch. Run `GITHUB_TOKEN=$(gh auth token) python3 scripts/intake.py --base [FULL BASE SHA] --live` before pushing.
- Update README status, docs/agent-settings/CHECKS.md if the check changes, planning/graph.json statuses, then `python3 scripts/plan.py generate`. Sync changed issue bodies with `python3 scripts/issue_body.py set [OWNER/REPO] N FILE` and update the body_sha256 values in planning/intake.json.
- Add to docs/evidence/deed-[NN]-journal.md: what you decided, what failed and how it was corrected. No credentials, no raw chat.

## Checks before reporting

The full CHECKS.md command; the product build and tests from a fresh `git clone` of your branch in a temporary directory; a re-read of your whole diff. Report only results you observed.

## Commits and pull request

Small, focused commits whose messages explain why. Push the branch and open a DRAFT pull request against main that names the check covering the change and says the scenarios are unreviewed drafts. Wait for the hosted checks on the final commit and read the result. Push nothing after that commit: put the run links in the pull request description and in a comment on issue #[N], changed from a file and read back. A commit that only records a passing run starts a new run on a head nobody has read.

## Hard limits

Never merge; never push to main; no mainnet; no keypair, seed, API key or .env committed or printed; no changes to repository settings, secrets or visibility; no publication; no sudo; touch no other repository. Avoid writing files that trigger a permission prompt when an alternative exists: temporary files go in the system temporary directory, never in the harness's own state folder. Use only the tools you were started with; if the work needs another, say what you could not do instead of calling it. A denied permission or a check that never starts is a stop: write what happened on issue #[N] and end. [TIME BOX FROM THE ISSUE]: if it will not fit, stop and report what is left on the issue rather than widening scope or dropping a scenario.

## Finish

Write [STATE DIR]/handoff.md: pull request URL, final commit SHA, each check with its observed result and CI run URL, [OUTCOME-SPECIFIC ITEMS], open risks, and the exact next action.
