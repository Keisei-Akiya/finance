import polars as pl

def dividends_reinvestment_return(data, initial_shares):
    """
    配当金再投資をシミュレーションする関数
    :param data: 終値と配当金があるデータフレーム
    :param initial_shares: 初日の持ち株数
    :return: 配当金再投資を考慮したデータフレーム
    """
    shares_list = [initial_shares]

    for i in range(1, len(data)):
        # 前日の持ち株数
        prev_shares = shares_list[-1]

        # 当日の配当金
        dividend = data['Dividends'][i]

        # 当日の株価
        price = data['Close'][i]

        # 当日の配当金で購入できる株数
        additional_shares = dividend * prev_shares // price

        # 当日の持ち株数
        shares_list.append(prev_shares + additional_shares)

    data = data.with_columns([
        pl.Series("Shares", shares_list, dtype=pl.Float64)
    ]).with_columns([
        # 持ち株の時価総額
        (pl.col('Close') * pl.col('Shares')).alias('Value')
    ]).with_columns([
        # 時価総額の対数
        (pl.col('Value').log()).alias('LogValue')
    ])
    data = data.with_columns([
        # 対数累積リターン
        (pl.col('LogValue') - data['LogValue'][0]).alias('LogReturn')
    ]).with_columns([
        # 累積リターン
        ((pl.col('LogReturn').exp() - 1) * 100).alias('Return')
    ])

    return data