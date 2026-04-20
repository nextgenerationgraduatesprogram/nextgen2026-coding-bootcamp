# NextGen Coding Bootcamp

This four-session boot camp introduces the core workflow skills needed to run a computational research project from setup to reproducible handoff. We will learn how to structure a research repository, run analyses through scripts and configuration, capture logs and outputs, use coding tools such as Copilot to accelerate development, and produce work that another researcher can rerun, review, and extend.

## Before Session 1

Whether you are working manually or with an AI coding agent, follow these steps to set up your environment.

- [ ] **Install VS Code**
- [ ] **Windows only**: install [WSL and Ubuntu 24.04](https://apps.microsoft.com/store/detail/ubuntu-2404-lts/9P7N5RW865B8)
- [ ] **Install the VS Code `WSL` and `Python` extensions**
- [ ] **Install Git, Python 3.11+, and `uv`**
  - **uv** (Recommended): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] **Fork & Clone** this repository:
  ```bash
  git clone https://github.com/<your-username>/nextgen2026-coding-bootcamp.git
  cd nextgen2026-coding-bootcamp
  git remote add upstream https://github.com/nextgenerationgraduatesprogram/nextgen2026-coding-bootcamp.git
  ```
- [ ] **Set your Git name and email**
- [ ] **Initialize the environment**: `uv sync`

See **[Development Environment Setup](./docs/00-development-environment.md)** for detailed checks.

## Session Branches

This repository uses separate branches for each session.

- `starter/session-<n>`: starting point for the session
- `solutions/session-<n>`: completed reference version for the session

To begin a session, switch to its starter branch:

```bash
git switch starter/session-1
```

## Learning Objectives

By the end of the boot camp, we will be able to:

- set up a clean research code repository with a sensible project structure, isolated environment, and version control
- run analyses from scripts and configuration files rather than relying on notebook cell order
- capture logs, outputs, and artifacts in a way that supports reproducibility and debugging
- write and run basic tests to make research code safer to change
- use AI coding tools productively through spec-driven development, documentation, and review
- package a small research project so that another person can clone it, run it, and understand how results were produced

---

## 🤖 Working with AI Coding Agents

This repository is optimized for collaboration with AI agents.

### 📜 Rules for Agents
If you are using an AI agent (e.g., GitHub Copilot, Cursor), please direct it to read the **[CODING_AGENT_RULES.md](./CODING_AGENT_RULES.md)** file immediately. These rules ensure the agent follows the project's architectural standards:
- Reusable logic in `src/`.
- Thin interfaces in `scripts/`.
- Reproducible notebooks that import from the package.
- Safe, non-destructive command execution.

---

## 📚 Repository Structure

- `src/`: Durable, reusable research logic (the "engine").
- `scripts/`: Task-specific scripts that call the engine.
- `notebooks/`: Exploratory analysis and visualization.
- `data/raw/`: Read-only input data.
- `results/`: Generated outputs (ignored by Git, except for `.gitkeep`).

## 📖 Session Guides
- If you are on the **main branch**: Start with the **[Development Environment Setup](./docs/00-development-environment.md)**.
- If you are on a **session branch**: Start with the **[Session 1 Overview](./docs/session-overview.md)** (or the relevant session doc).
