import sys
from pathlib import Path

import pandas as pd
import pytest

# Make the module importable without packaging
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from calc_pv_timeseries import calc_pv_feedin

TEST_DATA_DIR = Path(__file__).resolve().parent /"test_data"
GSEE_FILE = TEST_DATA_DIR / "gsee_timeseries_sample.csv"
EXPECTED_FILE = TEST_DATA_DIR / "pv_timeseries_expected.csv"


def test_pv_feedin_sum_matches_precalculated():
    expected = pd.read_csv(EXPECTED_FILE, index_col=0, parse_dates=True)
    result = calc_pv_feedin(GSEE_FILE)

    for col in expected.columns:
        assert result[col].sum() == pytest.approx(expected[col].sum(),
                                                  rel=1e-5), \
            f"Sum mismatch for column '{col}'"
