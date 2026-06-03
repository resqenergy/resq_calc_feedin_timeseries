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
    "coords": (52.43, 13.54), # coords of pv plant (52.43, 13.54) => Adlershof (Berlin)
    "roughness_length": 0.6,  #Source: https://wind-data.ch/tools/profile.php?h=2&v=10&z0=0.6&abfrage=Aktualisieren
    "weather_columns": [("pressure",0), ("temperature",2), ("wind_speed",10), ("roughness_length",0)] # (variable name, heights) source: heights taken from data/10_Testreferenzjahre_TRY/metadata_testreferenceyears.pdf
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
    year= resolve_year(weatherdata_file.name, args["year"])
    columns=["pressure_surface","wind_speed","air_temperature_mean"]

    df = pd.read_csv(weatherdata_file, sep=";", usecols=columns)
    df.set_index(pd.date_range(start=f"1/1/{year}",periods=args["periods"], freq="h"), inplace=True)

    df.rename(columns={
        "pressure_surface":"pressure",
        "air_temperature_mean":"temperature"},
        inplace=True)
    df["roughness_length"] = args["roughness_length"]

    # transfer temperature from °C to Kelvin
    df["temperature"]=df["temperature"]+273.15

    df=df[["pressure","temperature", "wind_speed", "roughness_length"]]
    df.columns= pd.MultiIndex.from_tuples(args["weather_columns"], names=["variable_name","height"])
    return df


if __name__ == "__main__":
    for file in WEATHER_DATA_DIR.iterdir():
        if file.is_file() and ".txt" in file.name and "try_mean_rcp85.p3" in file.name:

            weather_df=read_and_preprocess_weather_data(file, args)
            print("Success")


