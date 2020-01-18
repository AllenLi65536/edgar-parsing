import sys
from os.path import join
import sklearn.cluster as cluster

if __name__ == "__main__":
    inpath = sys.argv[1]
    
    ciks = []

    # Read similarity matrix
    with open(join(inpath, "similarityMatrix.txt"), 'r') as f:
        ciks = f.readline().split(",")
        similarityMatrix = [[0 for x in range(len(ciks))] for y in range(len(ciks))]
        i = 0
        for line in f:
            similarityMatrix[i] = line.split(",")
            i += 1

   # TODO Clustering

