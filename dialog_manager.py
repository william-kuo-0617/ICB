from deep_dialog import dialog_config
from rule_simulator import *
act_sett = ['request']
slot_sett = ['country1']
goal_sett = ['Exchange']

class DialogManager:

	def __init__(self,user,act_set,slot_set):
        #self.agent = agent
		self.user = user
		self.act_set=act_set
		self.slot_set=slot_set
		s0elf.user_action=None
		self.reward=0
		self.episode_over=False

	def initialize_episode(self):
		""" Refresh state for new dialog """
		self.reward = 0
		self.episode_over = False
		self.user_action = self.user.initialize_episode()
        
		if dialog_config.run_mode < 3:
			print ("New episode, user goal:")
			#print (json.dumps(self.user.goal, indent=2))
		print(self.user_action['nl'])

user_sim = RuleSimulator()
dm = DialogManager(user_sim, act_sett, slot_sett, gaol_sett)
dm.initialize_episode()