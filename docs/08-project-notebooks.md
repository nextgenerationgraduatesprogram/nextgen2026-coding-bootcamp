# Notebooks

This step adds a notebook to the repo, but the main point is not the notebook interface itself. The main point is that the notebook should use project code rather than becoming the only place where the logic exists.

Notebooks are very good at exploration, inspection, and narrative work, but they are not a great place to hide the only copy of a reusable workflow. In this session they stay in a supporting role: useful, but secondary to the package code in `src/`.

In this guide, you will start Jupyter from the project environment and create a very small notebook that imports `make_summary()` from the package. By the end of this step, the notebook should be acting as a client of the project instead of competing with it.

## Step 1: Start Jupyter from the project root

Run:

```bash
uv run --with jupyterlab jupyter lab
```

This starts JupyterLab using the environment managed by `uv`. The project already has `ipykernel` in the `dev` group for kernel support, and `--with jupyterlab` supplies the notebook interface at run time.

The design choice here is the same one you used with `uv run python`: the project launches the tool through the managed environment instead of relying on a separate global installation.

## Step 2: Create the notebook

Create `notebooks/example.ipynb` and add a markdown cell with:

```markdown
# Session 1 notebook demo

This notebook is a client of the project package.
```

Then add a code cell with:

```python
from nextgen2026_coding_bootcamp.viz import make_summary

summary = make_summary()
summary
```

Add one more code cell with:

```python
summary.assign(mean_reading=summary["mean_reading"].round(2))
```

This is enough to show the main idea. The notebook is using project code from `src/` instead of copying the summary logic into the notebook.

That separation is useful for maintenance. If the summary logic changes later, you want to change it once in `src/` and then let the notebook pick up the new behavior through an import.

## Step 3: Optionally create a named kernel

If you want a named kernel on your own machine, run:

```bash
uv run python -m ipykernel install --user --name nextgen2026-coding-bootcamp --display-name "nextgen2026-coding-bootcamp"
```

That command is optional for the session, but it is useful if you want a cleaner long-lived notebook setup.

## Resources

- Project Jupyter docs: https://docs.jupyter.org/
- What Jupyter is for: https://docs.jupyter.org/en/latest/what_is_jupyter.html
- Installing kernels: https://docs.jupyter.org/en/latest/install/kernels.html
- `uv run`: https://docs.astral.sh/uv/reference/cli/

Next: [Build](./09-project-build.md)
