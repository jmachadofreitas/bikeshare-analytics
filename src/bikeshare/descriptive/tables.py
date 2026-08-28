import polars as pl

from bikeshare.descriptive.types import (
    DailyDemand,
    DataQualitySummary,
    HourlyDemandHistogram,
    HourlyDemandProfile,
    ProfileReferenceLevels,
    RiderSegmentProfile,
    WeatherDemand,
)


def data_quality_summary(observations: pl.DataFrame) -> DataQualitySummary:
    """Summarise checks that establish whether the hourly series is usable."""

    duplicate_timestamps = observations.select(pl.col("timestamp").is_duplicated().sum()).item()
    missing_values = sum(observations.null_count().row(0))

    return DataQualitySummary(
        pl.DataFrame(
            {
                "check": [
                    "Hourly observations",
                    "Coverage starts",
                    "Coverage ends",
                    "Duplicate timestamps",
                    "Missing values",
                ],
                "value": [
                    str(observations.height),
                    str(observations["timestamp"].min()),
                    str(observations["timestamp"].max()),
                    str(duplicate_timestamps),
                    str(missing_values),
                ],
            }
        )
    )


def daily_demand(observations: pl.DataFrame) -> DailyDemand:
    """Aggregate rental demand to the daily grain for trend inspection."""
    return DailyDemand(
        observations.group_by("dteday")
        .agg(
            pl.col("cnt").sum().alias("total_rentals"),
            pl.col("casual").sum().alias("casual_rentals"),
            pl.col("registered").sum().alias("registered_rentals"),
        )
        .sort("dteday")
    )


def hourly_demand_histogram(
    observations: pl.DataFrame,
    *,
    bin_width: int = 25,
) -> HourlyDemandHistogram:
    """Preaggregate hourly rental counts into fixed-width histogram bins.

    The returned table is intentionally small enough to embed in an Altair
    specification, rather than passing every hourly observation to the browser.
    """
    if bin_width <= 0:
        raise ValueError("bin_width must be a positive integer.")

    return HourlyDemandHistogram(
        observations.select(((pl.col("cnt") // bin_width) * bin_width).alias("bin_start"))
        .group_by("bin_start")
        .agg(pl.len().alias("hours_observed"))
        .with_columns((pl.col("bin_start") + bin_width).alias("bin_end"))
        .sort("bin_start")
    )


def hourly_demand_profile(observations: pl.DataFrame) -> HourlyDemandProfile:
    """Return average hourly rentals by working-day status."""
    return HourlyDemandProfile(
        observations.select("hr", "cnt", "workingday")
        .with_columns(
            pl.when(pl.col("workingday") == 1)
            .then(pl.lit("Working day"))
            .otherwise(pl.lit("Non-working day"))
            .alias("day_type")
        )
        .group_by("hr", "day_type")
        .agg(pl.col("cnt").mean().alias("mean_demand"))
        .sort("day_type", "hr")
    )


def rider_segment_profile(observations: pl.DataFrame) -> RiderSegmentProfile:
    """Show how casual and registered demand changes within a day."""
    return RiderSegmentProfile(
        observations.select("hr", "workingday", "casual", "registered")
        .with_columns(
            pl.when(pl.col("workingday") == 1)
            .then(pl.lit("Working day"))
            .otherwise(pl.lit("Non-working day"))
            .alias("day_type")
        )
        .group_by("hr", "day_type")
        .agg(
            pl.col("casual").mean().alias("Casual riders"),
            pl.col("registered").mean().alias("Registered riders"),
        )
        .unpivot(
            index=["hr", "day_type"],
            variable_name="rider_type",
            value_name="mean_demand",
        )
        .sort("day_type", "rider_type", "hr")
    )


def weather_demand(observations: pl.DataFrame) -> WeatherDemand:
    """Summarise observed hourly demand by the recorded weather situation."""
    weather_labels = {
        1: "Clear / few clouds",
        2: "Mist / cloudy",
        3: "Light rain or snow",
        4: "Heavy rain or snow",
    }
    return WeatherDemand(
        observations.group_by("weathersit")
        .agg(
            pl.len().alias("hours_observed"),
            pl.col("cnt").mean().alias("mean_demand"),
            pl.col("cnt").median().alias("median_demand"),
        )
        .with_columns(
            pl.col("weathersit")
            .replace_strict(weather_labels, return_dtype=pl.String)
            .alias("weather")
        )
        .select("weathersit", "weather", "hours_observed", "mean_demand", "median_demand")
        .sort("weathersit")
    )


def profile_reference_levels(profile: HourlyDemandProfile) -> ProfileReferenceLevels:
    """Return reference levels used by ``hourly_demand_profile_figure``."""
    return ProfileReferenceLevels(
        profile.select(
            pl.col("mean_demand").min().alias("Minimum"),
            pl.col("mean_demand").mean().alias("Average"),
            pl.col("mean_demand").max().alias("Maximum"),
        ).unpivot(variable_name="statistic", value_name="value")
    )
