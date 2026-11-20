# Brief: the core outcome (`-002`)

Paste the shared parts from [_common.md](_common.md) around this goal.

## Goal ([ID] only)

[THE USER OUTCOME FROM THE ISSUE, IN ONE SENTENCE.]

- [EACH IN-SCOPE BEHAVIOUR FROM THE ISSUE, ONE BULLET EACH, STATED AS WHAT THE USER OR CALLER OBSERVES.]
- Out of scope: [THE ISSUE'S NON-GOALS, PLUS ANYTHING THAT BELONGS TO THE STRETCH OUTCOME].
- Tests for every scenario, written before or alongside the code. A test of a rejection asserts the named error AND that state did not change.
- Security, from docs/SECURITY.md: [FOR A PROGRAM: every instruction checks signer, account owner, PDA seeds and arithmetic overflow, and each check has a failing test. FOR AN APP: keys stay server-side, inputs are validated before a wallet is asked to sign.]
- Prove the important guards by mutation: remove the guard, see the matching test fail, restore it.
- Keep a scenario-to-test table in docs/evidence/[ID].md with commands and observed results.
- [GENERATED CLIENTS OR ARTEFACTS TO REGENERATE, WITH A CLEAN-TREE CHECK IN CI.]
- No devnet deployment or transactions unless the issue puts them in scope.

Add to the checks: a security self-review of the change against the list above.

Handoff adds: scenario-to-test mapping; security checks applied; every limitation you found, including ones you chose not to fix, so the owner can decide before merge.
