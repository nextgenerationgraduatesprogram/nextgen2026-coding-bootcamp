# Repository Instructions for Coding Agents

## Purpose
This repository teaches reproducible, reviewable workflow development on the Bike Sharing dataset.

## Canonical Commands
- Full test suite: `uv run pytest -q`
- Full workflow: `uv run python scripts/run_workflow.py --profile base --run-name local-run`
- Stage scripts:
  - `uv run python scripts/00_fetch.py --config configs/stages/fetch.yaml --run-name fetch-only`
  - `uv run python scripts/01_prepare.py --config configs/stages/prepare.yaml --run-name prepare-only`
  - `uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml --run-name analyze-only`
  - `uv run python scripts/03_report.py --config configs/stages/report.yaml --run-name report-only`

## Repository Map
- `src/nextgen2026_coding_bootcamp/steps/`: stage logic (Entry points: `run_fetch`, `run_prepare`, `run_analyze`, `run_report`)
- `scripts/`: CLI wrappers and workflow runner
- `configs/`: run/path/stage/profile configuration
- `tests/`: regression and workflow checks
- `runs/`: run-scoped artifacts and manifests
- `docs/`: workshop guides, templates, and archive

---

## 1. Environment & Dependency Management
- **Tool**: Always use `uv` for environment management, package installation, and execution.
- **Lockfile**: Always keep `uv.lock` in sync with `pyproject.toml`.
- **Execution**: Use `uv run <command>` or `uv run python <script>` to ensure the project environment is used.

## 2. Code Organization (The "Thin Interface" Rule)
- **Source (`src/`)**: All durable, reusable logic must live in `src/nextgen2026_coding_bootcamp/`.
- **Scripts (`scripts/`)**: Scripts should be "thin." They should handle CLI arguments and call functions from `src/`. Do not put core business/research logic in scripts.
- **Notebooks (`notebooks/`)**: Notebooks are for exploration and visualization. They must import project code from `src/` rather than redefining logic.
- **Commands**: Define official project entry points in `pyproject.toml` under `[project.scripts]`.

## 3. Data & Results Handling
- **Raw Data (`data/raw/`)**: Treat raw data as read-only. Never modify files in this directory.
- **Results (`results/`)**: All generated outputs (CSVs, plots, logs) must go into `results/`.
- **Traceability**: For all formal analysis runs, use the `run_id` pattern. Outputs must be stored in unique, timestamped directories under `runs/` to prevent overwrites and preserve provenance.
- **Paths**: Use `Path(__file__).resolve()` or relative path logic rooted in the project structure. Do not use hardcoded absolute paths.

## 4. Version Control & Session Management
- **Syncing Upstream**: Before starting a new session, ensure the fork is synced:
    1. `git fetch upstream`
    2. `git merge upstream/main` (on the main branch)
- **Session Start**: At the beginning of a session, always:
    1. Check `git status`.
    2. Check the current branch state.
    3. `git fetch upstream` to check for new session branches (e.g., `starter/session-2`).
    4. Switch to the relevant session branch or create a specific feature branch if requested.
    5. **Rule Restoration**: If `AGENTS.md` is missing on the new branch, restore it using `git show <previous-branch>:AGENTS.md > AGENTS.md`.
    6. **README Merging**: Preserve the master project overview in `README.md`. If a session update replaces the README, merge the new session-specific content below the existing project overview and agent rules.
- **Experiment Management**: Use the **"Branching Out"** method for experiments. Create dedicated branches for hypothesis testing or parameter variants (e.g., `experiment/quantile-0.95`) and commit both config snapshots and results to those branches.
- **Commits**: Make small, logical commits. Use prefixing (e.g., `feat:`, `fix:`, `build:`, `docs:`) as per Conventional Commits where possible.
- **Ignored Files**: Ensure local artifacts like `.venv/`, `__pycache__/`, and `dist/` are never committed.
- **Lockfiles**: Always commit `uv.lock`.

## 5. Safety, Destructive Commands & Explainability
- **Destructive Commands**: Before running any destructive commands (e.g., `git reset --hard`, `rm -rf` on non-build directories, `git clean -fd`), the agent **must**:
    1. Explain the reason for the command.
    2. Explain the meaning and impact of the specific code/command (Explainability).
    3. Request explicit permission from the user.

## 6. Coding Style
- **Type Hints**: Use Python type hints for all function signatures.
- **Docstrings**: Provide concise docstrings for functions in `src/`.
- **Main Pattern**: Always use the `if __name__ == "__main__": main()` pattern in scripts and entry points.

---

## 7. Delegation & Review (Core Principles)
- **Delegation Strategy**: Use one agent per bounded contract. Request a plan before implementation. Keep diffs small and scoped.
- **Review Requirements**: Every delegated change must include:
  - contract alignment check (does it do what was approved?)
  - diff review (is the code idiomatic and safe?)
  - test evidence (including extensions to existing tests for new features)
  - artifact/output inspection (are the results scientifically plausible?)
  - explicit Accept/Revise/Reject decision

