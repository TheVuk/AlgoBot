import ast
import traceback
from kafka import KafkaConsumer
from json import loads
import threading
from src.loghandler import log
from src.main.algo_bot_objects import AlgoBotObjects as AB_Obj
from src.hrhd.ibservices.ib_services import IBService as IB_Obj
from src.main.algobot import AlgoBot

# setting up general logger
logger = log.setup_custom_logger('root')
consumer = KafkaConsumer("HRHD",
                         bootstrap_servers=['127.0.0.1:9092'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='algobots',
                         value_deserializer=lambda x: loads(x.decode('utf-8')))


class TickConsumer(object):
    algo_obj = AlgoBot()

    def start(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
        return thread

    def run(self):
        for message in consumer:
            message = message.value
            self.algo_obj.algo(message)



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

            consumer_obj = TickConsumer()
            algo_thread = consumer_obj.start()

            ib_conn = IB_Obj()
            ib_conn.connect_ib(ib_conn)

            hrhd_obj = HDHD()
            hrhd_thread = hrhd_obj.start(ib_conn)

        else:
            ab_main = AlgoBot()
    except Exception as ex:
        logger.error(traceback.format_exc())


if __name__ == '__main__':
    logger.info("**AlgoBot Initiated")
    main()


