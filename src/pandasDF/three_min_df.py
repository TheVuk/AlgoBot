from src.main.algo_bot_objects import AlgoBotObjects as abObj
from src.pandasDF import three_min_indicators as indi_obj
import traceback
from src.loghandler import log
import time
import pandas as pd

logger = log.setup_custom_logger('root')


class ThreeMinDF(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_three_min_df(ticks):

        def get_ohlc():
            try:
                data = pd.DataFrame(abObj.three_min_ticks, columns=['time', 'price'])
                data['time'] = pd.to_datetime(data['time'], unit='s', utc=True)
                data = data.set_index('time')
                data = data.tz_convert(tz='Asia/Kolkata')
                ti = data.loc[:, ['price']]
                three_min_bars = ti.price.resample('3min').ohlc()
                for index, row in three_min_bars.iterrows():
                    abObj.three_min_pd_DF = abObj.three_min_pd_DF.append(row)
                    # print(row.name, str(row['open']),row['high'],row['low'],row['close'])
                    indi_obj.load_indicators()
            except:
                print(traceback.format_exc())
                logger.error(traceback.format_exc())

        tick_time = ticks.get('Timestamp')
        tick_price = ticks.get('Price')
        try:
            # print(ticks)
            if len(abObj.three_min_ticks) > 0:

                if int(str(time.strftime("%M", time.localtime(int(tick_time))))) > abObj.c_three_min:
                    get_ohlc()
                    abObj.three_min_ticks.clear()
                    abObj.three_min_ticks.append([tick_time, tick_price])
                    abObj.c_three_min = int(str(time.strftime("%M", time.localtime(int(tick_time)))))+2
                    #print(" - " , abObj.c_three_min)
                    if abObj.c_three_min == 0:
                        abObj.c_three_min = int(time.strftime("%M", time.localtime(int(tick_time)))) + 2

                else:
                    abObj.three_min_ticks.append([tick_time, tick_price])
                    # print(tick_time, tick_price)
                    if int(str(time.strftime("%M", time.localtime(int(ticks.get('Timestamp')))))) == 0:
                        abObj.c_three_min = int(str(time.strftime("%M", time.localtime(int(tick_time)))))+2

            else:
                abObj.c_three_min = int(str(time.strftime("%M", time.localtime(int(tick_time)))))+2
                abObj.three_min_ticks.append([tick_time, tick_price])
                # print(tick_time, tick_price)
        except:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())

