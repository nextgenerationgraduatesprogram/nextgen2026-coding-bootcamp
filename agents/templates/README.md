# Session 3 Templates

These are the canonical blank templates for the prompt-first workshop flow. Keep these files as source templates. Ask the agent to draft filled versions into `agents/docs/` for human review.

1. `01-task-spec.md`
   Use when the human has chosen a task and wants the agent to draft the approved task spec, including risk, scope, and verification.
2. `02-agent-brief.md`
   Use after the task spec is approved to draft the bounded implementation handoff, minimal context bundle, and required return format.
3. `03-review-and-decision.md`
   Use after implementation to draft the review record, evidence summary, decision recommendation, and next git action.
4. `04-hardening-note.md`
   Use at the end of the session to capture what should become durable repo structure or repeatable workflow.

Naming pattern for drafts:

- `agents/docs/<task-slug>-01-task-spec.md`
- `agents/docs/<task-slug>-02-agent-brief.md`
- `agents/docs/<task-slug>-03-review-and-decision.md`
- `agents/docs/<task-slug>-04-hardening-note.md`
