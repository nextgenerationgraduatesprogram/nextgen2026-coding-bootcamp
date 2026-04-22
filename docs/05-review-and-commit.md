# 05 — Review and Commit

## What practical question does this guide answer?

This guide answers the post-implementation question: how should you turn tests, artifacts, diff review, and current git state into an explicit decision before commit or merge?

The answer should be drafted into `@03-review-and-decision.md`, then reviewed by you before deciding whether to accept, revise, or reject the branch outcome.

## Why this matters

Passing tests alone is not enough. You still have to judge whether the change stayed inside the approved spec, respected the behavioural contract, used the right stage boundary, and represented the artifact honestly.

This phase combines review and commit discipline on purpose. The workshop is trying to build the habit that commit and merge actions follow approved review evidence instead of arriving as a separate, loosely connected step.

It also keeps failure recovery explicit. If the branch is not good enough to keep, the review outcome should tell you whether to revise on top of the current work or restore back to the pre-implementation checkpoint and try again.

## Steps

### Step 1 — Gather the evidence

```bash
uv run pytest -q
uv run python scripts/run_workflow.py --profile base --run-name s3-review-check
LATEST_RUN=$(ls -1dt runs/*s3-review-check* | head -n1)
git status --short --branch
git diff --stat
git diff
find "$LATEST_RUN" -maxdepth 2 -type f | sort
```

Gather both mechanical and readable evidence. For the running example, that means the behavioural tests, broader repo tests, current diff, generated CSVs, and report markdown.

### Step 2 — Ask the agent to draft the review record

```text
Using `agents/docs/<task-slug>-01-task-spec.md`, `agents/docs/<task-slug>-02-implementation-plan.md`, the current git status, the current diff, the test outputs, and the generated artifacts, fill the format specified in `@03-review-and-decision.md`.
Place the result in `agents/docs/<task-slug>-03-review-and-decision.md` for review.
Make an explicit `Accept / Revise / Reject` recommendation with reasons.
Do not make git changes.
```

### Step 3 — Review the recommendation, not just the format

The draft should help you answer:

- does the diff match the approved spec and plan?
- do the behavioural tests and broader tests line up with the implementation?
- do the artifacts support what the report says?
- should the branch be accepted, revised, or rejected?

Do not assume that a neatly written review draft is automatically correct. It still has to be checked against the actual evidence.

### Step 4 — Use the approved review record to decide the git action

The approved review record is the gate for what happens next:

- `Accept` means the branch is ready for commit or merge, with cleanup only if review still requires one.
- `Revise` means fix the problem on the branch before anything is committed or merged.
- `Reject` means stop, restore or discard the bad implementation work, and return to the last good checkpoint rather than hiding the mistake inside more unrelated edits.

If the work is accepted and you move into refinement, prefer to start a fresh chat for that final phase. The refinement chat should begin from the approved review record and the concrete session outcome rather than from the entire implementation history.

## Outputs

- `agents/docs/<task-slug>-03-review-and-decision.md` exists as a review draft grounded in the diff, tests, artifacts, and git state.
- The review record has been checked for contract alignment, diff quality, test evidence, and artifact support.
- The next commit or merge action is explicit rather than implied.

## Discussion

1. What would make you choose `Revise` instead of `Accept` even if the full suite passed?
2. What kind of diff change would tell you the implementation solved the wrong problem?
3. What evidence would make you question the report narrative even if the artifact file looks correct?
4. How should the review record use the approved spec, implementation plan, and `AGENTS.md` together rather than treating tests as the only authority?
5. When is rejection the right teaching move instead of one more revision loop?
6. Why is it useful to make commit or merge decisions part of the review artifact itself?

## Next

Continue to [06 — Refinement](./06-refinement.md).
