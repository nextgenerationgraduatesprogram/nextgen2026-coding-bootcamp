# Project Structure

This step creates the top-level directories used by the project. We do this early because a research repo becomes much easier to read when each kind of work has a clear home.

The key idea here is separation of roles. If code, exploratory work, raw inputs, and generated outputs all end up mixed together, the repo becomes harder to read and harder to trust.

In this guide, you are creating places for scripts, notebooks, raw data, and generated results. You will also add a small example dataset so the later workflow has something concrete to run on. By the end of this step, the repo should have the main folders that Session 1 relies on.

One of the big workshop objectives is to help students answer two questions quickly:

- where should this file go?
- should this file be treated as source, input, output, or local clutter?

A good repo structure answers those questions before a mess has time to form.

## Step 1: Create the working directories

Run:

```bash
mkdir -p scripts notebooks data/raw results
touch results/.gitkeep
```

`src/` already exists because the project scaffold created it in the previous step. The new folders separate the other kinds of work that the repo will hold.

The `touch` command creates an empty placeholder file. Git does not track empty directories by themselves, so `results/.gitkeep` gives Git something tiny to remember. Later, the actual files produced in `results/` will stay ignored, but the directory itself will still be part of the project shape.

## Step 2: Add the example dataset

Create `data/raw/measurements.csv` with this content:

```csv
sample_id,group,reading
1,a,10.2
2,A,11.1
3,a,
4,b,9.8
5,B,10.4
6,b,10.1
7,c,12.2
8,C,11.9
9,c,13.0
```

This file is deliberately small. It is enough to show the workflow without hiding the structure under too much data.

There is also a design choice in committing this file to Git for the workshop. In a real project, you would not necessarily commit all raw data, especially if it is large or sensitive. Here, the CSV is tiny and pedagogically useful, so committing it makes the lesson simpler and more reproducible.

## Step 3: Understand what each directory is for

`src/` is for reusable project code. `scripts/` is for thin operational files and one-off helpers. `notebooks/` is for exploration that imports project code. `data/raw/` holds input data. `results/` holds generated outputs.

That split matters because each directory answers a different question:

- `src/`: what is the durable implementation?
- `scripts/`: what are the thin helper interfaces around that implementation?
- `notebooks/`: where can someone explore without redefining the project?
- `data/raw/`: what did the workflow start with?
- `results/`: what did the workflow create?

The split between `data/raw/` and `results/` is especially important. Inputs and outputs should not be mixed together, because that makes it harder to tell what the workflow started with and what it created.

This is one of the deeper lessons of the session: repo structure is not decoration. It is part of how a project communicates meaning.

## Resources

- Ubuntu command line basics: https://documentation.ubuntu.com/desktop/en/latest/tutorial/the-linux-command-line-for-beginners/
- The Turing Way on project repositories: https://book.the-turing-way.org/project-design/pd-overview/project-repo/project-repo-advanced

Next: [Project Dependencies](./04-project-dependencies.md)
