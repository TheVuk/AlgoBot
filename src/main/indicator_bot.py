import traceback
from src.loghandler import log
from concurrent.futures import ThreadPoolExecutor
from src.pandasDF.one_min_df import OneMinDF as oneDF
from src.main.vukalgo.sapm import Sapm

logger = log.setup_custom_logger('root')

sapm_obj = Sapm()

class IndicatorBot(object):

    def __init__(self):
        pass

    @staticmethod
    def one_min_data_frame(ticks):
        oneDF.generate_one_min_df(ticks)

    def algo(self, ticks):
        try:
            executors_list = []
            with ThreadPoolExecutor(max_workers=5) as executor:
                executors_list.append(executor.submit(self.one_min_data_frame(ticks)))
                executors_list.append(executor.submit(sapm_obj.do_samp(ticks)))

        except:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())


if __name__ == '__main__':
    a = IndicatorBot()
    a.algo("[[2123123, 12]]")

