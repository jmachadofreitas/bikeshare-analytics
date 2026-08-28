"""Experimental

Semantic table types for descriptive figures.

Each type shares its root name with the table builder and figure that use it:
``hourly_demand_profile`` -> ``HourlyDemandProfile`` -> ``hourly_demand_profile_figure``.
"""

from typing import NewType

import polars as pl

DataQualitySummary = NewType("DataQualitySummary", pl.DataFrame)
DailyDemand = NewType("DailyDemand", pl.DataFrame)
HourlyDemandHistogram = NewType("HourlyDemandHistogram", pl.DataFrame)
HourlyDemandProfile = NewType("HourlyDemandProfile", pl.DataFrame)
ProfileReferenceLevels = NewType("ProfileReferenceLevels", pl.DataFrame)
RiderSegmentProfile = NewType("RiderSegmentProfile", pl.DataFrame)
WeatherDemand = NewType("WeatherDemand", pl.DataFrame)
