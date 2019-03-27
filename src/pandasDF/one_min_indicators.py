from src.main.algo_bot_objects import AlgoBotObjects as abObj
from src.loghandler import log
import pandas as pd
import traceback
import talib as tb

# Init Logging Facilities
logger = log.setup_custom_logger('root')


def load_indicators():
    try:
        #logger.info("Genrating Indicators")
        moving_average(int(abObj.parser.get('ma', 'interval')))
        exponential_moving_average(int(abObj.parser.get('ema', 'interval')))
        macd(int(abObj.parser.get('macd', 'fast_interval')), int(abObj.parser.get('macd', 'slow_interval')))
        average_directional_movement_index(int(abObj.parser.get('adx', 'interval')),
                                           int(abObj.parser.get('adx', 'interval_ADX')))
        rsi(int(abObj.parser.get('rsi', 'interval')))
        if abObj.start_sapm is True:
            flag_it()
    except:
        logger.error(traceback.format_exc())


def flag_it():
    try:
        # Long Entry
        prev_row = abObj.one_min_pd_DF.loc[abObj.one_min_pd_DF.index[len(abObj.one_min_pd_DF)-2]]
        cur_row = abObj.one_min_pd_DF.loc[abObj.one_min_pd_DF.index[-1]]
        # MAEMA Flag Settings for long
        if cur_row['EMA'] > prev_row['EMA']\
                and cur_row['close'] > cur_row['EMA']\
                and prev_row['close'] > prev_row['EMA'] and cur_row['MA'] > prev_row['MA']:
            abObj.one_min_long_flags['MAEMA'] = 1
        else:
            abObj.one_min_long_flags['MAEMA'] = 0

        # RSI Flag Settings for long
        if int(abObj.parser.get('rsi', 'long_low')) <= cur_row['RSI'] <= int(abObj.parser.get('rsi', 'long_high')):
            abObj.one_min_long_flags['RSI'] = 1
        else:
            abObj.one_min_long_flags['RSI'] = 0

        # ADX Flag Settings for long
        if cur_row['PosDI'] > cur_row['NegDI'] and cur_row['ADX'] > prev_row['ADX'] and\
                cur_row['ADX'] > cur_row['NegDI']:
            # and cur_row['PosDI'] > prev_row['PosDI']\
            abObj.one_min_long_flags['ADX'] = 1
        else:
            abObj.one_min_long_flags['ADX'] = 0

        # MACD Flag Setting for long
        if cur_row['MACD'] > cur_row['MACDsign'] \
                and (cur_row['MACD']+prev_row['MACD']) > (cur_row['MACDsign']+prev_row['MACDsign']):
            #and cur_row['MACD'] < float(abObj.parser.get('macd', 'long_range'))\
            abObj.one_min_long_flags['MACD'] = 1
        else:
            abObj.one_min_long_flags['MACD'] = 0

        # Shot Entry
        # MAEMA Flag Settings for shot
        if cur_row['EMA'] < prev_row['EMA'] \
                and cur_row['close'] < cur_row['EMA'] \
                and prev_row['close'] < prev_row['EMA'] and cur_row['MA'] < prev_row['MA']:
            abObj.one_min_shot_flags['MAEMA'] = 1
        else:
            abObj.one_min_shot_flags['MAEMA'] = 0

        # RSI Flag Settings for shot
        if int(abObj.parser.get('rsi', 'shot_low')) <= cur_row['RSI'] <= int(abObj.parser.get('rsi', 'shot_high')):
            abObj.one_min_shot_flags['RSI'] = 1
        else:
            abObj.one_min_shot_flags['RSI'] = 0

        # ADX Flag Settings for short
        if cur_row['NegDI'] > cur_row['PosDI'] and cur_row['ADX'] > prev_row['ADX'] and\
                cur_row['ADX'] > cur_row['PosDI']:
                #and cur_row['NegDI'] > prev_row['NegDI'] \
            abObj.one_min_shot_flags['ADX'] = 1
        else:
            abObj.one_min_shot_flags['ADX'] = 0

        # MACD Flag Setting for shot
        if cur_row['MACD'] < cur_row['MACDsign']\
            and (cur_row['MACD'] + prev_row['MACD']) < (cur_row['MACDsign'] + prev_row['MACDsign']):
            # and cur_row['MACD'] < float(abObj.parser.get('macd', 'shot_range')) and \
            abObj.one_min_shot_flags['MACD'] = 1
        else:
            abObj.one_min_shot_flags['MACD'] = 0
        # print(cur_row.name,str(cur_row['open']),cur_row['high'],cur_row['low'],cur_row['close']
        #       ,cur_row['MA'],cur_row['EMA'],cur_row['MACD'],cur_row['ADX'],cur_row['RSI'])
        # print("*L",abObj.one_min_long_flags)
        # print("*S",abObj.one_min_shot_flags)

    except:
        logger.error(traceback.format_exc())


