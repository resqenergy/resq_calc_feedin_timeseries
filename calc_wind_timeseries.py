import logging
from pathlib import Path

import pandas as pd
from windpowerlib import ModelChain, WindTurbine, create_power_curve

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
    """Resolve the calendar year for a TRY weather data file.

    The year can be derived from a period key in the filename ('p1', 'p2', 'p3',
    'reference') or supplied explicitly via args['year']. Providing both is an error.

    Period-to-year mapping:
        p1        -> 2020  (near-future climate scenario)
        p2        -> 2035  (mid-future climate scenario)
        p3        -> 2050  (far-future climate scenario)
        reference -> 2011  (historical reference year)

    Args:
        weatherdata_name (str): Filename (or path string) of the TRY weather file.
        year (int | None): Explicit year override from args['year']. Must be in
            [2000, 2500] if provided. Defaults to args['year'] (None).

    Returns:
        int: The resolved calendar year.

    Raises:
        ValueError: If both a period key and an explicit year are given, if neither
            is given, or if the explicit year is outside [2000, 2500].
    """
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


def read_and_preprocess_weather_data(weatherdata_file, args=args):
    """Read and preprocess a TRY weather file into the windpowerlib MultiIndex format.

    Reads the semicolon-separated TRY file, selects the relevant columns, converts
    temperature from °C to Kelvin, adds a constant roughness-length column, and
    returns a DataFrame with a two-level column MultiIndex as expected by windpowerlib
    (see data/windpowerlib_weather.csv for the reference structure).

    The calendar year is resolved automatically from the filename via resolve_year().
    Column names and measurement heights for the MultiIndex are taken from
    args['weather_columns'].

    Args:
        weatherdata_file (str | Path): Path to the TRY weather file (.txt, semicolon-separated).
        args (dict): Configuration dict with the following keys:
            year (int | None): Explicit year override; None to derive from filename.
            periods (int): Number of hourly time steps (typically 8760).
            roughness_length (float): Constant surface roughness length [m].
            weather_columns (list[tuple]): (variable_name, height) pairs used to
                build the MultiIndex, e.g. [('pressure', 0), ('temperature', 2),
                ('wind_speed', 10), ('roughness_length', 0)].

    Returns:
        pd.DataFrame: Hourly time series indexed by a DatetimeIndex, with a
            MultiIndex column (variable_name, height). Contains pressure [Pa],
            temperature [K], wind speed [m/s], and roughness length [m].
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


