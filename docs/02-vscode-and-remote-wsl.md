# VS Code and Remote WSL Setup

Visual Studio Code (`VS Code`) is the code editor we use for the bootcamp. We use it because it gives you one place to edit files, run a terminal, install extensions, and connect directly into your Ubuntu 24.04 WSL environment while keeping the development experience simple.

In this guide, you are setting up the editor and connecting it to your Linux environment. The goal is to make sure you are editing files and running commands inside Ubuntu 24.04 rather than in the Windows filesystem.

Windows users should follow the full guide.
macOS and Linux users can skip the WSL-specific step and install only VS Code and the `Python` extension.

## Reference

- VS Code: [Developing in WSL](https://code.visualstudio.com/docs/remote/wsl)
- VS Code: [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments) # TODO: can you check whether this is relevant cause we're using uv

## Step 1: Install Visual Studio Code

Install VS Code for your operating system from the official [Visual Studio Code download page](https://code.visualstudio.com/download).

Open VS Code after installing it.

## Step 2: Install extensions

Open the **Extensions** sidebar view (`Ctrl+Shift+X`) in VS Code and install:

- `WSL`
- `Python`

The `Python` extension is still useful when the project uses `uv`: `uv` manages environments and dependencies, while the extension provides editor features like IntelliSense, debugging, testing, and interpreter selection inside VS Code.

## Step 3: Connect VS Code to Ubuntu 24.04 on WSL

Open **Windows PowerShell** and run:

```powershell
wsl -d Ubuntu-24.04
```

Then run this in the Linux shell:

```bash
code ~
```

If `code` is not found:

1. Open VS Code normally from Windows.
2. Press `Ctrl+Shift+P`.
3. Run `WSL: Connect to WSL`.
4. Choose `Ubuntu-24.04`.

Then open a folder inside `/home/<username>`.

## Step 4: Check the connection

On Windows, check that:

- the bottom-left corner shows a WSL connection to `Ubuntu-24.04`
- the integrated terminal opens (`Ctrl+Shift+~`) in a Linux shell
- paths (e.g. run `pwd`) look like `/home/<username>/...`, not `C:\...`

If VS Code is not connected to `Ubuntu-24.04`, close the window, run `WSL: Connect to WSL`, choose `Ubuntu-24.04`, and reopen the folder from `/home/<username>/...`.

## Step 5: Check the Python extension

In the VS Code window you will use for development:

1. Open the **Extensions** panel.
2. Search for `Python`.
3. Confirm it is enabled in the current environment.

If the Python extension is only enabled on the Windows side, enable it in the WSL window as well.

Continue to [Toolchain Setup](./03-toolchain-setup.md).
