import traceback
from src.loghandler import log
from concurrent.futures import ThreadPoolExecutor
from src.dataframe.slow_df import SlowDF as SLDF
from src.dataframe.fast_df import FastDF as FADF
from src.main.vukalgo.sapm import Sapm as sapm

logger = log.setup_custom_logger('root')

sapm_obj_one = sapm()


class IndicatorBot(object):

    def __init__(self):
        pass

    @staticmethod
    def data_frame(ticks):
        # print(ticks)
        SLDF.generate_slow_min_df(ticks)
        FADF.generate_fast_min_df(ticks)

    @staticmethod
    def exe_sapm(ticks):
        sapm_obj_one.do_samp(ticks)

    def algo(self, ticks):
        try:
            executors_list = []
            with ThreadPoolExecutor(max_workers=5) as executor:
                if ticks.get('Price') is not None:
                    executors_list.append(executor.submit(self.data_frame(ticks)))
                    executors_list.append(executor.submit(self.exe_sapm(ticks)))

        except:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())


if __name__ == '__main__':
    a = IndicatorBot()
    a.algo("[[2123123, 12]]")

