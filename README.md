# Workshop Projects — Session 3

## What this workshop is

In this workshop, you will work in a small group on one bounded coding task inside a scaffolded repository. Each project uses the same overall workflow shape — `fetch`, `prepare`, `analyze`, and `report` — but applies it to a different type of problem. You will use AI coding tools as part of your workflow to understand the task, write a specification, implement a bounded change, test the result, and prepare a merge request.

The goal is not to build a complete project from scratch. The goal is to make one meaningful change to an existing workflow and review that change properly.

## Project options

You will work on one of three project branches.

- **Image processing**: Use a small public image dataset to generate a new analysis artifact and include it in the report output.
- **Time series**: Use a small public time-series dataset to generate a new summary artifact and include it in the report output.
- **Semantic analysis**: Use a small public text dataset and the OpenAI API to perform semantic analysis, and include the results in the report output.

Each project follows the same structure, but the data and implementation details differ.

## Getting started

First, create your own fork of this repository on GitHub. A fork is a Git hosting step, not a plain `git` step, so you cannot create one with `git` alone. If you already use GitHub CLI for this, that is also fine.

Then clone your fork of the repository and move into it.

```bash
git clone <your-fork-url>
cd <repo-name>
```

Then fetch the remote branches and create your own working branch from the project branch for your group, chose `<problem>` from one of `image-analysis`, `timeseries-analysis`, and `text-analysis`.

```bash
git fetch origin
git branch -r
git switch -c <your-name>/session-4-<problem> origin/starter/session-4-<problem>
git push -u origin <your-name>/session-4-<problem>
```

You should now be working on your own branch, based on the problem branch for your project.

## What to read next

Once you are on the correct problem branch, read these files in order:

1. `docs/01-project-brief.md`
2. `docs/02-project-workflow.md`
3. `docs/03-agentic-workflow.md`
4. `docs/04-validation-and-merge.md`

The project brief and repo workflow docs are branch-specific. The AI workflow and validation docs are shared.

## Submission

At the end of the workshop, commit your changes, push your branch, and open a merge request with:

- a short description of what you changed
- what checks you ran
- anything still incomplete or uncertain
