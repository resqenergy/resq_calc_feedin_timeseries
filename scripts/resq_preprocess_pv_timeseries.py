import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results"
PV_CONFIG_FILE=DATA_DIR/ "pv_config.csv"
PV_TIMESERIES_FILE=DATA_DIR / "pv_feed_in_ts.csv"

def main():

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

    result.to_csv(RESULTS_DIR / "pv_feedin_try_rcp85_p3.csv")


if __name__ == "__main__":
    main()