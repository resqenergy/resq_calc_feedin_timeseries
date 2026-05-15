from pathlib import Path
import pandas as pd
import warnings

DATA_DIR=Path(__file__).parent / "data"
RESULTS_DIR=Path(__file__).parent / "results"
PV_CONFIG_FILE=DATA_DIR/ "pv_config.csv"
GSEE_TIMESERIES_DIR=DATA_DIR / "gsee_timeseries"

def calc_pv_feedin(gsee_timeseries_file,pv_config=PV_CONFIG_FILE):
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

    gsee_timeseries = pd.read_csv(gsee_timeseries_file,
                                header=[0, 1],
                                parse_dates=True,
                                index_col=0).rename_axis("timeindex")
    gsee_timeseries.columns = gsee_timeseries.columns.set_levels(
        [pd.to_numeric(level) for level in gsee_timeseries.columns.levels]
    )

    pv_timeseries = pd.DataFrame()

    for technology, group in pv_config.groupby("technology"):
        ts = sum(
            gsee_timeseries[(row.tilt,row.azimuth)] * row.weight
            for _, row in group.iterrows()
        )
        pv_timeseries[technology] = ts

    return pv_timeseries

if __name__ == "__main__":
    for file in GSEE_TIMESERIES_DIR.iterdir():
        if file.is_file() and "gsee_timeseries" in file.name:

            pv_timeseries = calc_pv_feedin(file)

            filename=file.name.split("-")
            result_path = RESULTS_DIR / f"pv_timeseries-{filename[1]}-{filename[2]}"

            pv_timeseries.to_csv(result_path)

            print(f"PV timeseries successfully saved to: {result_path}")