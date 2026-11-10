from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class DailyRecord:
    id: int
    date: date
    accidents_lag_1: float
    accidents_lag_7: float
    accidents_roll_7: float
    dow: int
    month: int
    created_at: datetime