from configparser import ConfigParser
import os
import pandas as pd


class AlgoBotObjects:
    # General config to set config file
    parser = ConfigParser()
    parser.read(os.getenv("ALGOBOT_CONFIG"))

    start_sapm = False
    # all below used in one min data frame
    one_min_ticks = []
    c_one_min = 0
    one_min_pd_DF = pd.DataFrame([])
    one_min_long_flags = {'SAPM': 0, 'MAEMA': 0, 'ADX': 0, 'MACD': 0, 'RSI': 0}
    one_min_shot_flags = {'SAPM': 0, 'MAEMA': 0, 'ADX': 0, 'MACD': 0, 'RSI': 0}

    indicator_thread = None
    hrhd_thread = None
    sapm_thread = None

    three_min_pd_DF = pd.DataFrame([])
    three_min_ticks = []
    c_three_min = 0

