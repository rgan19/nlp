import sys
def add(dictionary,first,second,value):
    if first not in dictionary.keys():
        dictionary[first]={}
    dictionary[first][second]=float(value)


def retrieveweights(filename):
    overalldict={}
    transitiondict={}
    emissiondict={}
    with open(filename, 'r') as f:
        for line in f:
            if line != "":
                emission = True
                nature=line.split(":")[0]
                value=line[line.index(':')+1:].split(" ")[1]
                first=line[line.index(':')+1:].split(" ")[0].split("+")[0]            
                second=line[line.index(':')+1:].split(" ")[0].split("+")[1]
                if nature == "transition":
                    emission = False
                if emission:
                    add(emissiondict,first,second,value)
                else:
                    add(transitiondict,first,second,value)
        
                 
    overalldict['transition']=transitiondict
    overalldict['emission']=emissiondict
    return overalldict

def weight(first,second,overalldict,emission):
    if emission:
        print(overalldict['emission'][first][second])
    else:
        print(overalldict['transition'][first][second])

def scoreofsequence(x,y,overalldict):
    y.append("STOP")
    y.insert(0,"START")
    score = 0
    for i in range(1,len(y)):
        score += overalldict['transition'][y[i-1]][y[i]]
        if i != (len(y)-1):
            score += overalldict['emission'][y[i]][x[i-1]]
    return score

def viterbi(x,overalldict):
    worddict={0:{"START":0}}
    pointer={}
    y=[]
    for i in range(len(x)):
        worddict[i+1]={}
        pointer[i]={}
        for currenty in worddict[i].keys():
            score = worddict[i][currenty]
            if currenty !='STOP':
                for nexty in overalldict['transition'][currenty].keys():
                    current=score+overalldict['transition'][currenty][nexty]
                    if nexty !='STOP':
                        current+=overalldict['emission'][nexty].get(x[i],0)
                        if ((worddict[i+1].get(nexty)!=None and current > worddict[i+1][nexty]) or (worddict[i+1].get(nexty)==None)):
                            pointer[i][nexty]=currenty
                            worddict[i+1][nexty]=current
                    
    worddict[len(x)+1]={}
    pointer[len(x)]={}
    for currenty in worddict[len(x)].keys():
        nexty="STOP"
        if currenty!='STOP':
            score = worddict[len(x)][currenty]+overalldict['transition'][currenty][nexty]
            if (worddict[len(x)+1].get(nexty)!=None and score > worddict[len(x)+1][nexty]) or (worddict[len(x)+1].get(nexty)==None):
                pointer[len(x)][nexty]=currenty
                worddict[len(x)+1][nexty]=score
    current="STOP"
    y.append(current)
    for i in range(len(x),-1,-1):
        y.insert(0,pointer[i][current])
        current = pointer[i][current]
    return y[1:-1]

def test(testfile,output,overalldict):
    x = []
    y = []
    with open(output, "w") as output:
        for line in open(testfile, "r"):
            if line == "\n":
                y=viterbi(x,overalldict)
                for i in range(len(x)):
                    string = str(x[i]) + " " + str(y[i]) +"\n"
                    output.write(string)
                x=[]
                output.write("\n")
            else:
                x.append(line[:-1])


# =============================================================================
# overalldict = retrieveweights("results")
# x = [ 'All', 'in', 'all',',','the','food','was','great','(','except','for','the','dessserts',')','.']
# y = ['O','O','O','O','O','B-positive','O','O','O','O','O','O','B-negative','O','O']
# print(scoreofsequence(x,y,overalldict))
# print(viterbi(x,overalldict))
# print(test("dev.in","dev.p2.out",overalldict))
# 
# =============================================================================
if __name__ == "__main__":
    if len(sys.argv) < 3: #original = 3
        print ('Please make sure you have installed Python 3.4 or above!')
        print ("Usage on Windows:  python part2.py [dict file] [dev.in file] [dev.out file]")
        print ("Usage on Linux/Mac:  python3 part2.py [dict file] [dev.in file] [dev.out file]")
        sys.exit()

    overalldict = retrieveweights(sys.argv[1])
    test(sys.argv[2],sys.argv[3],overalldict)










