import csv
import fileinput
import json
import sys
from cdparser.Features import Features
from cdparser.LabeledEntry import LabeledEntry
import sklearn_crfsuite
from sklearn_crfsuite import metrics
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

class Classifier:
    def __init__ (self, training_data=None):
        self.training_set_labeled = []
        self.training_set_features = []
        self.training_set_labels = []
        self.validation_set_labeled = []
        self.validation_set_features = []
        self.validation_set_labels = []
        self.crf = None

    def load_labeled_data(self, path_to_csv, rows_to_ignore=0):
        rows = []
        labeled_data = []
        with open(path_to_csv, 'r') as csvfile:
            rdr = csv.reader(csvfile)
            index = -1
            for row in rdr:
                index += 1
                if index >= rows_to_ignore:
                    rows.append(row)
        example_number = -1
        example = None
        for row in rows:
            sentence_number = int(row[0])
            if sentence_number > example_number:
                example_number = sentence_number
                if example == None:
                    example = []
                else:
                    labeled_data.append(example)
                    example = []
            example.append((row[1], row[2]))
        labeled_data.append(example)
        return labeled_data

    def listen(self, file, model):
        self.model = joblib.load(model)
        for line in fileinput.input(file):
            entry = LabeledEntry(line.rstrip())
            labeled_entry = self.label(entry, self.model)
            print(json.dumps(labeled_entry.categories))

    def load_training(self, path_to_csv, rows_to_ignore=0):
        self.training_set_labeled = self.load_labeled_data(path_to_csv, rows_to_ignore)
        self.__process_training_data()

    def __process_training_data(self):
        self.training_set_features = [Features.get_sentence_features(s) for s in self.training_set_labeled]
        self.training_set_labels = [Features.get_sentence_labels(s) for s in self.training_set_labeled]

    def train(self, name):
        self.crf = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=0.01,
            c2=0.01,
            max_iterations=1000,
            all_possible_transitions=False,
            verbose=True
            )
        X_Train, X_Test, Y_Train, Y_Test = train_test_split(self.training_set_features, self.training_set_labels, test_size=0.1, random_state=69)
        self.crf.fit(X_Train, Y_Train)
        Y_Pred = self.crf.predict(X_Test)
        Y_Test_flat = [label for seq in Y_Test for label in seq]
        Y_Pred_flat = [label for seq in Y_Pred for label in seq]
        print(classification_report(Y_Test_flat, Y_Pred_flat))
        token_accuracy = accuracy_score(Y_Test_flat, Y_Pred_flat)
        print(f"Per-token accuracy: {token_accuracy:.2f}")


        model_filename = name + '.pkg'
        joblib.dump(self.crf, model_filename)

    def predict_labeled_tokens(self, labeled_tokens, model):
        features_set = [Features.get_sentence_features(labeled_tokens)]
        return model.predict(features_set)[0]

    def label(self, labeled_entry, model):
        if isinstance(labeled_entry, list):
            return [self.label(x, model) for x in labeled_entry]
        else:
            labeled_entry.token_labels = self.predict_labeled_tokens(labeled_entry.tokens, model)
            labeled_entry.is_parsed = True
            labeled_entry.reduce_labels()
            return labeled_entry