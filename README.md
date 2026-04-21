# Session 3 - Controlled Agent Collaboration for Workflow Extensions

This repository teaches controlled use of AI coding agents inside the Bike Sharing workflow. The goal is not to make the agent the center of the session. The goal is to show how bounded delegation fits into a reviewable workflow that still belongs to the humans operating the repository.

Core operating rule:

`assess task -> decide how to check it -> specify it -> load context -> delegate -> verify/integrate -> manage git -> improve process`

## Start Here

1. Read the docs map: [docs/README.md](./docs/README.md)
2. Start with the workshop entry chapter: [docs/00-session-overview.md](./docs/00-session-overview.md)
3. Review durable agent instructions: [AGENTS.md](./AGENTS.md)

## Coding Agent Setup

This session is tool-agnostic. Use any coding agent you prefer, but install and authenticate one before you start the workshop.

If you prefer working inside VS Code instead of a terminal-first CLI, official VS Code extensions are also available for Codex, Gemini Code Assist, and Claude Code.

### Shared Prerequisites

- Git
- Python plus [`uv`](https://docs.astral.sh/uv/)
- Node.js 20+ if you plan to use an npm-installed agent CLI
- VS Code if you plan to use an editor extension instead of the CLI

```Bash
# install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash

# restart your terminal, then install Node 20
nvm install 20
nvm use 20
nvm alias default 20

# verify
node -v
npm -v
```

### Option A: Codex CLI

```bash
npm install -g @openai/codex
codex
```

On first run, sign in with your ChatGPT account or an OpenAI API key.

Official docs: <https://developers.openai.com/codex/cli>

VS Code extension: <https://developers.openai.com/codex/ide>

### Option B: Gemini CLI

```bash
npm install -g @google/gemini-cli
gemini
```

On first run, choose `Sign in with Google`. If you prefer, you can also use a Gemini API key instead.

Official docs:

- Install: <https://geminicli.com/docs/get-started/installation/>
- Auth: <https://geminicli.com/docs/get-started/authentication/>
- VS Code extension: <https://developers.google.com/gemini-code-assist/docs/set-up-gemini>

### Option C: Claude Code

Recommended installer from Anthropic:

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude
```

Alternative npm install:

```bash
npm install -g @anthropic-ai/claude-code
claude
```

On first run, complete the browser login flow. Claude Code requires a paid Claude or Anthropic Console account.

Official docs: <https://code.claude.com/docs/en/getting-started>

VS Code extension: <https://code.claude.com/docs/en/vs-code>

### Recommendation

Pick one agent and use it consistently for the session. The repository commands stay the same regardless of which agent you use.

## Baseline Health Check

Run these before any delegation:

```bash
uv run pytest -q
uv run python scripts/run_workflow.py --profile base --run-name baseline-check
```

## What This Session Teaches

- choosing a bounded workflow change inside `fetch -> prepare -> analyze -> report`
- matching review burden to task risk before implementation begins
- writing task contracts and loading only the context the agent needs
- using a plan-first delegation loop and verifying the result in layers
- keeping git discipline and turning repeated lessons into durable repo improvements

## Documentation Structure

- Operator guide and templates: [`docs/`](./docs)
- Historical snapshots: [`docs/archive/INDEX.md`](./docs/archive/INDEX.md)
