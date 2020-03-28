from typing import Union, Dict

import numpy as np
import pandas as pd


class AbstractModel(object):
    def __init__(self, name: str, plots: Dict[str, bytes]):
        """
        Load model info

        :param name: model name
        :param plots: Dict of saved images
        """
        self.name = name
        self.plots = plots

    def predict_proba(self, item: pd.DataFrame) -> Union[float, np.ndarray]:
        """
        Calculate default probability of a company using custom model

        :param item: pandas Series, index - names, values - values
        :return: float - default probability

        """
        raise NotImplementedError()
