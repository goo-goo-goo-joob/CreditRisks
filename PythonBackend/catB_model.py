import io
import zipfile

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

from .abstract_model import AbstractModel


class CatBModel(AbstractModel):
    cols = None
    grB = CatBoostClassifier()

    def __init__(self, name: str, file_stream: io.BytesIO):
        super().__init__(name, file_stream)
        with zipfile.ZipFile(file_stream) as zfile:
            with zfile.open('colsС.npy') as f:
                self.cols = np.load(f, allow_pickle=True)
            with zfile.open('model4_1') as f:
                self.lr = grB.load_model(f)

    def predict_proba(self, item: pd.DataFrame) -> float:
        obj = item[self.cols]
        proba = self.lr.predict_proba(obj)[:, 1]
        return proba[0]
