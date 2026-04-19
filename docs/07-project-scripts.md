# Project Scripts

This step adds two small scripts. They are useful because not every Python file in the repo needs to become a project command, but they should still stay thin and depend on the code in `src/` instead of duplicating it.

Scripts are a good place for operational helpers and direct execution demos. They are a bad place for the only copy of important workflow logic. If a script grows logic that other parts of the repo also need, that logic should move into `src/`.

By the end of this step, you should have one script that makes Python's runtime behavior visible and another that reuses the summary logic from the package.

This chapter connects directly back to the workshop goals:

- `src/` should hold the durable implementation
- scripts should act as thin interfaces around that implementation
- students should be able to reason about what Python is actually doing when a file runs

## Step 1: Add a direct-execution demo script

Create `scripts/runtime_demo.py` with this content:

```python
from pathlib import Path
import sys


def main() -> None:
    print(f"__name__ = {__name__}")
    print(f"sys.argv = {sys.argv}")
    print(f"cwd = {Path.cwd()}")
    print(f"results exists? {Path('results').exists()}")


if __name__ == "__main__":
    main()
```

This script is intentionally small. Its job is to make direct script execution visible rather than to hold important workflow logic.

It also makes several useful Python runtime ideas concrete:

- `__name__` shows how Python identifies the module it is running
- `sys.argv` shows the command-line arguments passed to the script
- `Path.cwd()` shows the current working directory inherited from the shell

Under the hood, when you run `python scripts/runtime_demo.py hello world`, Python:

- starts the interpreter
- sets `sys.argv` from the command line
- sets `__name__` to `"__main__"` for that file
- executes the file from top to bottom
- reaches the `if __name__ == "__main__":` guard and calls `main()`

This is a good place to notice the continuity with `hello.py`. In the previous chapter, `hello.py` showed the shape of a clean entry point. Here, `runtime_demo.py` shows the runtime details that sit around that shape.

## Step 2: Add a script that imports from `src/`

Create `scripts/show_summary.py` with this content:

```python
from nextgen2026_coding_bootcamp.viz import make_summary


def main() -> None:
    print(make_summary())


if __name__ == "__main__":
    main()
```

This file matters because it shows the intended design: the script imports reusable code from the package instead of rewriting the same summary logic.

That distinction is what keeps `scripts/` from turning into a second application layer. The script controls a small task, but the real summary logic still has one home in `src/`.

In workshop terms, this script is demonstrating a healthy dependency direction:

- `scripts/` may depend on `src/`
- `src/` should not depend on one-off scripts

That direction keeps the core implementation reusable.

## Step 3: Run both scripts

Run:

```bash
uv run python scripts/runtime_demo.py hello world
uv run python scripts/show_summary.py
```

The first script shows you what direct execution looks like. The second script shows how small operational files can reuse the package code cleanly.

This is an important distinction for the workshop:

- a project command such as `uv run viz` is part of the official interface
- a script in `scripts/` may be useful, but it is usually more local and task-specific

## Resources

- `uv run`: https://docs.astral.sh/uv/reference/cli/
- Python `__main__`: https://docs.python.org/3/library/__main__.html
- Python command-line usage: https://docs.python.org/3/using/cmdline.html

Next: [Notebooks](./08-project-notebooks.md)
