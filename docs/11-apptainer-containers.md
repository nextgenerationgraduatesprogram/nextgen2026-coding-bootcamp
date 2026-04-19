# Appendix: Apptainer

This appendix is optional as well. It is useful when you need a portable runtime in an environment that expects Apptainer.

The same idea from the Docker appendix still applies here: container work comes after the project path is already clear. Apptainer is packaging an existing workflow, not solving the earlier design problems for you.

The goal here is modest. You should be able to build a SIF either from the local Docker image or directly from the repository definition file, then run that image through the same project command path.

## Step 1: Build from the local Docker image

If you already built the Docker image, run:

```bash
apptainer build nextgen2026-coding-bootcamp-session-1.sif docker-daemon://nextgen2026-coding-bootcamp-session-1:latest
apptainer run nextgen2026-coding-bootcamp-session-1.sif
```

## Step 2: Or build directly from the definition file

Run:

```bash
apptainer build --fakeroot nextgen2026-coding-bootcamp-session-1.sif apptainer.def
apptainer run nextgen2026-coding-bootcamp-session-1.sif
```

Just like the Docker appendix, this is packaging the workflow after the project path is already clear and reproducible. The container layer comes after the repo design, not before it.

The short takeaway is:

- build the repo workflow first
- containerize that finished workflow second
- keep the same command path inside and outside the container

## Resources

- Apptainer build guide: https://apptainer.org/docs/user/main/build_a_container.html
- `apptainer build`: https://apptainer.org/docs/user/main/cli/apptainer_build.html
- `apptainer run`: https://apptainer.org/docs/user/main/cli/apptainer_run.html

Next: [Session Overview](./session-overview.md)
