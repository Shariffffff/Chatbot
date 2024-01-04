import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

# Download necessary NLTK models and corpora


stemmer = PorterStemmer()

def tokenize(sentence):
    """
    Tokenizes a sentence into words.
    """
    return word_tokenize(sentence)

def stem(word):
    """
    Stems a word to its root form.
    """
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    """
    Returns a bag of words array.
    """
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in sentence_words: 
            bag[idx] = 1
    return bag