def moving_average(n):
    try:
        MA = pd.Series(abObj.one_min_pd_DF['close'].tail(n).rolling(n, min_periods=n).mean(), name='MA')
        if 'MA' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(MA.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(MA.tail(1).index, 'MA', MA.tail(1)[0])
    except:
        logger.error(traceback.format_exc())


def exponential_moving_average(n):
    try:
        EMA = pd.Series(abObj.one_min_pd_DF['close'].tail(n).ewm(span=n, min_periods=n).mean(), name='EMA')
        if 'EMA' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(EMA.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(EMA.tail(1).index, 'EMA', EMA.tail(1)[0])
    except:
        logger.error(traceback.format_exc())


def macd(n_fast, n_slow):
    try:
        EMAfast = pd.Series(abObj.one_min_pd_DF['close'].tail(n_slow+10).ewm(span=n_fast, min_periods=n_slow).mean())
        EMAslow = pd.Series(abObj.one_min_pd_DF['close'].tail(n_slow+10).ewm(span=n_slow, min_periods=n_slow).mean())
        MACD = pd.Series(EMAfast - EMAslow, name='MACD')
        MACDsign = pd.Series(MACD.ewm(span=9, min_periods=9).mean(), name='MACDsign')
        MACDdiff = pd.Series(MACD - MACDsign, name='MACDdiff')
        if 'MACD' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(MACD.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(MACD.tail(1).index, 'MACD', MACD.tail(1)[0])

        if 'MACDsign' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(MACDsign.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(MACDsign.tail(1).index, 'MACDsign', MACDsign.tail(1)[0])

        if 'MACDdiff' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(MACDdiff.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(MACDdiff.tail(1).index, 'MACDdiff', MACDdiff.tail(1)[0])
    except:
        logger.error(traceback.format_exc())


def average_directional_movement_index(n, n_ADX):
    try:
        df = abObj.one_min_pd_DF.tail(100)
        i = 0
        UpI = []
        DoI = []
        for row in df.iterrows():
            if (i != 0):
                UpMove = df.loc[df.index[i]]['high'] - df.loc[df.index[i - 1]]['high']
                DoMove = df.loc[df.index[i - 1]]['low'] - df.loc[df.index[i]]['low']
                if UpMove > DoMove and UpMove > 0:
                    UpD = UpMove
                else:
                    UpD = 0
                UpI.append(UpD)

                if DoMove > UpMove and DoMove > 0:
                    DoD = DoMove
                else:
                    DoD = 0
                DoI.append(DoD)
            i = i + 1
        i = 0
        TR_l = [0]
        for row in df.iterrows():
            if i != 0:
                TR = max(df.loc[df.index[i]]['high'], df.loc[df.index[i-1]]['close']) - min(
                    df.loc[df.index[i]]['low'], df.loc[df.index[i - 1]]['close'])
                TR_l.append(TR)
            i = i + 1
        TR_s = pd.Series(TR_l)
        ATR = pd.Series(TR_s.ewm(span=n, min_periods=n).mean())
        UpI = pd.Series(UpI)
        DoI = pd.Series(DoI)
        PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean() / ATR, name='PosDI')
        NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean() / ATR, name='NegDI')
        ADX = pd.Series((abs(PosDI - NegDI) / (PosDI + NegDI)).ewm(span=n_ADX, min_periods=n_ADX).mean(),
                        name='ADX')

        if 'PosDI' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(PosDI.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(abObj.one_min_pd_DF.tail(1).index, 'PosDI', PosDI.loc[PosDI.index[len(PosDI)-2]])

        if 'NegDI' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(NegDI.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(abObj.one_min_pd_DF.tail(1).index, 'NegDI', NegDI.loc[NegDI.index[len(NegDI)-2]])

        if 'ADX' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(ADX.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(abObj.one_min_pd_DF.tail(1).index, 'ADX', ADX.tail(1).values[0])

    except:
        print(traceback.format_exc())
        logger.error(traceback.format_exc())


def rsi(n):
    try:
        RSI = pd.Series(tb.RSI(abObj.one_min_pd_DF['close'].values, timeperiod=n), index=abObj.one_min_pd_DF.index,
                                name='RSI')
        if 'RSI' not in abObj.one_min_pd_DF.columns:
            abObj.one_min_pd_DF = abObj.one_min_pd_DF.join(RSI.tail(1))
        else:
            abObj.one_min_pd_DF._set_value(RSI.tail(1).index, 'RSI', RSI.tail(1)[0])
    except:
        logger.error(traceback.format_exc())
