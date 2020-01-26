import io
import zipfile

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
        self.plots = {}
        with zipfile.ZipFile(file_stream) as zfile:
            for file in zfile.filelist:
                if file.filename.startswith('plots/') and file.file_size > 0:
                    file_name = file.filename.split('/')[1].split('.')[0]
                    with zfile.open(file) as f:
                        self.plots[file_name] = f.read()

    def predict_proba(self, item: pd.DataFrame) -> float:
        """
        Calculate default probability of a company using custom model

        :param item: pandas Series, index - names, values - values
        :return: float - default probability

        """
        raise NotImplementedError()
