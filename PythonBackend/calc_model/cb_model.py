import numpy as np
import pandas as pd
from catboost import CatBoostClassifier

from .abstract_model import AbstractModel


class CatBoostModel(AbstractModel):
    def __init__(self, name, plots, cols, cb):
        super().__init__(name, plots)
        assert isinstance(cols, np.ndarray)
        assert isinstance(cb, CatBoostClassifier)
        self.cols = cols
        self.model = cb

    def predict_proba(self, item: pd.DataFrame) -> float:
        obj = item[self.cols]
        proba = self.model.predict_proba(obj)[:, 1]
        if len(proba) == 1:
            return proba[0]
        return proba
