# syntax=docker/dockerfile:1.7

FROM python:3.10-slim

# install uv from Astral's published image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# nice-to-have for containers
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_DEV=1

# install dependencies first for better layer caching
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# now add the project itself
COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# pick one stable entrypoint
CMD ["uv", "run", "hello"]