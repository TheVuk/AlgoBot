from configparser import ConfigParser
import os
import pandas as pd


class AlgoBotObjects:
    # General config to set config file
    parser = ConfigParser()
    parser.read(os.getenv("ALGOBOT_CONFIG"))

    # all below used in one min data frame
    #one_min_df = None
    one_min_ticks = []
    c_one_min = 0
    one_min_pd_DF = pd.DataFrame([])
    #one_min_pd_DF['time'] = pd.to_datetime(one_min_pd_DF['Time'], unit='s', utc=True)
    #one_min_pd_DF = one_min_pd_DF.set_index('Time')
    #one_min_pd_DF = one_min_pd_DF.tz_convert(tz='Asia/Kolkata')

    # all below used in three min data frame
    #three_min_df = None
    three_min_pd_DF = pd.DataFrame([])
    three_min_ticks = []
    c_three_min = 0

