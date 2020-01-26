import io
import os
import zipfile

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier

from .abstract_model import AbstractModel


class CatBModel(AbstractModel):
    cols = None
    clf = CatBoostClassifier()
    filename = 'catboost_cant_read_from_memory'

    def __init__(self, name: str, file_stream: io.BytesIO):
        super().__init__(name, file_stream)
        with zipfile.ZipFile(file_stream) as zfile:
            with zfile.open('colsC.npy') as f:
                self.cols = np.load(f, allow_pickle=True)
            with zfile.open('model4_1') as f, open(CatBModel.filename, 'wb') as cf:
                cf.write(f.read())
            self.clf.load_model(CatBModel.filename)
            os.remove(CatBModel.filename)

    def predict_proba(self, item: pd.DataFrame) -> float:
        obj = item[self.cols]
        proba = self.clf.predict_proba(obj)[:, 1]
        if len(proba) == 1:
            return proba[0]
        return proba
