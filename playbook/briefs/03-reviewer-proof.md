# Brief: reviewer proof (`-003`)

Paste the shared parts from [_common.md](_common.md) around this goal.

## Goal ([ID] only)

A hiring manager or grant reviewer can confirm what was built and that it works from the README alone, in ten minutes.

1. Reproduction on [LOCAL RUNTIME], then devnet. Devnet rules are in docs/playbook/PLAYBOOK.md step 4. Payer: the keypair file named by `DEVNET_PAYER_KEYPAIR` ([PATH], about [BALANCE] SOL). Spend cap agreed with the owner: [CAP] SOL; report the balance before and after; stop if the cap would be exceeded.
   [IF A PROGRAM IS DEPLOYED: throwaway program keypair generated outside the repository, declared id synced, upgrade authority stays on a throwaway or the payer key, `--max-len` close to the binary size, recover the buffer if a deploy fails midway.]
2. A reproduction script with a package-script name that runs the core scenarios on devnet with throwaway fixtures, reads results back from the chain, shows one rejection as a signed simulation with its named error and unchanged state, prints an explorer link for every sent transaction and waits for finalized. Tidy, stable console output. Save one real run's output to docs/evidence/ with no secrets; the demo video replays it.
3. README for the reviewer: what was built; stack and pinned versions; quickstart (local first, then devnet); a short architecture note with a Mermaid diagram; deployed ids with explorer links; a claim-to-evidence table where every claim links to a commit, CI run, transaction signature or file; security checks applied; known limitations stated plainly. Plain language, no marketing. Do not claim features from outcomes that are not built.
4. A `secret-scan` CI job: a secret scanner pinned by SHA-256 over the full history and tree, plus an env and keypair filename check.
5. docs/evidence/[ID].md: commands, observed results, ids, every signature, payer balance before and after, and what was NOT proven.

NOT yours: the demo recording. The directing session produces it afterwards from your saved output and signatures. Do not create video files.

Add to the checks: the secret scanner locally if available; each devnet signature confirmed finalized with no error by RPC.

Handoff adds: deployed ids; every signature and what it shows; payer balance before and after; path of the saved script output.
