from typing import Any

from sklearn.model_selection import train_test_split

import pandas as pd

from services.config import TEST_SIZE, SEED
from services.feature import get_features


def load_features(withDate: bool = False) -> tuple[Any, Any, Any, Any, Any]:
    records = get_features(1, -1)
    df = pd.DataFrame(records["items"])
    df["date"] = pd.to_datetime(df["date"])

    num_cols = df.columns.drop("date")
    df[num_cols] = df[num_cols].apply(pd.to_numeric)

    version = df["version"].max()

    if (withDate):
        df = df.drop(columns=["version"])
    else:
        df = df.drop(columns=["date", "version"])

    features = df.drop(columns="accidents")
    targets = df["accidents"]

    X_train, X_test, y_train, y_test = train_test_split(features, targets, shuffle=False, test_size = TEST_SIZE, random_state = SEED)

    return X_train, X_test, y_train, y_test, version

