#!/usr/bin/env python
import os, sys, glob
from collections import defaultdict
from collections import Counter
import functools
import random


class Learn(object):
    def __init__(self):
        self.fname = ""     #path to training data
        self.spamFiles = [] #list of all spam files in training data
        self.hamFiles = []  #list of all ham files in training data
        self.allFiles = []  # list of tuples containing spam and ham info
        self.weightDict = defaultdict(lambda:0) #contains the weight of every dict with default wt as zero
        self.maxIter = 30   #maximum number of iterations on training for weights
        self.bias = 0       #bias of the training data

    def getData(self):
        """
            This function is used to parse the vocab list and training data provided to us.
        """

        for root, dirnames, filenames in os.walk(self.fname):
            if "spam" in dirnames:
                spamdir = os.path.join(root, "spam")
                self.spamFiles.extend([os.path.join(spamdir, x) for x in os.listdir(spamdir) if x.endswith(".txt")])

        for sFile in self.spamFiles:
            with open(sFile, "r", encoding="latin1") as f:
                wordlist = f.read().split()
                self.allFiles.append((1, wordlist))

        for root, dirnames, filenames in os.walk(self.fname):
            if "ham" in dirnames:
                hamdir = os.path.join(root, "ham")
                self.hamFiles.extend([os.path.join(hamdir, x) for x in os.listdir(hamdir) if x.endswith(".txt")])

        for hFile in self.hamFiles:
            with open(hFile, "r", encoding="latin1") as f:
                wordlist = f.read().split()
                self.allFiles.append((-1, wordlist))

        # print(self.allFiles)

        return


    def trainPerceptrons(self):
        """
        function to train the weights of given data for perceptrons
        :return: nothing but sets up the weight and bias of the training data
        """

        for i in range(1, self.maxIter):
            random.shuffle(self.allFiles)       #shuffling the order of data

            for sample in self.allFiles:
                y , wordlist = sample
                alpha = 0

                for word in wordlist:
                    alpha += self.weightDict[word]

                alpha += self.bias

                if (y * alpha <= 0):
                    for word in wordlist:
                        self.weightDict[word] += y
                        self.bias += y

        result = {'bias': self.bias, 'weight': dict(self.weightDict)}

        try:
            with open('per_model.txt', 'w') as f:
                f.write(str(result))
        except:
            print("something went wrong with FIL IO")
            exit(1)

        return

if __name__ == "__main__":
    if (len(sys.argv)) != 2:
        print("Usage: python3 per_learn.py /path/to/input")
        exit(1)

    dataPath = sys.argv[1]

    learn_obj = Learn()
    learn_obj.fname = dataPath
    learn_obj.getData()
    learn_obj.trainPerceptrons()

    exit(0)
