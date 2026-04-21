# 🧬 Research Workflow Template

This repository is a standardized template for reproducible research and data analytics projects. It follows the **"Engine vs. Wrapper"** architecture to ensure that scientific logic is decoupled from execution, configuration, and reporting.

While currently containing a **Bike-Share Analysis** as a bootcamp example, the structure is designed to be reused for any predictive or analytical system.

---

## 🚀 Quick Start: Run the Pipeline

To verify the environment and run the full end-to-end workflow, execute the following commands in order:

```bash
# 1. Fetch raw data
uv run python scripts/00_fetch.py --config configs/stages/fetch.yaml

# 2. Prepare/Clean data
uv run python scripts/01_prepare.py --config configs/stages/prepare.yaml

# 3. Analyze data (with optional parameter override)
uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml --set analysis.high_demand_quantile=0.90

# 4. Generate Report/Plots
uv run python scripts/03_report.py --config configs/stages/report.yaml
```

---

## 🏗️ Architectural Patterns (The Template Utility)

### 1. The "Engine vs. Wrapper" Pattern
- **The Engine (`src/`)**: Durable, reusable method logic. Decoupled from CLI arguments and specific file paths.
- **The Ignition (`scripts/`)**: Thin executable wrappers. They handle user input and call the engine.
- **Benefits**: Logic is testable in isolation; scripts are easy to replace or automate.

### 2. Composed Configuration
- **Settings (`configs/`)**: Instead of monolithic files, we use small, focused YAML files (`run.yaml`, `paths.yaml`, `stages/*.yaml`).
- **Composition**: Scripts merge these files at runtime, allowing you to change a dataset path or a model threshold without touching the code.

### 3. CLI Standard
- Every script follows a unified interface: `--config <path>` and `--set <KEY=VALUE>` for overrides.

---

## 🧪 Experiment Management: The Branching Method

To ensure reproducibility and clear provenance for scientific experiments, follow the **"Branching Out"** method:

1.  **Baseline Branch**: Keep your `main` or `stable` branch as the validated baseline.
2.  **Experiment Branch**: For every new hypothesis, parameter sweep, or model variant, create a dedicated branch (e.g., `experiment/quantile-0.95`).
3.  **Durable State**: Commit the configuration changes and the resulting metrics/plots directly to that branch.
4.  **Comparison**: This allows you to use `git diff` to compare not just code, but the *assumptions* (configs) and *outcomes* (results) of different experiments side-by-side.

---

## 🤖 Working with AI Coding Agents
This project is optimized for AI-assisted development. Please refer to **[CODING_AGENT_RULES.md](./CODING_AGENT_RULES.md)** for session synchronization and architectural safety rules.

## 📚 Repository Structure
- `src/`: Reusable logic ("The Engine").
- `scripts/`: Task-specific execution ("The Ignition").
- `configs/`: Composable YAML settings.
- `data/`: Raw and intermediate data storage (Git-ignored).
- `results/`: Generated artifacts, plots, and summaries.
