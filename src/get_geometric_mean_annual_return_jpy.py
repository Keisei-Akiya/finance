import pandas as pd
import numpy as np

def get_geometric_mean_annual_return_jpy(data):
    """
    円建て年次幾何平均リターンを計算する関数

    Parameters:
        data (pd.DataFrame): 円建てのデータフレーム

    Returns:
        float: 与えられたデータセットの円建て年次幾何平均リターン
    """

    data['Return_JPY'] = data['Close_JPY'].pct_change(fill_method=None)

    annual_return = (1 + data['Return_JPY'].dropna()).resample('YE').prod() - 1

    geometric_mean_annual_return = ((np.prod(1 + annual_return) ** (1 / len(annual_return))) - 1) * 100

    return geometric_mean_annual_return