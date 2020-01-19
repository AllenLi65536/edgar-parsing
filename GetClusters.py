import sys
from os.path import join
import sklearn.cluster as cluster
import numpy as np

if __name__ == "__main__":
    inpath = sys.argv[1]
    
    ciks = []

    # Read similarity matrix
    print("Reading similarity matrix")
    with open(join(inpath, "similarityMatrix.txt"), 'r') as f:
        ciks = f.readline().split(",")[:-1]
        similarityMatrix = [[0 for x in range(len(ciks))] for y in range(len(ciks))]
        i = 0
        for line in f:
            similarityMatrix[i] = line.split(",")[:-1]
            i += 1
    
    # Make the matrix symmetric
    print("Making matrix symmetric")
    for i in range(len(ciks)):
        similarityMatrix[i][i] = 1
        for j in range(i):
            similarityMatrix[i][j] = similarityMatrix[j][i]

    # TODO Clustering
    mat = np.matrix(similarityMatrix).astype(np.float64)
   
    #eigen_values, eigen_vectors = np.linalg.eigh(mat)
    #result = cluster.KMeans(n_clusters=200, init='k-means++').fit_predict(eigen_vectors[:, 2:4])
    
    #result = cluster.DBSCAN().fit_predict(mat)
    result = cluster.SpectralClustering(300).fit_predict(mat)
    
    print(result)
    with open(join(inpath, "ClusterResult.txt"), 'w') as f:
        for cik in ciks:
            f.write("%s,"%(cik))
        f.write("\n")
        for i in range(len(result)):
            f.write("%s,"%(result[i]))
        f.write("\n")

