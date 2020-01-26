import io
import zipfile

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

from .abstract_model import AbstractModel


class SGDModel(AbstractModel):
    cols = None
    sc = StandardScaler()
    lr = SGDClassifier()

    def __init__(self, name: str, file_stream: io.BytesIO):
        super().__init__(name, file_stream)
        with zipfile.ZipFile(file_stream) as zfile:
            with zfile.open('cols.npy') as f:
                self.cols = np.load(f, allow_pickle=True)
            with zfile.open('standart_scaler.pkl') as f:
                self.sc = joblib.load(f)
            with zfile.open('sgd_model.pkl') as f:
                self.lr = joblib.load(f)

    def predict_proba(self, item: pd.DataFrame) -> float:
        obj = item[self.cols]
        scaled_data = self.sc.transform(obj)
        proba = self.lr.predict_proba(scaled_data)[:, 1]
        return proba[0]
