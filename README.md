# NextGen Coding Bootcamp

This four-session boot camp introduces the core workflow skills needed to run a computational research project from setup to reproducible handoff. We will learn how to structure a research repository, run analyses through scripts and configuration, capture logs and outputs, use coding tools such as Codex to accelerate development, and produce work that another researcher can rerun, review, and extend.

## Before Session 1

- [ ] Windows only: install WSL and Ubuntu 24.04
- [ ] Install VS Code
- [ ] Install the VS Code `WSL` and `Python` extensions
- [ ] In Linux or WSL, install `git`, `python3`, and `uv`
- [ ] Set your Git name and email
- [ ] Clone this repository into `~/work` and open it in VS Code

See [Development Environment Setup](./docs/00-development-environment.md) for the full setup steps and checks.

## Getting Started

Follow these steps when you begin Session 1.

### Step 1: Clone the repository and open it

Run:

```bash
mkdir -p ~/work
cd ~/work
git clone https://github.com/nextgenerationgraduatesprogram/nextgen2026-coding-bootcamp.git
cd nextgen2026-coding-bootcamp
code .
```

When you first clone the repository, you will land on `main`. Stay on `main` at first so you can read the instructions and understand how the repository is organized. Do not do your session work on `main`.

### Step 2: List the available branches

Run:

```bash
git fetch origin --prune
git branch -a
```

`git branch -a` shows both your local branches and the shared branches from GitHub under `remotes/origin/...`.

For Session 1, you should expect to see these shared branches:

- `remotes/origin/main`
- `remotes/origin/starter/session-<n>`
- `remotes/origin/solutions/session-<n>`

### Step 3: Understand what each branch is for

Each branch in this repository has one job.

| Branch | Purpose | Work here? |
| --- | --- | --- |
| `main` | Orientation, setup instructions, and repository overview | No |
| `starter/session-<n>` | Clean starting point for a session | No |
| `<your-name>/session-<n>` | Your personal working branch for that session | Yes |
| `solutions/session-<n>` | Completed reference solution | No |

The important rule is simple: only edit and commit on your own branch. Do not work on `main`, `starter/...`, or `solutions/...`.

This keeps the shared branches clean, makes it obvious where your work lives, and gives you a simple recovery path if you need to start again.

### Step 4: Create your own Session 1 branch

Create your own working branch from the Session 1 starter branch.

Replace `<your-name>` with a short lowercase name such as `sam` or `sam-lee`.

```bash
git fetch origin --prune
git switch -c <your-name>/session-<n> origin/starter/session-<n>
git branch --show-current
git status
```

`git switch -c` creates a new local branch for you based on `origin/starter/session-<n>`.

`git branch --show-current` should show `<your-name>/session-<n>`.

`git status` should show that you are on your own branch and that your working tree is clean.

### Step 5: Do all of your Session 1 work on that branch

Once you have created `<your-name>/session-<n>`, stay on that branch while you work. Make your edits there. Make your commits there.

If you are ever unsure where you are working, run:

```bash
git branch --show-current
```

If you later set up a fork to submit your work for review, `origin` will point to your fork and the workshop repository will become `upstream`. From that point on, start future sessions from `upstream/starter/session-<n>` instead of `origin/starter/session-<n>`.

## Use the Solution Branch

The solution branch is for reference only. You can inspect the completed state like this:

```bash
git switch solutions/session-<n>
```

When you are ready to continue your own work, switch back to your branch:

```bash
git switch <your-name>/session-<n>
```

Always switch back to your own branch before editing files or making commits.

## Start Over If Needed

If your working branch gets messy, you can delete it and recreate it from the clean starter branch:

```bash
git switch main
git branch -D <your-name>/session-<n>
git fetch origin --prune
git switch -c <your-name>/session-<n> origin/starter/session-<n>
```

This reset works cleanly because `starter/session-<n>` stays untouched.

If you have already set up a fork for review, replace `origin` with `upstream` in those commands.

## Optional: Submit Your Work for Review

The main workshop workflow is local-first. If you want feedback on your session work, you can submit your existing session branch as a pull request from your own fork.

A fork is a separate GitHub repository under your account. It is not the same thing as a branch.

The optional review flow is:

1. Fork this repository on GitHub.
2. Reconfigure your local remotes so `origin` points to your fork and `upstream` points to the workshop repository.
3. Push `<your-name>/session-<n>` to your fork.
4. Open a pull request from your forked branch into `starter/session-<n>` for review.

See [Submit Work for Review](./docs/05-submit-work-for-review.md) for the full step-by-step workflow.

## Learning Objectives

By the end of the boot camp, we will be able to:

- set up a clean research code repository with a sensible project structure, isolated environment, and version control
- run analyses from scripts and configuration files rather than relying on notebook cell order
- capture logs, outputs, and artifacts in a way that supports reproducibility and debugging
- write and run basic tests to make research code safer to change
- use AI coding tools productively through spec-driven development, documentation, and review
- package a small research project so that another person can clone it, run it, and understand how results were produced
