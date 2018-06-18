# love connected <3
import random
import numpy as np
import random
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import statistics

def simple_oracle(Mr, Mrs, Mr_to_Mrs_Right):# given number and the right_list, returning if they are perfect match
	if(Mr_to_Mrs_Right[Mr] != Mrs):
		return False;
	else:
		return True;
def sequential_algorithm(decision_map):# a algorithm given the decision_map, returning the next 10 picks
	my_picks = []
	for i in range(100):
		for j in range(100):
			if(decision_map[i][j] == 0):
				my_picks.append([i, j])
			if(len(my_picks) == 10):
				return my_picks
def event(algorithm): # given the algorithm, do a one-time-event and return the picking times.
	random.seed(datetime.now())
	Mr_to_Mrs_Right = [i for i in range(100)]
	random.shuffle(Mr_to_Mrs_Right)
	# 0 for "unknown", 1 for "perfect match", -1 for "not perfect match"
	decision_map = [[0 for i in range(100)] for j in range(100)]
	
	rounds, perfect_pick_found = 0, 0
	while(perfect_pick_found < 10):
		next_picks = algorithm(decision_map)
		rounds += 1
		for i in range(10):
			if(simple_oracle(next_picks[i][0], next_picks[i][1], Mr_to_Mrs_Right)):
				for j in range(100):
					decision_map[next_picks[i][0]][j] = -1
					decision_map[j][next_picks[i][1]] = -1
				decision_map[next_picks[i][0]][next_picks[i][1]] = 1
				perfect_pick_found += 1
			else:
				decision_map[next_picks[i][0]][next_picks[i][1]] = -1
	return rounds
def random_experiment(algorithm, iteration):# given the algorithm and iteration times, sampling as many events as the iteration.
	sample_space, mean = [], 0
	for i in range(iteration):
		n = event(algorithm)
		print("Iteration %d: outcome is %d times" %(i, n))
		sample_space.append(n)
		mean += n
	dev = statistics.stdev(sample_space)
	return mean / iteration, sample_space, dev
def draw(mean, history, dev, name): # draw your outcome and save it as png
	mpl.style.use('seaborn')
	plt.hist(history, color = '#fccf0d', edgecolor='#2a2927', linewidth=4.0)
	plt.title(name)
	plt.text(mean, 1200, r'$\mu=%f,\ \sigma=%s$'%(mean, dev))
	plt.xlabel("Picking Rounds")
	plt.ylabel("Frequency")
	fig = plt.gcf()
	plt.savefig(name + '.png')

if __name__ == '__main__':
	mean, history, dev = random_experiment(sequential_algorithm, 10000)
	draw(mean, history, dev, "Sequential Algorithm")
