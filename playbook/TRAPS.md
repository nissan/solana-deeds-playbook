# Known traps

Facts that cost a retry on Deeds #1 to #3. Each was true when observed in November 2026; check before relying on one.

## Devnet

- The public devnet RPC faucet answered `410: The RPC faucet is closed on this cluster`. A provider's devnet airdrop returned HTTP 500 twice. The web faucet needs a person. Ask the owner to top up the shared payer.
- The public devnet RPC rate-limits sends (`429 Too Many Requests`) partway through a multi-transaction script. Use the owner's keyed RPC when it is available, or back off between sends.
- An RPC node's token index can trail a transfer that was just confirmed. Poll before asserting a balance.
- RPC error codes come back as `bigint` from `@solana/kit`. Comparing them to a number fails the comparison, not the transaction.

## Toolchain

- A template can declare a newer Node than the deed's stack decision. Pin the decided version and make it strict (`engine-strict=true`).
- Where a version manager tracks "latest" Node, the system Node can sit ahead of the pinned one on `PATH` inside package scripts, and globally installed helper tools vanish at each Node upgrade.
- `avm install` switches the machine's default Anchor version. Switch it back afterwards and tell the owner.
- A user-level cargo `target-dir` sends build output outside the repository. Override it in the repository's `.cargo/config.toml`.
- Anchor creates `init_if_needed` accounts before it runs `has_one` and seeds checks, so a caller can see a later check's error. The transaction still reverts.
- Templates ship their own agent skill folders and advisories. Remove the former; run the package audit and patch the latter.

## Process

- A CI workflow that hard-codes a pinned commit keeps passing or failing on the old pin after the contract moves. Read the pin from the contract file.
- A builder writing a file the harness treats as sensitive (`.npmrc`, `.env`) stops on a permission prompt and looks busy from outside.
- A cleanup command that matches processes by pattern can match its own shell.
- A browser tab with a password manager's autofill menu open cannot be driven. Ask the owner to close the menu or do the step.
- Test libraries that simulate a browser may lack functions a UI library calls (`Element.getAnimations`). Stub only when a component needs it.

## Video

- A screen recorder emits no frames once the page stops changing. Hold the last frame as a still.
- Burned-in captions sized for a slide cover a user interface. Keep them to two short lines at a small size, and ship a sidecar file too.
- A synthetic voice can sound stiff even when the script reads well. Listen for pauses, emphasis and the pronunciation of numbers and product names.
