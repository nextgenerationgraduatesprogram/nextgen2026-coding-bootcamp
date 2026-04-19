# Project Source Code

This step adds the reusable project logic. Up to this point you have created the scaffold, the directory structure, the example data, and the environment. Now the repo starts to contain the actual workflow logic.

The main design decision in this step is that durable logic belongs in `src/`. Scripts and notebooks are useful interfaces, but they should not become the only place where important logic exists. Putting the core code in `src/` gives the repo one canonical implementation that multiple interfaces can reuse.

By the end of this step, the repo should expose two project commands: `hello` and `viz`.

## Step 1: Replace the generated `hello.py`

Open the generated file `src/nextgen2026_coding_bootcamp/hello.py` and replace its contents with:

```python
def main() -> None:
    print("Hello from nextgen2026-coding-bootcamp!")


if __name__ == "__main__":
    main()
```

This file is intentionally simple. It gives you the smallest possible example of a project command backed by package code and a good place to slow down and look at what Python is doing under the hood.

When Python reads this file, it executes it from top to bottom:

- it defines the function `main`
- it reaches the `if __name__ == "__main__":` block
- if the file is being run as the entry script, that condition is true and `main()` is called
- if the file is being imported from somewhere else, that condition is false and the function is merely made available

That `__name__` variable is one of Python's "dunder" names, short for double-underscore names. They carry special meaning in the runtime. Here, `__name__` tells the file whether it is being run directly or imported as a module.

Why use `main()` instead of just writing `print(...)` at the top level?

- it makes the entry behavior explicit
- it prevents work from happening automatically on import
- it gives you a named function that other code can call later

We are not using `sys.argv` or the working directory in `hello.py` yet on purpose. `hello.py` is teaching program shape, not program complexity. The next step and the scripts chapter will make runtime details such as arguments, current working directory, and `__name__` more visible.

## Step 2: Add the main example workflow

Create `src/nextgen2026_coding_bootcamp/viz.py` with this content:

```python
from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "measurements.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
SUMMARY_PATH = RESULTS_DIR / "summary_by_group.csv"
FIGURE_PATH = RESULTS_DIR / "mean_by_group.png"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["group"] = df["group"].astype(str).str.strip().str.upper()
    df["reading"] = pd.to_numeric(df["reading"], errors="coerce")
    return df.dropna(subset=["group", "reading"])


def make_summary() -> pd.DataFrame:
    df = load_data()
    return (
        df.groupby("group", as_index=False)
        .agg(mean_reading=("reading", "mean"), n=("reading", "size"))
        .sort_values("group")
    )


def save_plot(summary: pd.DataFrame) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    ax = summary.plot(kind="bar", x="group", y="mean_reading", legend=False)
    ax.set_ylabel("Mean reading")
    ax.set_title("Mean reading by group")

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(FIGURE_PATH, dpi=150)
    plt.close(fig)


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    summary = make_summary()
    summary.to_csv(SUMMARY_PATH, index=False)
    save_plot(summary)

    print("Wrote results/summary_by_group.csv")
    print("Wrote results/mean_by_group.png")


if __name__ == "__main__":
    main()
```

This file does the real work of the session. It reads the sample CSV, cleans the input values, groups the data, writes a summary table, and saves a figure.

This is where the earlier steps come together:

- the directory structure gives the workflow a predictable place to read input and write output
- the dependency step made `pandas` and `matplotlib` available
- the package scaffold gives this logic an importable home in `src/`
- the `main()` pattern gives the repo a clean entry point

Several design decisions are packed into this example:

- `PROJECT_ROOT` is derived from the module path so the workflow can find `data/raw/` and `results/` relative to the repo instead of relying on a fragile working-directory assumption
- `load_data()`, `make_summary()`, and `save_plot()` split the workflow into small named steps, which makes the code easier to reuse and easier to inspect from scripts or notebooks
- `matplotlib.use("Agg")` tells Matplotlib to render without needing a display, which helps in headless environments such as servers or CI
- `RESULTS_DIR.mkdir(exist_ok=True)` makes the write step explicit instead of assuming the output directory already exists

The broader workshop lesson is that `viz.py` is the durable implementation of the workflow. That is why it belongs in `src/` rather than inside a notebook or an ad hoc script.

## Step 3: Expose the project commands

Update the `[project.scripts]` section in `pyproject.toml` so it looks like this:

```toml
[project.scripts]
hello = "nextgen2026_coding_bootcamp.hello:main"
viz = "nextgen2026_coding_bootcamp.viz:main"
```

This is how the repo defines the stable commands that `uv run` will expose.

That design choice is important. Instead of asking users to remember `python -m ...` or a file path under `src/`, the project defines one stable command surface. That makes the workflow easier to teach and easier to reuse.

Under the hood, this means the project is declaring: "when someone runs `hello`, call `main()` from this module." That is more stable than asking a user to know where a source file lives inside the repo.

## Step 4: Run the new commands

Run:

```bash
uv run hello
uv run viz
```

At this point, the repo is doing real work. It is reading data, using project code from `src/`, and writing outputs into `results/`.

That is one of the main Session 1 goals: the repo should have one clear command path that leads from declared environment to reusable code to visible output.

## Resources

- `uv run` and project commands: https://docs.astral.sh/uv/reference/cli/
- uv projects guide: https://docs.astral.sh/uv/guides/projects/
- uv packaging guide: https://docs.astral.sh/uv/guides/package/
- Python `__main__`: https://docs.python.org/3/library/__main__.html

Next: [Project Scripts](./07-project-scripts.md)
