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
	if normA==normB:	#to prevent sqrt rounding errors
		result = dotProduct/normA
	else:
		k = math.sqrt(normA)*math.sqrt(normB)
		if k==0:
			result = float('nan')
		else:
			result = dotProduct/k
	return result