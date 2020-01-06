import sys
from tqdm import tqdm
from glob import glob
from os.path import join

import multiprocessing as mp
from joblib import Parallel, delayed
import math

def getCosineSimilarity(a,b):
    #return 1
    #return a[0]+b[0]
    if len(a) != len(b):
        print("Attempted to compute similarity between vectors of different length. Abort mission!")
        return 0

    dotProduct = 0
    normA = 0
    normB = 0
    for i in range(len(a)):
        dotProduct += a[i] & b[i]
        normA += a[i]
        normB += b[i]
    if normA==normB:        #to prevent sqrt rounding errors
        return dotProduct/normA
    else:
        k = math.sqrt(normA*normB)
        if k==0:
            return float('nan')
        else:
            return dotProduct/k
    return 0

if __name__ == "__main__":
    inpath = sys.argv[1]
    allFiles = tqdm(sorted(glob(join(inpath, "*.txt.csv"))))

    accList = []
    with open(join(inpath, "accumulatedCleaned.txt"), 'r') as f:
        for line in f:
            accList.append(line.split(":")[0])
    
    #qMatrix = [[0 for x in range(len(accList))] for y in range(len(allFiles))]
    qMatrix = dict() 
   
    for filename in allFiles: # Parallizable
        # extract cik
        cik = filename.split('/')[-1].split('_')[0]
        
        idvList = []
        with open(filename, 'r') as f:
            for line in f:
                idvList.append(line.split(":")[0])
        
        if cik not in qMatrix:
            qMatrix[cik] = [0 for x in range(len(accList))]
        for i in range(len(accList)):
            if accList[i] in idvList:
                qMatrix[cik][i] = 1
    
    print("Outputing qMatrix")
    with open(join(inpath, "qMatrix.txt"), 'w') as f:
        for i in qMatrix.keys():
            f.write("%s:"%(i))
            for j in range(len(accList)):
                f.write("%s,"%(qMatrix[i][j]))
            f.write("\n")
    
    qMatrixKeys = sorted(qMatrix.keys())
    similarityMatrix = [[0 for x in range(len(qMatrixKeys))] for y in range(len(qMatrixKeys))]

    print("Calculating similarityMatrix")
    # TODO Parallize
    #pool = mp.Pool(mp.cpu_count())
    
    for i in range(len(qMatrixKeys)):
        print(qMatrixKeys[i])
        
        #tmpList = list(qMatrixKeys[i:])
        #similarityMatrix[i] = [pool.apply(getCosineSimilarity, args=(qMatrix[qMatrixKeys[i]], qMatrix[qMatrixj])) for qMatrixj in tmpList]        

        for j in range(i+1, len(qMatrixKeys)):
            similarityMatrix[i][j] = getCosineSimilarity(qMatrix[qMatrixKeys[i]], qMatrix[qMatrixKeys[j]])
    #pool.close()
    
    print("Outputing similarityMatrix")
    with open(join(inpath, "similarityMatrix.txt"), 'w') as f:
        for i in range(len(qMatrixKeys)):
            f.write("%s,"%(qMatrixKeys[i]))
        f.write("\n")
        for i in range(len(similarityMatrix)):
            for j in range(len(similarityMatrix[i])):
                f.write("%s,"%(similarityMatrix[i][j]))
            f.write("\n")
