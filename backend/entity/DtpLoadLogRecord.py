from dataclasses import dataclass, asdict, fields
from datetime import datetime
from typing import Optional


@dataclass
class DtpLoadLogRecord:
    id: Optional[int]
    file_name: Optional[str]
    started_at: datetime
    finished_at: Optional[datetime]
    status: str
    rows_total: int
    rows_inserted: int
    error: Optional[str]

    def to_params(self) -> dict:
        return asdict(self)


DTP_LOAD_LOG_COLUMNS = [f.name for f in fields(DtpLoadLogRecord)]