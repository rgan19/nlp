import sys
import yaml
import sklearn_crfsuite


def get_train_data(file):
    # y_count_dict = {}
    data = []
    with open(file, "r", encoding="utf-8") as f:
        sentence = []
        # current_pair = []
        for line in f.readlines():
            if line == "\n":
                data.append(sentence)
                sentence = []
            else:
                word, tag = line.split()
                sentence.append((word, tag))
    return data

class CRF(object):
    def __init__(self):
        return

    def fit(self, train_data):
        feature_conf = self.load_yaml_conf("part5/crf_feature/features.yaml")
        x_train = [self.sent_to_features(s, feature_conf) for s in train_data]
        y_train = [self.sent_to_labels(s) for s in train_data] 
        self.crf_model = self.train_crf(x_train, y_train)
    
    def predict(self, test_file, outfile):
        if not self.crf_model:
            print("No model trained.")
        test_data = self.read_test_file(test_file)
        x_test = []
        for line in test_data:
            word_arr = line.splitlines()
            word_arr_features = self.sent_to_features_test(word_arr, self.load_yaml_conf("part5/crf_feature/features.yaml"))
            x_test.append(word_arr_features)
        y_predict = self.crf_model.predict(x_test)
        
        tag_sequences = []
        for i, line in enumerate(test_data):
            word_arr = line.splitlines()
            tag_sequences.append([(word_arr[j], y_predict[i][j]) for j in range(len(word_arr))])
        self.create_test_result_file(tag_sequences, outfile)
    
    def train_crf(self, x_train, y_train):
        crf = sklearn_crfsuite.CRF(
            algorithm="lbfgs",
            c1=0.1,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True
        )
        return crf.fit(x_train, y_train)

    def load_yaml_conf(self, conf_file):
        """Read features from a yaml config file
        """
        with open(conf_file, 'r') as f:
            try:
                result = yaml.load(f)
            except yaml.YAMLError as err:
                print(err)
        return result
    
    def feature_selector(self, word, tag, feature_conf, conf_switch):
        feature_dict = {
            'bias': 1.0,
            conf_switch + '_word.lower()': word.lower(),  
            conf_switch + '_word[-3]': word[-3:],  
            conf_switch + '_word[-2]': word[-2:],  
            conf_switch + '_word.isupper()': word.isupper(),  
            conf_switch + '_word.istitle()': word.istitle(),  
            conf_switch + '_word.isdigit()': word.isdigit(),  
            conf_switch + '_word.islower()': word.islower(),
            conf_switch + '_tag': tag 
        }
        return {i: feature_dict.get(i) for i in feature_conf[conf_switch] if i in feature_dict.keys()}

    def sent_to_features(sent):
        return [word_to_features(sent, i) for i in range(len(sent))]

    def sent_to_labels(sent):
        return [label for word, label in sent]

    def word_to_features(self, line, index, feature_conf):
        """Extract features based on the given word in sentence"""
        word, tag = line[index]
        features = self.feature_selector(word, tag, feature_conf, "current")
        if index > 0:
           prev_word, prev_tag = line[index-1]
           features.update(self.feature_selector(prev_word, prev_tag, feature_conf, "previous"))
        else:
            features["BOS"] = True
        
        if index < len(line) - 1:
            next_word, next_tag = line[index+1]
            features.update(self.feature_selector(next_word, next_tag, feature_conf, "next"))
        else:
            features["EOS"] = True
        return features
    
    def word_to_features_test(self, line, index, feature_conf):
        """Extract features based on the given word in sentence"""
        word = line[index]
        features = self.feature_selector(word, None, feature_conf, "current")
        if index > 0:
           prev_word = line[index-1]
           features.update(self.feature_selector(prev_word, None, feature_conf, "previous"))
        else:
            features["BOS"] = True
        
        if index < len(line) - 1:
            next_word = line[index+1]
            features.update(self.feature_selector(next_word, None, feature_conf, "next"))
        else:
            features["EOS"] = True
        return features
    
    def sent_to_features(self, line, feature_conf):
        return [self.word_to_features(line, i, feature_conf) for i in range(len(line))]
    
    def sent_to_features_test(self, line, feature_conf):
        return [self.word_to_features_test(line, i, feature_conf) for i in range(len(line))]

    def sent_to_labels(self, line):
        return [tag for _, tag in line]
    
    def read_test_file(self, file):
        with open(file, 'r', encoding="utf-8") as f:
            test_data = f.read().rstrip().split('\n\n')
        return test_data
    
    def create_test_result_file(self, test_result, filename):
        with open(filename, "w",  encoding="utf-8") as f:
            for sequence in test_result:
                for word, tag in sequence:
                    f.write(f"{word} {tag}\n")
                f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print ('Please make sure you have installed Python 3.4 or above!')
        print ("Usage on Windows:  python emission.py [train file] [dev.in file] [result filepath]")
        print ("Usage on Linux/Mac:  python3 emission.py [train file] [dev.in file] [result filepath]")
        sys.exit()

    train_data = get_train_data(sys.argv[1])
    crf = CRF()
    crf.fit(train_data)
    crf.predict(sys.argv[2], sys.argv[3])