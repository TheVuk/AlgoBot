from src.main.algo_bot_objects import AlgoBotObjects as abObj
from src.loghandler import log
import pandas as pd
import talib as tb
import traceback

# Import Homebrew

# Init Logging Facilities
logger = log.setup_custom_logger('root')


def moving_average(n):
    """Calculate the moving average for the given data.

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    MA = pd.Series(abObj.three_min_pd_DF['close'].tail(n).rolling(n, min_periods=n).mean(), name='MA')
    if 'MA' not in abObj.three_min_pd_DF.columns:
        abObj.three_min_pd_DF = abObj.three_min_pd_DF.join(MA.tail(1))
    else:
        abObj.three_min_pd_DF._set_value(MA.tail(1).index, 'MA', MA.tail(1)[0])


def exponential_moving_average(n):
    """

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    EMA = pd.Series(abObj.three_min_pd_DF['close'].tail(n).ewm(span=n, min_periods=n).mean(), name='EMA')
    if 'EMA' not in abObj.three_min_pd_DF.columns:
        abObj.three_min_pd_DF = abObj.three_min_pd_DF.join(EMA.tail(1))
    else:
        abObj.three_min_pd_DF._set_value(EMA.tail(1).index, 'EMA', EMA.tail(1)[0])


def macd(n_fast, n_slow):
    """Calculate MACD, MACD Signal and MACD difference

    :param df: pandas.DataFrame
    :param n_fast:
    :param n_slow:
    :return: pandas.DataFrame
    """
    EMAfast = pd.Series(abObj.three_min_pd_DF['close'].tail(n_slow+10).ewm(span=n_fast, min_periods=n_slow).mean())
    EMAslow = pd.Series(abObj.three_min_pd_DF['close'].tail(n_slow+10).ewm(span=n_slow, min_periods=n_slow).mean())
    MACD = pd.Series(EMAfast - EMAslow, name='MACD')
    MACDsign = pd.Series(MACD.ewm(span=9, min_periods=9).mean(), name='MACDsign')
    MACDdiff = pd.Series(MACD - MACDsign, name='MACDdiff')
    if 'MACD' not in abObj.three_min_pd_DF.columns:
        abObj.three_min_pd_DF = abObj.three_min_pd_DF.join(MACD.tail(1))
    else:
        abObj.three_min_pd_DF._set_value(MACD.tail(1).index, 'MACD', MACD.tail(1)[0])

    if 'MACDsign' not in abObj.three_min_pd_DF.columns:
        abObj.three_min_pd_DF = abObj.three_min_pd_DF.join(MACDsign.tail(1))
    else:
        abObj.three_min_pd_DF._set_value(MACDsign.tail(1).index, 'MACDsign', MACDsign.tail(1)[0])

    if 'MACDdiff' not in abObj.three_min_pd_DF.columns:
        abObj.three_min_pd_DF = abObj.three_min_pd_DF.join(MACDdiff.tail(1))
    else:
        abObj.three_min_pd_DF._set_value(MACDdiff.tail(1).index, 'MACDdiff', MACDdiff.tail(1)[0])

def adx(n):
    try:
        ADX = pd.Series(tb.ADX(abObj.three_min_pd_DF['high'].values, abObj.three_min_pd_DF['low'].values,
                               abObj.three_min_pd_DF['close'].values, timeperiod=n), index=abObj.three_min_pd_DF.index,
                                name='ADX')
        if 'ADX' not in abObj.three_min_pd_DF.columns:
            abObj.three_min_pd_DF = abObj.three_min_pd_DF.join(ADX.tail(1))
        else:
            abObj.three_min_pd_DF._set_value(ADX.tail(1).index, 'ADX', ADX.tail(1)[0])

    except:
        logger.error(traceback.format_exc())

def rsi(n):
    try:
        RSI = pd.Series(tb.RSI(abObj.three_min_pd_DF['close'].values, timeperiod=n), index=abObj.three_min_pd_DF.index,
                                name='RSI')
        if 'RSI' not in abObj.three_min_pd_DF.columns:
            abObj.three_min_pd_DF = abObj.three_min_pd_DF.join(RSI.tail(1))
        else:
            abObj.three_min_pd_DF._set_value(RSI.tail(1).index, 'RSI', RSI.tail(1)[0])
    except:
        logger.error(traceback.format_exc())
