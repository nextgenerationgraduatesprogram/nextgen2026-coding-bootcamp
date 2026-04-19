# Project Dependencies

This step makes the environment explicit. A research repo is much easier to reproduce when the packages it needs are declared in the project and the resolved versions are saved in a lockfile.

The main distinction here is between what the project needs to run, what you need while developing it, and what should remain machine-local. Keeping those ideas separate makes the environment easier to explain and easier to reproduce later.

In this guide, you will add the libraries used by the example workflow and the notebook tool needed for the session. By the end of this step, `pyproject.toml`, `.venv/`, and `uv.lock` should all reflect the project environment.

## Step 1: Add the runtime dependencies

Run:

```bash
uv add pandas matplotlib
```

These packages are part of the actual workflow, so they belong in the main dependency list. If someone clones the repo and wants to run the project commands, these are the kinds of dependencies they should receive automatically.

## Step 2: Add the development tools

Run:

```bash
uv add --dev ipykernel
```

This tool supports notebooks, but it is not part of the runtime path for the project itself. That is why it belongs in the `dev` group instead of the main dependency list. This is a useful design habit: runtime dependencies support the workflow itself, while development dependencies support how you work on the workflow.

## Step 3: Sync the environment

Run:

```bash
uv sync
```

This creates the local virtual environment and writes the lockfile that captures the resolved versions.

That split is important:

- `.venv/` is the local installation on your machine
- `uv.lock` is the durable record of what was resolved

One is machine-local state. The other is project state.

That is why we want to commit `uv.lock` but not `.venv/`.

Why commit the lockfile:

- it records the exact dependency resolution
- it helps collaborators and future-you recreate the same environment
- it makes changes to the environment visible in Git history

Why not commit `.venv/`:

- it is large and machine-specific
- it contains installed files, not project intent
- it can be recreated from `pyproject.toml` plus `uv.lock`

## Step 4: Look at the updated project file

The relevant parts of `pyproject.toml` should now look like this:

```toml
dependencies = [
    "matplotlib>=3.10.8",
    "pandas>=2.3.3",
]

[dependency-groups]
dev = [
    "ipykernel>=7.2.0",
]
```

At this point, the repo is starting to describe its own environment instead of relying on memory or machine-specific setup.

It helps to think about the files this way:

- `pyproject.toml` is the human-edited statement of intent
- `uv.lock` is the exact solved answer
- `.venv/` is the local installation produced from that answer

When you change dependencies, commit `pyproject.toml` and `uv.lock` together. Do not commit `.venv/`.

## Optional: Alternate package sources

Most Session 1 projects can stop here. If you later need a package from a non-default index or from a direct URL, `uv` can record that source in `pyproject.toml` as well. That is useful, but it is a later concern for most workshop repos, so treat it as background knowledge rather than a required step.

## Resources

- `uv add` and `uv sync`: https://docs.astral.sh/uv/reference/cli/
- uv dependency management: https://docs.astral.sh/uv/concepts/projects/dependencies/
- uv package indexes: https://docs.astral.sh/uv/concepts/indexes/

Next: [Running Python](./05-running-python.md)
