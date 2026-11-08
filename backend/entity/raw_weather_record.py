from dataclasses import dataclass, fields
from datetime import datetime
from typing import Optional


@dataclass
class RawWeatherRecord:
    id: int
    url: str
    requested_at:datetime
    responded_at: Optional[datetime]
    html: Optional[str]
    fetch_error: Optional[str]
    parse_error: Optional[str]


WEATHER_COLUMNS = [f.name for f in fields(RawWeatherRecord)]