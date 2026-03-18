# resq_precalc_pv_timeseries

This repository contains scripts for precalculating PV feed-in time-series data.  
Each PV system is defined by tilt and azimuth angles, and the script calculates
weighted sums per technology.

## Project Structure
resq_precalc_pv_timeseries/

├── scripts/

│ └── calculate_weighted_pv_timeseries_from_config.py # Main script with docstrings

├── data/

│ └── .gitkeep

├── results/

│ └── .gitkeep

├── pyproject.toml # uv project

├── uv.lock # Lockfile

├── .gitignore

└── README.md



## Environment Setup

The Python environment is managed with `uv`:

```bash
uv sync
```
