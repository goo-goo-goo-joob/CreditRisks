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


methodCols = ['financialDebt', 'CreditLeverage', 'FinancialIndependence', 'DebtBurden',
              'CoverageDebtWithAccumulatedProfit',
              'ReturnAssetsNetProfit', 'ReturnAssetsOperatingProfit', 'OperatingMargin', 'NetProfitMargin',
              'LiabilityCoverageOperatingProfit', 'OperatingProfitFinancialDebtRatio', 'FinancialDebtRevenueRatio',
              'CurrentLiquidity', 'QuickLiquidity', 'InstantLiquidity', 'LevelOfOperatingAssets', 'turnoverDebtorDebt',
              'turnoverReserves', 'turnoverCreditDebt', 'FinancialCycle', 'AssetTurnover']


def add_features(X: pd.DataFrame):
    for year in ['-1', '0']:
        y = '3' if year == '0' else '9'
        z = '9' if year == '0' else '4'
        X[f'year_{year}_financialDebt'] = X[f'year_0_1500{y}'] + X[f'year_0_1400{y}'] + X[f'year_0_1250{y}']
        financial_debt = X[f'year_{year}_financialDebt']
        X[f'year_{year}_CreditLeverage'] = X[f'year_0_1300{y}'] / X[f'year_0_1500{y}']
        X[f'year_{year}_FinancialIndependence'] = X[f'year_0_1300{y}'] / X[f'year_0_1600{y}']
        X[f'year_{year}_DebtBurden'] = financial_debt / X[f'year_0_1600{y}']
        X[f'year_{year}_CoverageDebtWithAccumulatedProfit'] = X[f'year_0_1300{y}'] / financial_debt
        X[f'year_{year}_ReturnAssetsNetProfit'] = X[f'year_0_2400{y}'] / X[f'year_0_1600{y}']
        X[f'year_{year}_ReturnAssetsOperatingProfit'] = X[f'year_0_2200{y}'] / X[f'year_0_1600{y}']
        X[f'year_{year}_OperatingMargin'] = X[f'year_0_2200{y}'] / pd.concat([X[f'year_0_2110{y}'], financial_debt],
                                                                             axis=1).max(axis=1)
        X[f'year_{year}_NetProfitMargin'] = X[f'year_0_2400{y}'] / pd.concat([X[f'year_0_2110{y}'], financial_debt],
                                                                             axis=1).max(axis=1)  # impotant
        X[f'year_{year}_LiabilityCoverageOperatingProfit'] = X[f'year_0_2200{y}'] / (
                X[f'year_0_1400{y}'] + X[f'year_0_1500{y}'])
        X[f'year_{year}_OperatingProfitFinancialDebtRatio'] = X[f'year_0_2200{y}'] / financial_debt
        X[f'year_{year}_FinancialDebtRevenueRatio'] = financial_debt / X[f'year_0_2110{y}']  # impotant
        X[f'year_{year}_CurrentLiquidity'] = X[f'year_0_1200{y}'] / X[f'year_0_1500{y}']
        X[f'year_{year}_QuickLiquidity'] = (X[f'year_0_1200{y}'] - X[f'year_0_1210{y}']) / X[f'year_0_1500{y}']
        X[f'year_{year}_InstantLiquidity'] = X[f'year_0_1250{y}'] / X[f'year_0_1500{y}']  # impotant
        X[f'year_{year}_LevelOfOperatingAssets'] = (X[f'year_0_1210{y}'] + X[f'year_0_1230{y}'] - X[
            f'year_0_1520{y}']) / X[f'year_0_2110{y}']
        X[f'year_{year}_turnoverDebtorDebt'] = 365 * (X[f'year_0_1230{y}'] + X[f'year_{year}_1230{z}']) / (
                2 * X[f'year_0_2110{y}'])
        X[f'year_{year}_turnoverReserves'] = 365 * (X[f'year_0_1210{y}'] + X[f'year_{year}_1210{z}']) / (
                2 * X[f'year_0_2110{y}'])
        X[f'year_{year}_turnoverCreditDebt'] = 365 * (X[f'year_0_1520{y}'] + X[f'year_{year}_1520{z}']) / (
                2 * X[f'year_0_2110{y}'])
        X[f'year_{year}_FinancialCycle'] = X[f'year_{year}_turnoverDebtorDebt'] + X[f'year_{year}_turnoverReserves'] - \
                                           X[f'year_{year}_turnoverCreditDebt']
        X[f'year_{year}_AssetTurnover'] = X[f'year_0_2110{y}'] / X[f'year_0_1600{y}']
        for col in methodCols:
            X[f'year_{year}_{col}'].replace(np.nan, 0, inplace=True)


class LRModel(AbstractModel):
    def __init__(self, name, plots, input_cols, cols, ce, wz, sc, lr):
        super().__init__(name, plots)
        assert isinstance(input_cols, np.ndarray)
        assert isinstance(cols, np.ndarray)
        assert isinstance(ce, category_encoders.CatBoostEncoder)
        assert isinstance(wz, Winsorizator)
        assert isinstance(sc, StandardScaler)
        assert isinstance(lr, LogisticRegression)
        self.input_cols = input_cols
        self.cols = cols
        self.ce = ce
        self.wz = wz
        self.sc = sc
        self.lr = lr

    def predict_proba(self, item: pd.DataFrame) -> Union[float, np.ndarray]:
        item = item[self.input_cols]
        add_features(item)
        item = item[self.cols]
        item = self.ce.transform(item)
        self.wz.transform(item)
        item = self.sc.transform(item)
        proba = self.lr.predict_proba(item)[:, 1]
        if len(proba) == 1:
            return proba[0]
        return proba
