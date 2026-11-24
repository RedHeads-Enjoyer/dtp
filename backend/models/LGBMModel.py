from lightgbm import LGBMRegressor
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit, RandomizedSearchCV
from models.AccidentModel import AccidentModel
from services.config import CV_SPLITS


class LGBMModel(AccidentModel):
    def __init__(self, conn):
        super().__init__(3, conn)
        self.model = None

    def fit(self, X, y):
        param_grid = {
            "n_estimators": [100, 300, 500],
            "learning_rate": [0.01, 0.05, 0.1],
            "max_depth": [3, 5, 7],
        }

        search = RandomizedSearchCV(
            estimator=LGBMRegressor(random_state=self.random_seed, verbose=-1),
            param_distributions=param_grid,
            n_iter=10,
            scoring="neg_mean_absolute_error",
            cv=TimeSeriesSplit(n_splits=CV_SPLITS),
            random_state=self.random_seed,
            n_jobs=-1,
        )

        search.fit(X, y)

        self.model = search.best_estimator_
        self.params = {
            **search.best_params_
        }

    def predict(self, X):
        return self.model.predict(X)
