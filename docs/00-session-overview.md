# Session Overview

Session 2 frames notebook-to-workflow migration as a research design task: making analytical results traceable from assumptions and data inputs through to reported outputs. The chapter defines the run contract that later chapters implement piece by piece.

The purpose is to make reproducibility explicit before any refactoring work begins. By clarifying outcomes, assumptions, and failure modes up front, the rest of the sequence can be taught as a coherent method pathway rather than a disconnected set of coding steps.

## 1. What This Chapter Adds

This section defines the session-level success criteria and operating assumptions that all later chapters depend on. Treat these as acceptance criteria for methodological readiness, not optional checklist items.

By the end of the core path (`00`-`07`), students should be able to:

1. run the full workflow with explicit configuration;
2. recover exactly what happened in a run from durable files;
3. compare runs without guessing parameter or path differences;
4. use tests as a pre-interpretation quality gate.

## 2. Why This Matters for Researchers

Notebook-first exploration remains essential for hypothesis generation, but publication-grade evidence needs explicit controls that survive reruns and team handoffs. This section names the failure modes that motivate every technical decision in the core path.

Common failure modes in notebook-only delivery:

1. hidden state from out-of-order cell execution;
2. mutable literals that blur run provenance;
3. shared output paths that overwrite evidence;
4. manual reruns that cannot be audited consistently.

These are methodological risks, not formatting issues.

## 3. Build Steps

Complete these steps in order to establish a stable execution baseline before discussing architecture. A valid baseline prevents later chapters from being derailed by environment ambiguity.

### Step 1: Confirm environment tools

```bash
uv --version
```

### Step 2: Confirm required Python packages

```bash
uv run python -c "import pandas, omegaconf, matplotlib, pytest; print('env-ok')"
```

### Step 3: Confirm session assumptions

For this course delivery, students enter with `fetch` and `prepare` already implemented. The core teaching focus is how to make `analyze` and downstream execution reproducible.

## 4. Run Checkpoint

Use this checkpoint to verify that the prewritten `fetch` and `prepare` assumptions hold and that `analyze` is runnable on real data. Passing this run confirms the teaching baseline for the rest of the session.

```bash
uv run python scripts/00_fetch.py --config configs/stages/fetch.yaml
uv run python scripts/01_prepare.py --config configs/stages/prepare.yaml
uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml
```

## 5. Transition

Next chapter: [Project Structure](./01-project-structure.md). It introduces boundary decisions that every downstream control relies on, so this transition is a dependency step rather than a topic switch.
