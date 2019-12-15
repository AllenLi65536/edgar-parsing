from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import EnglishStemmer

porter = PorterStemmer()
lancaster = LancasterStemmer()
snowball = EnglishStemmer()

def stemPorter(word):
	return porter.stem(word)

def stemLancaster(word):
	return lancaster.stem(word)

def stemSnowball(word):
	return snowball.stem(word)