# 04 — Implementation

## What practical question does this guide answer?

This guide answers the build question: how should the approved implementation plan be carried out without losing control of scope, tests, or stage boundaries?

Implementation starts only after the spec is approved, the behavioural tests exist, the implementation plan is reviewed, and that approved planning state has been checkpointed in git. Feature code is not the first artifact in the loop.

## Why this matters

The workshop is teaching controlled implementation, not free-form code generation. The approved spec tells you what problem to solve. The behavioural tests make the expected behaviour executable. The implementation plan defines the intended path. Implementation should follow those contracts rather than replace them.

This phase is also where the repo starts changing most quickly, so the stop-and-escalate rules matter. If the implementation uncovers a wider change, a wrong stage boundary, or a scientific meaning change, revise the spec or plan before continuing.

## Steps

### Step 1 — Kick off implementation from the approved plan

Use the approved `agents/docs/<task-slug>-02-implementation-plan.md` as the handoff contract for implementation.

The implementation kickoff should require the agent to:

- restate the approved task
- inspect the planned file surfaces
- implement only the approved scope
- satisfy the existing behavioural tests
- add any planned unit or integration tests needed beyond the behavioural contract
- stop if the work exceeds the approved boundaries

If you do not yet have a checkpoint commit for the approved spec, behavioural tests, and implementation plan, **make the commit first and only then begin feature implementation**.

### Step 2 — Keep implementation aligned to the approved artifacts

During implementation, compare the work back to:

- `agents/docs/<task-slug>-01-task-spec.md`
- the behavioural tests in `tests/`
- `agents/docs/<task-slug>-02-implementation-plan.md`
- `AGENTS.md`

If the implementation drifts beyond those artifacts, stop and revise the spec or plan before continuing.

### Step 3 — Keep the branch reviewable

Do not wait until the end of the session to inspect git state.

```bash
git status --short
git diff --stat
git diff
```

Prefer small, reviewable commits over one large end-of-session dump. If the agent goes down the wrong path, fix or discard that work while it is still isolated on the branch.

### Step 4 — Run the planned checks during implementation

Run the behavioural tests first, then run any new unit or integration tests added by the implementation, and only then widen out to broader verification.

The important thing is to preserve the logic of the loop:

- behavioural contract first
- supporting tests next
- broader validation after the implementation slice is coherent

### Step 5 — Restore or clean bad implementation work deliberately

If an implementation slice is not good enough to keep, use the checkpoint and restore only the affected work instead of improvising a larger cleanup.

For tracked files, restore the files you want to discard:

```bash
git status --short
git restore --worktree --staged <tracked-files-to-discard>
```

If you need to restore those files back to the checkpoint commit explicitly, use the checkpoint commit ID you recorded before feature work began:

```bash
git restore --source=<checkpoint-commit> --worktree --staged <tracked-files-to-discard>
```

For untracked files created by a bad implementation slice, remove only the specific paths you intend to discard:

```bash
git clean -fd -- <untracked-paths-to-remove>
```

Do not use broad cleanup commands casually. Inspect `git status --short` first, keep the cleanup scoped to the files created by the failed slice, and preserve the approved spec, behavioural tests, and implementation plan.

When the implementation slice is coherent and ready for review, prefer to start a fresh chat for the review phase. Give that chat the approved artifacts, the current diff, the test outputs, and the generated outputs instead of the full implementation conversation.

## Outputs

- The approved implementation plan has been turned into actual repo changes.
- Behavioural tests are being satisfied by implementation rather than rewritten to fit the code.
- Any added unit or integration tests remain aligned to the approved scope.
- The branch stays reviewable throughout implementation.
- Bad implementation slices can be discarded cleanly without losing the approved planning artifacts.

## Discussion

1. What would tell you that implementation has started solving a different problem from the approved spec?
2. When should you revise the plan instead of continuing to code?
3. What is the difference between satisfying the behavioural contract and merely getting tests to pass?
4. Which missing context should be fetched during implementation, and which missing context is really a sign that the plan was weak?
5. Why is git inspection during implementation safer than one large end-of-session review?
6. Which implementation discoveries are legitimate local decisions, and which ones require renewed approval?

## Next

Continue to [05 — Review and Commit](./05-review-and-commit.md).
