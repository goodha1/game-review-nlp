import pandas as pd
import numpy as np
import string
import re
from collections import defaultdict

from nltk.tokenize import word_tokenize


class NaiveBayesNLP:
    """Naive Bayes classfier for binary sentiment analysis"""

    def __init__(self):
        self.vocab = set()

    def clean(self, text):
        remove = str.maketrans("", "", string.punctuation + string.digits)
        return text.translate(remove).lower()

    def word_frequency(self, clean_text):
        """Laplace +1 smooth"""
        freq = defaultdict(lambda: 1)
        for word in re.split("\W+", clean_text):
            self.vocab.add(word)
            freq[word] += 1
        return freq

    def train(self, X, y):
        self.pos = np.log(np.mean(y == 1))
        self.neg = np.log(np.mean(y == -1))
        self.pos_wc = self.word_frequency(self.clean(" ".join(X[y == 1])))
        self.neg_wc = self.word_frequency(self.clean(" ".join(X[y == -1])))
        self.pos_n = sum(self.pos_wc.values())
        self.neg_n = sum(self.neg_wc.values())

    def predict(self, X):
        result = []
        for x in X:
            pos, neg = 0, 0
            freqs = self.word_frequency(self.clean(x))
            for word, _ in freqs.items():
                if word not in self.vocab:
                    continue
                pos += np.log(self.pos_wc[word] / self.pos_n)
                neg += np.log(self.neg_wc[word] / self.neg_n)
            pos += self.pos
            neg += self.neg
            if pos > neg:
                result.append(1)
            else:
                result.append(-1)
        return result


train = pd.read_csv("train-ns", sep="\t")
test_file = "dev-ns"
test = pd.read_csv(test_file, sep="\t")

train_x = np.array(train["review"])
train_y = np.array(train["label"])
test_x = np.array(test["review"])
test_y = np.array(test["label"])

nb = NaiveBayesNLP()
nb.train(train_x, train_y)
result = nb.predict(test_x)
print(result)

# def tokenize(sentence):
#     return [word for word in word_tokenize(sentence) if word.isalpha()]
