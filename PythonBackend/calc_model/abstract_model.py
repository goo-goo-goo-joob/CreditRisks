import io

import pandas as pd


class AbstractModel(object):
    name = None

    def __init__(self, name: str, file_stream: io.BytesIO):
        """
        Load model from a file

        :param name: model dump
        :param file_stream: byte stream with model data
        """
        self.name = name

    def predict_proba(self, item: pd.DataFrame) -> float:
        """
        Calculate default probability of a company using custom model

        :param item: pandas Series, index - names, values - values
        :return: float - default probability

        """
        raise NotImplementedError()
