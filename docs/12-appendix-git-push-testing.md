# Appendix: Automated Testing on Git Push

This appendix defines a deterministic push-time validation gate shared between local development and CI. It makes baseline quality checks explicit before workflow changes enter shared branches.

A consistent gate protects collaborative reproducibility by reducing the chance that unvalidated changes alter run behavior unnoticed. Aligning local hooks and CI ensures branch history reflects the same minimum validation standard.

## 1. What This Chapter Adds

This section defines the minimum enforcement elements needed for consistent pre-merge validation:

1. one stable push-test command;
2. local `pre-push` hook enforcement;
3. CI workflow parity with the same command.

## 2. Why This Matters for Researchers

If push-time validation is discretionary, regressions can enter shared history and undermine downstream interpretations. A deterministic gate keeps collaboration artifacts aligned with reproducibility expectations.

## 3. Build Steps

Implement the gate in order: define one authoritative command, enforce it locally, then mirror it in CI. This sequence prevents policy drift between development and integration environments.

### Step 1: Define the push gate command

This step formalizes the minimum automated checks required before code reaches shared branches. A single stable command reduces ambiguity about what 'passing' means in collaboration. Keep the gate focused on core reproducibility risks rather than exhaustive long-running suites.


```bash
uv run pytest -q \
  tests/test_config.py \
  tests/test_fetch.py \
  tests/test_prepare.py \
  tests/test_analyze_report.py \
  tests/test_workflow_smoke.py
```

### Step 2: Add local pre-push hook

This step enforces the gate at the developer boundary so failures are caught before remote integration. It shortens feedback loops and reduces noisy CI churn. Treat hook bypass as an exception path, not normal workflow.


Create `.git/hooks/pre-push`:

```bash
#!/usr/bin/env bash
set -euo pipefail

uv run pytest -q \
  tests/test_config.py \
  tests/test_fetch.py \
  tests/test_prepare.py \
  tests/test_analyze_report.py \
  tests/test_workflow_smoke.py
```

Make executable:

```bash
chmod +x .git/hooks/pre-push
```

### Step 3: Mirror the same gate in CI

This step aligns remote enforcement with local expectations so branch protection has deterministic meaning. Consistency between hook and CI prevents 'works locally' discrepancies in validation scope. If the gate changes, update both locations together to avoid policy drift.


Minimal `.github/workflows/ci.yml`:

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync
      - run: uv run pytest -q tests/test_config.py tests/test_fetch.py tests/test_prepare.py tests/test_analyze_report.py tests/test_workflow_smoke.py
```

## 4. Run Checkpoint

Use this checkpoint to verify both gate execution and local enforcement readiness. Passing indicates the same baseline command can be trusted in local and CI contexts.

```bash
uv run pytest -q tests/test_config.py tests/test_fetch.py tests/test_prepare.py tests/test_analyze_report.py tests/test_workflow_smoke.py
test -x .git/hooks/pre-push && echo "pre-push hook ready"
```

## 5. Transition

Appendix sequence complete. Return to [Session 2 Guide](./README.md) to navigate the full learning path and decide which extensions to operationalize next.
