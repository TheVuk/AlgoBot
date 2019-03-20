import traceback
import time
from src.loghandler import log
from concurrent.futures import ThreadPoolExecutor
from src.pandasDF.one_min_df import OneMinDF as oneDF
from src.pandasDF.three_min_df import ThreeMinDF as threeDF

logger = log.setup_custom_logger('root')


class AlgoBot(object):

    def __init__(self):
        pass

    @staticmethod
    def one_min(ticks):
        #print("Iam one min", ticks)
        oneDF.generate_one_min_df(ticks)

    @staticmethod
    def three_min(ticks):
        #print("Iam three min", ticks)
        threeDF.generate_three_min_df(ticks)

    def algo(self, ticks):
        try:
            self.one_min(ticks)
            # self.three_min(ticks)
            # executors_list = []
            # with ThreadPoolExecutor(max_workers=5) as executor:
            #     executors_list.append(executor.submit(self.one_min(ticks)))
            #     executors_list.append(executor.submit(self.three_min(ticks)))
            #print("main")
        except:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())


if __name__ == '__main__':
    a = AlgoBot()
    a.algo("[[2123123, 12]]")

