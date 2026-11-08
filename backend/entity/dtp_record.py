from dataclasses import dataclass, asdict, fields
from datetime import datetime
from typing import Any, Optional

INT_FIELDS = {"participants_count", "dead_count", "injured_count"}
FLOAT_FIELDS = {"longitude", "latitude"}
DATETIME_FIELDS = {"datetime"}


def _parse(name: str, raw: Optional[str]) -> Any:
    if raw is None:
        return None
    if name in INT_FIELDS:
        return int(float(raw))
    if name in FLOAT_FIELDS:
        return float(raw.replace(",", "."))
    if name in DATETIME_FIELDS:
        return datetime.fromisoformat(raw)
    return raw


@dataclass
class DtpRecord:
    id: int
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
    def from_csv_row(cls, row: dict[str, str]) -> "DtpRecord":
        values = {}
        for f in fields(cls):
            raw = (row.get(f.name) or "").strip() or None
            values[f.name] = _parse(f.name, raw)
        values["id"] = int(row["id"])
        return cls(**values)

    def to_params(self) -> dict:
        return asdict(self)

DTP_COLUMNS = [f.name for f in fields(DtpRecord)]