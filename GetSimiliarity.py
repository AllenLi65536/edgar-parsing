import sys
from tqdm import tqdm
from glob import glob
from os.path import join


from joblib import Parallel, delayed
import math

def getCosineSimilarity(a,b):
    if len(a) != len(b):
        print("Attempted to compute similarity between vectors of different length. Abort mission!")
        return 0

    dotProduct = 0.0
    normA = 0.0
    normB = 0.0
    for i in range(len(a)):
        dotProduct += a[i]*b[i]
        normA += a[i]*a[i]
        normB += b[i]*b[i]
    if normA==normB:        #to prevent sqrt rounding errors
        result = dotProduct/normA
    else:
        k = math.sqrt(normA)*math.sqrt(normB)
        if k==0:
            result = float('nan')
        else:
            result = dotProduct/k
    return result

if __name__ == "__main__":
    inpath = sys.argv[1]
    allFiles = tqdm(sorted(glob(join(inpath, "*.txt.csv"))))

    accList = []
    with open(join(inpath, "accumulatedCleaned.txt"), 'r') as f:
        for line in f:
            accList.append(line.split(":")[0])
    
    #for word in accList:
    #    print(word, end= ' ')

    qMatrix = [[0 for x in range(len(accList))] for y in range(len(allFiles))]
   
    # TODO extract cik
    count = 0
    for filename in allFiles: # Parallizable
        
        idvList = []
        with open(filename, 'r') as f:
            for line in f:
                idvList.append(line.split(":")[0])
        
        for i in range(len(accList)):
            if accList[i] in idvList:
                qMatrix[count][i] = 1
        count += 1
    
    print("Outputing qMatrix")
    with open(join(inpath, "qMatrix.txt"), 'w') as f:
        for i in range(len(allFiles)):
            for j in range(len(accList)):
                f.write("%s,"%(qMatrix[i][j]))
            f.write("\n")

    
    similarityMatrix = [[0 for x in range(len(allFiles))] for y in range(len(allFiles))]

    print("Calculating similarityMatrix")
    # Parallizable?
    for i in range(len(allFiles)):
        for j in range(i+1, len(allFiles)):
            similarityMatrix[i][j] = getCosineSimilarity(qMatrix[i], qMatrix[j])
    
    print("Outputing similarityMatrix")
    with open(join(inpath, "similarityMatrix.txt"), 'w') as f:
        for i in range(len(allFiles)):
            for j in range(len(allFiles)):
                f.write("%s,"%(similarityMatrix[i][j]))
            f.write("\n")
