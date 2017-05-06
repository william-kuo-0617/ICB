import dialog_config
from episoda import *
import pdb
class RuleSimulator(object):
    """docstring for RuleSimulator"""
    def __init__(self):
        #super(RuleSimulator, self).__init__()
        self.initialize_episode()

    def initialize_episode(self):
        """ Initialize a new episode (dialog) 
        state['history_slots']: keeps all the informed_slots
        state['rest_slots']: keep all the slots (which is still in the stack yet)
        """
        self.state = {}
        self.state['history_slots'] = {}
        self.state['inform_slots'] = {}
        self.state['request_slots'] = {}
        self.state['rest_slots'] = []
        self.state['turn'] = 0
        self.reward = 0
        self.episode_over = False
        self.dialog_status = dialog_config.NO_OUTCOME_YET
        
        self.goal = episode() #random generate a user goal


        # self.goal['request_slots']['ticket'] = 'UNK'
        # self.constraint_check = dialog_config.CONSTRAINT_CHECK_FAILURE
        """ Debug: build a fake goal mannually """
        #self.debug_falk_goal()
        
        # sample first action
        user_action = {}
        user_action['diaact'] = self.state['diaact']
        user_action['inform_slots'] = self.state['inform_slots']
        user_action['request_slots'] = self.state['request_slots']
        user_action['turn'] = self.state['turn']
        user_action['nl'] = initializer(self.goal)

        assert (self.episode_over != 1),' but we just started'
        pdb.set_trace()

        return user_action

    def next(self, system_action):
        """ Generate next User Action based on last System Action """
        
        self.state['turn'] += 2
        self.episode_over = False
        self.dialog_status = dialog_config.NO_OUTCOME_YET
        
        
        ##get system action
        sys_act = system_action['system_action']


        # if (self.max_turn > 0 and self.state['turn'] > self.max_turn):
        #     self.dialog_status = dialog_config.FAILED_DIALOG
        #     self.episode_over = True
        #     self.state['diaact'] = "closing"
        # else:
        self.state['history_slots'].update(self.state['inform_slots'])
        self.state['inform_slots'].clear()

        if sys_act == "inform":
            self.response_inform(system_action)
        elif sys_act == "multiple_choice":
            self.response_multiple_choice(system_action)
        elif sys_act == "request":
            self.response_request(system_action) 
        elif sys_act == "closing":
            self.response_thanks(system_action)
        elif sys_act == "confirm_answer":
            self.response_confirm_answer(system_action)
        elif sys_act == "response":
            self.response_response(system_action)
        elif sys_act == "closing":
            self.episode_over = True
            #self.state['diaact'] = "thanks"

        #self.corrupt(self.state)
        
        response_action = {}
        response_action['diaact'] = self.state['diaact']
        response_action['inform_slots'] = self.state['inform_slots']
        response_action['request_slots'] = self.state['request_slots']
        response_action['turn'] = self.state['turn']
        response_action['nl'] = ""
        
        # add NL to dia_act
        self.add_nl_to_action(response_action)                       
        return response_action, self.episode_over, self.dialog_status

    def response_response(self, system_action):
        response = []
        error = 0
        if system_action['action'][0] != self.goal.goal:
            response.append(str("intent error"))
            error = 1
        for i in system_action['slot']:
            if self.goal.inform_slots.get(i) == None or self.goal.inform_slots.get(i) != system_aciton['slot'][i]
                response.append(str("slot error with "+i+" "+self.goal.inform_slots.get(i)+" "+system_aciton['slot'][i]"."))
                error = 1
                break
        if error
            self.reward -= 10
            return random.choice(response)
        else
            self.reward += 20
            response.append(str"Thanks!")
            return random.choice(response)


    def response_request(self,system_action):
        response = []
        if self.goal.goal == 'Exchange':
            if system_action['action_item'][0] != 'exchange':
                response.append(str("intent error"))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'country1':
                response.append(str(self.goal.inform_slots['country1']))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'country2':
                response.append(str(self.goal.inform_slots['country2']))
            elif len(system_action['slot']) == 2:
                response.append(str("The exchange rate between "+self.goal.inform_slots['country1']+" and "+self.goal.inform_slots['country2']+"."))
                response.append(str(self.goal.inform_slots['country1']+" and "+self.goal.inform_slots['country2']+"."))
                response.append(str("Between "+self.goal.inform_slots['country1'][0]+" and "+self.goal.inform_slots['country2'][0]+"."))
            self.reward -= 2
            return random.choice(response)
        elif self.goal.goal == 'Query':
            if system_action['action_item'][0] != 'query':
                response.append(str("intent error"))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'stock':
                response.append(str(self.goal.inform_slots['company_name']))
                response.append(str("the information of "+self.goal.inform_slots['company_name']+", please."))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'date':
                response.append(str(str(self.goal.inform_slots['date'])+"'s")) 
            elif: len(system_action['slot']) == 2:
                response.append(str("l'd like to see "+str(self.goal.inform_slots['date'])+"'s "+self.goal.inform_slots['company_name']+" stock price."))
                response.append(str("Please show me "+str(self.goal.inform_slots['date'])+"'s "+self.goal.inform_slots['company_name']+" stock price."))
            self.reward -= 2
            return random.choice(response)
        elif self.goal.goal == 'Get_exchange_rate':
            if system_action['action_item'][0] != 'get_exchange_rate':
                response.append(str("intent error"))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'Money_name':
                response.append(str(self.goal.inform_slots['Money_name']))
                response.append(str("To "+self.goal.inform_slots['Money_name']+"."))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'action':
                response.append(str("I want to "+self.goal.inform_slots['action']+" some."))
                response.append(str("To "+self.goal.inform_slots['action']+" it."))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'types':
                response.append(str(self.goal.inform_slots['type']+", please."))
                response.append(str("with "+self.goal.inform_slots['action']+"."))
            self.reward -= 2
            return random.choice(response)
        elif self.goal.goal == 'USDX':
            if system_action['action_item'][0] != 'USDX':
                response.append(str("intent error"))
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
                response.append("From "+str(goal.inform_slots['time_start'])+" to "+str(self.goal.inform_slots['time_end'])+".")
                response.append("Between "+str(goal.inform_slots['time_start'])+" and "+str(self.goal.inform_slots['time_end'])+".")
            self.reward -= 2
            return random.choice(response)
    def response_inform(self,system_action):
        pass
    def response_confirm_answer(self,system_action):
        
    


if __name__ == '__main__':
    r = RuleSimulator()
    pdb.set_trace()