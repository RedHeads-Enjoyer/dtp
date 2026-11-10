from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass(frozen=True)
class WeatherParsedRecord:
    station_id: int
    observed_date: date
    temp_min: Decimal | None
    temp_mean: Decimal | None
    temp_max: Decimal | None
    temp_dev: Decimal | None
    precipitation: Decimal | None
    parsed_at: datetime