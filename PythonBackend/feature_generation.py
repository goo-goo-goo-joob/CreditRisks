import numpy as np
import pandas as pd


def add_features(x: pd.DataFrame):
    method_cols = ['financialDebt', 'CreditLeverage', 'FinancialIndependence', 'DebtBurden',
                   'CoverageDebtWithAccumulatedProfit',
                   'ReturnAssetsNetProfit', 'ReturnAssetsOperatingProfit', 'OperatingMargin', 'NetProfitMargin',
                   'LiabilityCoverageOperatingProfit', 'OperatingProfitFinancialDebtRatio', 'FinancialDebtRevenueRatio',
                   'CurrentLiquidity', 'QuickLiquidity', 'InstantLiquidity', 'LevelOfOperatingAssets', 'turnoverDebtorDebt',
                   'turnoverReserves', 'turnoverCreditDebt', 'FinancialCycle', 'AssetTurnover']

    for year in [0, -1]:
        x[f'year_{year}_okved2'] = x[f'year_{year}_okved'].str.extract(r'(^[0-9]+.[0-9]+)').fillna('__null__')
        x[f'year_{year}_okved1'] = x[f'year_{year}_okved'].str.extract(r'(^[0-9]+)').fillna('__null__')

        x[f'year_{year}_financialDebt'] = x[[f'year_{year}_1500', f'year_{year}_1400', f'year_{year}_1250']].sum(axis=1)
        financial_debt = x[f'year_{year}_financialDebt']
        x[f'year_{year}_CreditLeverage'] = x[f'year_{year}_1300'] / x[f'year_{year}_1500']
        x[f'year_{year}_FinancialIndependence'] = x[f'year_{year}_1300'] / x[f'year_{year}_1600']
        x[f'year_{year}_DebtBurden'] = financial_debt / x[f'year_{year}_1600']
        x[f'year_{year}_CoverageDebtWithAccumulatedProfit'] = x[f'year_{year}_1300'] / financial_debt
        x[f'year_{year}_ReturnAssetsNetProfit'] = x[f'year_{year}_2400'] / x[f'year_{year}_1600']
        x[f'year_{year}_ReturnAssetsOperatingProfit'] = x[f'year_{year}_2200'] / x[f'year_{year}_1600']
        x[f'year_{year}_OperatingMargin'] = x[f'year_{year}_2200'] / x[[f'year_{year}_2110', f'year_{year}_financialDebt']].max(axis=1)
        x[f'year_{year}_NetProfitMargin'] = x[f'year_{year}_2400'] / x[[f'year_{year}_2110', f'year_{year}_financialDebt']].max(axis=1)
        x[f'year_{year}_LiabilityCoverageOperatingProfit'] = x[f'year_{year}_2200'] / x[[f'year_{year}_1400', f'year_{year}_1500']].sum(axis=1)
        x[f'year_{year}_OperatingProfitFinancialDebtRatio'] = x[f'year_{year}_2200'] / financial_debt
        x[f'year_{year}_FinancialDebtRevenueRatio'] = financial_debt / x[f'year_{year}_2110']
        x[f'year_{year}_CurrentLiquidity'] = x[f'year_{year}_1200'] / x[f'year_{year}_1500']
        x[f'year_{year}_QuickLiquidity'] = (x[f'year_{year}_1200'] - x[f'year_{year}_1210']) / x[f'year_{year}_1500']
        x[f'year_{year}_InstantLiquidity'] = x[f'year_{year}_1250'] / x[f'year_{year}_1500']
        x[f'year_{year}_LevelOfOperatingAssets'] = (x[f'year_{year}_1210'] + x[f'year_{year}_1230'] - x[f'year_{year}_1520']) / x[f'year_{year}_2110']
        x[f'year_{year}_turnoverDebtorDebt'] = 365 * (x[f'year_{year}_1230'] + x[f'year_{year - 1}_1230']) / (2 * x[f'year_{year}_2110'])
        x[f'year_{year}_turnoverReserves'] = 365 * (x[f'year_{year}_1210'] + x[f'year_{year - 1}_1210']) / (2 * x[f'year_{year}_2110'])
        x[f'year_{year}_turnoverCreditDebt'] = 365 * (x[f'year_{year}_1520'] + x[f'year_{year - 1}_1520']) / (2 * x[f'year_{year}_2110'])
        x[f'year_{year}_FinancialCycle'] = x[f'year_{year}_turnoverDebtorDebt'] + x[f'year_{year}_turnoverReserves'] - x[f'year_{year}_turnoverCreditDebt']
        x[f'year_{year}_AssetTurnover'] = x[f'year_{year}_2110'] / x[f'year_{year}_1600']
        for col in method_cols:
            x[f'year_{year}_{col}'].replace(np.inf, 1000000, inplace=True)
            x[f'year_{year}_{col}'].replace(-np.inf, -1000000, inplace=True)
            x[f'year_{year}_{col}'].replace(np.nan, 0, inplace=True)
