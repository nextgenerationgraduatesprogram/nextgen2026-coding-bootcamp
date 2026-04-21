# 06 — Verification and Decision

## What practical question does this guide answer?

This guide answers the post-implementation question: how should the human turn tests, diffs, artifact inspection, and current git state into an explicit decision?

In the new workflow, the human asks the agent to draft that reasoning into `@03-review-and-decision.md`, then reviews the recommendation before deciding whether to fix, commit, merge, revert, or stop.

## Why this matters

Passing tests alone is not enough. The human still has to judge whether the change respected the approved scope, used the right stage boundary, and represented the artifact honestly.

This is a useful teaching moment because it shows students that “have the agent summarize the evidence” is not the same thing as “let the agent decide unilaterally.” The review draft is assistance for judgment, not a replacement for it.

## Steps

### Step 1 — Gather the evidence

```bash
uv run pytest -q tests/test_analyze_report.py tests/test_workflow_smoke.py
uv run pytest -q
uv run python scripts/run_workflow.py --profile base --run-name s3-review-check
LATEST_RUN=$(ls -1dt runs/*s3-review-check* | head -n1)
git status --short --branch
git diff --stat
git diff
find "$LATEST_RUN" -maxdepth 2 -type f | sort
```

The important thing here is to gather both mechanical and human-readable evidence. For the running example, that means you want the tests, the branch state, the diff, the generated CSV, and the report markdown.

### Step 2 — Ask the agent to draft the review and decision record

```text
Using `agents/docs/<task-slug>-01-task-spec.md`, the current git status, the current diff, the test outputs, and the generated artifacts, fill the format specified in `@03-review-and-decision.md`.
Place the result in `agents/docs/<task-slug>-03-review-and-decision.md` for review.
Make an explicit `Accept / Revise / Reject` recommendation with reasons.
Do not make git changes.
```

If the first draft needs revision after human review, use:

```text
Revise `agents/docs/<task-slug>-03-review-and-decision.md` using the review comments below.
Keep the same template structure.
Tighten the evidence summary, decision, and next git action.
Do not make git changes.
```

### Step 3 — Review the recommendation, not just the format

The draft should help the human answer questions like:

- did the change actually stay inside the approved task spec?
- do the tests and artifacts line up?
- does the report say only what the artifact supports?
- if the result is weak, should the branch get one more corrective commit or should this work stop here?

Students should not assume that a neatly written review draft is automatically correct. It still has to be checked against the actual evidence.

### Step 4 — Use the approved review record to decide the git action

There is no separate git stage after review. The approved `agents/docs/<task-slug>-03-review-and-decision.md` record is the gate for what happens next on the branch.

Use the `Next Git Action` section to make the branch decision explicit:

- `Accept` means the branch is ready for merge, with a final cleanup commit only if review still requires one.
- `Revise` means fix the problem on the branch before anything is merged.
- `Reject` means stop, revert, or discard the branch rather than hiding the mistake inside more unrelated edits.

This is where students should clean up mistakes while the work is still isolated. The workshop is trying to build the habit that merge decisions follow approved review evidence instead of arriving as a separate, loosely connected step.

## Outputs

- `agents/docs/<task-slug>-03-review-and-decision.md` exists as a review draft grounded in the diff, test outputs, and generated artifacts.
- That draft has been reviewed for evidence quality and for whether its `Accept / Revise / Reject` recommendation is actually justified.
- The approved review record names the next git action for the branch instead of leaving commit or merge decisions implicit.

## Discussion

1. What would make you choose `Revise` instead of `Accept` even if the tests passed?
2. Which parts of the temperature-band task are still fundamentally human-reviewed, not fully automated?
3. What kind of diff change would tell you the agent had solved the wrong problem?
4. What evidence would make you question the report narrative even if the artifact file looks correct?
5. When is rejection the right teaching move instead of one more revision loop?

## Next

Continue to [08 — Refinement and Hardening](./08-refinement.md).
