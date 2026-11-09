from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class DailyRecord:
    id: int
    date: date
    accidents: int
    lag_1: float
    lag_7: float
    roll_7: float
    dow: int
    month: int
    created_at: datetime