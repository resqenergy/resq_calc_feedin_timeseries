# resq_calc_feedin_timeseries

This repository contains scripts for precalculating feed-in time-series for pv 
(wind and solarthermal timeseries may be added later).

## Project Structure
resq_precalc_pv_timeseries/


├── data/

│ └── .gitkeep

├── results/

│ └── .gitkeep

├── pyproject.toml # uv project

├── uv.lock # Lockfile

├── .gitignore

└── README.md

│└── calc_pv_timeseries.py 


## Environment Setup

The Python environment is managed with `uv`:

```bash
uv sync
```
