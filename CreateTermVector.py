##
# Gets a dictionary mapping words to their frequencies for a given list of word information.
##
def getTermFrequencyDict(wordInfoList):
    termFrequencyDict = dict()
    for wordInfo in wordInfoList:

        ##if is internalPunctuationWord or Stopword
        #if wordInfo[1] or wordInfo[2]:
        #    continue
        word = wordInfo #[0]
        if word in termFrequencyDict:
            termFrequencyDict[word] += 1
        else:
            termFrequencyDict[word] = 1
    return termFrequencyDict


"""
##
# Convienience method. Currently NOT USED.
##
def getTermVectorsToCompareTwoFiles(termFrequencyDict1,termFrequencyDict2):
    listOfAllWords = list()
    for key in termFrequencyDict1:
        if key not in listOfAllWords:
            listOfAllWords.append(key)
    for key in termFrequencyDict2:
        if key not in listOfAllWords:
            listOfAllWords.append(key)

    termVector1 = [None]*len(listOfAllWords)
    termVector2 = [None]*len(listOfAllWords)
    for i in range(len(listOfAllWords)):
        currentWord = listOfAllWords[i]
        termVector1[i] = termFrequencyDict1[currentWord] if currentWord in termFrequencyDict1 else 0
        termVector2[i] = termFrequencyDict2[currentWord] if currentWord in termFrequencyDict2 else 0
    return (termVector1,termVector2)


##
# Convienience method. Currently NOT USED.
##
def getTermVectorsForListOfFiles(listOfTermFrequencyDicts):
    nrOfDicts = len(listOfTermFrequencyDicts)
    listOfAllWords = list()
    for dictionary in listOfTermFrequencyDicts:
        for key in dictionary:
            if key not in listOfAllWords:
                listOfAllWords.append(key)

    listOfTermVectors = list()
    for k in range(nrOfDicts):  ##init listOfTermVectors
        termVector = [None]*len(listOfAllWords)
        listOfTermVectors.append(termVector)

    for i in range(len(listOfAllWords)):
        currentWord = listOfAllWords[i]
        for j in range(nrOfDicts):
            (listOfTermVectors[j])[i] = (listOfTermFrequencyDicts[j])[currentWord] if currentWord in listOfTermFrequencyDicts[j] else 0

    return listOfTermVectors
    """
