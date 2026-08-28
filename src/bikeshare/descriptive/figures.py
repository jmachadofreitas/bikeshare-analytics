from typing import cast

import altair as alt

from bikeshare.descriptive.types import (
    DailyDemand,
    HourlyDemandHistogram,
    HourlyDemandProfile,
    ProfileReferenceLevels,
    RiderSegmentProfile,
    WeatherDemand,
)


def hourly_demand_profile_figure(
    profile: HourlyDemandProfile,
    reference_levels: ProfileReferenceLevels,
) -> alt.LayerChart:
    demand_lines = (
        alt.Chart(profile)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "hr:Q",
                title="Hour of day",
                scale=alt.Scale(domain=[0, 23]),
                axis=alt.Axis(values=list(range(0, 24, 2)), format="02d"),
            ),
            y=alt.Y(
                "mean_demand:Q",
                title="Average hourly rentals",
                scale=alt.Scale(zero=True),
            ),
            color=alt.Color(
                "day_type:N",
                title=None,
                legend=alt.Legend(orient="top", direction="horizontal", columns=0),
            ),
            tooltip=[
                alt.Tooltip("day_type:N", title="Day type"),
                alt.Tooltip("hr:Q", title="Hour", format="02d"),
                alt.Tooltip("mean_demand:Q", title="Average rentals", format=".1f"),
            ],
        )
    )

    summary_rules = (
        alt.Chart(reference_levels)
        .mark_rule(color="#666666", opacity=0.8)
        .encode(
            y="value:Q",
            strokeDash=alt.StrokeDash(
                "statistic:N",
                title=None,
                sort=["Minimum", "Average", "Maximum"],
                legend=alt.Legend(
                    orient="top",
                    direction="horizontal",
                    columns=0,
                ),
            ),
            tooltip=[
                alt.Tooltip("statistic:N", title="Statistic"),
                alt.Tooltip("value:Q", title="Average rentals", format=".1f"),
            ],
        )
    )

    return cast(
        alt.LayerChart,
        (demand_lines + summary_rules).properties(
            title="Average hourly bike demand",
            width=700,
            height=400,
        ),
    )


def daily_demand_figure(demand: DailyDemand) -> alt.Chart:
    """Plot the daily demand trend across the full observation period."""
    return (
        alt.Chart(demand)
        .mark_line(color="#409ce3", strokeWidth=1.5)
        .encode(
            x=alt.X("dteday:T", title="Date"),
            y=alt.Y("total_rentals:Q", title="Daily rentals", scale=alt.Scale(zero=True)),
            tooltip=[
                alt.Tooltip("dteday:T", title="Date"),
                alt.Tooltip("total_rentals:Q", title="Total rentals", format=","),
            ],
        )
        .properties(
            title="Daily bike-share demand",
            width=700,
            height=260,
        )
    )


def hourly_demand_histogram_figure(histogram: HourlyDemandHistogram) -> alt.Chart:
    """Plot a preaggregated distribution of observed hourly demand."""
    return (
        alt.Chart(histogram)
        .mark_bar(color="#65b5f2")
        .encode(
            x=alt.X("bin_start:Q", bin="binned", title="Hourly rentals"),
            x2="bin_end:Q",
            y=alt.Y("hours_observed:Q", title="Hours observed"),
            tooltip=[
                alt.Tooltip("bin_start:Q", title="Rental range starts", format=","),
                alt.Tooltip("bin_end:Q", title="Rental range ends", format=","),
                alt.Tooltip("hours_observed:Q", title="Hours observed", format=","),
            ],
        )
        .properties(
            title="Distribution of hourly bike-share demand",
            width=700,
            height=260,
        )
    )


def rider_segment_profile_figure(profile: RiderSegmentProfile) -> alt.FacetChart:
    """Compare intraday patterns for casual and registered riders."""
    chart = (
        alt.Chart(profile)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "hr:Q",
                title="Hour of day",
                axis=alt.Axis(values=list(range(0, 24, 2))),
            ),
            y=alt.Y(
                "mean_demand:Q",
                title="Average hourly rentals",
                scale=alt.Scale(zero=True),
            ),
            color=alt.Color(
                "rider_type:N",
                title=None,
                scale=alt.Scale(range=["#8bc0e9", "#ffc574"]),
            ),
            strokeDash=alt.StrokeDash("rider_type:N", title=None),
            tooltip=[
                alt.Tooltip("day_type:N", title="Day type"),
                alt.Tooltip("rider_type:N", title="Rider type"),
                alt.Tooltip("hr:Q", title="Hour", format="02d"),
                alt.Tooltip("mean_demand:Q", title="Average rentals", format=".1f"),
            ],
        )
        .properties(width=340, height=260)
    )
    return cast(
        alt.FacetChart,
        chart.facet(
            column=alt.Column(
                "day_type:N",
                title=None,
                sort=["Working day", "Non-working day"],
            ),
        ).properties(title="Intraday demand by rider segment"),
    )


def weather_demand_figure(summary: WeatherDemand) -> alt.Chart:
    """Compare average hourly demand across observed weather conditions."""
    return (
        alt.Chart(summary)
        .mark_bar(color="#41a7f4")
        .encode(
            y=alt.Y("weather:N", title=None, sort=alt.SortField("weathersit")),
            x=alt.X(
                "mean_demand:Q",
                title="Average hourly rentals",
                scale=alt.Scale(zero=True),
            ),
            tooltip=[
                alt.Tooltip("weather:N", title="Weather situation"),
                alt.Tooltip("hours_observed:Q", title="Hours observed", format=","),
                alt.Tooltip("mean_demand:Q", title="Mean rentals", format=".1f"),
                alt.Tooltip("median_demand:Q", title="Median rentals", format=".1f"),
            ],
        )
        .properties(
            title="Average demand by weather situation",
            width=700,
            height=180,
        )
    )
