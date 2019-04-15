from src.hrhd.ibservices.ib_client_wrap import IBClient, IBWrapper
from src.hrhd.brokerlib.ibapi.utils import iswrapper
from src.hrhd.brokerlib.ibapi.contract import *
from src.hrhd.brokerlib.ibapi.common import *
from src.main.algo_bot_objects import AlgoBotObjects as Ab_Obj
from json import dumps
from kafka import KafkaProducer
from random import randint
import json
import os
import sys
import traceback
import logging
import time

logger = logging.getLogger('root')
DEFAULT_GET_CONTRACT_ID = 43


# marker for when queue is finished
SYM_MAP_PATH = os.path.dirname(os.environ['ALGOBOT_CONFIG'])+os.sep+"IB_NSE_Map.json"
producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))

TWS_IP = Ab_Obj.parser.get('common', 'gateway_ip')
TMS_PORT = int(Ab_Obj.parser.get('common', 'gateway_port'))
IB_CLIENT_ID = int(Ab_Obj.parser.get('common', 'IB_ClientId'))


class IBService(IBWrapper, IBClient):
    contract = None
    hdate_prev = Ab_Obj.parser.get('common', 'back_test_prev_date')
    hdate = Ab_Obj.parser.get('common', 'back_test_date')
    cdate = ""
    exe_iterator = 0
    # back_test_symbols = json.loads(Ab_Obj.parser.get('common', 'back_test_symbols'))
    back_test_symbol = Ab_Obj.parser.get('common', 'back_test_symbol')
    running_hdate = False

    def __init__(self):
        try:
            IBWrapper.__init__(self)
            IBClient.__init__(self, wrapper=self)
            self._my_contract_details = {}
        except Exception as ex:
            logger.error(ex)
            logger.error(traceback.format_exc())

    @staticmethod
    def connect_ib(ib_connection):
        try:
            if not ib_connection.isConnected():
                ib_connection.connect(TWS_IP, TMS_PORT, clientId=IB_CLIENT_ID)
                logger.info("serverVersion:%s connectionTime:%s" % (ib_connection.serverVersion(),
                                                                    ib_connection.twsConnectionTime()))
        except Exception as ex:
            logger.error(ex)
            logger.error(traceback.format_exc())

    @staticmethod
    def get_ib_symbol_from_map(nse_symbol):
        try:
            map_json = json.loads(open(str(SYM_MAP_PATH)).read())
            for sym in map_json:
                if sym['NSE_Symbol'] == nse_symbol:
                    return sym['IB_Symbol']
            return nse_symbol
        except Exception as ex:
            logger.error("No mapping value found for NSE Symbol:%s" % nse_symbol)
            logger.error(traceback.format_exc())

    def get_stk_contract(self, symbol):
        try:
            contract = Contract()
            contract.symbol = self.get_ib_symbol_from_map(symbol)
            contract.secType = "STK"
            contract.currency = "INR"
            contract.exchange = "NSE"
            return contract
        except Exception as ex:
            logger.error(ex)
            logger.error(traceback.format_exc())

    @iswrapper
    def historicalTicksLast(self, reqId:int, ticks: ListOfHistoricalTickLast, done: bool):
        self.full_day_data(ticks)

    def full_day_data(self, ticks):
        try:

            if len(ticks) >= 1000:
                i = 0
                for tick in ticks:
                    str(time.strftime("%D %H:%M:%S", time.localtime(int(tick.time))))
                    data = {'Symbol': self.back_test_symbol, 'Price': tick.price, 'Timestamp': tick.time}
                    producer.send("HRHD", value=data)
                    i = i + 1
                    # if self.running_hdate is True:
                    #     print('Price - ', tick.price, 'Timestamp-', tick.time)
                    if i == 1000:
                        self.reqHistoricalTicks(randint(10, 999), self.contract,
                                                str(self.cdate) + " " +
                                                str(time.strftime("%H:%M:%S", time.localtime(int(tick.time)))),
                                                "", 1000, "TRADES", 1, True, [])
                        break
            else:
                for tick in ticks:
                    data = {'Symbol': self.back_test_symbol, 'Price': tick.price,
                            'Timestamp': tick.time}
                    # if self.running_hdate is True:
                    #     print('Price - ', tick.price, 'Timestamp-', tick.time)
                    producer.send("HRHD", value=data)
                if self.running_hdate is True:
                    time.sleep(100)
                    Ab_Obj.slow_min_pd_DF.to_csv(r'~/Desktop/slow_' + self.back_test_symbol + '_' + self.hdate + '.csv')
                    Ab_Obj.fast_min_pd_DF.to_csv(r'~/Desktop/fast_' + self.back_test_symbol + '_' + self.hdate + '.csv')
                    print("--------------------------------------------------------------------------------------")
                    print("-----Execution Completed For " + self.back_test_symbol + " & CSV Generated in Desktop-----")
                    print("--------------------------------------------------------------------------------------")
                    print("-------------------------Execution Completed For All the Symbols----------------------")
                    sys.exit()
                if self.running_hdate is False:
                    time.sleep(60)
                    print("Requesting current day data...")
                    self.running_hdate = True
                    Ab_Obj.slow_min_ticks.clear()
                    Ab_Obj.fast_min_ticks.clear()
                    # Ab_Obj.c_fast_min = 18
                    self.cdate = self.hdate
                    Ab_Obj.start_sapm = True
                    self.reqHistoricalTicks(1, self.contract, str(self.hdate) + " 09:15:00", "", 1000, "TRADES", 1,
                                             True, [])

        except Exception as ex:
            logging.error(traceback.format_exc())
            print(traceback.format_exc())

    def get_hrhd_data(self, ibcon):
        try:
            # self.back_test_symbol = self.back_test_symbols[self.exe_iterator]
            self.contract = self.get_stk_contract(self.back_test_symbol)
            self.cdate = self.hdate_prev
            ibcon.reqHistoricalTicks(1, self.contract, str(self.hdate_prev)+" 09:15:00", "", 1000, "TRADES", 1, True, [])
            ibcon.run()
        except:
            logger.error(traceback.format_exc())
