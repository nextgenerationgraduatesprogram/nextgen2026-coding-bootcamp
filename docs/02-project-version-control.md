# Git Version Control

This step is about keeping the repo state visible while you build it. We use Git from the start so that you can see what changed, keep machine-local files out of version control, and save meaningful milestones as you go.

A maintainable repo needs visible history as much as good file layout. Git gives you that history. Without it, a workshop repo quickly turns into a sequence of edits with no checkpoints.

In this guide, the repository already exists, so you do not need to spend time creating a new Git repo. By the end of this step, you should know how to inspect the repo state, create a branch for your work, understand what Git should and should not track, and safely undo a local change.

Reference

Git Book: https://git-scm.com/book/en/v2

## Step 1: Inspect the current repo state

Run:

```bash
git status
```

This is the command you should use repeatedly while working through the session. It tells you which files changed, which files are new, and which files are ready to commit.

The deeper point is that Git gives you feedback while you work. Instead of hoping you remember what changed, you can ask the repo directly.

## Step 2: Create a working branch if you want one

Run:

```bash
git switch -c my-session-1
```

You do not have to use that exact branch name, but creating a branch gives you a clean place to make your changes. The reason to branch is not ceremony. It is to make your work easier to isolate, compare, and reset if needed.

## Step 3: Understand what `.gitignore` is doing

Open `.gitignore` and look for examples such as `.venv/`, `dist/`, and the `results/` rules.

`.gitignore` is not retroactive magic. It is simply a list of path patterns that tells Git, "do not bother showing these untracked files to me by default." That matters because a real project produces a lot of noise:

- virtual environments
- build artifacts
- editor settings
- caches
- generated outputs

Most of those files are not the project. They are byproducts of working on the project.

As a rule of thumb, include files that describe the project and exclude files that merely happen to exist on one machine.

Usually include:

- source code
- docs
- configuration
- small pedagogically useful example data
- lockfiles such as `uv.lock`
- placeholder files such as `results/.gitkeep` when you want Git to preserve an otherwise empty directory

Usually exclude:

- `.venv/` because it is a machine-local installation
- `dist/` and other build artifacts because they can be recreated
- caches and editor state because they are local noise
- generated results because they are outputs of the workflow, not the workflow definition itself

`uv.lock` is the important exception to the "generated files are local" rule. Even though it is generated, it records the exact resolved environment used by the project. That makes it part of the project state and therefore worth committing.

## Step 4: Practice making a change and restoring it

A useful Git skill is not only saving work, but safely undoing local edits when you change your mind.

Try a small reversible example with a tracked file:

```bash
printf "\nTemporary note for Git practice.\n" >> README.md
git diff README.md
git restore README.md
git status
```

What is happening here:

- the first command changes a tracked file
- `git diff` shows the exact line you added
- `git restore README.md` discards that uncommitted change and returns the file to the last committed state
- the final `git status` confirms that the temporary edit is gone

If you prefer, you can make the change manually in your editor instead of using `printf`. The important part is learning the restore cycle.

## Step 5: Save your work as you complete steps

When you finish a meaningful part of the session, use:

```bash
git add <files>
git commit -m "build: describe the step you completed"
```

You do not need to push anywhere for Session 1. The goal here is to keep the repo state understandable and recoverable while you work.

One good habit is to commit related files together. For example, if you add dependencies, commit both `pyproject.toml` and `uv.lock` in the same snapshot. If you change source code and docs together, commit both together.

## Resources

- Git basics: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository
- `git status`: https://git-scm.com/docs/git-status.html
- `git switch`: https://git-scm.com/docs/git-switch.html
- `git restore`: https://git-scm.com/docs/git-restore
- `.gitignore`: https://git-scm.com/docs/gitignore

Next: [Project Structure](./03-project-structure.md)
