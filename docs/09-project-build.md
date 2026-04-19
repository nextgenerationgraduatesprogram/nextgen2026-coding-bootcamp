# Build

This final core step is short, but it is worth understanding clearly. The point is not to make build the center of the research workflow. The point is to show that the project now has a coherent package shape.

That design decision is worth making explicit. Session 1 is mainly about building a maintainable research repo, not about publishing to PyPI. Even so, a repo that can build cleanly usually has a clearer project definition than one that only works through ad hoc local commands.

By the end of this step, the repo should be able to produce build artifacts in `dist/`, which is a useful sign that the package structure is consistent.

In this context, "building" means turning the source tree into standard Python distribution artifacts that another tool or machine could install. You are asking the packaging system to take the project metadata, package layout, and source files and produce a portable representation of the project.

## Step 1: Build the project

Run:

```bash
uv build
```

This writes a source distribution and a wheel into `dist/`.

Those two artifacts answer slightly different needs:

- the source distribution is a packaged snapshot of the source code and project metadata
- the wheel is a ready-to-install built package format

You do not need to memorize the formats yet. The important point is that the project can now describe itself well enough for standard packaging tools to assemble it.

## Step 2: Understand why this works

Build works here because the repo now has:

- a package directory in `src/`
- a project configuration file in `pyproject.toml`
- declared dependencies
- defined project commands

You do not need to run `uv build` every time you change the code. It is simply a clean way to confirm that the project shape supports packaging as well as local development.

For a research repo, this is useful even if you never publish anything publicly. A clean build is evidence that:

- the package layout is coherent
- the metadata is in the right place
- the project can travel more easily between machines
- you are relying less on "works on my laptop" assumptions

In other words, build is not the workflow, but it is a valuable structural confirmation of the workflow.

Another useful mental model is:

- `uv run ...` confirms that the project works from the repo
- `uv build` confirms that the project is shaped well enough to be packaged

From here, you can stop at the end of the core Session 1 path or continue into the optional container appendices.

## Resources

- `uv build`: https://docs.astral.sh/uv/reference/cli/
- uv packaging guide: https://docs.astral.sh/uv/guides/package/

Next: [Appendix: Docker](./10-docker-containers.md)
