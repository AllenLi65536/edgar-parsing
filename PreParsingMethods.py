import re
import StopWords
import time
import sys      ##care with these 3 lines
import Stemming

import nltk
#nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet
nouns = {x.name().split('.', 1)[0] for x in wordnet.all_synsets('n')}

from nltk.stem import WordNetLemmatizer 
# Init the Wordnet Lemmatizer
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    # Map POS tag to first character lemmatize() accepts
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

##regex for punctuation (only compute once)
punctuationRegex = "!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}“”’~—£€"
reg1 = re.compile("^["+punctuationRegex+"]+")
reg2 = re.compile("["+punctuationRegex+"]+$")
reg3 = re.compile("\w+["+punctuationRegex+"]+\w+")
url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+') 
numberReg = re.compile("^-?[0-9]+$")
##whitespace regex
regWhiteSpaceString = re.compile("\s+")

def preParsing(wordList,with_stem):
    
    outList = []
    for word in wordList:
        # Replace strange quotes
        word = word.replace('“', '\"')
        word = word.replace('”', '\"')
        word = word.replace('’', '\'')
        
        ##check if string is empty
        if isEmptyOrWhitespaceString(word):
            continue

        ##remove unnecessary punctuation
        word,isInternalPunctuationWord = removePunctuation(word)
        
        if isInternalPunctuationWord:
            continue
        
        if isEmptyOrWhitespaceString(word):  ##check if removePunctuation created empty string
            continue

        ##check if word is number, this is done after removePunctuation to catch numbers like 1,7 and 130.000
        if isNumber(word):
            continue

        if isSingleLetter(word) or not word.isalpha():
            continue

        ##lowercase word before further processing. CARE: can change some outcomes (eg. change IT to it which gets stopword-filtered)
        word = word.lower()
        
        ##check if newWord is a stopword
        if StopWords.isStopword(word):
            continue

        # Lemmatize
        word = lemmatizer.lemmatize(word, get_wordnet_pos(word))
        
        # Check if it is noun
        if word not in nouns:
            continue

        ##stemming
        if with_stem:
            word = Stemming.stemPorter(word)
        #wordInfo[0] = word
        
        #wordInfo = [None]*3
        #wordInfo[1] = StopWords.isStopword(newWord)
        #wordInfo[2] = isInternalPunctuationWord
        #wordInfo[0] = newWord
        
        outList.append(word)
    
    #outList = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in outList]    

    return outList

def isEmptyOrWhitespaceString(word):
    return (not word or regWhiteSpaceString.match(word))        ##empty strings are false by default

def removePunctuation(word):
    isInternalPunctuationWord = False
    ##check for internal punctuation
    newWord = re.sub(reg1,"",word)
    newWord = re.sub(reg2,"",newWord)
    if newWord.startswith("http"):
        return "", True
    if reg3.match(newWord):
        isInternalPunctuationWord = True
        newWord = re.sub(reg3,"",newWord)
    if url.match(newWord):
        isInternalPunctuationWord = True
        newWord = re.sub(url,"",newWord)

        
    """if reg3.match(word):
        isInternalPunctuationWord = True
        newWord = word
    else:       
        newWord = re.sub(reg1,"",word)
        newWord = re.sub(reg2,"",newWord)"""
    return newWord,isInternalPunctuationWord

def isNumber(word):
    return numberReg.match(word)

def isSingleLetter(word):
    return len(word)==1

# Unit testing
if __name__ == "__main__":
    print(removePunctuation("(nyse:dpg),"))
#    print(removePunctuation("3,128"))
#    print(removePunctuation("http://www.stats.gov.cn/tjgb"))
