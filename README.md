# Session 2 - Reproducible Research Workflow

Session 2 shows how to turn notebook-first exploration into an auditable workflow that can support defensible research claims. The goal is methodological clarity: a reviewer should be able to trace how assumptions, data transformations, and outputs connect from start to finish.

The guide uses an incremental teaching model so we will learn one reproducibility control at a time and understand why it exists before layering on the next. This structure is designed For us who need both conceptual justification and executable practice, not just a final code snapshot.

Assumption for this delivery: `00_fetch` and `01_prepare` are already implemented when we will start, so most conceptual depth is placed on `02_analyze` and the reproducibility controls around it.

## Start Here

Use this order to establish context before implementation details. It prevents we will from treating commands as recipes without understanding their methodological role.

1. [docs/README.md](./docs/README.md) for the chapter map.
2. [docs/00-session-overview.md](./docs/00-session-overview.md) for outcomes, assumptions, and workflow contract.

## What we will Build

These outcomes define what “reproducible enough for research use” means in this session. Each item corresponds to a control that reduces ambiguity in interpretation and comparison.

By the end of the core sequence, we will should be able to show:

- one canonical command for a run
- explicit configuration choices
- durable runtime logs
- run-scoped artifacts and a manifest
- automated tests that protect analytical behavior and provenance

Core run contract:

`config -> command -> log -> artifacts -> manifest -> tests`

## Core Path

Follow the core path in sequence because each chapter introduces prerequisites for the next. Skipping ahead usually creates hidden gaps in provenance controls.

1. [Session Overview](./docs/00-session-overview.md)
2. [Project Structure](./docs/01-project-structure.md)
3. [Configuration](./docs/02-config.md)
4. [Command-Line Interface](./docs/03-cli.md)
5. [Logging and Observability](./docs/04-observability.md)
6. [Traceable Runs](./docs/05-traceability.md)
7. [Workflow Orchestration](./docs/06-orchestration.md)
8. [Testing the Workflow](./docs/07-testing.md)

## Appendices

Use appendices only after the core path is stable. They scale or operationalize the workflow contract, but they do not replace core reproducibility fundamentals.

9. [Experiment Tracking](./docs/08-appendix-experiment-tracking.md)
10. [Workflow Engines](./docs/09-appendix-workflow-engines.md)
11. [Multiruns](./docs/10-appendix-multiruns.md)
12. [Hydra](./docs/11-appendix-hydra.md)
13. [Automated Testing on Git Push](./docs/12-appendix-git-push-testing.md)

## How To Read This Repo

Treat the repository as a training scaffold for research workflow design, not as a static template. The discipline is to validate each checkpoint before moving forward so methodological assumptions remain explicit.

Treat each chapter as a checkpointed method lesson:

- read rationale first
- implement the chapter snapshot
- run the checkpoint commands
- move forward only after the checkpoint passes
