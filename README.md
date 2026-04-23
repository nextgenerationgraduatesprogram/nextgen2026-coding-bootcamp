# NextGen Coding Bootcamp

This four-session boot camp introduces the core workflow skills needed to run a computational research project from setup to reproducible handoff. We will learn how to structure a research repository, run analyses through scripts and configuration, capture logs and outputs, use coding tools such as Copilot to accelerate development, and produce work that another researcher can rerun, review, and extend.

---

# 🚀 Session 2 - Reproducible Research Workflow

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

---

## 🤖 Working with AI Coding Agents

This repository is optimized for collaboration with AI agents.

### 📜 Rules for Agents
If you are using an AI agent (e.g., GitHub Copilot, Cursor), please direct it to read the **[CODING_AGENT_RULES.md](./CODING_AGENT_RULES.md)** file immediately. These rules ensure the agent follows the project's architectural standards:
- **Automatic Syncing**: The rules require the agent to fetch from `upstream` at the start of every session to ensure they are working with the latest workshop material.
- **Project Structure**: Reusable logic must live in `src/`, with thin interfaces in `scripts/`.
- **Reproducibility**: Notebooks must import from the package instead of redefining logic.
- **Safety & Explainability**: Safe, non-destructive command execution with explicit user approval. Agents must explain the meaning and impact of any destructive code before running it.

## 📚 Repository Structure

- `src/`: Durable, reusable research logic (the "engine").
- `scripts/`: Task-specific scripts that call the engine.
- `notebooks/`: Exploratory analysis and visualization.
- `data/raw/`: Read-only input data.
- `results/`: Generated outputs (ignored by Git, except for `.gitkeep`).

## 📖 Session Guides
- If you are on the **main branch**: Start with the **[Development Environment Setup](./docs/00-development-environment.md)**.
- If you are on a **session branch**: Start with the **[Session Overview](./docs/00-session-overview.md)**.
