import io

import pandas as pd

from .abstract_model import AbstractModel


class BankModel(AbstractModel):

    def __init__(self, name: str, file_stream: io.BytesIO):
        super().__init__(name, file_stream)

    def predict_proba(self, item: pd.DataFrame) -> float:
        return float('nan')
