import sys
from tqdm import tqdm
from glob import glob
from os.path import join

import concurrent.futures

import multiprocessing as mp
from multiprocessing.pool import ThreadPool
from joblib import Parallel, delayed
import math

def getCosineSimilarity(a, b):
    #if len(a) != len(b):
    #    print("Attempted to compute similarity between vectors of different length. Abort mission!")
    #    return 0
    
    # Normalize the vector to unit length
    #lenA = sum(a) 
    #lenB = sum(B) 
    #return sum(i[0] & i[1] for i in zip(a, b)) / math.sqrt(lenA*lenB)

    return sum(i[0] * i[1] for i in zip(a, b))
    
#    dotProduct = sum(i[0] * i[1] for i in zip(a, b))
#    normA = sum(a)
#    normB = sum(b)
#    if normA == normB:        #to prevent sqrt rounding errors
#        return dotProduct/normA
#    else:
#        k = math.sqrt(normA*normB)
#        if k == 0:
#            return float('nan')
#        else:
#            return dotProduct/k
#    return 0

if __name__ == "__main__":
    inpath = sys.argv[1]
    allFiles = tqdm(sorted(glob(join(inpath, "*.txt.csv"))))

    accList = []
    with open(join(inpath, "accumulatedCleaned.txt"), 'r') as f:
        for line in f:
            accList.append(line.split(":")[0])
    
    qMatrix = dict() 
   
    for filename in allFiles: # Parallelizable
        # extract cik
        cik = filename.split('/')[-1].split('_')[0]
        
        idvList = []
        with open(filename, 'r') as f:
            for line in f:
                idvList.append(line.split(":")[0])
        
        if cik not in qMatrix:
            qMatrix[cik] = [1 if accList[x] in idvList else 0 for x in range(len(accList))]
    
    print("Outputing qMatrix")
    with open(join(inpath, "qMatrix.txt"), 'w') as f:
        for i in qMatrix.keys():
            
            # Normalize the vector to unit length
            length = sum(qMatrix[i]) #sum(j & j for j in qMatrix[i])
            length = math.sqrt(length)
            if length == 0:
                length = 1 # avoid divid by 0
            
            f.write("%s:"%(i))
            for j in range(len(accList)):
                qMatrix[i][j] /= length
                f.write("%s,"%(qMatrix[i][j]))
            f.write("\n")
    
    qMatrixKeys = sorted(qMatrix.keys())
    similarityMatrix = [[0 for x in range(len(qMatrixKeys))] for y in range(len(qMatrixKeys))]

    print("Calculating similarityMatrix")
    # Improvement:  Parallelize
    # Following multithread does not actually improve throughput
    # It did use multithread in processing, however, each thread 
    # has pretty low CPU usage. Not fully utilizing CPU power.

    #pool = mp.Pool(mp.cpu_count())
    
    #pool = ThreadPool(processes=40)
    
    for i in range(len(qMatrixKeys)):
        print(qMatrixKeys[i])
        
        for j in range(i+1, len(qMatrixKeys)):
            similarityMatrix[i][j] = getCosineSimilarity(qMatrix[qMatrixKeys[i]], qMatrix[qMatrixKeys[j]])
        
        print(similarityMatrix[i][i+1])
        
        #tmpList = list(qMatrixKeys[i:])

        #similarityMatrix[i] = [pool.apply(getCosineSimilarity, args=(qMatrix[qMatrixKeys[i]], qMatrix[qMatrixj])) \
        #        for qMatrixj in tmpList]        

#        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
#            futureToJ = {executor.submit(getCosineSimilarity, qMatrix[qMatrixKeys[i]], qMatrix[qMatrixKeys[j]]):j \
#                    for j in range(i+1, len(qMatrixKeys))}
#            for future in concurrent.futures.as_completed(futureToJ):
#                j = futureToJ[future]
#                try:
#                    similarityMatrix[i][j] = future.result()
#                except Exception as exc:
#                    print('generated an exception: %s' % (exc))
#                #else:
#                #    print('page is %d bytes' % (url, len(data)))
#
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
