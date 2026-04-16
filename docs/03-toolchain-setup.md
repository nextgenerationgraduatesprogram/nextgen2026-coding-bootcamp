# Toolchain Setup

`uv` is the Python tool we use to manage Python installations, environments, and project dependencies. We use it because it is fast, simple, and gives the bootcamp a consistent Python workflow instead of having different learners using different setup tools.

In this guide, you are installing the core command-line tools needed for Python development on this machine. The goal is to make sure the base tooling is ready before you start working with any specific project repository.

Run the commands in this file from your Linux shell.
On Windows, that means Ubuntu 24.04 in WSL.

## Reference

- Astral: [Installing uv](https://docs.astral.sh/uv/getting-started/installation/)

## Step 1: Install core system packages

In your Linux shell, run:

```bash
sudo apt update
sudo apt install -y git curl ca-certificates build-essential python3 python3-venv
```

If you are on macOS or another Linux distribution, install the equivalent packages and continue.

## Step 2: Install `uv`

Run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
```

Then run:

```bash
uv --version
```

If `uv` is not found, run `source "$HOME/.local/bin/env"` again or open a new Linux shell and retry.

## Step 3: Validate the toolchain

Run:

```bash
git --version
uv --version
python3 --version
```

If `python3` is not found, run this in the Linux shell:

```bash
sudo apt update
sudo apt install -y python3 python3-venv
python3 --version
```

Continue to [Git and Repository Setup](./04-git-and-repo-setup.md).
