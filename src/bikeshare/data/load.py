"""Load the UCI hourly data into the analytical time-series grain."""

from pathlib import Path

import polars as pl

from bikeshare.data.download import RAW_DATA_DIR

HOURLY_DATA_PATH = RAW_DATA_DIR / "hour.csv"


def load_hourly_observations(path: Path = HOURLY_DATA_PATH) -> pl.DataFrame:
    """Return hourly rentals with a validated timestamp and chronological order."""
    observations = pl.read_csv(path, try_parse_dates=True).with_columns(
        pl.col("dteday").cast(pl.Date),
        pl.datetime(
            year=pl.col("dteday").dt.year(),
            month=pl.col("dteday").dt.month(),
            day=pl.col("dteday").dt.day(),
            hour=pl.col("hr"),
        ).alias("timestamp"),
    )

    return observations.sort("timestamp")
