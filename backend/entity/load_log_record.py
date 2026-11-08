from dataclasses import dataclass, fields
from datetime import datetime
from typing import Optional


@dataclass
class LoadLogRecord:
    id: int
    file_name: Optional[str]
    started_at: datetime
    finished_at: Optional[datetime]
    status: str
    rows_total: Optional[int]
    rows_inserted: Optional[int]
    error: Optional[str]


LOAD_LOG_COLUMNS = [f.name for f in fields(LoadLogRecord)]