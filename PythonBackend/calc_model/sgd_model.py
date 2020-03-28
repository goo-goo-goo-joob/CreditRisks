import pandas as pd

from .abstract_model import AbstractModel


class SGDModel(AbstractModel):
    def __init__(self, name, plots, cols, sc, lr):
        super().__init__(name, plots)
        self.cols = cols
        self.sc = sc
        self.lr = lr

    def predict_proba(self, item: pd.DataFrame) -> float:
        obj = item[self.cols]
        scaled_data = self.sc.transform(obj)
        proba = self.lr.predict_proba(scaled_data)[:, 1]
        if len(proba) == 1:
            return proba[0]
        return proba
