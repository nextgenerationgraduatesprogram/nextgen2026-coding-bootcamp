# Agent Templates

These templates support the artifact-driven workflow in `docs/03-ai-agent-workflow.md`.

## Numbered Convention

- `agents/templates/01-requirements-template.md`
- `agents/templates/02-behavioural-tests-template.md`

Only steps 1 and 2 are precreated in the repo.

For steps 3 through 5, the user should create these template files themselves before prompting the agent:

- `agents/templates/03-implementation-plan-template.md`
- `agents/templates/04-implementation-request-template.md`
- `agents/templates/05-validation-template.md`

## Generated Artifact Naming

Ask the agent to write completed step artifacts into `agents/docs/` using a shared task slug:

- `agents/docs/<task-slug>-01-requirements.md`
- `agents/docs/<task-slug>-02-behavioural-tests.md`
- `agents/docs/<task-slug>-03-implementation-plan.md`
- `agents/docs/<task-slug>-04-implementation-request.md`
- `agents/docs/<task-slug>-05-validation.md`

Keep the same task slug across all five files for one feature.
