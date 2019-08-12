import sys
import math

f = {}
tags = []
obs = []
y_count_dict = {}

def train (file=None):
	# y_count_dict = {}
	emission_count_dict = {}
	with open(file, "r") as f:
		for line in f.readlines():
			if line == "\n":
				continue
			word, tag = line.split()
			if word not in obs: 
				obs.append(word)
			if tag not in tags:
				tags.append(tag)


			if (word, tag) in emission_count_dict:
				emission_count_dict[(word, tag)] += 1
			else:
				emission_count_dict[(word, tag)] = 1

			if tag in y_count_dict:
				y_count_dict[tag] += 1
			else: 
				y_count_dict[tag] = 1

	#all other possible emission probabilities
	for i in range(len(tags)):
		for j in range(len(obs)):
			word = obs[j]
			tag = tags[i]
			if (word, tag) not in emission_count_dict:
				emission_count_dict[(word, tag)] = 0

	calc_e(y_count_dict, emission_count_dict)

def calc_e(y_count_dict, emission_count_dict):
	e = {}
	for (word, tag) in emission_count_dict.keys():
		prob = emission_count_dict[(word, tag)] / (y_count_dict[tag])
		e[(word, tag)] = prob

		str_key = "emission:" + tag + "+" + word
		if emission_count_dict[(word, tag)] == 0:
			val  = - math.inf
		else:
			val = math.log(prob)

		f[str_key] = val

	return e
	
	

def train_transition(train):
	
	with open(train, 'r') as f:
		data = f.read().rstrip().splitlines()

	counts_uv = {}
	count_start = 1

	for i in range(len(data)):
		element = data[i]
		
		# print ("{} |length {}".format(element, len(element)))
		if (len(element) != 0):
			temp = element.split()
			u = temp[1] #current tag

		if (i != len(data) - 1):
			if len(data[i+1]) != 0: #check if next tag is empty
				v = data[i+1].split()[-1] #get next tag
				uv = (u, v)

				if (uv not in counts_uv):
					counts_uv[uv] = 1
				else:
					counts_uv[uv] += 1
		

		if (len(element) == 0):
			
			start_y1 = ("START", data[i+1].split()[-1])

			count_start += 1

			if (start_y1 not in counts_uv):
				counts_uv[start_y1] = 1
			else:
				counts_uv[start_y1] += 1


			stop_yn = (data[i-1].split()[-1], "STOP")

			if (stop_yn not in counts_uv):
				counts_uv[stop_yn] = 1
			else:
				counts_uv[stop_yn] += 1


	y_count_dict["START"] = count_start
	y_count_dict["STOP"] = count_start

	# for all the possible tag combinations in tags list (excluding start and stop)
	for i in range(len(tags)):
		if ("START", tags[i]) not in counts_uv:
			counts_uv[("START", tags[i])] = 0
		if (tags[i], "STOP") not in counts_uv:
			counts_uv[(tags[i], "STOP")] = 0

		for j in range(len(tags)):
			curr = tags[i]
			next_tag = tags[j]
			if (curr, next_tag) not in counts_uv:
				counts_uv[(curr, next_tag)] = 0
	return calc_transition(y_count_dict, counts_uv)

def calc_transition(y_count_dict, counts_uv):

	q = {}
	for tag_uv, count in counts_uv.items():
		y_j = tag_uv[0]
		y_i = tag_uv[1]
		q[(y_i, y_j)] = count / y_count_dict[y_j]

		str_key = "transition:" + y_j + "+" + y_i
		if count == 0:
			val  = - math.inf
		else:
			val = math.log(count/y_count_dict[y_j])
		f[str_key] = val
	return q


def get_features(file=None):
	train(file)
	train_transition(file)

	# To write the list of features into a file to check
	with open("results", "w") as output:
		for (key, val) in f.items():
			output.write("{} {} \n".format(key, val))

	return f

if __name__ == "__main__":
    if len(sys.argv) < 2: #original = 3
        print ('Please make sure you have installed Python 3.4 or above!')
        print ("Usage on Windows:  python emission.py [train file]")
        print ("Usage on Linux/Mac:  python3 emission.py [train file]")
        sys.exit()

    e_dict = get_features(sys.argv[1])
   