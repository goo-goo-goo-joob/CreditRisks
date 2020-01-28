import io

import numpy as np
import pandas as pd

from .abstract_model import AbstractModel


def winsorization(x: pd.Series, l: int, r: int) -> pd.Series:
    return x.apply(lambda xx: r if xx > r else xx if xx > l else l)


def min_max_norm(X: pd.Series, l: int, r: int) -> pd.Series:
    return (X - l) / (r - l)


def calibration(X: pd.Series, alpha: float, beta: float) -> pd.Series:
    return X.apply(lambda x: min(1, np.exp(alpha * x + beta)))


class WeightTuple:
    winsLeft = None
    winsRight = None
    transform = None
    normLeft = None
    normRight = None
    weight = None

    def __init__(self, WinsLeft=None, WinsRight=None, Transform=None, NormLeft=None, NormRight=None, Weight=None):
        self.winsLeft = -np.inf if WinsLeft is None else WinsLeft
        self.winsRight = np.inf if WinsRight is None else WinsRight
        self.transform = (lambda x: x) if Transform is None else Transform
        self.normLeft = 0 if NormLeft is None else NormLeft
        self.normRight = 1 if NormRight is None else NormRight
        self.weight = 0 if Weight is None else Weight

    def calc(self, x: float):
        return self.weight * min_max_norm(self.transform(winsorization(x, self.winsLeft, self.winsRight)),
                                          self.normLeft,
                                          self.normRight)


MacroeconomicRiskP = WeightTuple(Weight=-2.18)
IndustryRatingP = WeightTuple(Weight=-0.393, NormLeft=2, NormRight=3)
BusinessModelRiskP = WeightTuple(Weight=-0.656)
NetProfitMarginP = WeightTuple(Weight=-0.379, NormLeft=0.001, NormRight=0.025, WinsLeft=-0.049, WinsRight=0.082)
FinancialDebtRevenueRatioP = WeightTuple(Weight=-0.369, NormLeft=0.322, NormRight=2.684, WinsRight=3.842,
                                         Transform=lambda x: -np.log(x + 0.0001))
InstantLiquidityP = WeightTuple(Weight=-0.734, NormLeft=0.002, NormRight=0.048, WinsRight=0.068)
ManagementScoreP = WeightTuple(Weight=-0.371, NormRight=0.167, WinsRight=0.068)
DealRatioP = WeightTuple(Weight=-0.812)
Bias = 0.257


class BankModel(AbstractModel):

    def __init__(self, name: str, file_stream: io.BytesIO):
        super().__init__(name, file_stream)

    def predict_proba(self, item: pd.DataFrame) -> float:
        item['financialDebt'] = item['year_0_15003'] + item['year_0_14003'] + item['year_0_12503']
        item['NetProfitMargin'] = item['year_0_24003'] / pd.concat([item['year_0_21103'], item['financialDebt']],
                                                                   axis=1).max(axis=1)
        item['FinancialDebtRevenueRatio'] = item['financialDebt'] / item['year_0_21103']
        item['InstantLiquidity'] = item['year_0_12503'] / item['year_0_15003']
        item['managementScore'] = (item['PositiveShareholders'] +
                                   item['NegativeShareholders'] +
                                   item['DesireToInvest'] +
                                   item['WithdrawalFunds'] +
                                   item['OwnershipConflict'] +
                                   item['ManagementShareholdersConflict']) / 6
        item['DealRatio'] = (item['OwnFundsTransaction'] + item['RelevantRepayment']) / 2
        proba = calibration(Bias + MacroeconomicRiskP.calc(item['MacroeconomicRisk']) +
                            IndustryRatingP.calc(item['IndustryRating']) +
                            BusinessModelRiskP.calc(item['BusinessModelRisk']) +
                            NetProfitMarginP.calc(item['NetProfitMargin']) +
                            FinancialDebtRevenueRatioP.calc(item['FinancialDebtRevenueRatio']) +
                            InstantLiquidityP.calc(item['InstantLiquidity']) +
                            ManagementScoreP.calc(item['managementScore']) +
                            DealRatioP.calc(item['DealRatio']), 0.528, -1.014)
        if len(proba) == 1:
            return proba[0]
        return proba
