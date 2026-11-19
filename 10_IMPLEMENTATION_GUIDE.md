# Implementation Guide

## Structure
Present in this repository:
- `02_EVIDENCE_REGISTRY.csv` – claims with status and sources.
- `04_SCENARIO_ASSUMPTIONS.csv` – parameter table distinguishing observed, forecast and assumption.
- `05_SIMULATION_ENGINE.py` – Monte Carlo engine (requires numpy, pandas).
- `06_SIMULATION_SUMMARY.csv` – p10 / p50 / p90 per year and variable from the default run (seed 42).
- `phase1_5/` – claim, source and technology-sample registries, dependency edges, contradiction log, hand-off notes.

Referred to in the reports but not uploaded:
- `01_TECHNOLOGY_REGISTRY.csv` (100 technologies), `03_DEPENDENCY_GRAPH.json`, `bottleneck_analysis.txt`, `dependency_graph.png`.

## How to Extend
1. Enrich Technology Registry with additional primary sources for remaining entries.
2. Add more edges to dependency graph or import into NetworkX for further centrality / community detection.
3. Modify `run_simulation()` parameters or add new variables (e.g., materials intensity, capital stock).
4. Re-score innovation candidates with domain-expert weights.
5. Integrate with external data feeds for living updates.

`05_SIMULATION_ENGINE.py` was run to produce `06_SIMULATION_SUMMARY.csv`. `python 05_SIMULATION_ENGINE.py --full` also writes every run to `06_SIMULATION_RESULTS.csv`.
