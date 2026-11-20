from models.AccidentModel import AccidentModel


class BaseModel(AccidentModel):
    def __init__(self, conn):
        super().__init__(1, conn)

    def fit(self, X, y):
        self.params = {
            "value": "accidents_lag_1"
        }
        pass

    def predict(self, X):
        return X["accidents_lag_1"].to_numpy()