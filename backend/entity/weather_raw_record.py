from dataclasses import dataclass, fields
from datetime import datetime
from typing import Optional


@dataclass
class WeatherRawRecord:
    url: str
    requested_at:datetime
    responded_at: Optional[datetime]
    html: Optional[str]
    fetch_error: Optional[str]
    parse_error: Optional[str]


WEATHER_RAW_COLUMNS = [f.name for f in fields(WeatherRawRecord)]