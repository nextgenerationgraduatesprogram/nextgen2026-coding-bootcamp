# Testing the Workflow

This chapter formalizes testing as executable method assurance. It maps distinct risk types to distinct test categories so workflow correctness, handoffs, provenance artifacts, and analytical expectations are checked automatically.

The pedagogical goal is to treat test outcomes as part of scientific decision quality, not just software hygiene. Running tests before interpretation helps distinguish intended methodological updates from unintended regressions.

## 1. What This Chapter Adds

This section defines a compact test portfolio that maps directly to distinct research risks:

1. unit tests for local function correctness;
2. integration tests for stage handoff contracts;
3. smoke tests for full run contract viability;
4. known-answer tests for fixed-reference correctness;
5. invariant tests for always-true structural properties.

## 2. Why This Matters for Researchers

From a research perspective, tests are controls against silent method drift and accidental contract breakage. They provide structured evidence that run behavior remains interpretable after change.

- Unit tests protect transformations from small accidental regressions.
- Integration tests protect interface continuity between stages.
- Smoke tests protect reproducibility infrastructure (config/log/manifest/artifacts).
- Known-answer tests protect interpretation on a fixed reference case.
- Invariant tests protect general data-quality and schema assumptions.

Together, they reduce the chance that a new result is accepted for the wrong reason.

## 3. Build Steps

Apply these steps from coverage design to deterministic execution and governance interpretation. The sequence ensures tests are both technically valid and methodologically useful.

### Step 1: Add at least one test per risk type

This step ensures each major risk class has a concrete automated control. From a research standpoint, different failures require different tests: correctness, interface continuity, run viability, reference values, and invariants. Missing a class leaves blind spots in method assurance.


Recommended mapping in this repo:

1. Unit: `tests/test_prepare.py`
2. Integration: `tests/test_integration_stage_handoff.py`
3. Smoke: `tests/test_workflow_smoke.py`
4. Known-answer: `tests/test_known_answer.py`
5. Invariant: `tests/test_invariants.py`

### Step 2: Keep tests deterministic

This step removes external instability so failures represent code changes, not environmental noise. Deterministic tests are crucial when test outcomes gate interpretation decisions. Mock network and constrain fixtures so the same commit yields the same test outcome.


- Mock network in fetch tests.
- Use tiny inline fixture tables for prepare/analyze tests.
- Disable heavy plotting in smoke tests where not required.

### Step 3: Use assertion style that matches claim type

This step aligns statistical/numeric claims with appropriate assertion precision. Exact assertions are best for structural guarantees, while tolerance checks are safer for floating-point transforms. A mismatch here can either hide regressions or create noisy false failures.


Representative assertions:

```python
assert list(prepared.columns) == PREPARED_COLUMNS
assert abs(prepared.loc[0, "temp_c"] - 3.28) < 1e-6
assert summary["high_demand_threshold"] == 25.0
assert prepared["hour"].between(0, 23).all()
```

Use exact checks for structure/categorical behavior and tolerance-aware checks for floating-point values.

### Step 4: Treat test pass/fail as part of method governance

This step frames testing as part of scientific process control, not just engineering hygiene. Before accepting new results, classify failures as intended methodological change versus unintended regression. Document that decision path so baseline updates remain transparent.


Before interpreting a new run:

1. run tests;
2. if failures occur, classify as intended method change vs regression;
3. only then accept new result baselines.

## 4. Run Checkpoint

Use this checkpoint to confirm both minimal run viability and full-suite stability. Passing indicates that execution, provenance, and analytical contracts are currently aligned.

```bash
uv run pytest -q tests/test_workflow_smoke.py
uv run pytest -q
```

## 5. Transition

Core path complete. Continue to appendices only after this baseline passes consistently: [Experiment Tracking](./08-appendix-experiment-tracking.md).
