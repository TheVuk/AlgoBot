from configparser import ConfigParser
import os
import pandas as pd


class AlgoBotObjects:
    # General config to set config file
    parser = ConfigParser()
    parser.read(os.getenv("ALGOBOT_CONFIG"))
    indicator_thread = None
    hrhd_thread = None
    sapm_thread = None
    start_sapm = False

    # all below used in fast min data frame
    fast_min_ticks = []
    fast_min = int(parser.get('common', 'fast_df'))
    cur_fast_min = 0
    fast_min_pd_DF = pd.DataFrame([])

    # all below used in slow min data frame
    slow_min_ticks = []
    slow_min = int(parser.get('common', 'slow_df'))
    cur_slow_min = 0
    slow_min_pd_DF = pd.DataFrame([])
    # end

    # General flags
    long_flags = {'FA_SAPM': 0, 'FA_MAEMA': 0, 'FA_ADX': 0, 'FA_MACD': 0, 'FA_RSI': 0,
                  'SL_SAPM': 0, 'SL_MAEMA': 0, 'SL_ADX': 0, 'SL_MACD': 0, 'SL_RSI': 0}

    short_flags = {'FA_SAPM': 0, 'FA_MAEMA': 0, 'FA_ADX': 0, 'FA_MACD': 0, 'FA_RSI': 0,
                   'SL_SAPM': 0, 'SL_MAEMA': 0, 'SL_ADX': 0, 'SL_MACD': 0, 'SL_RSI': 0}
