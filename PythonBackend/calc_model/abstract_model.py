import pandas as pd


class AbstractModel(object):
    def __init__(self, filename: str):
        """
        Load model from a file
        
        :param filename: model dump
        """
        raise NotImplementedError()

    def predict_proba(self, item: pd.Series) -> float:
        """
        Calculate default probability of a company using custom model

        :param item: pandas Series, index - names, values - values
        :return: float - default probability

        """
        raise NotImplementedError()
