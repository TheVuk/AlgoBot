from src.main.algo_bot_objects import AlgoBotObjects as abObj
from src.pandasDF import one_min_indicators as indi_obj
from src.loghandler import log
import traceback
import time
import pandas as pd

logger = log.setup_custom_logger('root')


class OneMinDF(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_one_min_df(ticks):

        def get_ohlc():
            try:
                data = pd.DataFrame(abObj.one_min_ticks, columns=['time', 'price'])
                data['time'] = pd.to_datetime(data['time'], unit='s', utc=True)
                data = data.set_index('time')
                data = data.tz_convert(tz='Asia/Kolkata')
                ti = data.loc[:, ['price']]
                one_min_bars = ti.price.resample('1min').ohlc()
                for index, row in one_min_bars.iterrows():
                    abObj.one_min_pd_DF = abObj.one_min_pd_DF.append(row)
                indi_obj.load_indicators()
            except:
                print(traceback.format_exc())
                logger.error(traceback.format_exc())
        tick_time = ticks.get('Timestamp')
        tick_price = ticks.get('Price')
        try:
            if len(abObj.one_min_ticks) > 0:
                if int(str(time.strftime("%M", time.localtime(int(tick_time))))) != abObj.c_one_min:
                    #print(abObj.one_min_ticks, ',')
                    get_ohlc()
                    abObj.one_min_ticks.clear()
                    abObj.one_min_ticks.append([tick_time, tick_price])
                    abObj.c_one_min = int(str(time.strftime("%M", time.localtime(int(tick_time)))))
                else:
                    abObj.one_min_ticks.append([tick_time, tick_price])
            else:
                abObj.c_one_min = int(str(time.strftime("%M", time.localtime(int(tick_time)))))
                abObj.one_min_ticks.append([tick_time, tick_price])
        except:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())



