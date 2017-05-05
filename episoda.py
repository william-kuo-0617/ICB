import random
from datetime import date
import requests
import pandas as pd
import json
from bson import json_util
#from __future__ import print_function
def initializer(episode1):
    init_temp = []
    if episode1.goal == 'Exchange':
        init_temp = ["Please give me the exchange rate of "+episode1.inform_slots['country1']+" to "+episode1.inform_slots['country2']+"\n","I'd like to know the exchange rate of "+episode1.inform_slots['country1']+" to "+episode1.inform_slots['country2']+"\n"]
        init_temp.append(str("What is the exchange rate of "+episode1.inform_slots['country2']+"?"))
        init_temp.append(str("How's the exchange rate of "+episode1.inform_slots['country2']+"?"))
        init_temp.append(str("Give me the exchange rate"))
        init_temp.append(str("I'd like to know the exchange rate"))
        init_temp.append(str("Exchange rate, please."))
        init_temp.append(str("The exchange rate between "+episode1.inform_slots['country1']+" and "+episode1.inform_slots['country2']+"."))
        return random.choice(init_temp)
    elif episode1.goal == 'Query':
        init_temp = ["Please give me the share price detail of "+episode1.inform_slots['symbol']+" "+str(episode1.inform_slots['date'])+"\n", "What is the close price of "+episode1.inform_slots['symbol']+" on "+str(episode1.inform_slots['date'])+"?\n", "I'd like to know the open and low price of "+episode1.inform_slots['symbol']+" on "+str(episode1.inform_slots['date'])+"\n"]
        init_temp.append(str("Give me "+str(episode1.inform_slots['date'])+"'s stock price"))
        init_temp.append(str("the information of "+episode1.inform_slots['company_name']+", please"))
        init_temp.append(str("I would like to see some stock information"))
        init_temp.append(str("Show me the stock price."))
        init_temp.append(str("I would like to see "+str(episode1.inform_slots['date'])+"'s "+episode1.inform_slots['company_name']+" stock price"))
        init_temp.append(str("Please show me "+str(episode1.inform_slots['date'])+"'s "+episode1.inform_slots['company_name']+" stock price."))
        return random.choice(init_temp)
    elif episode1.goal == 'Get_exchange_rate':
        init_temp = ["what's the exchange rate of "+episode1.inform_slots['buy']+" "+episode1.inform_slots['Money_name']+" by TWD now in bank with "+episode1.inform_slots['type']+"?\n", "I want to "+episode1.inform_slots['buy']+" some "+episode1.inform_slots['Money_name']+" with "+episode1.inform_slots['type']+"?\n"]
        init_temp.append(str("I would like to "+episode1.inform_slots['buy']+" some "+episode1.inform_slots['Money_name']+"."))
        init_temp.append(str("I'd like to "+episode1.inform_slots['buy']+" some "+episode1.inform_slots['Money_name']+"."))
        init_temp.append(str("I want to "+episode1.inform_slots['buy']+" some "+episode1.inform_slots['Money_name']+"."))
        init_temp.append(str("I want to exchange my "+episode1.inform_slots['Money_name']+"."))
        init_temp.append(str(""))
        return random.choice(init_temp)
    elif episode1.goal == 'USDX':
        init_temp.append(str("Give me the USDX until "+str(episode1.inform_slots['time_end'])+"."))
        init_temp.append(str("I'd like to know the USDX until "+str(episode1.inform_slots['time_end'])+"."))
        init_temp.append(str("I want to know the USDX until "+str(episode1.inform_slots['time_end'])+"."))
        init_temp.append(str("I'd like to know the USDX since "+str(episode1.inform_slots['time_start'])+"."))
        init_temp.append(str("I want to know the USDX since "+str(episode1.inform_slots['time_start'])+"."))
        init_temp.append(str("I'd like to know the USDX until "+str(episode1.inform_slots['time_start'])+"."))
        init_temp.append(str("I'd like to know the USDX."))
        init_temp.append(str("Give me the USDX."))
        init_temp.append(str("I want to know the USDX"))
        return random.choice(init_temp)


