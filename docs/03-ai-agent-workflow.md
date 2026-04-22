# AI Agent Workflow

This workshop should feel iterative, not one-shot. The goal is to use the agent to produce a series of reviewable artifact files in `agents/docs/`, approving each one before moving to the next step.

The recommended flow is:

1. iterate on requirements until the feature is documented clearly enough to approve
2. iterate on behavioural tests until the expected behaviour is locked
3. iterate on an implementation plan until the build sequence is clear
4. request implementation from the approved plan
5. validate the result yourself and ask the agent to validate it too

## Steps

### Step 1. Iterate On Requirements

Start by getting the feature requirements into a document you are happy with. Do not implement anything yet. Keep revising the requirements artifact until it is precise enough to approve.

Use this template and output file:

- Template: `agents/templates/01-requirements-template.md`
- Artifact: `agents/docs/<task-slug>-01-requirements.md`

Prompt the agent like this:

```text
Read `AGENTS.md`, `docs/project-card.md`, `src/nextgen2026_coding_bootcamp/steps/analyze.py`, `src/nextgen2026_coding_bootcamp/steps/report.py`, `configs/base.yaml`, `configs/stages/analyze.yaml`, `configs/stages/report.yaml`, and `agents/templates/01-requirements-template.md`.

Fill the template and write the completed requirements artifact to `agents/docs/<task-slug>-01-requirements.md`.

Keep the requirements bounded to the current workflow shape. Do not implement anything yet.
```

Review the generated file, revise the prompt if needed, and repeat until the requirements document is approved.

### Step 2. Iterate On Behavioural Tests

Once the requirements are approved, use them to define the behavioural tests you expect to build before implementation. Do not implement anything yet.

Use this template and output file:

- Template: `agents/templates/02-behavioural-tests-template.md`
- Artifact: `agents/docs/<task-slug>-02-behavioural-tests.md`

Prompt the agent like this:

```text
Read `agents/docs/<task-slug>-01-requirements.md` and `agents/templates/02-behavioural-tests-template.md`.

Fill the template and write the completed behavioural-tests artifact to `agents/docs/<task-slug>-02-behavioural-tests.md`.

Propose behavioural tests for the approved feature only. Do not implement anything yet.
```

Review the test artifact, revise it until the expected behaviour is locked, and approve it before moving on.

### Step 3. Iterate On The Implementation Plan

Before asking for code changes, create your own implementation-plan template file. The repo does not precreate this one for you.

Create this template file yourself:

- Template to create: `agents/templates/03-implementation-plan-template.md`
- Artifact to generate: `agents/docs/<task-slug>-03-implementation-plan.md`

Suggested headings for your template:

- Approved artifact references
- In-scope files and out-of-scope files
- Ordered implementation steps
- Tests to write or update
- Verification commands
- Stop and escalate conditions
- Approval

Prompt the agent like this after you have created the template:

```text
Read `agents/docs/<task-slug>-01-requirements.md`, `agents/docs/<task-slug>-02-behavioural-tests.md`, and `agents/templates/03-implementation-plan-template.md`.

Fill the template and write the completed implementation-plan artifact to `agents/docs/<task-slug>-03-implementation-plan.md`.

Keep the plan bounded to the approved requirements and behavioural tests. Do not implement anything yet.
```

Revise the implementation plan until it is decision-complete and approved.

### Step 4. Request Implementation

Before you ask the agent to implement the plan, create a checkpoint commit so you can clean up or restore the branch easily if the implementation goes sideways.

```bash
git status --short
git add agents/docs agents/templates
git commit -m "Checkpoint before implementation"
```

Then create your own implementation-request template file. The repo does not precreate this one for you.

Create this template file yourself:

- Template to create: `agents/templates/04-implementation-request-template.md`
- Artifact to generate: `agents/docs/<task-slug>-04-implementation-request.md`

Suggested headings for your template:

- Approved artifact references
- Files the agent may change
- Files the agent must not change
- Verification commands to run after implementation
- Stop conditions

Prompt the agent like this after you have created the template:

```text
Read `agents/docs/<task-slug>-01-requirements.md`, `agents/docs/<task-slug>-02-behavioural-tests.md`, `agents/docs/<task-slug>-03-implementation-plan.md`, and `agents/templates/04-implementation-request-template.md`.

Fill the template and write the completed implementation-request artifact to `agents/docs/<task-slug>-04-implementation-request.md`.

Then implement the approved plan. Keep changes inside the approved scope and run the verification commands listed in the implementation plan.
```

### Step 5. Validate The Result

Validation should happen twice: once by you, and once by the agent. Run the checks yourself, inspect the artifacts, and then ask the agent to record an evidence-based validation artifact.

Create this template file yourself:

- Template to create: `agents/templates/05-validation-template.md`
- Artifact to generate: `agents/docs/<task-slug>-05-validation.md`

Suggested headings for your template:

- Approved artifact references
- Checks run
- Diff review
- Artifact inspection
- Issues found
- Decision and next action

Run your own validation first using the commands in `docs/04-validation-review-and-merge-request.md`.

Then prompt the agent like this:

```text
Read `agents/docs/<task-slug>-01-requirements.md`, `agents/docs/<task-slug>-02-behavioural-tests.md`, `agents/docs/<task-slug>-03-implementation-plan.md`, `agents/docs/<task-slug>-04-implementation-request.md`, `agents/templates/05-validation-template.md`, and `docs/04-validation-review-and-merge-request.md`.

Validate the implementation against the approved artifacts, the diff, the tests that were run, the workflow run, and the generated outputs.

Fill the template and write the completed validation artifact to `agents/docs/<task-slug>-05-validation.md`. Do not implement new changes during this step.
```

Keep the validation artifact with the other generated docs so the full decision trail for the feature remains reviewable.
