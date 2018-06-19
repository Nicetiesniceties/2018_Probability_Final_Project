# love connected <3
import random
import numpy as np
import random
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import statistics
people = 100
people = 100
query = 10
def simple_oracle(Mr, Mrs, Mr_to_Mrs_Right):# given number and the right_list, returning if they are perfect match
	if(Mr_to_Mrs_Right[Mr] != Mrs):
		return False;
	else:
		return True;
def sequential_algorithm(decision_map):# a algorithm given the decision_map, returning the next 10 picks #{{{
	my_picks = []
	for i in range(people):
		for j in range(people):
			if(decision_map[i][j] == 0):
				my_picks.append([i, j])
			if(len(my_picks) == query):
				return my_picks
	return my_picks
#}}}
def max_mispicks_algorithm(decision_map):#{{{
	count = 0
	for i in range(people):
		for j in range(people):
			if(decision_map[i][j] == 0):
				count += 1
			if(count == query):
				break
		if(count == query):
			break
	mypicks = [[-1, -1]] * count
	mispicks_mypicks = [0] * count
	decision_map_T =  decision_map[::-1]
	mispicks_map = [[0 for i in range(people)] for j in range(people)]
	for i in range(people):
		for j in range(people):
			if(decision_map[i][j] == 1):
				mispicks_map[i][j] = -1
			elif(decision_map[i][j] == -1):
				mispicks_map[i][j] == -1
			else:
				mispicks_map[i][j] += decision_map[i].count(-1) + decision_map_T[j].count(-1)
	for i in range(people):
		for j in range(people):
			MIN = min(mispicks_mypicks)
			if(mispicks_map[i][j] >= MIN):
				mypicks[mispicks_mypicks.index(MIN)] = [i, j]
				mispicks_mypicks[mispicks_mypicks.index(MIN)] = mispicks_map[i][j]
	print(mypicks)
	return mypicks
#}}}
def scatter_algorithm(decision_map):#{{{
	mypicks = [[-1, -1]] * size
	mispicks_mypicks = [201] * size
	decision_map_T = decision_map[::-1]
	fake_decision_map = decision_map
	mispicks_map = [[0 for i in range(size * size)] for j in range(size * size)]
	for i in range(size * size):
		for j in range(size * size):
			if(decision_map[i][j] == 1):
				mispicks_map[i][j] = 201
			elif(decision_map[i][j] == -1):
				mispicks_map[i][j] == 201
			else:
				mispicks_map[i][j] += decision_map[i].count(-1) + decision_map_T[j].count(-1)
	for i in range(size * size):
		for j in range(size * size):
			MAX = max(mispicks_mypicks)
			if(mispicks_map[i][j] <= MAX):
				mypicks[mispicks_mypicks.index(MAX)] = [i, j]
				mispicks_mypicks[mispicks_mypicks.index(MAX)] = mispicks_map[i][j]
	# print(mypicks)
	return mypicks
#}}}
def random_algorithm(decision_map):# a algorithm given the decision_map, returning the next 10 picks #{{{
	my_picks, num, count = [], 0, 0
	for i in range(people):
		for j in range(people):
			if(decision_map[i][j] == 0):
				count += 1
			if(count == query):
				break
		if(count == query):
			break
	while(num < count):
		i = random.randint(0, people - 1)
		j = random.randint(0, people - 1)
		# print([i, j])
		if(( not [i, j] in my_picks) and (decision_map[i][j] == 0)):
			my_picks.append([i, j])
			num += 1
	return my_picks
#}}}
def event(algorithm): # given the algorithm, do a one-time-event and return the picking times.#{{{
	random.seed(datetime.now())
	Mr_to_Mrs_Right = [i for i in range(people)]
	random.shuffle(Mr_to_Mrs_Right)
	# 0 for "unknown", 1 for "perfect match", -1 for "not perfect match"
	decision_map = [[0 for i in range(people)] for j in range(people)]
	rounds, perfect_pick_found, history = 0, 0, []
	while(perfect_pick_found < people):
		# print("found: %d" % (perfect_pick_found))
		next_picks = algorithm(decision_map)
		# print(decision_map)
		rounds += 1
		# print(next_picks)
		for i in range(len(next_picks)):
			if(simple_oracle(next_picks[i][0], next_picks[i][1], Mr_to_Mrs_Right)):
				for j in range(people):
					decision_map[next_picks[i][0]][j] = -1
					decision_map[j][next_picks[i][1]] = -1
				decision_map[next_picks[i][0]][next_picks[i][1]] = 1
				perfect_pick_found += 1
				history.append(rounds)
			else:
				decision_map[next_picks[i][0]][next_picks[i][1]] = -1
	return rounds, history
#}}}
def random_experiment(algorithm, iteration):# given the algorithm and iteration times, sampling as many events as the iteration.#{{{
	sample_space, mean = [], 0
	history = np.zeros(100)
	for i in range(iteration):
		n, temp = event(algorithm)
		history += temp
		print("Iteration %d: outcome is %d rounds" %(i, n))
		sample_space.append(n)
		mean += n
	dev = statistics.stdev(sample_space)
	np.save(str(algorithm) + ' ' + str(iteration), sample_space)
	return mean / iteration, sample_space, dev, history / iteration
#}}}
def draw_histogram(mean, sample_space, dev, iteration, name): # draw your outcome and save it as png #{{{
	mpl.style.use('seaborn')
	plt.hist(sample_space, color = '#fccf0d', edgecolor='#2a2927', linewidth=2.0)
	plt.title(name)
	plt.text(mean, sample_space.count(int(mean)), r'$\mu=%f,\ \sigma=%s$'%(mean, dev), bbox={'facecolor':'grey', 'alpha':0.5, 'pad':10})
	plt.xlabel("Picking Rounds")
	plt.ylabel("Frequency")
	fig = plt.gcf()
	plt.savefig(name + '.png')
	plt.gcf().clear()
#}}}
def draw_history(mean, iteration, history, name): # draw your history and save it as png #{{{
	mpl.style.use('seaborn')
	plt.plot(history, [i for i in range(1, 101)], mfc = '#1a2c56', marker = 'o', markersize = 3.5, color = '#d1a683')
	# plt.plot(history, color = '#fccf0d', marker = 'o')
	plt.title(name)
	plt.text(100, 0, r"Iteration: %d, $\mu:$ %f" % (iteration, mean), bbox={'facecolor':'grey', 'alpha':0.5, 'pad':10})
	plt.xlabel("Rounds Taken")
	plt.ylabel("The i-th Perfect Match Found")
	plt.axvline(x = mean, color = "#fccf0d")
	fig = plt.gcf()
	plt.savefig(name + '.png')
	plt.gcf().clear()
#}}}
if __name__ == '__main__':
	people = 100
	query = 10
	iteration = 1000
	name = "Sequential Method"
	mean, sample_space, dev, history = random_experiment(sequential_algorithm, iteration)
	draw_histogram(mean, sample_space, dev, iteration, name  + "\n" + str(datetime.now()))
	draw_history(mean, iteration, history, name + " History \n" + str(datetime.now()))
