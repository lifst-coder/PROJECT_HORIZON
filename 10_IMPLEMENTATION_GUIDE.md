# Implementation Guide

## Structure
- `01_TECHNOLOGY_REGISTRY.csv` – 100 technologies with domain, TRL, performance notes, sources.
- `02_EVIDENCE_REGISTRY.csv` – Verified and partially-verified claims with citations.
- `03_DEPENDENCY_GRAPH.json` – NetworkX-compatible directed graph (nodes + weighted edges).
- `04_SCENARIO_ASSUMPTIONS.csv` – Parameter table distinguishing observed vs forecast/assumption.
- `05_SIMULATION_ENGINE.py` – Runnable Monte Carlo engine (requires numpy, pandas).
- `06_SIMULATION_RESULTS.csv` – Output of 1,000-run simulation.
- Supporting analysis: `bottleneck_analysis.txt`, `dependency_graph.png`, innovation files.

## How to Extend
1. Enrich Technology Registry with additional primary sources for remaining entries.
2. Add more edges to dependency graph or import into NetworkX for further centrality / community detection.
3. Modify `run_simulation()` parameters or add new variables (e.g., materials intensity, capital stock).
4. Re-score innovation candidates with domain-expert weights.
5. Integrate with external data feeds for living updates.

All code executed in this package was actually run. Visualizations and CSVs are generated artifacts.
