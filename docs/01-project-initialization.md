# Project Initialization

This step creates the basic project scaffold. We start here because the rest of the session depends on one choice: the repo should behave like an application you can run while still keeping its code importable from other places.

That is why this guide uses `uv init --package`. A research repo often sits between two extremes. It is usually more structured than a pile of loose scripts, but it is not necessarily trying to become a reusable library on day one. The packaged-project layout is a good middle path because it gives you one project root, one package directory, and one place to define commands and dependencies.

The scaffold is not the finished repo, but it gives later steps something coherent to attach to.

## Step 1: Make sure you are on the starter branch

Run:

```bash
git switch starter/session-1
```

## Step 2: Initialize the project

Run:

```bash
uv init --package --python 3.10 --name nextgen2026-coding-bootcamp
```

This command tells `uv` to initialize a packaged project in the current directory and to target Python 3.10.

The three key ideas in that command are:

- `--package`: create a package-shaped repo instead of a single loose script
- `--python 3.10`: declare which Python version the repo is meant to use
- `--name ...`: define the project name that will appear in packaging metadata

## Step 3: Inspect the generated files

After the command finishes, look at these three parts of the scaffold:

- `.python-version`
- `pyproject.toml`
- `src/nextgen2026_coding_bootcamp/`

`.python-version` pins the local Python version. This reduces ambiguity about which interpreter the repo is supposed to use.

`src/nextgen2026_coding_bootcamp/` is where importable project code will live. The design decision here is that the repo root is the project, while `src/` is only for importable code. That makes later steps easier to reason about. Code in `src/` can be reused by scripts and notebooks. Everything else in the repo can then stay focused on interface or workflow rather than becoming a second home for the same logic.

## Step 4: Read the generated `pyproject.toml`

Open `pyproject.toml`. The exact generated contents may vary slightly across `uv` versions, but the important sections are the same.

At a high level:

- `[project]` describes the package itself
- `name` is the installable project name
- `version` is the project version
- `description` and `readme` describe the project for humans and packaging tools
- `requires-python` declares the supported Python version range
- `dependencies` will later list runtime packages the workflow needs
- `[build-system]` tells packaging tools how to build the project

That split is useful because `pyproject.toml` plays two roles at once:

- it is human-facing project configuration
- it is machine-facing packaging metadata

It is worth pausing here because `pyproject.toml` becomes one of the most important files in the repo. Later, when you add dependencies, console entry points, or build settings, they all attach to this file instead of being scattered across ad hoc shell commands.

One good mental model is:

- `.python-version` answers "which Python do we want?"
- `pyproject.toml` answers "what is this project and how should tools treat it?"
- `src/` answers "where does the importable code live?"

At this point, you do not need to edit much yet. The important thing is to understand what the scaffold is giving you and why the session uses this layout instead of loose standalone files.

## Resources

- `uv init`: https://docs.astral.sh/uv/reference/cli/
- uv projects guide: https://docs.astral.sh/uv/guides/projects/
- `pyproject.toml` specification background: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/

Next: [Git Version Control](./02-project-version-control.md)
