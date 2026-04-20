# Appendix: Multiruns

This appendix defines a disciplined multirun protocol for parameter sweeps. It treats sweep design as a methodological activity with explicit variant definitions, run mapping, and completeness checks.

The benefit is defensible comparison: conclusions from sweeps are stronger when each planned variant is accounted for and linked to a full run record. This reduces interpretation risk from missing or ambiguously labeled runs.

## 1. What This Chapter Adds

This section defines the sweep protocol components needed for auditable cross-run comparison:

1. an explicit sweep surface;
2. deterministic variant naming;
3. completeness checks for planned variants;
4. a local summary index for cross-run comparison.

## 2. Why This Matters for Researchers

Ad hoc sweeps often produce ambiguous comparison sets with missing variants or unclear mappings. A formal protocol protects interpretability by making coverage and variant identity explicit.

This chapter is engine-agnostic. It can use the `run_once` adapter from Appendix `09` or another execution surface that preserves the same run contract.

## 3. Build Steps

Move from variable-surface definition to baseline execution and then reusable sweep automation. This sequence makes completeness checks easier to reason about before scaling.

### Step 1: Define one sweep variable

Start with one primary variable for clear interpretation:

- `analysis.high_demand_quantile`

### Step 2: Baseline with manual CLI sweep

Use a transparent baseline before automation:

```bash
for q in 0.85 0.90 0.95; do
  uv run python scripts/run_workflow.py \
    --profile base \
    --run-name "q${q}" \
    --set analysis.high_demand_quantile=${q}
done
```

### Step 3: Move to reusable sweep driver

This step codifies sweep execution and summary generation into repeatable code. It uses `run_once` from Appendix `09` as the execution adapter.

`scripts/sweep_quantiles.py`

```python
from __future__ import annotations

import csv
import json
from pathlib import Path

from nextgen2026_coding_bootcamp.engine_runner import run_once

QUANTILES = [0.80, 0.85, 0.90, 0.95]


def _read_manifest(run_dir: Path) -> dict:
    return json.loads((run_dir / "manifest.json").read_text())


def main() -> int:
    rows: list[dict] = []

    for q in QUANTILES:
        run_dir = run_once(
            profile="base",
            overrides=[f"analysis.high_demand_quantile={q}"],
            run_name=f"sweep-q{int(q * 100)}",
        )
        manifest = _read_manifest(run_dir)
        prepare = manifest.get("artifacts", {}).get("prepare", {})

        rows.append(
            {
                "run_id": manifest.get("run_id", run_dir.name),
                "quantile": q,
                "prepare_rows_out": prepare.get("rows_out"),
                "run_dir": str(run_dir),
            }
        )

    summary_dir = Path("runs") / "summaries"
    summary_dir.mkdir(parents=True, exist_ok=True)
    summary_path = summary_dir / "quantile_sweep.csv"

    with summary_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run_id", "quantile", "prepare_rows_out", "run_dir"])
        writer.writeheader()
        writer.writerows(rows)

    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Step 4: Define completeness expectations

For any sweep execution, check that:

1. every planned variant produced one run record;
2. each row in the summary index maps to one `run_id` and one `run_dir`;
3. failed variants are explicitly visible and not silently dropped.

## 4. Run Checkpoint

Use this checkpoint to verify variant completeness and summary-index integrity. Passing means each planned quantile maps to a recoverable run record.

```bash
uv run python scripts/sweep_quantiles.py
cat runs/summaries/quantile_sweep.csv
```

Optional quick completeness check:

```bash
rows=$(($(wc -l < runs/summaries/quantile_sweep.csv)-1)); echo "rows=${rows}"
```

## 5. Comparison Hooks

Use layered comparison surfaces so quick filtering and deep provenance inspection remain connected:

1. local summary index (`runs/summaries/quantile_sweep.csv`) for deterministic batch tables;
2. experiment tracker from Appendix `08` for filtering and dashboard views.

The authoritative evidence remains each run directory.

## 6. Failure Controls for Sweeps

Treat these controls as safeguards against invalid comparison sets and silent protocol drift:

1. Fail fast while piloting a new sweep definition.
2. Include sweep parameters in `run_name` for triage.
3. Keep sweep size small until runtime costs and artifact quality are stable.
4. Avoid changing stage code during an active sweep batch.

## 7. Transition

Next appendix: [Hydra](./11-appendix-hydra.md). With sweep protocol established, you can now change configuration ergonomics without changing run semantics.
