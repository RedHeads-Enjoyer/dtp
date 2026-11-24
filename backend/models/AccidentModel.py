import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import numpy as np
from sklearn.metrics import mean_absolute_error

from models.data import load_features
from services.config import SEED


class AccidentModel(ABC):
    def __init__(self, model_id: int, conn):
        self.conn = conn
        self.model_id = model_id
        self.random_seed = SEED
        self.version = None
        self.params = None
        self.artifact_path = None
        self.train_start = None
        self.train_end = None
        self.test_start = None
        self.test_end = None
        self.n_train = None
        self.n_test = None
        self.mae_train = None
        self.mae_test = None
        self.mase_train = None
        self.mase_test = None

    def load_data(self):
        X_train, X_test, y_train, y_test, self.version = load_features()
        self.n_train = len(X_train)
        self.n_test = len(X_test)

        return X_train, X_test, y_train, y_test

    def evaluate(self, X_train, X_test, y_train, y_test) -> None:
        y_pred_train = self.predict(X_train)
        y_pred_test = self.predict(X_test)

        self.mae_train = mean_absolute_error(y_train, y_pred_train)
        self.mae_test = mean_absolute_error(y_test, y_pred_test)

        self.mase_train = self._mase(y_train, y_pred_train, y_train)
        self.mase_test = self._mase(y_test, y_pred_test, y_train)



    def run(self) -> tuple[Any, Any]:
        """Шаблонный метод: задаёт порядок шагов."""
        X_train, X_test, y_train, y_test = self.load_data()
        self.train_start = datetime.now()
        self.fit(X_train, y_train)
        self.train_end = datetime.now()

        self.test_start = datetime.now()
        self.evaluate(X_train, X_test, y_train, y_test)
        self.test_end = datetime.now()

        self._save()

        return self.mase_test, self.mase_test

    def _save(self) -> None:
        sql = """
              INSERT INTO runs (model_id, params, feature_version, artifact_path, random_seed, \
                                train_start, train_end, test_start, test_end, \
                                n_train, n_test, \
                                mae_train, mae_test, mase_train, mase_test)
              VALUES (%(model_id)s, %(params)s, %(feature_version)s, %(artifact_path)s, %(random_seed)s,\
                      %(train_start)s, %(train_end)s, %(test_start)s, %(test_end)s, \
                      %(n_train)s, %(n_test)s, \
                      %(mae_train)s, %(mae_test)s, %(mase_train)s, %(mase_test)s)
              RETURNING id \
              """
        values = {
            "model_id": self.model_id,
            "params": json.dumps(self.params) if self.params is not None else None,
            "feature_version": self.version,
            "artifact_path": self.artifact_path,
            "random_seed": self.random_seed,
            "train_start": self.train_start,
            "train_end": self.train_end,
            "test_start": self.test_start,
            "test_end": self.test_end,
            "n_train": self.n_train,
            "n_test": self.n_test,
            "mae_train": self.mae_train,
            "mae_test": self.mae_test,
            "mase_train": self.mase_train,
            "mase_test": self.mase_test,
        }

        with self.conn.cursor() as cur:
            cur.execute(sql, values)
            self.id = cur.fetchone()[0]
        self.conn.commit()

    @staticmethod
    def _mase(y_true, y_pred, y_train):
        y_true = np.asarray(y_true, dtype=float)
        y_pred = np.asarray(y_pred, dtype=float)
        y_train = np.asarray(y_train, dtype=float)

        mae_model = np.mean(np.abs(y_true - y_pred))
        mae_naive = np.mean(np.abs(np.diff(y_train)))

        return mae_model / mae_naive

    @abstractmethod
    def fit(self, X, y) -> None:
        ...

    @abstractmethod
    def predict(self, X) -> np.ndarray:
        ...