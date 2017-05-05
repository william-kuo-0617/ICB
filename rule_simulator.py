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
        #sys_act = system_action['diaact']


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
        elif sys_act == "thanks":
            self.response_thanks(system_action)
        elif sys_act == "confirm_answer":
            self.response_confirm_answer(system_action)
        elif sys_act == "closing":
            self.episode_over = True
            self.state['diaact'] = "thanks"

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

        

    def response_thanks(self,system_action):
        pass


    def response_request(self,system_action):
        pass
    def response_inform(self,system_action):
        pass
    def response_confirm_answer(self,system_action):
        pass  
    


if __name__ == '__main__':
    r = RuleSimulator()
    pdb.set_trace()