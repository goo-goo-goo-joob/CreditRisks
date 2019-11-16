import io
import zipfile

import numpy as np
import pandas as pd

from calc_model import AbstractModel


class RandomModel(AbstractModel):
    """
    Возвращает вероятность дефолта в соответствии с биномиальным распределением
    """
    rand_n = None
    rand_p = None
    rand_count = None

    def __init__(self, name: str, file_stream: io.BytesIO):
        super().__init__(name, file_stream)
        with zipfile.ZipFile(file_stream) as zfile:
            with zfile.open('data.txt') as f:
                self.rand_n, self.rand_p, self.rand_count = map(float, f.readline().split())
                self.rand_count = int(self.rand_count)

    def predict_proba(self, item: pd.Series) -> float:
        return np.random.binomial(self.rand_n, self.rand_p, self.rand_count).sum() / self.rand_count
