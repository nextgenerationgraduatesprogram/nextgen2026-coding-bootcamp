# Windows Setup: WSL and Ubuntu 24.04

Windows Subsystem for Linux (`WSL`) lets you run a Linux environment directly on Windows, and Ubuntu 24.04 is the Linux distribution we use for the bootcamp. We use this setup so everyone works in the same Linux-based terminal environment, which makes commands, tools, and project setup more consistent across the cohort.

In this guide, you are setting up the Linux environment that the rest of the bootcamp tools will run inside. By the end of this step, you should have Ubuntu 24.04 installed, opening correctly, and ready to use from the terminal.

If you are on macOS or Linux, skip this file and go to [VS Code and Remote Setup](./02-vscode-and-remote-wsl.md).

## Reference

- Microsoft: [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
- Microsoft: [Set up a WSL development environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment)

## Step 1: Install WSL

Open **Windows PowerShell as Administrator** and run:

```powershell
wsl --install -d Ubuntu-24.04
```

Restart Windows if prompted.

If `wsl` is not recognized, make sure you opened **Windows PowerShell as Administrator** and run the command again.

## Step 2: Start Ubuntu 24.04 and create your Linux user

Open **Windows PowerShell** and run:

```powershell
wsl -d Ubuntu-24.04
```

Then:

1. Wait for the first-time setup to finish.
2. Create a Linux username and password when prompted.

If the Ubuntu window closes immediately, run `wsl -d Ubuntu-24.04` again. If it still closes, reinstall the distro and repeat this step.

## Step 3: Update Ubuntu 24.04 packages

Open **Windows PowerShell** and run:

```powershell
wsl -d Ubuntu-24.04
```

Then run this in the Linux shell:

```bash
sudo apt update
sudo apt upgrade -y
```

## Step 4: Validate the installation

In **Windows PowerShell**:

```powershell
wsl -l -v
```

Check that `Ubuntu-24.04` is listed and `VERSION` is `2`.

If `VERSION` is `1`, run this in **Windows PowerShell**:

```powershell
wsl --set-version Ubuntu-24.04 2
```

Open **Windows PowerShell** and run:

```powershell
wsl -d Ubuntu-24.04
```

## Step 5: Make Ubuntu 24.04 the default WSL distro if needed

If you have more than one WSL distro and Ubuntu 24.04 is not the default, run this in **Windows PowerShell**:

```powershell
wsl --set-default Ubuntu-24.04
```

## Step 6. Get used to using the Linux terminal

You will use the Ubuntu terminal a lot in this bootcamp. These basic commands are enough to get around comfortably:

```bash
pwd         # show your current folder
ls          # list files and folders here
ls -la      # list all files, including hidden ones
cd ~        # go to your home folder
cd folder   # move into a folder
cd ..       # move up one folder
mkdir demo  # create a new folder
rm -rf demo # delete a folder
cat file.txt # print a file's contents
clear       # clear the terminal screen
```

Example:

```bash
cd ~/nextgen2026-coding-bootcamp
ls
cd docs
pwd
```

If you want a beginner-friendly walkthrough, Ubuntu's guide is a good reference:
https://documentation.ubuntu.com/desktop/en/latest/tutorial/the-linux-command-line-for-beginners/


Continue to [VS Code and Remote Setup](./02-vscode-and-remote-wsl.md).
