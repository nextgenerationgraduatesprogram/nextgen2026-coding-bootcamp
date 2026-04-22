# Session 3 - Controlled Agent Collaboration for Workflow Extensions

This repository shows you how to use AI coding agents inside the Bike Sharing workflow without giving up control of the work. The session teaches a bounded, reviewable workflow where the agent helps draft specs, tests, plans, and review artifacts, while you keep control of approval, interpretation, and merge decisions.

Core operating rule:

`define the problem -> clarify and approve the specification -> design behavioural tests -> implement those tests -> design the implementation plan -> implement the plan and supporting tests -> review and commit -> refine the workflow`

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
- clarifying the problem specification before feature work begins
- defining executable behavioural tests before feature implementation
- designing an implementation plan with deliberate context and file references
- reviewing the work against specs, tests, artifacts, and git state before commit
- turning repeated lessons into durable repo instructions, tests, and templates
