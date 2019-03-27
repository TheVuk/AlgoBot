
from src.main.vukalgo.sapm_objects import SapmObjects as so
from src.main.algo_bot_objects import AlgoBotObjects as abObj
import time, traceback, datetime

from src.loghandler import log
logger = log.setup_custom_logger('root')

entime = datetime.datetime.strptime(abObj.parser.get('common', 'back_test_date')+' 09:20:00', '%Y%m%d %H:%M:%S')
ent930am = time.mktime(entime.timetuple())
extime = datetime.datetime.strptime(abObj.parser.get('common', 'back_test_date')+' 15:15:00', '%Y%m%d %H:%M:%S')
exit320pm = time.mktime(extime.timetuple())

class Sapm():

    def do_samp(self, ticks):
        if abObj.start_sapm is True:
            self.algo(ticks.get('Timestamp'), ticks.get('Price'))
            if so.SL == 0.0:
                so.SL = round(ticks.get('Price') * (float(abObj.parser.get('sapm', 'SL')) / 100), 1)
                so.TSL = round(ticks.get('Price') * (float(abObj.parser.get('sapm', 'TSL')) / 100), 1)
                print("STOP LOSS", str(so.SL), " TRAILING STOP LOSS", so.TSL)



    def algo(self, ticktime, tickprice):
        try:
            if (ticktime > exit320pm):
                if (so.LBuy_Position == True):
                    print("*** LONG EXIT ," + str(
                        time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))) + "," + str(tickprice))
                    # print(so.LB_TSL)
                    # so.LB_TSL[:] = []
                    print("LONG postion :" + str(tickprice - so.LB_Price))
                    so.net_profit.append(tickprice - so.LB_Price)
                    so.LBuy_Position = False
                    so.LB_Price = 0
                    so.No_Trades = so.No_Trades + 1
                    print("NET :" + str(sum(so.net_profit)))
                    print("Number of TRADES :" + str(so.No_Trades))
                if (so.SSell_Position == True):
                    print("*** SHORT EXIT ," + str(
                        time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))) + "," + str(tickprice))
                    # print(so.SS_TSL)
                    # so.SS_TSL[:] = []
                    print("SHORT postion :" + str(so.SS_Price - tickprice))
                    so.net_profit.append(so.SS_Price - tickprice)
                    so.SSell_Position = False
                    so.SS_Price = 0
                    so.No_Trades = so.No_Trades + 1
                    print("NET :" + str(sum(so.net_profit)))
                    print("Number of TRADES :" + str(so.No_Trades))
            if (so.LBuy_Position == True):
                if (tickprice >= (so.LSL_Price + so.SL + so.TSL)):
                    so.LSL_Price = so.LSL_Price + so.TSL
                elif (tickprice <= so.LSL_Price) or\
                    (abObj.one_min_pd_DF.loc[abObj.one_min_pd_DF.index[-1]]['ADX']
                     < abObj.one_min_pd_DF.loc[abObj.one_min_pd_DF.index[len(abObj.one_min_pd_DF) - 2]]['ADX']):
                    print(
                        "* LONG EXIT ," + str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))) + "," + str(
                            tickprice))
                    # print(so.LB_TSL)
                    # so.LB_TSL[:] = []
                    print("LONG postion :" + str(tickprice - so.LB_Price))
                    so.net_profit.append(tickprice - so.LB_Price)
                    so.LBuy_Position = False
                    so.LB_Price = 0
                    so.No_Trades = so.No_Trades + 1
                    print("NET :" + str(sum(so.net_profit)))
                    print("Number of TRADES :" + str(so.No_Trades))


            if (so.SSell_Position == True):
                if (tickprice <= (so.SSL_Price - so.SL - so.TSL)):
                    so.SSL_Price = so.SSL_Price - so.TSL
                elif (tickprice >= so.SSL_Price)or\
                    (abObj.one_min_pd_DF.loc[abObj.one_min_pd_DF.index[-1]]['ADX']
                     < abObj.one_min_pd_DF.loc[abObj.one_min_pd_DF.index[len(abObj.one_min_pd_DF) - 2]]['ADX']):
                    print(
                        "* SHORT EXIT ," + str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))) + "," + str(
                            tickprice))
                    # print(so.SS_TSL)
                    # so.SS_TSL[:] = []
                    print("SHORT postion :" + str(so.SS_Price - tickprice))
                    so.net_profit.append(so.SS_Price - tickprice)
                    so.SSell_Position = False
                    so.SS_Price = 0
                    so.No_Trades = so.No_Trades + 1
                    print("NET :" + str(sum(so.net_profit)))
                    print("Number of TRADES :" + str(so.No_Trades))

            if (ticktime < exit320pm and ticktime > ent930am):
                if len(so.titicks) > 0:
                    if (float(ticktime) - float(so.titicks[0][0])) >= so.TI:
                        so.titicks.append([ticktime, tickprice])
                        sum_value = 0.0
                        for i in so.titicks:
                            sum_value = sum_value + i[1]
                        if len(so.avgs) < 3:
                            so.avgs.append(sum_value / len(so.titicks))
                        else:
                            so.avgs[0] = so.avgs[1]
                            so.avgs[1] = so.avgs[2]
                            so.avgs[2] = (sum_value / len(so.titicks))
                            # print("*Avg - "+str(so.avgs[2]) + ",
                            # TickTime - "+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))))
                        if len(so.avgs) == 3:
                            pv_delta = (so.avgs[2] - so.avgs[0]) / so.avgs[2] * 100
                            # print(str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+" " +
                            #        str(pv_delta)+","+str(tickprice))
                            if pv_delta >= so.DTH:
                                abObj.one_min_long_flags['SAPM'] = 1
                                so.TI_SAPM_LONG = ticktime + 120
                                # print("LFLAG - ",str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))), abObj.one_min_long_flags)
                            if abObj.one_min_long_flags['SAPM'] == 1 and abObj.one_min_long_flags['MAEMA'] == 1\
                                    and abObj.one_min_long_flags['ADX'] == 1 and abObj.one_min_long_flags['MACD'] == 1\
                                    and so.LBuy_Position is False:
                                print("LONG ENTRY ," + str(
                                    time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))) + "," + str(tickprice))
                                so.LB_Price = tickprice
                                so.LBuy_Position = True
                                so.LSL_Price = tickprice - so.SL
                            elif ticktime > so.TI_SAPM_LONG:
                                abObj.one_min_long_flags['SAPM'] = 0

                            if pv_delta <= (so.DTH * -1):
                                abObj.one_min_shot_flags['SAPM'] = 1
                                so.TI_SAPM_SHORT = ticktime + 120
                                # print("SFLAG -",str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))), abObj.one_min_shot_flags)
                            if abObj.one_min_shot_flags['SAPM'] == 1 and abObj.one_min_shot_flags['MAEMA'] == 1\
                                    and abObj.one_min_shot_flags['ADX'] == 1 and abObj.one_min_shot_flags['MACD'] == 1\
                                    and so.SSell_Position is False:
                                print("SHORT ENTRY ," + str(
                                    time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))) + "," + str(tickprice))
                                so.SS_Price = tickprice
                                so.SSell_Position = True
                                so.SSL_Price = tickprice + so.SL
                            elif ticktime > so.TI_SAPM_SHORT:
                                abObj.one_min_shot_flags['SAPM'] = 0

                        so.titicks.clear()
                    else:
                        so.titicks.append([ticktime, tickprice])
                else:
                    so.titicks.append([ticktime, tickprice])

        except:
            logger.error(traceback.format_exc())


if __name__ == '__main__':
    sobj = Sapm()
    testlist = [[1548906300, 165.0], [1548906303, 165.25], [1548906309, 165.15]]
    for item in testlist:
        sobj.algo(item[0], item[1])
    print(so.titicks)
