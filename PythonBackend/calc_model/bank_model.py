from typing import Union, Dict

import numpy as np
import pandas as pd

from .abstract_model import AbstractModel


def winsorization(x: np.ndarray, left: float, right: float) -> np.ndarray:
    return np.clip(x, left, right)


def min_max_norm(x: np.ndarray, left: float, right: float) -> np.ndarray:
    return (x - left) / (right - left)


def calibration(x: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    return np.clip(np.exp(alpha * x + beta), None, 1)


def linear_transformer(x):
    return x


def neg_log_transformer(x: Union[float, np.ndarray]):
    return -np.log(x + 0.0001)


class WeightTuple:
    def __init__(self, wins_left=None, wins_right=None, transform=None, norm_left=None, norm_right=None, w=None):
        self.winsLeft = -np.inf if wins_left is None else wins_left
        self.winsRight = np.inf if wins_right is None else wins_right
        self.transform = linear_transformer if transform is None else transform
        self.normLeft = 0 if norm_left is None else norm_left
        self.normRight = 1 if norm_right is None else norm_right
        self.weight = 0.0 if w is None else w

    def calc(self, x: Union[float, np.ndarray]):
        return self.weight * min_max_norm(self.transform(winsorization(x, self.winsLeft, self.winsRight)),
                                          self.normLeft,
                                          self.normRight)


class BankModel(AbstractModel):

    def __init__(self, name: str, plots: Dict[str, bytes], bias: float, calibration_alpha: float,
                 calibration_beta: float, weight_pairs: Dict[str, WeightTuple]):
        super().__init__(name, plots)
        self.bias = bias
        self.calibration_alpha = calibration_alpha
        self.calibration_beta = calibration_beta
        self.weight_pairs = weight_pairs

    def __calc_col(self, x: pd.Series):
        name = x.name.split('_')[-1]
        w_pair = self.weight_pairs[name]
        return w_pair.calc(x)

    def predict_proba(self, item: pd.DataFrame) -> Union[float, np.ndarray]:
        item['managementScore'] = item[['PositiveShareholders',
                                        'NegativeShareholders',
                                        'DesireToInvest',
                                        'WithdrawalFunds',
                                        'OwnershipConflict',
                                        'ManagementShareholdersConflict']].mean(axis=1)
        item['DealRatio'] = item[['OwnFundsTransaction', 'RelevantRepayment']].mean(axis=1)
        proba = calibration(self.bias +
                            self.__calc_col(item['MacroeconomicRisk']) +
                            self.__calc_col(item['IndustryRating']) +
                            self.__calc_col(item['BusinessModelRisk']) +
                            self.__calc_col(item['year_0_NetProfitMargin']) +
                            self.__calc_col(item['year_0_FinancialDebtRevenueRatio']) +
                            self.__calc_col(item['year_0_InstantLiquidity']) +
                            self.__calc_col(item['managementScore']) +
                            self.__calc_col(item['DealRatio']), self.calibration_alpha, self.calibration_beta)
        if len(proba) == 1:
            return proba[0]
        return proba
