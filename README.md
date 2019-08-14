# 50.040 Natural Language Processing Project

### Part 1: Features Dictionary
Calculates the transition and emission probabilities. The resulting features are stored in a dictionary

Run the following command to start training:
```
python3 part1.py [train file]
# for example
python3 part1.py data/EN/train data/EN/features
```

### Part 2: Viterbi Algorithm 

Run the following command to start training:
```
python3 part2.py [dictionary file from part 1] [dev.in] [dev.out]
# for example
python3 part2.py results data/EN/dev.in data/EN/dev.p2.out
```



### Part 5: Viterbi Algorithm 

* HMM 
```
python part5/hmm/viterbi.py [train file] [dev.in file] [result filepath]
#for example
python part5/hmm/viterbi.py data/ES/train data/ES/dev.in data/ES/dev.p5.out
```

* CRF with more features (Built with Library)

```
python part5/crf_feature/crf_library.py [train file] [dev.in file] [result filepath]
#for example
python part5/crf_feature/crf_library.py data/ES/train data/ES/dev.in data/ES/dev.p5.out
```
