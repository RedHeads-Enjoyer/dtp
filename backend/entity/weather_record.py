from dataclasses import dataclass, fields
from datetime import date
from datetime import datetime


@dataclass
class WeatherRecord:
    station_id: int
    observed_date: date
    created_at: datetime
    temp_mean_lag_1: float | None
    temp_mean_mean_3: float | None
    temp_mean_mean_7: float | None
    temp_min_lag_1: float | None
    temp_min_min_3: float | None
    temp_max_lag_1: float | None
    temp_change: float | None
    temp_dev_lag_1: float | None
    precipitation_lag_1: float | None
    precipitation_sum_3: float | None
    precipitation_sum_7: float | None

WEATHER_COLUMNS = [f.name for f in fields(WeatherRecord)]