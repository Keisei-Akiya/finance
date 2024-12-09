import pandas as pd
import numpy as np

def get_geometric_mean_annual_return(data):
    """
    Calculate the geometric mean annual return of a given dataset

    Parameters
    ----------
    data : pandas.DataFrame
        Dataset that contains the stock data

    Returns
    -------
    float
        Geometric mean annual return of the given dataset
    """
    data['Return'] = data['Close'].pct_change()

    annual_return = (1 + data['Return'].dropna()).resample('YE').prod() - 1

    geometric_mean_annual_return = ((np.prod(1 + annual_return) ** (1 / len(annual_return))) - 1) * 100

    return geometric_mean_annual_return