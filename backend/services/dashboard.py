from models.BaseModel import BaseModel
from models.data import load_features

import joblib
import pandas as pd


def get_dashboard_data(conn) -> dict:
    _, X_test, _, y_test, _ = load_features(withDate=True)

    test_dates  = X_test["date"].dt.strftime("%Y-%m-%d").tolist()
    actual_test = y_test.tolist()

    return {
        "metrics":  _build_metrics(conn),
        "forecast": _build_forecast(conn, X_test, test_dates, actual_test),
    }


def _build_metrics(conn) -> list[dict]:
    model_map = {1: "Baseline", 2: "Ridge", 3: "LightGBM"}
    metrics = []

    for model_id, model_name in model_map.items():
        row = _fetch_last_run(conn, model_id)
        if row:
            metrics.append({
                "model_name": model_name,
                "mae_test":   round(row["mae_test"],   5),
                "mase_test":  round(row["mase_test"],  5),
            })

    if metrics:
        best = min(metrics, key=lambda m: m["mase_test"])
        for m in metrics:
            m["is_best"] = m["model_name"] == best["model_name"]

    return metrics


def _build_forecast(conn, X_test, test_dates: list, actual_test: list, last_n: int = 30) -> list[dict]:
    next_date  = str((pd.Timestamp(X_test["date"].iloc[-1]) + pd.Timedelta(days=1)).date())
    next_preds = _predict_next(conn, X_test)

    history = [
        {"date": test_dates[i], "actual": actual_test[i]}
        for i in range(max(0, len(test_dates) - last_n), len(test_dates))
    ]

    return history + [{"date": next_date, **next_preds}]


def _predict_next(conn, X_test) -> dict:
    X = X_test.drop(columns=["date"]).iloc[[-1]]
    return {
        "baseline": _predict_baseline(X),
        "ridge":    _predict_sklearn(conn, model_id=2, X=X),
        "lgbm":     _predict_sklearn(conn, model_id=3, X=X),
    }


def _predict_baseline(X) -> float:
    return round(float(BaseModel().predict(X)[0]))


def _predict_sklearn(conn, model_id: int, X) -> float | None:
    path = _fetch_artifact_path(conn, model_id)
    if path is None:
        return None
    try:
        return round(float(joblib.load(path).predict(X)[0]))
    except Exception:
        return None


def _fetch_last_run(conn, model_id: int) -> dict | None:
    sql = """
        SELECT mae_test, mase_test
        FROM runs WHERE model_id = %(model_id)s
        ORDER BY id DESC LIMIT 1
    """
    with conn.cursor() as cur:
        cur.execute(sql, {"model_id": model_id})
        row = cur.fetchone()

    if row is None:
        return None

    mae_test, mase_test = row
    return {
        "mae_test":   mae_test,
        "mase_test":  mase_test,
    }


def _fetch_artifact_path(conn, model_id: int) -> str | None:
    sql = """
        SELECT artifact_path FROM runs
        WHERE model_id = %(model_id)s AND artifact_path IS NOT NULL
        ORDER BY id DESC LIMIT 1
    """
    with conn.cursor() as cur:
        cur.execute(sql, {"model_id": model_id})
        row = cur.fetchone()

    return row[0] if row else None
