# Brief: toolchain and scaffold (`-001`)

Paste the shared parts from [_common.md](_common.md) around this goal.

## Goal ([ID] only)

A pinned toolchain and an empty scaffold that builds and runs one trivial test from a clean clone, locally and in CI.

- Pin exact versions of everything in the issue's stack line: [STACK FROM THE ISSUE]. Use the repository's version-manager file and commit the lock files. Verify downloaded toolchain binaries by SHA-256 in CI.
- Scaffold with [TEMPLATE OR GENERATOR FROM THE ISSUE]. Remove agent skill folders the template ships. Run the package audit and patch advisories.
- Where the template's declared runtime differs from the stack decision, pin the decided version and make it strict.
- ONE trivial test that exercises the real toolchain end to end (for a program: load the built program and run an instruction). No product behaviour; that belongs to the core outcome.
- Tests must pass with no network beyond the machine. If the test runtime can fork a live cluster, start it offline; any account a test needs from a live cluster is saved in the repository as a fixture with the slot and date it was captured, refreshed by a script run by hand, never in CI. A fork that fetches from a free public endpoint passes until a later outcome adds reads, then fails on a different test each run.
- [OWNER DECISIONS ALREADY MADE, FOR EXAMPLE THE TEST RUNTIME OR UI LIBRARY]. Do not add alternatives.
- Add a CI job that builds and runs the test: actions pinned by commit SHA, read-only permissions, `persist-credentials: false`. Keep the existing jobs.
- README: status, quickstart, pinned versions table.

Handoff adds: pinned versions; anything you installed or changed on the machine outside the repository.
