# PROJECT HORIZON

A research package on enabling technologies for AI-scale compute, robotics, energy and biomanufacturing
through 2050: an evidence registry, scenario assumptions, a small Monte Carlo engine and project ideas.
Outputs are scenario bands under stated assumptions, not forecasts.

## Start here
- `00_EXECUTIVE_SUMMARY.md` – findings and limitations
- `phase1_5/PHASE1_5_SUMMARY_KO.md` – 검증 결과 요약 (한국어)
- `09_VALIDATION_REPORT.md` – four review cycles, including the corrections made on 2026-11-20

## Run the simulation
```bash
pip install numpy pandas
python 05_SIMULATION_ENGINE.py          # writes 06_SIMULATION_SUMMARY.csv
```

## What is and is not here
Present: evidence registry (`02`), assumptions (`04`), engine (`05`), result summary (`06`), opportunity and
project write-ups (`07`, `08`), validation (`09`), guide (`10`), gaps (`11`), next actions (`12`), and the
Phase 1.5 registries under `phase1_5/`.

Not uploaded: the 100-technology registry (`01`) and the dependency graph (`03`). The repository holds a
5-row technology sample and 4 dependency edges instead.
