import os
import pickle

import numpy as np
import pandas as pd

import feature_impact
from feature_generation import add_features

RESULT_DTYPES = {'DesireToInvest': np.int32,
                 'IndustryRating': np.int32,
                 'ManagementShareholdersConflict': np.int32,
                 'NegativeShareholders': np.int32,
                 'OwnFundsTransaction': np.int32,
                 'OwnershipConflict': np.int32,
                 'PositiveShareholders': np.int32,
                 'RelevantRepayment': np.int32,
                 'WithdrawalFunds': np.int32,
                 'region': np.uint32,
                 'year_-1_1100': np.float32,
                 'year_-1_1150': np.float32,
                 'year_-1_1200': np.float32,
                 'year_-1_1210': np.float32,
                 'year_-1_1230': np.float32,
                 'year_-1_1250': np.float32,
                 'year_-1_1300': np.float32,
                 'year_-1_1310': np.float32,
                 'year_-1_1400': np.float32,
                 'year_-1_1500': np.float32,
                 'year_-1_1510': np.float32,
                 'year_-1_1520': np.float32,
                 'year_-1_1600': np.float32,
                 'year_-1_1700': np.float32,
                 'year_-1_2100': np.float32,
                 'year_-1_2110': np.float32,
                 'year_-1_2120': np.float32,
                 'year_-1_2200': np.float32,
                 'year_-1_2300': np.float32,
                 'year_-1_2400': np.float32,
                 'year_-1_okved': str,
                 'year_-2_1100': np.float32,
                 'year_-2_1150': np.float32,
                 'year_-2_1200': np.float32,
                 'year_-2_1210': np.float32,
                 'year_-2_1230': np.float32,
                 'year_-2_1250': np.float32,
                 'year_-2_1300': np.float32,
                 'year_-2_1310': np.float32,
                 'year_-2_1400': np.float32,
                 'year_-2_1500': np.float32,
                 'year_-2_1510': np.float32,
                 'year_-2_1520': np.float32,
                 'year_-2_1600': np.float32,
                 'year_-2_1700': np.float32,
                 'year_-2_2100': np.float32,
                 'year_-2_2110': np.float32,
                 'year_-2_2120': np.float32,
                 'year_-2_2200': np.float32,
                 'year_-2_2300': np.float32,
                 'year_-2_2400': np.float32,
                 'year_0_1100': np.float32,
                 'year_0_1150': np.float32,
                 'year_0_1200': np.float32,
                 'year_0_1210': np.float32,
                 'year_0_1230': np.float32,
                 'year_0_1250': np.float32,
                 'year_0_1300': np.float32,
                 'year_0_1310': np.float32,
                 'year_0_1400': np.float32,
                 'year_0_1500': np.float32,
                 'year_0_1510': np.float32,
                 'year_0_1520': np.float32,
                 'year_0_1600': np.float32,
                 'year_0_1700': np.float32,
                 'year_0_2100': np.float32,
                 'year_0_2110': np.float32,
                 'year_0_2120': np.float32,
                 'year_0_2200': np.float32,
                 'year_0_2300': np.float32,
                 'year_0_2400': np.float32,
                 'year_0_okved': str}


def get_models(path=''):
    result = {}
    for file in os.listdir(path):
        if not file.endswith('.pkl'):
            continue
        with open(os.path.join(path, file), 'rb') as f:
            clf = pickle.load(f)
        name = clf.name
        result[name] = clf
    return result


def dict_to_df(data):
    df = pd.DataFrame.from_dict(data, orient='index').T
    res_types = {}
    for key, dtype in RESULT_DTYPES.items():
        if key in df.columns:
            res_types[key] = dtype
        if dtype == np.float:
            df[key] = df[key].str.replace(',', '.')
    return df.astype(dtype=res_types)


class CalcHandler:
    def __init__(self, path):
        self.models = get_models(path)

    def calc_probability(self, data):
        df = dict_to_df(data)
        add_features(df)

        result = {}
        for name, model in self.models.items():
            value = None
            try:
                value = model.predict_proba(df)
            except Exception as e:
                value = float('nan')
            finally:
                result[name] = value
        return result

    def get_plots(self, name):
        return self.models[name].plots

    def get_impact(self, name, data, feature, head, tail):
        df = dict_to_df(data)
        add_features(df)

        return feature_impact.plt_graph_to_base64(
            model=self.models[name],
            data=df,
            feature=feature,
            head=head,
            tail=tail
        )
