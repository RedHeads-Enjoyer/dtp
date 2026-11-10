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
    temp_dev: float
    temp_min: float
    temp_max: float
    temp_mean: float
    precipitation: float

    def as_tuple(self) -> tuple:
        return astuple(self)