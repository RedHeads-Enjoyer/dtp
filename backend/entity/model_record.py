from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class ModelRecord:
    id: int
    name: str
    params: dict[str, Any]
    feature_version: int
    random_seed: int
    artifact_path: str
    train_start: datetime
    train_end: datetime
    test_start: datetime
    test_end: datetime
    n_train: int
    n_test: int
    mae_train: float
    mae_test: float
    mase_train: float
    mase_test: float