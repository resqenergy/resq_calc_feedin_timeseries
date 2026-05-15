# resq_calc_feedin_timeseries

This repository contains scripts for precalculating PV feed-in time-series data.  
Each PV system is defined by tilt and azimuth angles, and the script calculates
weighted sums per technology.

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
