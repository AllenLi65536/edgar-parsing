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
    if len(a) != len(b):
        print("Attempted to compute similarity between vectors of different length. Abort mission!")
        return 0
    result = 0
    count = 0
    for i in range(len(a)):
        if a[i]*b[i] != 0:
            result += a[i]*b[i]
            count += 1
            print(str(a[i]*b[i]) + " " + str(count))
    return result

    #return sum(i[0] * i[1] for i in zip(a, b))


if __name__ == "__main__":
    inpath = sys.argv[1]
    
    qMatrix = dict() 
   
    print("Reading QMatrix")
    with open(join(inpath, "qMatrix.txt"), 'r') as f:
        for line in f:
            cik = line.split(":")[0]
            qMatrix[cik] = [float(i) for i in line.split(":")[1].split(',')[:-1] ]#list(map(float, line.split(":")[1].split(",")))
    
    print(getCosineSimilarity(qMatrix[str(1000045)], qMatrix[str(1000180)]))
    print(sum(i*i for i in qMatrix[str(1000045)]))
    print(sum(i*i for i in qMatrix[str(1000180)]))
            
