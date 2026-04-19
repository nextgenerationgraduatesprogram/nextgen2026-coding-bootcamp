# Appendix: Docker

This appendix is optional. Use it only after the core Session 1 workflow is already working locally.

Docker is not a substitute for a good repo structure. It is a way to package an already coherent workflow so that it runs in a controlled environment somewhere else.

The repo already contains a `dockerfile`, so Docker can package the same command path you have been using throughout the session. The point of this appendix is simply to show that the project can travel into a container without inventing a second workflow.

## Step 1: Build the Docker image

Run:

```bash
docker build -t nextgen2026-coding-bootcamp-session-1:latest -f dockerfile .
```

## Step 2: Run the image

Run:

```bash
docker run --rm -it nextgen2026-coding-bootcamp-session-1:latest
```

The container defaults to `uv run hello`. That matters because it shows that the container is wrapping the same stable project command path rather than inventing a separate interface.

If you want a one-line summary of the appendix, it is this:

- the repo works locally first
- Docker packages that existing workflow
- the container still runs the same command surface

## Resources

- Docker build reference: https://docs.docker.com/engine/reference/commandline/build
- Docker run reference: https://docs.docker.com/engine/containers/run/

Next: [Appendix: Apptainer](./11-apptainer-containers.md)
