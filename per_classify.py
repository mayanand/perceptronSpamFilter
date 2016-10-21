#!/usr/bin/env python

import sys, pprint, functools, os, glob
from collections import defaultdict
from math import log

class perclassify(object):
    """
        class to classify mails based on per_model.txt produced by
         per_learn.py
    """
    def __init__(self):
        self.permod_dict = {}
        self.wtDefDict = {}
        self.bias = 0
        self.hamTP = 0
        self.hamTN = 0
        self.hamFP = 0
        self.hamFN = 0
        self.spamTP = 0
        self.spamTN = 0
        self.spamFP = 0
        self.spamFN = 0

    def classify(self, file, outputHandle):
        """
        :param file: file path of the email to be classified
        :param outputHandle: the file handle of output file
        :return: returns nothing but gives the output the th file handle provided
        """

        words = []
        with open(file, "r", encoding="latin1") as f:
            words = f.read().split()

        alpha = 0
        for x in words:
            alpha += self.wtDefDict[x]

        alpha += self.bias

        # print("classifying now")

        if alpha > 0:
            if 'spam' in file:
                self.spamTP += 1
                self.hamTN += 1
            else:
                self.spamFP += 1
                self.hamFN += 1
            outputHandle.write(str("SPAM " + file + "\n"))

        else:
            if 'ham' in file:
                self.hamTP += 1
                self.spamTN += 1
            else:
                self.hamFP += 1
                self.spamFN += 1
            outputHandle.write(str("HAM " + file + "\n"))

        return

if __name__ == "__main__":
    if (len(sys.argv)) != 3:
        print("Usage: python3 per_classify.py /path/to/input output_filename")
        exit(1)

    dataPath = sys.argv[1]
    outputFile = sys.argv[2]

    print("The file name is: ", dataPath)
    print("the output filename is: ", outputFile)

    print("lets do eval now")

    with open("per_model.txt",'r') as f:
        permodel = eval(f.read())

    # permodel = {}


    # pprint.pprint(permodel)

    perclassify_obj = perclassify()
    perclassify_obj.permod_dict = permodel
    perclassify_obj.wtDefDict = defaultdict(lambda:0, permodel['weight'])
    perclassify_obj.bias = permodel['bias']
    devFiles = []

    for root, dirnames, filenames in os.walk(dataPath):
        for file in filenames:
            if file.endswith(".txt"):
                devFiles.append(os.path.join(root, file))

    print("found all the files")

    try:
        outputHandle = open(outputFile, 'w')
    except:
        print("issue with file io")


    print("on to classification now")
    for file in devFiles:
        perclassify_obj.classify(file, outputHandle)


    outputHandle.close()


    # print("Exiting classification")
    exit(0)


    # learn_obj = Learn()
    # learn_obj.fname = dataPath
    # learn_obj.getData()
    # learn_obj.find_token_probability()


