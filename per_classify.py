#!/usr/bin/env python

import sys, pprint, functools, os, glob
from math import log

class perclassify(object):
    """
        class to classify mails based on per_model.txt produced by
         per_learn.py
    """
    def __init__(self):
        self.permod_dict = {}
        self.hamTP = 0
        self.hamTN = 0
        self.hamFP = 0
        self.hamFN = 0
        self.spamTP = 0
        self.spamTN = 0
        self.spamFP = 0
        self.spamFN = 0

    def classify(self, file, outputHandle):

        words = []
        with open(file, "r", encoding="latin1") as f:
            words = f.read().split()

        alpha = 0
        for x in words:
            alpha += self.permod_dict['weight'][x]

        alpha += self.permod_dict['bias']

        if alpha > 0:
            outputHandle.write(str("SPAM " + file + "\n"))
        else:
            outputHandle.write(str("HAM " + file + "\n"))



        # wordSpam = []
        # for x in words:
        #     if x in self.nbmod_dict['word']:
        #         wordSpam.append(self.nbmod_dict['word'][x][0])
        #
        # logSpam = list(map(log, wordSpam))
        # spamProb = functools.reduce(lambda x, y: x + y, logSpam) + log(self.nbmod_dict['spam'])
        #
        # wordHam = []
        # for x in words:
        #     if x in self.nbmod_dict['word']:
        #         wordHam.append(self.nbmod_dict['word'][x][1])
        #
        # logHam = list(map(log, wordHam))
        # hamProb = functools.reduce(lambda x, y: x + y, logHam) + log(self.nbmod_dict['ham'])
        #
        # if hamProb > spamProb:
        #     if 'ham' in file:
        #         self.hamTP += 1
        #         self.spamTN += 1
        #     else:
        #         self.hamFP += 1
        #         self.spamFN += 1
        #     outputHandle.write(str("HAM " + file + "\n"))
        # else:
        #     if 'spam' in file:
        #         self.spamTP += 1
        #         self.hamTN += 1
        #     else:
        #         self.spamFP += 1
        #         self.hamFN += 1
        #
        #     outputHandle.write(str("SPAM " + file + "\n"))

        return


if __name__ == "__main__":
    if (len(sys.argv)) != 3:
        print("Usage: python3 per_classify.py /path/to/input output_filename")
        exit(1)

    dataPath = sys.argv[1]
    outputFile = sys.argv[2]

    # print("The file name is: ", dataPath)

    nbmodel = {}

    with open("per_model.txt",'r') as f:
        permodel = eval(f.read())

    # pprint.pprint(nbmodel)

    perclassify_obj = perclassify()
    perclassify_obj.permod_dict = permodel

    devFiles = []

    for root, dirnames, filenames in os.walk(dataPath):
        for file in filenames:
            if file.endswith(".txt"):
                devFiles.append(os.path.join(root, file))

    try:
        outputHandle = open(outputFile, 'w')
    except:
        print("issue with file io")

    for file in devFiles:
        perclassify_obj.classify(file, outputHandle)


    outputHandle.close()


    # print("Exiting classification")
    exit(0)


    # learn_obj = Learn()
    # learn_obj.fname = dataPath
    # learn_obj.getData()
    # learn_obj.find_token_probability()


