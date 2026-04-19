# Project Demonstration

This opening step shows you the finished Session 1 repo before you build it yourself. The goal is to make the destination concrete before you start creating the pieces one by one.

Session 1 is trying to move students toward a repo that is small, understandable, and runnable by someone other than its author. By the end of the session, a student should be able to:

- explain what the official command path for the project is
- describe why reusable code lives in `src/` instead of being scattered through scripts and notebooks
- distinguish between raw inputs in `data/raw/` and generated outputs in `results/`
- run the workflow and inspect a concrete output
- understand that a research repo is not just code, but code plus environment plus file layout plus repeatable commands

Seeing the finished state first makes the later edits easier to reason about. Instead of copying steps blindly, you already know what the repo is trying to become.

## Step 1: Switch to the finished branch

Run:

```bash
git switch solutions/session-1
```

This branch already contains the completed Session 1 work. Think of it as the reference state you are trying to understand and then recreate.

## Step 2: Run the finished project commands

Run:

```bash
uv run hello
uv run viz
```

`uv run hello` is the smallest example of the official project command path. It proves that the repo exposes a stable command instead of asking someone to remember a file path such as `python src/...`.

`uv run viz` is closer to a real research workflow. It reads the sample data, performs a small transformation, and writes outputs into `results/`. That is an important session outcome: the repo should have a command that does real work and leaves behind inspectable artifacts.

## Step 3: Inspect one of the generated outputs

Run:

```bash
sed -n '1,20p' results/summary_by_group.csv
```

This lets you see the kind of file the workflow produces. You can also look at `results/mean_by_group.png` in your file browser or editor.

The important idea here is that the repo does not stop at source code. It produces an output in a predictable location, which is part of what makes the workflow understandable to another researcher. A good project repo tells a story:

- what went in
- what command was run
- what came out

## Step 4: Look at the repo shape

At this point, look at the top-level folders and notice the division of work. `src/` holds reusable code, `scripts/` holds thin utilities, `notebooks/` is for exploration, `data/raw/` holds the input data, and `results/` holds generated outputs.

That division is deliberate. One of the main learning outcomes of this session is that maintainability comes from separation of concerns:

- package code should have one clear home
- operational helpers should stay thin
- exploratory work should not become the only copy of the workflow
- inputs and outputs should not be mixed together

The repo structure is doing communication work here. It is telling the next reader where to look and what each part of the project is for.

## Step 5: Return to the starter branch

When you are ready to build the repo yourself, switch back:

```bash
git switch starter/session-1
```

From here on, assume you will be creating directories and writing file contents yourself as the numbered docs instruct.

## Resources

- `git switch`: https://git-scm.com/docs/git-switch.html
- uv projects guide: https://docs.astral.sh/uv/guides/projects/
- `uv run`: https://docs.astral.sh/uv/reference/cli/

Next: [Project Initialization](./01-project-initialization.md)
