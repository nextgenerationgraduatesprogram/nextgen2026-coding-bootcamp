# Running Python

This step is a small but useful verification step. You have already declared the environment, and now you want to confirm that Python is actually running through that project environment.

The design decision here is to use the project as the entry point into Python instead of relying on a shell session, a globally activated environment, or whichever interpreter happens to be first on the machine. That keeps the workflow more predictable.

In this guide, you are not changing the repo structure. You are proving that the environment you just created is real and usable. By the end of this step, you should be able to launch Python through `uv` and import the packages you added.

## Step 1: Start Python through the project

Run:

```bash
uv run python
```

This launches the interpreter through the environment managed by the project rather than whichever Python happens to be first on your machine.

## Step 2: Import one package and verify both dependencies

Inside the interpreter, run:

```python
from importlib.metadata import version
import sys
import pandas

sys.executable
pandas.__version__
version("matplotlib")
```

Then leave the interpreter with `exit()` or `Ctrl-D`.

`sys.executable` shows which Python interpreter is actually running. That is a useful under-the-hood confirmation. It helps make the session's main point concrete: `uv run python` is not "just Python." It is Python launched through the project environment.

The point of this step is not just to see version numbers. The point is to confirm that the project controls the environment it is running in. Later, when you run project commands, scripts, or notebooks, you want that same environment discipline to keep applying.

## Resources

- `uv run`: https://docs.astral.sh/uv/reference/cli/
- uv projects guide: https://docs.astral.sh/uv/guides/projects/

Next: [Project Source Code](./06-project-source.md)
