# Repo Workflow And Missing Piece

This repository keeps the four-stage workflow shape intact: `fetch -> prepare -> analyze -> report`. The first two stages already work and produce inspectable artifacts. The last two stages are intentionally left incomplete so students can implement them from a real scaffold instead of from a blank repo.

## Steps

### Step 1. Run `fetch` and inspect the raw artifact

Start by materializing the digits dataset and looking at the raw payload.

```bash
uv run python scripts/00_fetch.py --config configs/base.yaml --run-name fetch-only
LATEST_FETCH=$(ls -1dt runs/*fetch-only* | head -n1)
find "$LATEST_FETCH" -maxdepth 3 -type f | sort
python - <<'PY'
from pathlib import Path
import numpy as np
latest = sorted(Path("runs").glob("*fetch-only*"), key=lambda p: p.stat().st_mtime)[-1]
with np.load(latest / "fetch" / "digits_raw.npz") as raw:
    print("files =", raw.files)
    print("images.shape =", raw["images"].shape)
    print("target.shape =", raw["target"].shape)
    print("target_names =", raw["target_names"].tolist())
    print("data.shape =", raw["data"].shape)
PY
```

The working `fetch` stage gives you the unnormalized digits dataset. You do not need to change it.

### Step 2. Run `prepare` and inspect the prepared artifacts

Then inspect the exact inputs that `analyze` must consume.

```bash
uv run python scripts/01_prepare.py --config configs/base.yaml --run-name prepare-only
LATEST_PREPARE=$(ls -1dt runs/*prepare-only* | head -n1)
find "$LATEST_PREPARE" -maxdepth 3 -type f | sort
python - <<'PY'
from pathlib import Path
import numpy as np
import pandas as pd
latest = sorted(Path("runs").glob("*prepare-only*"), key=lambda p: p.stat().st_mtime)[-1]
images = np.load(latest / "prepare" / "images.npy")
metadata = pd.read_csv(latest / "prepare" / "metadata.csv")
print("images.shape =", images.shape)
print("images.dtype =", images.dtype)
print("images.min =", float(images.min()))
print("images.max =", float(images.max()))
print("metadata.columns =", metadata.columns.tolist())
print(metadata.head().to_string(index=False))
print(metadata["label"].value_counts().sort_index().to_string())
PY
```

The current `prepare` contract is:

- `images.npy`: shape `(1797, 8, 8)`, `float32`, normalized to `[0.0, 1.0]`
- `metadata.csv`: columns `image_id` and `label`

These are the only inputs the analyze stage needs.

### Step 3. Inspect the missing code

Open the student-facing stubs before you implement anything.

```bash
sed -n '1,260p' src/nextgen2026_coding_bootcamp/steps/analyze.py
sed -n '1,260p' src/nextgen2026_coding_bootcamp/steps/report.py
sed -n '1,220p' configs/base.yaml
sed -n '1,220p' configs/stages/analyze.yaml
sed -n '1,220p' configs/stages/report.yaml
```

The current scaffold state is intentional:

- `analyze.py` resolves prepare inputs, validates config, and shows the expected helper structure
- `report.py` resolves analyze inputs, validates config, and shows the expected helper structure
- the analyze/report config blocks are placeholders that students must fill in

### Step 4. Fill in the config blocks

Students should put the same final values in `configs/base.yaml` and the matching stage fragments.

Use this structure for `analysis`:

```yaml
analysis:
  dataset_overview_name: dataset_overview.json
  class_summary_name: class_image_summary.csv
  representative_image_name: class_representatives.png
  generate_representative_image: true
  edge_threshold: 0.2
```

Use this structure for `report`:

```yaml
report:
  markdown_name: report.md
  include_representative_image: true
```

### Step 5. Implement the analyze stage

Use the provided helper names and return contract. The exact internals are up to you, but the stage should follow this structure:

```python
def run_analyze(cfg, ctx=None, images_npy=None, metadata_csv=None) -> dict:
    prepared_images_npy, prepared_metadata_csv = _resolve_prepare_inputs(...)
    analysis_cfg = _validate_analysis_config(cfg)

    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    images = np.load(prepared_images_npy)
    metadata = pd.read_csv(prepared_metadata_csv)

    overview = build_dataset_overview(images=images, metadata=metadata)
    summary = build_class_image_summary(
        images=images,
        metadata=metadata,
        edge_threshold=analysis_cfg["edge_threshold"],
    )

    # write dataset_overview.json
    # write class_image_summary.csv
    # optionally write class_representatives.png
    # copy outputs into ctx.run_dir / "analyze" when ctx is provided
    # return the artifact dictionary expected by the workflow
```

Reference code for shared-path and run-path behavior lives in `src/nextgen2026_coding_bootcamp/steps/prepare.py`.

### Step 6. Implement the report stage

The report stage must consume analyze artifacts, not recompute them.

```python
def run_report(cfg, ctx=None) -> dict:
    names = _validate_report_config(cfg)
    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    shared_inputs = _shared_analyze_paths(cfg, names)
    report_inputs = shared_inputs if ctx is None else _ctx_analyze_paths(cfg, ctx, names)

    # render report markdown from analyze artifacts
    # write the shared report
    # write a run-scoped report when ctx is provided
    # return the artifact dictionary expected by the workflow
```

Your report should include:

- dataset overview values from `dataset_overview.json`
- an analyze-artifact inventory
- a representative image reference when enabled
- a `Digit Class Profiles` Markdown table rendered from `class_image_summary.csv`

### Step 7. Write your own behavioural tests

Create your own analyze/report tests before implementation. A good default is:

- `tests/test_analyze_contract.py`
- `tests/test_report_contract.py`

Those tests should lock the final artifact contract you want to validate later in the session.
