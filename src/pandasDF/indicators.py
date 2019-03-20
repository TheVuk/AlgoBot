from src.main.algo_bot_objects import AlgoBotObjects as abObj
from src.loghandler import log
import pandas as pd
import numpy as np

# Import Homebrew

# Init Logging Facilities
logger = log.setup_custom_logger('root')


def moving_average(which_df, n):
    """Calculate the moving average for the given data.

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    if str(which_df).lower() == "1min":
        MA = pd.Series(abObj.one_min_pd_DF['close'].tail(n).rolling(n, min_periods=n).mean(), name='MA')
        if 'MA' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(MA.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(MA.tail(1).index, 'MA', MA.tail(1)[0])
    else:
        MA = pd.Series(abObj.three_min_pd_DF['close'].tail(n).rolling(n, min_periods=n).mean(), name='MA')
        if 'MA' not in abObj.three_min_pd_DF.columns:
            abObj.three_min_pd_DF = abObj.three_min_pd_DF.join(MA.tail(1))
        else:
            abObj.three_min_pd_DF._set_value(MA.tail(1).index, 'MA', MA.tail(1)[0])


def exponential_moving_average(which_df, n):
    """

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    if str(which_df).lower() == "1min":
        EMA = pd.Series(abObj.one_min_pd_DF['close'].tail(n).ewm(span=n, min_periods=n).mean(), name='EMA')
        if 'EMA' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(EMA.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(EMA.tail(1).index, 'EMA', EMA.tail(1)[0])
    else:
        EMA = pd.Series(abObj.three_min_pd_DF['close'].tail(n).ewm(span=n, min_periods=n).mean(), name='EMA')
        if 'EMA' not in abObj.three_min_pd_DF.columns:
            abObj.three_min_pd_DF = abObj.three_min_pd_DF.join(EMA.tail(1))
        else:
            abObj.three_min_pd_DF._set_value(EMA.tail(1).index, 'EMA', EMA.tail(1)[0])
