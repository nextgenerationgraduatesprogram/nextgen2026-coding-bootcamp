# Session Overview

This guide walks you through building the Session 1 repository from the sparse starter branch to the finished working state. The through-line is simple: one clear command path, reusable code in `src/`, thin scripts, and notebooks that import project code instead of becoming the project.

Research repos often start as a few commands and a few files, then become hard to maintain because the logic, environment, and workflow are no longer obvious. Session 1 builds the repo in layers so those decisions stay visible.

Assume that on the starter branch you will create the directories and files yourself as you work through the numbered docs. Some files begin as generated scaffolding, but the workshop expects you to type, inspect, and edit the contents so the repo shape makes sense rather than feeling magical.

Before you begin, make sure you have `git` and `uv` installed.

## Step 1: Use the finished branch as a reference

Open a terminal in the repository and run:

```bash
git switch solutions/session-1
```

This branch is useful because it gives you the destination. You are not expected to build from memory. Being able to compare your work to a finished version makes the design of each step easier to understand.

## Step 2: Do the real work on the starter branch

When you are ready to build the repo yourself, switch back:

```bash
git switch starter/session-1
```

This is the branch you should use while following the numbered docs below.

## Step 3: Work through the Session 1 docs in order

1. `docs/00-project-demo.md`
2. `docs/01-project-initialization.md`
3. `docs/02-project-version-control.md`
4. `docs/03-project-structure.md`
5. `docs/04-project-dependencies.md`
6. `docs/05-running-python.md`
7. `docs/06-project-source.md`
8. `docs/07-project-scripts.md`
9. `docs/08-project-notebooks.md`
10. `docs/09-project-build.md`

The last two docs are optional appendices:

- `docs/10-docker-containers.md`
- `docs/11-apptainer-containers.md`

Those appendices come last on purpose. Containers are useful, but they only help once the repo itself already has a clear workflow.

## Resources

- Git installation: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- uv installation: https://docs.astral.sh/uv/getting-started/installation/
- uv first steps: https://docs.astral.sh/uv/getting-started/first-steps/

Next: [Project Demonstration](./00-project-demo.md)
