import InputMethods
import CreateTermVector
#import Similarities
import time
import csv
import re
import sys

from tqdm import tqdm
from glob import glob

#from os import listdir
from os.path import join
import os

#import multiprocessing
from joblib import Parallel, delayed
def saveTermFreq (filename):
    print("Processing file: ", filename)
    
    termFrequencyDict = InputMethods.processSingleFile(InputMethods.readInFile(filename), False)

    filename = filename.split("/")[2] # filename = filename + "../../"
    with open(join(outpath, filename + ".csv"), 'w') as f:
        for key in termFrequencyDict.keys():
            f.write("%s:%s\n"%(key,termFrequencyDict[key]))    

if __name__ == "__main__":
   
    # Step 1: Get termFrequencyDict of each file in the inpath and save it.
    # Pretty much the same as ImportantWords.py
    # inpath = "edgar-10k-mda/form10k08_item7"
    inpath = sys.argv[1]
    outpath = inpath + "_dict"   
    
    allFiles = tqdm(sorted(glob(join(inpath, "*.txt"))))

    if not os.path.exists(outpath):
        os.makedirs(outpath)
    
    Parallel(n_jobs=-4)(delayed(saveTermFreq)(filename) for filename in allFiles)

    # Setp 2: Get accumulated list of step 1. (GetAccumulatedList.py)
    allFiles = tqdm(sorted(glob(join(outpath, "*.txt.csv"))))
    
    totalWordDict = dict()
    totalWordDictCount = dict()
    count = 0
    for filename in allFiles:
        f = open(filename, 'r')
        print("Processing file Nr. ",count,"  (",filename,")")
        
        for line in f:
            wordFrequencyTuple = line.split(":")
            word = wordFrequencyTuple[0]
            frequency = int(wordFrequencyTuple[1])
            if word in totalWordDict:
                totalWordDict[word] += frequency
                totalWordDictCount[word] += 1
            else:
                totalWordDict[word] = frequency
                totalWordDictCount[word] = 1
            
        print("Processed file Nr. ",count,"  (",filename,")")
        count += 1
    
    with open(join(outpath, "accumulated.txt"), 'w') as f:
        for key in totalWordDict.keys():
            f.write("%s:%s\n"%(key, totalWordDict[key]))    
    
    # Step 3: (CleanAccumulatedList.py)
    threshold = 0.25 * len(allFiles)
    with open(join(outpath, "accumulatedCleaned.txt"), 'w') as f:
        for key in list(totalWordDict):
            if not all(ord(c) < 128 for c in key):
                print(key, " removed non-ascii!")
                continue
            if not key.isalpha() or len(key) <= 2 : #or totalWordDict[key] <= 2:
                continue
            # Only include uncommon words
            if totalWordDictCount[key] < threshold:
                f.write("%s:%s\n"%(key, totalWordDict[key]))    
    
    
    #termVector1,termVector2 = CreateTermVector.getTermVectorsToCompareTwoFiles(termFrequencyDict1,termFrequencyDict2)
    #cosineSim = Similarities.getCosineSimilarity(termVector1,termVector2)

"""
##this gives the similarity from all files to the first. Currently NOT USED
def getSimilarityToFirst(files,rootpath):
    simVector = [None] * (len(files)-1)
    firstfile = files[0]    #compare against this file
    firstFileDict = InputMethods.processSingleFile(rootpath+firstfile)
    for i in range(1,len(files)):   
        totalpath = rootpath+files[i]
        secondFileDict = InputMethods.processSingleFile(totalpath)
        termVector1,termVector2 = CreateTermVector.getTermVectorsToCompareTwoFiles(firstFileDict,secondFileDict)
        cosineSim = Similarities.getCosineSimilarity(termVector1,termVector2)
        #print(cosineSim)
        simVector[i-1] = cosineSim
    return simVector

##
# Gets a dictionary mapping words to their frequencies for a given list of word information.
# Currently NOT USED.
##
def getTermFrequencyDict(wordInfoList):
    termFrequencyDict = dict()
    for wordInfo in wordInfoList:
        ##if is internalPunctuationWord or Stopword
        if wordInfo[1] == True or wordInfo[2] == True:
            continue
        word = wordInfo[0]
        if word in termFrequencyDict:
            termFrequencyDict[word] += 1
        else:
            termFrequencyDict[word] = 1
    return termFrequencyDict
    """
