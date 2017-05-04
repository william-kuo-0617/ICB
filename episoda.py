import random
from datetime import date
#from __future__ import print_function

class episode(object):
    """docstring for episode."""
    def __init__(self, arg):
        #super(episode, self).__init__()
        self.goal = self.getgoal()
        self.request = episode.request[self.goal]
        self.start_date = None
        self.inform_slots = self.slots_fill_in(self.start_date)
        self.dump()

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
                tmp[slot] = episode.slots[self.goal][slot][j]
        return tmp

    def dump(self):
        print"{goal:",self.goal,"};"
        print("{inform_slots:")
        for key,val in self.inform_slots.items():
            print("\t{0}: {1}".format(key,val))
        print("};")
        print "{request_slot:\n","\t{0}:{1}\n".format(self.request[0],self.request[1]),"};"
    def date_gen(self,start_date):
        start_date = self.start_date.toordinal() if self.start_date is not None else date.today().replace(day=1, month=1).toordinal()
        end_date = date.today().toordinal()
        random_day = date.fromordinal(random.randint(start_date, end_date))
        return random_day
# need real data 
###################################################
    Country = ["#value1","#value2","#value3"]     #
    Money_name = ["#value", "#value2", "#value3"] #
    field = ["#value1", "#value2", "#value3"]     #
    symbol = ["qq","ww","ee"]                     #
###################################################
    user_goal = ["Exchange","Query","Get_exchange_rate","USDX"]
    Exchange = {"country1":Country,"country2":Country}
    Query = {"symbol":symbol,"date":None,"field":field}
    USDX = {"time_start":None,"time_end":None}
    Get_exchange_rate = {"Money_name": Money_name, "type":["spot","cash"], "buy":[0,1]}
    slots = {"Exchange":Exchange, "Query":Query, "Get_exchange_rate":Get_exchange_rate,"USDX":USDX}
    request = {"Exchange":("taiwan_rate","UNK"),"Query":("price_info","UNK"),"Get_exchange_rate":("ex_rate","UNK"),"USDX":("index","UNK")}

    #diaact

episode1 = episode(object)
