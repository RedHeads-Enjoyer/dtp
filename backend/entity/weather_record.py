from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass(frozen=True)
class WeatherRecord:
    id: int
    station_id: int
    observed_date: date
    temp_min: Decimal | None
    temp_mean: Decimal | None
    temp_max: Decimal | None
    temp_dev: Decimal | None
    precipitation: Decimal | None
    raw_id: int | None
    parsed_at: datetime