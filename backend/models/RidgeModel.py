from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from models.AccidentModel import AccidentModel
from services.config import CV_SPLITS


class RidgeModel(AccidentModel):
    def __init__(self, conn):
        super().__init__(2, conn)
        self.model = None
        self.best_params = None

    def fit(self, X, y):
        param_grid = {
            "alpha": [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0],
            "solver": ["auto", "svd", "cholesky", "lsqr"],
        }

        grid_search = GridSearchCV(
            estimator=Ridge(),
            param_grid=param_grid,
            scoring="neg_mean_squared_error",
            cv=TimeSeriesSplit(n_splits=CV_SPLITS),
            n_jobs=-1,
        )
        grid_search.fit(X, y)

        self.model = grid_search.best_estimator_
        self.best_params = grid_search.best_params_

        self.params = {
            "alpha": float(self.best_params["alpha"]),
            "solver": self.best_params["solver"],
        }

    def predict(self, X):
        return self.model.predict(X)
