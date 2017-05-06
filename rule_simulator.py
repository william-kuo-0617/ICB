from episoda import *
import pdb
from pprint import pprint
class RuleSimulator(object):
    """docstring for RuleSimulator"""
    def __init__(self):
        #super(RuleSimulator, self).__init__()
        self.initialize_episode()

    def initialize_episode(self):
        self.episode_over = False
        self.success = False
        self.goal = episode(object) #random generate a user goal
        assert (self.episode_over != 1),' but we just started'

    def next(self, system_action):
        """ Generate next User Action based on last System Action """
        
        self.episode_over = False
        
        ##get system action
        sys_act = system_action['system_action'][0]
        print(sys_act)
        nl_response = None

        if sys_act == "inform":
            nl_response = self.response_inform(system_action)
        elif sys_act == "request":
            nl_response = self.response_request(system_action) 
        
        elif sys_act == "confirm_answer":
            nl_response = self.response_confirm_answer(system_action)
        elif sys_act == "response":
            nl_response = self.response_response(system_action)
        elif sys_act == "closing":
            nl_response = None
            self.episode_over = True
                               
        return nl_response

    def response_response(self, system_action):
        response = []
        error = 0
        if system_action['action_item'][0] != self.goal.goal:
            response.append(str("Thanks1"))
            error = 1
        if error == 0:    
            for i in system_action['slot']:
                if self.goal.inform_slots.get(i) == None or self.goal.inform_slots.get(i) != system_action['slot'][i]:
                    response.append(str("Thanks2"))
                    #response.append(str("slot error with "+i+" "+self.goal.inform_slots.get(i)+" "+system_aciton['slot'][i]"."))
                    error = 1
                    break
        if error==1:
            print ("ERROR!")
            self.episode_over = True
            return random.choice(response)
        else:
            self.success = True
            response.append(str("Thanks3"))
            return random.choice(response)


    def response_request(self,system_action):
        response = []
        if self.goal.goal == 'exchange':
            if system_action['action_item'][0] != 'exchange':
                response.append(str("Thanks"))
                self.episode_over = True
                return random.choice(response)
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'country1':
                response.append(str(self.goal.inform_slots['country1']))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'country2':
                response.append(str(self.goal.inform_slots['country2']))
            elif len(system_action['slot']) == 2:
                response.append(str("The exchange rate between "+self.goal.inform_slots['country1']+" and "+self.goal.inform_slots['country2']+"."))
                response.append(str(self.goal.inform_slots['country1']+" and "+self.goal.inform_slots['country2']+"."))
                response.append(str("Between "+self.goal.inform_slots['country1'][0]+" and "+self.goal.inform_slots['country2'][0]+"."))
            return random.choice(response)
        elif self.goal.goal == 'query':
            if system_action['action_item'][0] != 'query':
                response.append(str("Thanks"))
                self.episode_over = True
                return random.choice(response)
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'stock':
                response.append(str(self.goal.inform_slots['company_name']))
                response.append(str("the information of "+self.goal.inform_slots['company_name']+", please."))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'date':
                response.append(str(str(self.goal.inform_slots['date'])+"'s")) 
            elif len(system_action['slot']) == 2:
                response.append(str("l'd like to see "+str(self.goal.inform_slots['date'])+"'s "+self.goal.inform_slots['company_name']+" stock price."))
                response.append(str("Please show me "+str(self.goal.inform_slots['date'])+"'s "+self.goal.inform_slots['company_name']+" stock price."))
            return random.choice(response)
        elif self.goal.goal == 'get_exchange_rate':
            if system_action['action_item'][0] != 'get_exchange_rate':
                response.append(str("Thanks"))
                self.episode_over = True
                return random.choice(response)
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'Money_name':
                response.append(str(self.goal.inform_slots['Money_name']))
                response.append(str("To "+self.goal.inform_slots['Money_name']+"."))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'action':
                response.append(str("I want to "+self.goal.inform_slots['action']+" some."))
                response.append(str("To "+self.goal.inform_slots['action']+" it."))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'types':
                response.append(str(self.goal.inform_slots['type']+", please."))
                response.append(str("with "+self.goal.inform_slots['action']+"."))
            return random.choice(response)
        elif self.goal.goal == 'USDX':
            if system_action['action_item'][0] != 'USDX':
                response.append(str("Thanks"))
                self.episode_over = True
                return random.choice(response)
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'time_start':
                response.append(str(str(self.goal.inform_slots['time_start'])))
                response.append(str("In "+str(self.goal.inform_slots['time_start'])+"."))
                response.append(str("The time period starts in "+str(self.goal.inform_slots['time_start'])+"."))
                response.append(str("Start in "+str(self.goal.inform_slots['time_start'])+"."))
                return random.choice(response)
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'time_end':
                response.append(str("In "+str(self.goal.inform_slots['time_end'])+"."))
                response.append(str("The time period ends in "+str(self.goal.inform_slots['time_end'])+"."))
                response.append(str("Ends in" +str(self.goal.inform_slots['time_end'])+"."))
            elif len(system_action['slot']) == 2:
                response.append("From "+str(self.goal.inform_slots['time_start'])+" to "+str(self.goal.inform_slots['time_end'])+".")
                response.append("Between "+str(self.goal.inform_slots['time_start'])+" and "+str(self.goal.inform_slots['time_end'])+".")

            return random.choice(response)
    def response_inform(self,system_action):
        pass
    def response_confirm_answer(self,system_action):
        if system_action['action_item'][0] != self.goal.goal:
            response = "Thanks"
            self.episode_over = True
            return response
        for i in system_action['slot']:
            if  self.goal.inform_slots.get(i) == None:
                response = "Thanks"
                self.episode_over = True
                return response
            elif self.goal.inform_slots.get(i) != system_action['slot'][i]:
                response = "No."
                return response    
        response = "Yes."
        return response

if __name__ == '__main__':
    r = RuleSimulator()
    r.goal.dump()
    tmp = {}
    tmp['system_action'] = ['response']
    tmp['action_item'] = [r.goal.goal]
    tmp['slot'] = r.goal.inform_slots
    pprint(tmp)
    print ("---------")
    print (r.next(tmp))
    print(r.success,r.episode_over)
    pdb.set_trace()