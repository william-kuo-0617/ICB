from __future__ import print_function
import random
from datetime import date
import requests
import pandas as pd
import json
def initializer(episode1):
    init_temp = []
    if episode1.goal == 'exchange':
        init_temp = ["Please give me the exchange rate of "+episode1.inform_slots['country1']+" to "+episode1.inform_slots['country2']+"\n","I'd like to know the exchange rate of "+episode1.inform_slots['country1']+" to "+episode1.inform_slots['country2']+"\n"]
        init_temp.append(str("What is the exchange rate of "+episode1.inform_slots['country2']+"?"))
        init_temp.append(str("How's the exchange rate of "+episode1.inform_slots['country2']+"?"))
        init_temp.append(str("Give me the exchange rate"))
        init_temp.append(str("I'd like to know the exchange rate"))
        init_temp.append(str("exchange rate, please."))
        init_temp.append(str("The exchange rate between "+episode1.inform_slots['country1']+" and "+episode1.inform_slots['country2']+"."))
        return random.choice(init_temp)
    elif episode1.goal == 'query':
        init_temp = ["Please give me the share price detail of "+episode1.inform_slots['symbol']+" "+str(episode1.inform_slots['date'])+"\n", "What is the close price of "+episode1.inform_slots['symbol']+" on "+str(episode1.inform_slots['date'])+"?\n", "I'd like to know the open and low price of "+episode1.inform_slots['symbol']+" on "+str(episode1.inform_slots['date'])+"\n"]
        init_temp.append(str("Give me "+str(episode1.inform_slots['date'])+"'s stock price"))
        init_temp.append(str("the information of "+episode1.inform_slots['stock_name']+", please"))
        init_temp.append(str("I would like to see some stock information"))
        init_temp.append(str("Show me the stock price."))
        init_temp.append(str("I would like to see "+str(episode1.inform_slots['date'])+"'s "+episode1.inform_slots['stock_name']+" stock price"))
        init_temp.append(str("Please show me "+str(episode1.inform_slots['date'])+"'s "+episode1.inform_slots['stock_name']+" stock price."))
        return random.choice(init_temp)
    elif episode1.goal == 'get_exchange_rate':
        init_temp = ["what's the exchange rate of "+episode1.inform_slots['action']+" "+episode1.inform_slots['money_name']+" by TWD now in bank with "+episode1.inform_slots['types']+"?\n", "I want to "+episode1.inform_slots['action']+" some "+episode1.inform_slots['money_name']+" with "+episode1.inform_slots['types']+"?\n"]
        init_temp.append(str("I would like to "+episode1.inform_slots['action']+" some "+episode1.inform_slots['money_name']+"."))
        init_temp.append(str("I'd like to "+episode1.inform_slots['action']+" some "+episode1.inform_slots['money_name']+"."))
        init_temp.append(str("I want to "+episode1.inform_slots['action']+" some "+episode1.inform_slots['money_name']+"."))
        init_temp.append(str("I want to exchange my "+episode1.inform_slots['money_name']+"."))
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
        self.request_slots = episode.request[self.goal]
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
        print ("{\n\tgoal:\t",self.goal,',')
        print("\tinform_slots:{")
        for key,val in self.inform_slots.items():
            print("\t\t{0}: {1},".format(key,val))
        print("\t},")
        print ("\trequest_slot: {","{0}:{1}".format(self.request_slots[0],self.request_slots[1]),"},\n},")
    def date_gen(self,start_date):
        start_date = self.start_date.toordinal() if self.start_date is not None else date.today().replace(day=1, month=1).toordinal()
        end_date = date(2017,3,31).toordinal()
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

    x = pd.read_csv('../data/symbols.csv', delimiter = '\t', names = ['fuck', 'you'])
    company_name = x['you']
    symbol = x['fuck']
    field = ['date','open','high','low','close','volume','adj_close']     
                    

    user_goal = ["exchange","query","get_exchange_rate","USDX"]
    
    exchange = {"country1":Country,"country2":Country}
    query = {"symbol":symbol,"stock_name":company_name,"date":None,"field":field}
    USDX = {"time_start":None,"time_end":None}
    get_exchange_rate = {"money_name": Money_name, "types":["spot","cash"], "action":["buy","sell"]}
    slots = {"exchange":exchange, "query":query, "get_exchange_rate":get_exchange_rate,"USDX":USDX}
    
    request = {"exchange":("taiwan_rate","UNK"),"query":("price_info","UNK"),"get_exchange_rate":("ex_rate","UNK"),"USDX":("index","UNK")}

if __name__ == '__main__':
    for _ in range(100):
        episode1 = episode(object)
        episode1.dump()
        print(initializer(episode1))