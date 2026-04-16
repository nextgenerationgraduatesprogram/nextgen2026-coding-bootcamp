# Git and Repository Setup

`git` is the version control tool we use to download the repository, track changes, and collaborate on code. We use it because it is the standard tool for software projects and it gives everyone the same way to clone, update, and work with the bootcamp repository.

In this guide, you are configuring Git for your account, creating a folder for your work, cloning the bootcamp repository into it, and opening that repository in VS Code. The goal is to get you into a local copy of the project so you can start working in the same codebase as everyone else.

Run the commands in this file from your Linux shell.
On Windows, that means Ubuntu 24.04 in WSL.

## Reference

- Git: [First-Time Git Setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)

## Step 1: Configure Git identity

Run:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global --list
```

## Step 2: Create a work folder

Run:

```bash
mkdir -p ~/work
cd ~/work
```

Keep the repository under `/home/<username>/...`. Do not clone it into `/mnt/c/...`.

## Step 3: Clone the repository

Run:

```bash
git clone https://github.com/nextgenerationgraduatesprogram/nextgen2026-coding-bootcamp.git
cd nextgen2026-coding-bootcamp
```

If the clone fails because of access, use the GitHub access method your organization has approved and retry. Full GitHub authentication setup is outside this guide.

## Step 4: Open the repository in VS Code

From the repository folder, run:

```bash
code .
```

## Step 5: Validate repository access

Run:

```bash
pwd
git remote -v
git status
```

`pwd` should start with `/home/`.

If the repo path starts with `/mnt/c/`, move back to `~/work`, clone the repo again there, and reopen that copy in VS Code.
