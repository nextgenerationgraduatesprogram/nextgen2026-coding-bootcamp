# NextGen Coding Bootcamp

This four-session boot camp introduces the core workflow skills needed to run a computational research project from setup to reproducible handoff. We will learn how to structure a research repository, run analyses through scripts and configuration, capture logs and outputs, use coding tools such as Copilot to accelerate development, and produce work that another researcher can rerun, review, and extend.

## Before Session 1 (Quick Start Onboarding)

Whether you are working manually or with an AI coding agent, follow these steps to set up your environment.

### 1. Prerequisites
- [ ] **Install VS Code**
- [ ] **Windows only**: install [WSL and Ubuntu 24.04](https://apps.microsoft.com/store/detail/ubuntu-2404-lts/9P7N5RW865B8)
- [ ] **Install the VS Code `WSL` and `Python` extensions**
- [ ] **Install Git, Python 3.11+, and `uv`**
  - **uv** (Recommended): `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 2. Fork & Clone
- [ ] **Fork** this repository to your own GitHub account.
  > *A "Fork" is your personal copy of the project on GitHub. It allows you to save your progress and make changes without affecting the original repository.*
- [ ] **Clone** your fork and add the original as `upstream`:
  > *A "Clone" downloads your personal GitHub copy to your local machine so you can work on it in VS Code.*
  ```bash
  # Replace <your-username> with your actual GitHub username
  git clone https://github.com/<your-username>/nextgen2026-coding-bootcamp.git
  cd nextgen2026-coding-bootcamp

  # This connects your local copy back to the original workshop repo
  git remote add upstream https://github.com/nextgenerationgraduatesprogram/nextgen2026-coding-bootcamp.git
  ```

### 3. Final Checks & Environment
- [ ] **Set your Git name and email**
  > *This ensures that every change you save (commit) is correctly attributed to you.*
- [ ] **Initialize the environment**:
  > *`uv sync` automatically creates a virtual environment and installs all the libraries needed for the bootcamp.*
  ```bash
  uv sync
  ```

See **[Development Environment Setup](./docs/00-development-environment.md)** for detailed checks and troubleshooting.

## Session Branches

This repository uses separate branches for each session.

- `starter/session-<n>`: starting point for the session
- `solutions/session-<n>`: completed reference version for the session

### 🔄 Staying in Sync (How to get new sessions)
As the workshop progresses, new branches will be released. To get them into your fork:

1. **Fetch the updates**:
   ```bash
   git fetch upstream
   ```
2. **Start a new session** (e.g., Session 2):
   ```bash
   git checkout -b starter/session-2 upstream/starter/session-2
   ```
3. **Backup to your fork**:
   ```bash
   git push origin starter/session-2
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
- **Automatic Syncing**: The rules require the agent to fetch from `upstream` at the start of every session to ensure they are working with the latest workshop material.
- **Project Structure**: Reusable logic must live in `src/`, with thin interfaces in `scripts/`.
- **Reproducibility**: Notebooks must import from the package instead of redefining logic.
- **Safety & Explainability**: Safe, non-destructive command execution with explicit user approval. Agents must explain the meaning and impact of any destructive code before running it.

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
