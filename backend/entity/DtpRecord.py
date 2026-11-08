from dataclasses import dataclass, asdict, fields
from datetime import datetime
from typing import Optional


@dataclass
class DtpRecord:
    id: str
    tags: Optional[str]
    category: Optional[str]
    region: Optional[str]
    county: Optional[str]
    address: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    nearby: Optional[str]
    datetime: Optional[datetime]
    light: Optional[str]
    weather: Optional[str]
    road_conditions: Optional[str]
    participants_count: Optional[int]
    participant_categories: Optional[str]
    severity: Optional[str]
    dead_count: Optional[int]
    injured_count: Optional[int]

    @classmethod
    def from_csv_row(cls, row: dict) -> "DtpRecord":
        def val(key):
            v = row.get(key)
            return v if v else None

        def to_int(key):
            v = val(key)
            return int(v) if v is not None else None

        def to_float(key):
            v = val(key)
            return float(v.replace(",", ".")) if v is not None else None

        def to_dt(key):
            v = val(key)
            return datetime.fromisoformat(v) if v is not None else None

        return cls(
            id=row["id"],
            tags=val("tags"),
            category=val("category"),
            region=val("region"),
            county=val("county"),
            address=val("address"),
            longitude=to_float("longitude"),
            latitude=to_float("latitude"),
            nearby=val("nearby"),
            datetime=to_dt("datetime"),
            light=val("light"),
            weather=val("weather"),
            road_conditions=val("road_conditions"),
            participants_count=to_int("participants_count"),
            participant_categories=val("participant_categories"),
            severity=val("severity"),
            dead_count=to_int("dead_count"),
            injured_count=to_int("injured_count"),
        )

    def to_params(self) -> dict:
        return asdict(self)

DTP_COLUMNS = [f.name for f in fields(DtpRecord)]