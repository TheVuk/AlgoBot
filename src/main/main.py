import ast
import traceback
from kafka import KafkaConsumer
from json import loads
import threading
from src.loghandler import log
from src.main.algo_bot_objects import AlgoBotObjects as AB_Obj
from src.hrhd.ibservices.ib_services import IBService as IB_Obj
from src.main.indicator_bot import IndicatorBot


# setting up general logger
logger = log.setup_custom_logger('root')
ohlc_consumer = KafkaConsumer("HRHD",
                         bootstrap_servers=['127.0.0.1:9092'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='ohlc',
                         value_deserializer=lambda x: loads(x.decode('utf-8')))


class IndicatorConsumer(object):
    indicator_obj = IndicatorBot()

    def start(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
        return thread

    def run(self):
        for message in ohlc_consumer:
            message = message.value
            self.indicator_obj.algo(message)


class HDHD(object):

    def start(self, ib_conn):
        thread = threading.Thread(target=self.run(ib_conn), args=())
        thread.daemon = True
        thread.start()
        return thread

    def run(self, ib_conn):
        ib_conn.get_hrhd_data(ib_conn)


def main():
    try:
        if not ast.literal_eval(AB_Obj.parser.get('common', 'is_live')):
            print("Algo bot started to listening for message")

            indi_consumer_obj = IndicatorConsumer()
            indicator_thread = indi_consumer_obj.start()

            ib_conn = IB_Obj()
            ib_conn.connect_ib(ib_conn)

            hrhd_obj = HDHD()
            hrhd_thread = hrhd_obj.start(ib_conn)

        else:
            indi_consumer_obj = IndicatorConsumer()
            indicator_thread = indi_consumer_obj.start()

    except Exception as ex:
        logger.error(traceback.format_exc())


if __name__ == '__main__':
    logger.info("**AlgoBot Initiated")
    main()


