# NextGen Coding Bootcamp 2026

Welcome to the NextGen Coding Bootcamp. This repository provides a structured workflow for building reproducible computational research projects.

## 🚀 Quick Start: Onboarding

Whether you are working manually or with an AI coding agent (like GitHub Copilot), follow these steps to set up your environment.

### 1. Prerequisites
- **Git**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **uv**: We use `uv` for lightning-fast package and environment management.
  ```bash
  # macOS/Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # Windows (PowerShell)
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### 2. Fork & Clone
1. **Fork** this repository to your own GitHub account.
2. **Clone** your fork:
   ```bash
   git clone https://github.com/<your-username>/nextgen2026-coding-bootcamp.git
   cd nextgen2026-coding-bootcamp
   ```
3. **Add Upstream**: Keep your fork in sync with the original repo.
   ```bash
   git remote add upstream https://github.com/nextgenerationgraduatesprogram/nextgen2026-coding-bootcamp.git
   ```

### 3. Environment Setup
Initialize the project environment and install dependencies:
```bash
uv sync
```

---

## 🤖 Working with AI Coding Agents

This repository is optimized for collaboration with AI agents.

### 📜 Rules for Agents
If you are using an AI agent (e.g., GitHub Copilot, Cursor), please direct it to read the **[CODING_AGENT_RULES.md](./CODING_AGENT_RULES.md)** file immediately. These rules ensure the agent follows the project's architectural standards:
- Reusable logic in `src/`.
- Thin interfaces in `scripts/`.
- Reproducible notebooks that import from the package.
- Safe, non-destructive command execution.

### 📅 Session Workflow
For every new session or task, the agent should:
1. Sync with `upstream`.
2. Check `git status`.
3. Create a date-stamped feature branch (e.g., `session-1-analysis-2026-04-20`).

---

## 📚 Repository Structure

- `src/`: Durable, reusable research logic (the "engine").
- `scripts/`: Task-specific scripts that call the engine.
- `notebooks/`: Exploratory analysis and visualization.
- `data/raw/`: Read-only input data.
- `results/`: Generated outputs (ignored by Git, except for `.gitkeep`).
- `docs/`: Step-by-step session guides.

## 🛠 Useful Commands

- **Run Visualization**: `uv run viz`
- **Run Hello World**: `uv run hello`
- **Start Jupyter**: `uv run --with jupyterlab jupyter lab`
- **Build Package**: `uv build`

## 📖 Session Guides
- If you are on the **main branch**: Start with the **[Development Environment Setup](./docs/00-development-environment.md)**.
- If you are on a **session branch**: Start with the **[Session 1 Overview](./docs/session-overview.md)** (or the relevant session doc).
