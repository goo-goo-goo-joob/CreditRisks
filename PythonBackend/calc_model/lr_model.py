from typing import Union

import category_encoders
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from .abstract_model import AbstractModel


class Winsorizator:
    def __init__(self, left, right):
        assert 0 <= left <= 1 and 0 <= right <= 1
        self.left = left
        self.right = right
        self.data = None

    def fit(self, x: pd.DataFrame):
        self.data = x.quantile([self.left, self.right], axis=0)
        return self

    def transform(self, x: pd.DataFrame):
        x.clip(self.data.iloc[0], self.data.iloc[1], axis='columns', inplace=True)

    def fit_transform(self, x):
        self.fit(x).transform(x)


class LRModel(AbstractModel):
    def __init__(self, name, plots, cols, cat_cols, ce, wz, sc, lr):
        super().__init__(name, plots)
        assert isinstance(cols, np.ndarray)
        assert isinstance(cat_cols, np.ndarray)
        assert isinstance(ce, category_encoders.CatBoostEncoder)
        assert isinstance(wz, Winsorizator)
        assert isinstance(sc, StandardScaler)
        assert isinstance(lr, LogisticRegression)
        self.cols = cols
        self.cat_cols = cat_cols
        self.float_cols = sorted(list(set(self.cols) - set(self.cat_cols)))
        self.ce = ce
        self.wz = wz
        self.sc = sc
        self.lr = lr

    def predict_proba(self, item: pd.DataFrame) -> Union[float, np.ndarray]:
        item = item[self.cols]
        item_cat = self.ce.transform(item[self.cat_cols])
        item_float = item[self.float_cols].copy()
        self.wz.transform(item_float)
        item = np.hstack([item_float, item_cat])
        item = self.sc.transform(item)
        proba = self.lr.predict_proba(item)[:, 1]
        if len(proba) == 1:
            return proba[0]
        return proba
