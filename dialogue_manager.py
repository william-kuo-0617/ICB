from state import State
from nn import NLU
from rule_simulator import RuleSimulator, initializer

def run_an_episode():
	
	reward = 0
	currturn = 0
	maxturn = 12
	#system
	system = State()

	#user
	user = RuleSimulator()
	print "New episode, user goal:"
	user.goal.dump()
	over = user.episode_over
	nl_input = initializer(user.goal)
	print nl_input
	import pdb;pdb.set_trace()

	while (not over):
		#system side
		[slot,intent] = NLU(nl_input,system)
		system.update = (slot,intent,nl_input)
		frame_output = system.reply()
		currturn += 2
		if currturn>= maxturn :
			break
		reward -= 2
		#user side
		nl_input = user.next(frame_output)
		over = user.episode_over
		
	if user.success:
		reward += 2*maxturn
	else:
		reward -= maxturn

	return reward

if __name__ == '__main__':
	print (run_an_episode)
