import pandas as pd

def convert_to_jpy(data, exchange_rate):
    """
    ドルを円に換算する関数

    Parameters:
    data (pd.DataFrame): ドル建てのデータフレーム
    exchange_rate (pd.DataFrame): 為替レートのデータフレーム

    Returns:
    pd.DataFrame: 円建てのデータフレーム
    """
    data['Close_JPY'] = data['Close'] * exchange_rate['Close']
    return data