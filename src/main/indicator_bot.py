import traceback
from src.loghandler import log
from concurrent.futures import ThreadPoolExecutor
from src.main.algo_bot_objects import AlgoBotObjects as abObj
from src.pandasDF.one_min_df import OneMinDF as oneDF
from src.pandasDF.three_min_df import ThreeMinDF as threeDF
from src.main.vukalgo.sapm import Sapm as sapm_one_min
from src.main.vukalgo.sapm_three_min import Sapm as sapm_three_min

logger = log.setup_custom_logger('root')

sapm_obj_one = sapm_one_min()
sapm_obj_three = sapm_three_min()

class IndicatorBot(object):

    def __init__(self):
        pass

    @staticmethod
    def data_frame(ticks):
        if abObj.parser.get('sapm', 'DF') == "1min":
            oneDF.generate_one_min_df(ticks)
        elif abObj.parser.get('sapm', 'DF') == "3min":
            threeDF.generate_three_min_df(ticks)

    @staticmethod
    def exe_sapm(ticks):
        if abObj.parser.get('sapm', 'DF') == "1min":
            sapm_obj_one.do_samp(ticks)
        elif abObj.parser.get('sapm', 'DF') == "3min":
            sapm_obj_three.do_samp(ticks)

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

