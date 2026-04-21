# 04 — Context Management

## What practical question does this guide answer?

This guide answers the context question: what does the agent actually need to see to do the task well without getting flooded with irrelevant files?

In the prompt-first workflow, the answer should be drafted into `@02-agent-brief.md`, then reviewed by you before implementation begins.

## Why this matters

Giving the agent the whole repo is not the same as giving it the right context. Good supervision means choosing a minimal, defensible context bundle and explaining why each item is there.

This is where you build a useful habit: context should be justified, not merely attached. If you cannot explain why a file is in the context bundle, there is a good chance the agent does not need it yet.

## Steps

### Step 1 — Inspect the likely implementation surfaces

```bash
sed -n '1,260p' AGENTS.md
rg --files src/nextgen2026_coding_bootcamp/steps scripts tests configs | sort
```

The goal is to see where the likely implementation and verification work will live before drafting the brief.

### Step 2 — Ask the agent to draft the agent brief

```text
Using `agents/docs/<task-slug>-01-task-spec.md`, prepare the implementation handoff in the format specified in `@02-agent-brief.md`.
Place the result in `agents/docs/<task-slug>-02-agent-brief.md` for review.
Use the current repo structure to fill:
- approved objective
- bounded scope
- durable instructions
- minimal context bundle
- stop and escalate conditions
Do not implement code.
```

If the context is too broad or too vague, use:

```text
Revise `agents/docs/<task-slug>-02-agent-brief.md` using the review comments below.
Trim the context bundle to the minimum needed.
Keep the scope bounded.
Do not implement code.
```

### Step 3 — Review the bundle for both sufficiency and restraint

A good context bundle is not just short. It is explainable. You should be able to say:

- why each file is included
- what uncertainty it resolves
- what extra file they would add only if a new blocker appeared

That is what makes the reasoning chain legible later.

## Outputs

- `agents/docs/<task-slug>-02-agent-brief.md` exists as a draft implementation brief tied back to the approved task spec.
- That draft has been reviewed for minimal context, durable instructions, and explicit stop-and-escalate conditions.

## Discussion

1. What is the difference between too little context and too much context?
2. Which files belong in the first-turn bundle for the temperature-band task, and which should wait until a concrete blocker appears?
3. Why is it useful to have the agent explain why each context item is included?
4. What context tends to create noise rather than clarity in a first implementation turn?
5. How would you notice that the agent is leaning on generic assumptions instead of repo facts?

## Next

Continue to [05 — Delegation](./05-delegation.md).
