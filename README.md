# Session 1 - Build the Research Repo

This branch is the completed Session 1 reference state. It shows a small research repo with one official run path, reusable code in `src/`, thin scripts, and a notebook that imports project code instead of replacing it.

If you are working through the session step by step, start with `docs/session-overview.md`.

## Official Commands

Run the small demonstration command:

```bash
uv run hello
```

Run the example workflow that writes results:

```bash
uv run viz
```

Run the thin script that prints the summary through an import from `src/`:

```bash
uv run python scripts/show_summary.py
```

## Guide

Work through the Session 1 docs in order:

- `docs/session-overview.md` for the overview and branch setup
- `docs/00-project-demo.md` to preview the finished repo
- `docs/01-project-initialization.md` to `docs/09-project-build.md` for the core build sequence
- `docs/10-docker-containers.md` and `docs/11-apptainer-containers.md` for optional appendices

## Repository Map

- `src/nextgen2026_coding_bootcamp/`: reusable project code
- `scripts/`: thin operational helpers
- `notebooks/`: exploratory work that imports project code
- `data/raw/`: input data for the example workflow
- `results/`: generated outputs from the workflow
- `docs/`: the Session 1 student guide and appendices

## Learning Objectives

- build a packaged research repo from a sparse starter state
- manage runtime and development dependencies with `uv`
- keep reusable logic in `src/`
- separate the official workflow from scripts and notebooks
