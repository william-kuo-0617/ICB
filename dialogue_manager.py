from state import State
from nn_model import NN
from rule_simulator import RuleSimulator, initializer
import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from w2v import DataPrepare
import argparse
import fileinput

def run_an_episode():
	
	reward = 0
	currturn = 0
	maxturn = 12
	#system
	system = State()

	#user
	user = RuleSimulator()
	print ("New episode, user goal:")
	user.goal.dump()
	print('_ _ _ _ _ _ _ _ _ _ _ _')
	over = user.episode_over
	nl_input = initializer(user.goal)
	turn_by_turn(currturn,nl_input,,)
	import pdb;pdb.set_trace()
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	sess = tf.Session(config=config)
	nlu = NN(sess)
	while (not over):
		#system side
		slot,intent = nlu.predict(nl_input,system)
		system.update(slot,intent,nl_input)
		frame_output = system.reply()
		turn_by_turn(currturn+1,frame_output,'system')
		currturn += 2
		if currturn>= maxturn :
			break
		reward -= 2
		#user side
		nl_input = user.next(frame_output)
		turn_by_turn(currturn,nl_input,'user')
		over = user.episode_over
		
	if user.success:
		print("Successful")
		reward += 2*maxturn
	else:
		print("Fail")
		reward -= maxturn

	return reward
def turn_by_turn(currturn,turn,who):
	print("turn{0} {1}:".format(currturn,who),turn)
if __name__ == '__main__':
	print (run_an_episode)
