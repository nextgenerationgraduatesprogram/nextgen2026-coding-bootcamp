# NextGen Coding Bootcamp

This four-session boot camp introduces the core workflow skills needed to run a computational research project from setup to reproducible handoff. We will learn how to structure a research repository, run analyses through scripts and configuration, capture logs and outputs, use coding tools such as Codex to accelerate development, and produce work that another researcher can rerun, review, and extend.

## Before Session 1

- [ ] Windows only: install WSL and Ubuntu 24.04
- [ ] Install VS Code
- [ ] Install the VS Code `WSL` and `Python` extensions
- [ ] In Linux or WSL, install `git`, `python3`, and `uv`
- [ ] Set your Git name and email
- [ ] Clone this repository into `~/work` and open it in VS Code

See [Development Environment Setup](./docs/00-development-environment.md) for steps and checks.

## Session Branches

This repository uses separate branches for each session.

- `starter/session-<n>`: starting point for the session
- `solutions/session-<n>`: completed reference version for the session

To begin a session, switch to its starter branch:

```bash
git switch starter/session-1
```

To inspect a completed version, switch to the matching solutions branch:

```bash
git switch solutions/session-1
```

## Learning Objectives

By the end of the boot camp, we will be able to:

- set up a clean research code repository with a sensible project structure, isolated environment, and version control
- run analyses from scripts and configuration files rather than relying on notebook cell order
- capture logs, outputs, and artifacts in a way that supports reproducibility and debugging
- write and run basic tests to make research code safer to change
- use AI coding tools productively through spec-driven development, documentation, and review
- package a small research project so that another person can clone it, run it, and understand how results were produced
