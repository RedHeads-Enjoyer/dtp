from dataclasses import dataclass, astuple
from datetime import date


@dataclass(frozen=True)
class FeatureRecord:
    version: int
    date: date
    accidents_lag_1: float
    accidents_lag_7: float
    accidents_roll_7: float
    dow: int
    month: int
    temp_mean_lag_1: float
    temp_mean_mean_3: float
    temp_mean_mean_7: float
    temp_min_lag_1: float
    temp_min_min_3: float
    temp_max_lag_1: float
    temp_change: float
    temp_dev_lag_1: float
    precipitation_lag_1: float
    precipitation_sum_3: float
    precipitation_sum_7: float

    def as_tuple(self) -> tuple:
        return astuple(self)