#from state import State
#from nn import NLU
from rule_simulator import RuleSimulator, initializer

currturn = 0
maxturn = 12
#system
#system = State()

#user
user = RuleSimulator()
print "New episode, user goal:"
user.goal.dump()
over = user.episode_over
import pdb;pdb.set_trace()
nl_input = initializer(user)
while (not over):
	#system side
	[slot,intent] = NLU(nl_input,system)
	system.update = (slot,intent,nl_input)
	frame_output = system.reply()
	currturn += 2

	if currturn>= maxturn :
		break
	#user side
	nl_input = user.next(frame_output)
	over = user.episode_over
	
if user.success:
	pass
else:
	pass



