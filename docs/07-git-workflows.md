# 07 — Git Workflow

## What practical question does this guide answer?

This note now answers a narrower question: where did the git workflow guidance move?

Git is no longer taught here as a standalone stage. The workshop now treats branch, commit, cleanup, and merge behavior as part of the main supervision flow.

## Why this matters

That change matches the real development loop better. Students often want to create a branch at the start of the session, keep work reviewable with small commits, correct mistakes while the branch is still isolated, and merge only after the review record is approved.

Keeping those habits inside the surrounding workflow documents makes it clearer that git is part of task supervision rather than a detached final ceremony.

## Where To Find It

- [00 — Session Overview](./00-session-overview.md)
  Start the session by checking git state and creating a bounded task branch.
- [05 — Delegation](./05-delegation.md)
  Keep the implementation branch reviewable and commit in small, intentional slices.
- [06 — Verification and Decision](./06-verification.md)
  Use the approved review record to decide whether to fix, commit, merge, revert, or stop.
- [08 — Refinement and Hardening](./08-refinement.md)
  Capture which git habits should become durable repo process after the branch outcome is known.

## Next

Continue to [08 — Refinement and Hardening](./08-refinement.md).