## 8. Workflow Guardrails
- **Protect Core Transformations**: Do not change upstream data logic (the "source of truth") unless explicitly requested.
- **Respect Stage Boundaries**: Logic should be placed in the stage that "owns" the data transformation to prevent leaky abstractions.
- **Maintain CLI Semantics**: Do not change established command-line interfaces or argument signatures as they are often consumed by CI/CD or other users.

## 9. Risk & Task Selection
- **Assess "Blast Radius"**: Prefer delegating "Downstream" tasks (reporting, visualization, secondary analysis) over "Upstream" tasks (data fetching, core cleaning) as they have a smaller impact on total project integrity.
- **Review Burden Principle**: A task is well-delegated if the effort to review the results (diffs + artifacts) is significantly lower than the effort to implement it manually.

## 10. Resource Management & Performance
- **Monitor Context Usage**: Always track the estimated percentage of the context window being used.
- **Escalation Threshold**: If the context usage exceeds **60%**, stop and escalate to the user to discuss context trimming, file consolidation, or task splitting to maintain performance and avoid "forgetting" instructions.
# Coding Agent Instructions & Rules

> **IMPORTANT**: Every new AI session MUST start by reading this file and following the instructions in Section 4 (Version Control & Session Management).

This document outlines the architectural and workflow rules for any AI agent assisting with the `nextgen2026-coding-bootcamp` repository.

## 1. Environment & Dependency Management
- **Tool**: Always use `uv` for environment management, package installation, and execution.
- **Lockfile**: Always keep `uv.lock` in sync with `pyproject.toml`.
- **Execution**: Use `uv run <command>` or `uv run python <script>` to ensure the project environment is used.

## 2. Code Organization (The "Thin Interface" Rule)
- **Source (`src/`)**: All durable, reusable logic must live in `src/nextgen2026_coding_bootcamp/`.
- **Scripts (`scripts/`)**: Scripts should be "thin." They should handle CLI arguments and call functions from `src/`. Do not put core business/research logic in scripts.
- **Notebooks (`notebooks/`)**: Notebooks are for exploration and visualization. They must import project code from `src/` rather than redefining logic.
- **Commands**: Define official project entry points in `pyproject.toml` under `[project.scripts]`.

## 3. Data & Results Handling
- **Raw Data (`data/raw/`)**: Treat raw data as read-only. Never modify files in this directory.
- **Results (`results/`)**: All generated outputs (CSVs, plots, logs) must go into `results/`.
- **Traceability**: For all formal analysis runs, use the `run_id` pattern. Outputs must be stored in unique, timestamped directories under `runs/` to prevent overwrites and preserve provenance.
- **Paths**: Use `Path(__file__).resolve()` or relative path logic rooted in the project structure. Do not use hardcoded absolute paths.

## 4. Version Control & Session Management
- **Syncing Upstream**: Before starting a new session, ensure the fork is synced:
    1. `git fetch upstream`
    2. `git merge upstream/main` (on the main branch)
- **Session Start**: At the beginning of a session, always:
    1. Check `git status`.
    2. Check the current branch state.
    3. `git fetch upstream` to check for new session branches (e.g., `starter/session-2`).
    4. Switch to the relevant session branch or create a specific feature branch if requested.
    5. **Rule Restoration**: If `AGENTS.md` is missing on the new branch, restore it using `git show <previous-branch>:AGENTS.md > AGENTS.md`.
    6. **README Merging**: Preserve the master project overview in `README.md`. If a session update replaces the README, merge the new session-specific content below the existing project overview and agent rules.
- **Experiment Management**: Use the **"Branching Out"** method for experiments. Create dedicated branches for hypothesis testing or parameter variants (e.g., `experiment/quantile-0.95`) and commit both config snapshots and results to those branches.
- **Commits**: Make small, logical commits. Use prefixing (e.g., `feat:`, `fix:`, `build:`, `docs:`) as per Conventional Commits where possible.
- **Ignored Files**: Ensure local artifacts like `.venv/`, `__pycache__/`, and `dist/` are never committed.
- **Lockfiles**: Always commit `uv.lock`.

## 5. Safety, Destructive Commands & Explainability
- **Destructive Commands**: Before running any destructive commands (e.g., `git reset --hard`, `rm -rf` on non-build directories, `git clean -fd`), the agent **must**:
    1. Explain the reason for the command.
    2. Explain the meaning and impact of the specific code/command (Explainability).
    3. Request explicit permission from the user.

## 6. Coding Style
- **Type Hints**: Use Python type hints for all function signatures.
- **Docstrings**: Provide concise docstrings for functions in `src/`.
- **Main Pattern**: Always use the `if __name__ == "__main__": main()` pattern in scripts and entry points.
