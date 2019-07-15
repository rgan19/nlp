import sys
import math

f = {}
tags = []
obs = []

def train (file=None, k=1):
	y_count_dict = {}
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

	calc_e(y_count_dict, emission_count_dict)

def calc_e(y_count_dict, emission_count_dict):
	e = {}
	for (word, tag) in emission_count_dict.keys():
		prob = emission_count_dict[(word, tag)] / (y_count_dict[tag])
		e[(word, tag)] = prob

		str_key = "emission:" + tag + "+" + word
		val = math.log(prob)

		f[str_key] = val
	
	return f

if __name__ == "__main__":
    if len(sys.argv) < 2: #original = 3
        print ('Please make sure you have installed Python 3.4 or above!')
        print ("Usage on Windows:  python emission.py [train file] [dev.in file]")
        print ("Usage on Linux/Mac:  python3 emission.py [train file] [dev.in file]")
        sys.exit()

    e_dict = train(sys.argv[1])
    # tag_sequences = test(e_dict, sys.argv[2])
    # create_test_result_file(tag_sequences, "dev.p2.out")