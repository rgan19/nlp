# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 13:34:59 2019

@author: redfr
"""
from math import log,exp
import math
import copy
import sys

def logsumexp(A):
    k = max(A)
    return log(sum( exp(i-k) for i in A ))+k

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
                value=float(value)
                first=line[line.index(':')+1:].split(" ")[0].split("+")[0]            
                second= line[line.index(':')+1:].split(" ")[0][line[line.index(':')+1:].split(" ")[0].index("+")+1:]
                if nature == "transition":
                    emission = False
                if emission:
                    add(emissiondict,first,second,value)
                else:
                    add(transitiondict,first,second,value)
        
                 
    overalldict['transition']=transitiondict
    overalldict['emission']=emissiondict
    return overalldict

def forward(x,overalldict):
    worddict={0:{"START":0}}
    for i in range(len(x)):
        #print(x[i])
        worddict[i+1]={}
        for currenty in worddict[i].keys():
            for nexty in overalldict['transition'][currenty].keys():
                score=[]
                score.append(worddict[i][currenty])
                score.append(overalldict['transition'][currenty][nexty])
                if nexty !='STOP':
                    score.append(overalldict['emission'][nexty].get(x[i],-math.inf))
                    if (worddict[i+1].get(nexty)==None):
                        worddict[i+1][nexty]=logsumexp(score)
                    else:
                        score.append(worddict[i+1][nexty])
                        worddict[i+1][nexty]=logsumexp(score)
                    
    worddict[len(x)+1]={}
    for currenty in worddict[len(x)].keys():
        nexty="STOP"
        #print(currenty,nexty)
        score=[]
        score.append(worddict[len(x)][currenty])
        score.append(overalldict['transition'][currenty][nexty])
        if (worddict[len(x)+1].get(nexty)==None):
            worddict[len(x)+1][nexty]=logsumexp(score)
        else:
            score.append(worddict[len(x)+1][nexty])
            worddict[len(x)+1][nexty]=logsumexp(score)
    return worddict

def backward(x,overalldict):
    worddict={len(x)+1:{"STOP":1}}
    for i in range(len(x),0,-1):
        worddict[i]={}
        #print(x[i-1])
        for currenty in overalldict['transition']["START"].keys():
            for nexty in worddict[i+1].keys():
                score=[]
                score.append(worddict[i+1][nexty])
                if currenty !='STOP':
                    
                    score.append(overalldict['transition'][currenty][nexty])
                    #print(currenty,nexty)
                    #print(currenty,x[i-1])
                    score.append(overalldict['emission'][currenty].get(x[i-1],-math.inf))
                    if (worddict[i].get(currenty)==None):
                        worddict[i][currenty]=logsumexp(score)
                    else:
                        score.append(worddict[i][currenty])
                        worddict[i][currenty]=logsumexp(score)
    worddict[0]={}
    for nexty in worddict[1].keys():
        currenty="START"
        #print(currenty,nexty)
        score=[]
        score.append(worddict[1][nexty])
        score.append(overalldict['transition'][currenty][nexty])
        if (worddict[0].get(currenty)==None):
            worddict[0][currenty]=logsumexp(score)
        else:
            score.append(worddict[0][currenty])
            worddict[0][currenty]=logsumexp(score)
    return worddict



if __name__ == "__main__":
    if len(sys.argv) < 3: #original = 3
        print ('Please make sure you have installed Python 3.4 or above!')
        print ("Usage on Windows:  python part3.py [dict file] [train file] [grad file]")
        print ("Usage on Linux/Mac:  python3 part3.py [dict file] [train file] [grad file]")
        sys.exit()


    overalldict = retrieveweights(sys.argv[1])
    
    
    gradient = copy.deepcopy(overalldict)
    for i in gradient.keys():
        for j in gradient[i].keys():
            for k in gradient[i][j].keys():
                gradient[i][j][k]=0
                
    
    
    
    corpus = []
    x=[]
    y=["START"]
    words=set()
    tags=set()
    tags.add("START")
    tags.add("STOP")
    for line in open(sys.argv[2], "r",encoding='utf-8'):
        if line == "\n":
            y.append("STOP")
            corpus.append((x,y))
            x=[]
            y=[]
        else:
            broken = line.split(" ")
            x.append(broken[0])
            words.add(broken[0])
            y.append(broken[1][:-1])
            tags.add(broken[1][:-1])
    
    words=list(words)
    tags=list(tags)
    tags.remove("START")
    tags.remove("STOP")
    
    
    for (x,y) in corpus:
        bdict = backward(x,overalldict)
        fdict = forward(x,overalldict)
        z=bdict[0]['START']
    # =============================================================================
    #    print(bdict)
    #    print(fdict)
    #     print(z)
    #     print(x,y)
    #     print(len(x))
    # =============================================================================
        first="START"
        
        for second in tags:
            array=[gradient['transition'][first][second],fdict[0][first],bdict[1][second],overalldict['transition'][first][second]]
            gradient['transition'][first][second]=logsumexp(array)/z
        for i in range(1,len(x)):
            for first in tags:
                for second in tags:
                    array=[gradient['transition'][first][second],fdict[i][first],bdict[i+1][second],overalldict['transition'][first][second],overalldict['emission'][second][x[i-1]]]
                    gradient['transition'][first][second]=logsumexp(array)/z
                    array=[gradient['emission'][first][x[i]],fdict[i][first],bdict[i][first]]
                    gradient['emission'][first][x[i]]=logsumexp(array)/z
                    
        second="STOP"
        for first in tags:
            array=[gradient['transition'][first][second],fdict[len(x)][first],bdict[len(x)+1][second],overalldict['transition'][first][second]]
            gradient['transition'][first][second]=logsumexp(array)/z
    
            
    with open(sys.argv[3], "w") as output:
    	for i in gradient['emission'].keys():
            for j in gradient['emission'][i]:        
                output.write("emission:"+i+"+"+j+" "+str(gradient['emission'][i][j])+"\n")
    	for i in gradient['transition'].keys():
            for j in gradient['transition'][i]:        
                output.write("transition:"+i+"+"+j+" "+str(gradient['transition'][i][j])+"\n")