class episode(object):
    r=requests.get('https://tw.rter.info/capi.php')
    currency=r.json()
    """docstring for episode."""
    def __init__(self, arg):
        #super(episode, self).__init__()
        self.goal = self.getgoal()
        self.request_slot = episode.request[self.goal]
        self.start_date = None
        self.comp_ind = None
        self.inform_slots = self.slots_fill_in(self.start_date)

    def getgoal(self):
        return episode.user_goal[random.randint(0,len(episode.user_goal)-1)]

    def slots_fill_in(self,start_date):
        tmp = {}
        tmplist = list(episode.slots[self.goal]) #list of dictionry keys
        for slot in tmplist:
            if slot in ['date','time_end','time_start']:
                tmp[slot] = self.date_gen(self.start_date)
                if slot == 'time_start':
                    self.start_date = tmp[slot]
            else:
                j = random.randint(1,1000)%len(episode.slots[self.goal][slot])
                if slot in ['symbol','company_name']:
                    self.comp_ind = j if self.comp_ind is None else self.comp_ind
                    j = self.comp_ind if self.comp_ind is not None else j
                tmp[slot] = episode.slots[self.goal][slot][j]
        return tmp

    def dump(self):
        tmp = {}
        tmp['goal'] = self.goal
        tmp['inform_slots'] = self.inform_slots
        tmp['request_slot'] = self.request_slot
        json.dumps(tmp, default=json_util.default)
        # print("{goal:",self.goal,"};")
        # print("{inform_slots:")
        # for key,val in self.inform_slots.items():
        #     print("\t{0}: {1}".format(key,val))
        # print("};")
        # print("{request_slot:\n","\t{0}:{1}\n".format(self.request[0],self.request[1]),"};")
    def date_gen(self,start_date):
        start_date = self.start_date.toordinal() if self.start_date is not None else date.today().replace(day=1, month=1).toordinal()
        end_date = date.today().toordinal()
        random_day = date.fromordinal(random.randint(start_date, end_date))
        return random_day
# need real data 
    kick = ['COPPERHIGHGRADE', 'GOLD1OZ', 'PALLADIUM1OZ', 'PLATINUM1UZ999', 'SILVER1OZ999NY']
    Country = []
    for a in currency:
        if a in kick:
            continue
        elif a == 'USD':
            Country.append(a)
            continue
        elif a.replace('USD','') == '':
            continue
        Country.append(a.replace('USD','')) 
    
    Money_name = [ 'USD', 'HKD', 'GBP', 'AUD', 'CAD', 'SGD', 'CHF', 'JPY', 'ZAR', 'SEK', 'NZD', 'THB', 'PHP', 'IDR', 'EUR', 'KRW', 'VND', 'MYR', 'CNY']

    x = pd.read_csv('data/20170102/symbols.csv', delimiter = '\t', names = ['fuck', 'you'])
    company_name = x['you']
    symbol = x['fuck']
    field = ['date','open','high','low','close','volume','adj_close']     
                    

    user_goal = ["Exchange","Query","Get_exchange_rate","USDX"]
    
    Exchange = {"country1":Country,"country2":Country}
    Query = {"symbol":symbol,"company_name":company_name,"date":None,"field":field}
    USDX = {"time_start":None,"time_end":None}
    Get_exchange_rate = {"Money_name": Money_name, "type":["spot","cash"], "buy":["buy","sell"]}
    slots = {"Exchange":Exchange, "Query":Query, "Get_exchange_rate":Get_exchange_rate,"USDX":USDX}
    
    request = {"Exchange":("taiwan_rate","UNK"),"Query":("price_info","UNK"),"Get_exchange_rate":("ex_rate","UNK"),"USDX":("index","UNK")}

    #diaact
if __name__ == '__main__':
    episode1 = episode(object)
    episode1.dump()
    print(initializer(episode1))
#import pdb;pdb.set_trace()