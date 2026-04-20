# Submit Work for Review

This guide is optional. Use it when you want to submit your session work for instructor review on GitHub.

The core workshop workflow stays the same:

- clone the workshop repository
- read instructions on `main`
- create your own branch from the starter branch
- do all work on your own branch

This guide adds one more step after that: push your existing session branch to your own fork and open a pull request.

## Before you start

Use this guide after you already have a local working branch such as `alice/session-1`.

Check your current branch:

```bash
git branch --show-current
git status
```

Your work should be on your own session branch, not on `main`, `starter/...`, or `solutions/...`.

Commit the changes you want reviewed before you push them. If GitHub forking is disabled for this repository or organization, contact the instructors.

## Step 1: Fork the repository on GitHub

Open the workshop repository on GitHub and click **Fork**.

A fork is a separate repository under your own GitHub account. It is not the same thing as a branch. You will keep working on your existing local branch and push that branch to the fork.

After GitHub creates the fork, copy your fork URL. It will look like this:

```text
https://github.com/<your-username>/nextgen2026-coding-bootcamp.git
```

## Step 2: Reconfigure your local remotes

Right now, if you cloned the workshop repository directly, `origin` points to the workshop repository.

For the standard fork workflow, change your remotes so:

- `origin` points to your fork
- `upstream` points to the workshop repository

Run:

```bash
git remote rename origin upstream
git remote add origin https://github.com/<your-username>/nextgen2026-coding-bootcamp.git
git remote -v
```

After this, `git remote -v` should show:

- `origin` for your fork
- `upstream` for `nextgenerationgraduatesprogram/nextgen2026-coding-bootcamp`

## Step 3: Push your session branch to your fork

Push your current session branch to your fork:

```bash
git push -u origin <your-name>/session-1
```

Replace `<your-name>` with the branch name you actually created earlier.

The first push may prompt you to authenticate with GitHub.

## Step 4: Open the pull request

Open your fork on GitHub, then create a pull request with these settings:

- base repository: `nextgenerationgraduatesprogram/nextgen2026-coding-bootcamp`
- base branch: `starter/session-1`
- head fork: your fork
- compare branch: `<your-name>/session-1`

If GitHub does not show a **Compare & pull request** banner automatically, open the workshop repository, start a new pull request, and choose **compare across forks**.

Use `starter/session-1` as the default review target unless an instructor tells you to use a different branch.

Do not open the review pull request into `main`.

## Step 5: Continue working after review starts

Keep working on the same local branch if you need to make changes after opening the pull request.

Commit your changes locally, then push again:

```bash
git push
```

Because you used `git push -u` earlier, Git will keep pushing that branch to the matching branch on your fork and the pull request will update automatically.

## Step 6: Start later sessions after fork setup

After you rename the workshop repository remote to `upstream`, starter branches for future sessions will come from `upstream`, not `origin`.

For example, a future session branch would start like this:

```bash
git fetch upstream --prune
git switch -c <your-name>/session-2 upstream/starter/session-2
```

Use the same pattern for later sessions:

- fetch from `upstream`
- create your personal branch from `upstream/starter/session-<n>`
- push your branch to `origin`, which is now your fork

## References

- [About forks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks)
- [Fork a repository](https://docs.github.com/articles/fork-a-repo)
- [Configuring a remote repository for a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/configuring-a-remote-repository-for-a-fork)
- [Creating a pull request from a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
- [Managing the forking policy for your organization](https://docs.github.com/en/organizations/managing-organization-settings/managing-the-forking-policy-for-your-organization)
