"""Author: @srhbrnds
Date: 2026 - 03 - 18
"""
import pandas as pd
from pathlib import Path

# Directories
DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results"

# Files
PV_CONFIG_FILE=DATA_DIR/ "pv_config.csv"
PV_TIMESERIES_FILE=DATA_DIR / "pv_feed_in_ts.csv"
RESULTS_FILE=RESULTS_DIR / "pv_feedin_try_mean_rcp85_p3.csv"

def main():
    """
    Loads PV configuration and time-series data, calculates the weighted
    sum of feed-in per technology, and saves the results as a CSV file.

    Workflow:
    1. Load PV_CONFIG_FILE
    2. Load PV_TIMESERIES_FILE – timeseries data with MultiIndex columns
       (tilt, azimuth)
    3. For each technology, calculate the weighted sum of time series
       across all technologies
    4. Save the resulting DataFrame to RESULTS_FILE
    """

    pv_config=pd.read_csv(PV_CONFIG_FILE)
    pv_timeseries=pd.read_csv(PV_TIMESERIES_FILE,
                          header=[0,1],
                          parse_dates=True,
                          index_col=0)

    pv_timeseries.columns = pd.MultiIndex.from_tuples(
        [(int(t), int(a)) for t, a in pv_timeseries.columns],
        names=["tilt", "azimuth"]
    )

    result = pd.DataFrame()

    for technology, group in pv_config.groupby("technology"):
        ts = sum(
            pv_timeseries[(row.tilt,row.azimuth)] * row.weight
            for _, row in group.iterrows()
        )
        result[technology] = ts

    result.to_csv(RESULTS_FILE)


if __name__ == "__main__":
    main()