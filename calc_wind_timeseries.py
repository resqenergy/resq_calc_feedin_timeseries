import pandas as pd
from pathlib import Path
import windpowerlib

DATA_DIR=Path(__file__).parent / "data"
RESULTS_DIR=Path(__file__).parent / "results"
WEATHER_DATA_DIR=DATA_DIR/ "10_Testreferenzjahre_TRY"
WINDTUBRINE_FILE=DATA_DIR / "turbine-models-main"/ "turbine_models"/ "data"/ "Distributed"/ "Kestrele400nb_2.5kW_4.csv"

args = {
    "year": None,
    "periods":8760,
    "coords": (52.43, 13.54) # coords of pv plant (52.43, 13.54) => Adlershof (Berlin)
}

def resolve_year(weatherdata_name, year=args["year"]):
    period_map = {"p1": 2020,
                  "p2": 2035,
                  "p3": 2050,
                  "reference": 2011} # eigene Annahme hstorisches Referenzjahr

    # Check if any period key is present in the name
    period_in_name = next((k for k in period_map if k in weatherdata_name), None)

    if year is not None and period_in_name is not None:
        raise ValueError(
            "Ambiguous input: Provide either args['year'] OR valid weatherdata file and name including "
            "('p1', 'p2', 'p3') in WEATHERDATA_NAME - not both."
        )

    if year is None:
        if period_in_name is not None:
            return period_map[period_in_name]
        raise ValueError(
            "Missing year: WEATHERDATA_NAME must include 'p1', 'p2', or 'p3', "
            "or provide args['year'] manually."
        )

    if 2000 <= year <= 2500:
        warnings.warn(
            "Manual year provided. Ensure consistency with args['periods'].",
            UserWarning
        )
        return year

    raise ValueError("args['year'] must be between 2000 and 2500.")


def read_and_preprocess_weather_data(weatherdata_file, year, args= args):
    """ Function to read and preprocess weather data from data/10-Testrefrenzjahre_TRY into required weather data format
    supported by windpowerlib. This is an example of how the supported weather data format should look like:
    DATA_DIR/ "windpowerlib_weather.csv"
    Parameters:
        """

    columns=["pressure_surface","wind_speed","air_temperature_mean"]

    df_weatherdata = pd.read_csv(weatherdata_file, sep=";", usecols=columns)
    df_weatherdata.set_index(pd.date_range(start=f"1/1/{year}",periods=args["periods"], freq="h"), inplace=True)

    df_weatherdata.rename(columns={
        "pressure_surface":"pressure",
        "air_temperature_mean":"temperature"},
        inplace=True)

    # placeholder for more preprocessing

    return df_weatherdata

if __name__ == "__main__":
    for file in WEATHER_DATA_DIR.iterdir():
        if file.is_file() and ".txt" in file.name and "try_mean_rcp85.p3" in file.name:

            year=resolve_year(file.name)
            weather_df=read_and_preprocess_weather_data(file, year)


