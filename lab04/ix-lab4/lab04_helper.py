import re
import numpy as np
import nltk
import string #string operations
from scipy.sparse import csr_matrix
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from utils import load_json, load_pkl

def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

########
###Preprocessing functions
#######

stopwords = None
def removeStopWords(listWords,stopwords):
    """
    Filters out stopwords in a list of words
    """
    return list(filter(lambda x : len(x)>0 and x not in stopwords, listWords))

def toWordList(description):
    """
    takes a description (unique string) and separates it to lowercase words (not distincts) 
    """
    return description.lower().split(" ") 

def takeOutNumbers(listWords):
    """
    Takes a list of words and removes all numbers that are alone or a only seperated by h.
    Permits to keep words that exist with a number (ex: 3SAT)
    """
    pattern = re.compile(r"\d{1,2}h\d{0,2}$") #removes hours
    noHours = [pattern.sub("", i) for i in listWords] 
    return list(filter(lambda x : not x.isdecimal(), noHours)) #filters out numbers-only

def splitAppendedWords(descString):
    """
    Takes a description, and splits appended words (because of a missing \\n)
    """
    patternAppended = re.compile("([a-z][a-z])([A-Z])([a-z][a-z])") #regex used to split bonded words 
    return patternAppended.sub("\\1 \\2\\3", descString)

def removePunctuation(descString):
    """
    Removes punctuation signs in a long unique string. Treats dashes smartly.
    """
    punct = ",.!?+\n\t:;0'%&\"#/()[]`\xa0\xad" #list of characters that always need to be removed
    puncttrans = str.maketrans(punct," "*len(punct)) #translation rule : replace above char by a space
    patternDash = re.compile(" +- *| *- +") # regex used to treat dashes
    
    unDashed = patternDash.sub("", descString) 
    return unDashed.translate(puncttrans)


def cleanDesc(description,stopwords):
    noPunct = removePunctuation(description) #desc without punctuation
    unAppended = splitAppendedWords(noPunct)  #desc with split words
    
    wordlist = toWordList(unAppended)
    return removeStopWords(takeOutNumbers(wordlist),stopwords)

def cleaner(description):
    """
    Calls all above functions. First remove punctuation, then un-append words, split to space, then remove numbers
    and stopwords. 
    """
    lemmatizer = WordNetLemmatizer()
    stopwords = load_pkl('data/stopwords.pkl')
    noPunct = removePunctuation(description) #desc without punctuation
    unAppended = splitAppendedWords(noPunct)  #desc with split words
    wordlist = toWordList(unAppended)
    onlyWords = removeStopWords(takeOutNumbers(wordlist),stopwords)
    #return onlyWords
    newlist = []
    for i in onlyWords:
        newlist.append(lemmatizer.lemmatize(i))
    return newlist
  
def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

