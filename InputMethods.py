import re
import PreParsingMethods
import CreateTermVector
import Similarities
import time

def readInFile(path):
	k = []
	f = open(path,'r')
	for line in f:
		#line = f.readline()
		wordsInLine = re.split("\s+",line)
		k.extend(wordsInLine)
	return k

##
# Preparse single file then get term frequency dictionary.
##
def processSingleFile(wordArray, with_stem):
	#time1 = time.time()
	wordInfoList = PreParsingMethods.preParsing(wordArray, with_stem)
	#time2 = time.time()
	#print("preParsing-time: ",(time2-time1))
	return CreateTermVector.getTermFrequencyDict(wordInfoList)

"""
##
# The main of this program is normally NOT CALLED. It is just here for test purposes.
##
if __name__ == "__main__":
	wordArray1 = readInFile("C:/Users/Florian/Desktop/Uni/IDP/Parsed/All Files/10048/2052_10048_1995_19951222_item7.txt")
	wordArray2 = readInFile("C:/Users/Florian/Desktop/Uni/IDP/Parsed/All Files/10048/2052_10048_2000_20001219_item7.txt")
	termFrequencyDict1 = processSingleFile(wordArray1)
	termFrequencyDict2 = processSingleFile(wordArray2)

	print("Len dict1: ",len(termFrequencyDict1),"  Len dict2: ",len(termFrequencyDict2))
	termVector1,termVector2 = CreateTermVector.getTermVectorsToCompareTwoFiles(termFrequencyDict1,termFrequencyDict2)
	cosineSim = Similarities.getCosineSimilarity(termVector1,termVector2)
	print("Cosine Similartity: "+str(cosineSim))
        """
