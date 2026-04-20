# Coding Agent Instructions & Rules

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
- **Paths**: Use `Path(__file__).resolve()` or relative path logic rooted in the project structure. Do not use hardcoded absolute paths.

## 4. Version Control & Session Management
- **Syncing Upstream**: Before starting a new session, ensure the fork is synced:
    1. `git fetch upstream`
    2. `git merge upstream/main` (on the main branch)
- **Session Start**: At the beginning of a session, always:
    1. Check `git status`.
    2. Check the current branch state.
    3. Create a new working branch with the current date appended (e.g., `feature-name-2026-04-20`).
- **Commits**: Make small, logical commits. Use prefixing (e.g., `feat:`, `fix:`, `build:`, `docs:`) as per Conventional Commits where possible.
- **Ignored Files**: Ensure local artifacts like `.venv/`, `__pycache__/`, and `dist/` are never committed.
- **Lockfiles**: Always commit `uv.lock`.

## 5. Safety & Destructive Commands
- **Destructive Commands**: Before running any destructive commands (e.g., `git reset --hard`, `rm -rf` on non-build directories, `git clean -fd`), the agent **must**:
    1. Explain the reason for the command.
    2. Request explicit permission from the user.

## 6. Coding Style
- **Type Hints**: Use Python type hints for all function signatures.
- **Docstrings**: Provide concise docstrings for functions in `src/`.
- **Main Pattern**: Always use the `if __name__ == "__main__": main()` pattern in scripts and entry points.
