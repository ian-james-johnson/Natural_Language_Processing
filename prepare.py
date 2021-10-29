import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup
import re

import unicodedata
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import acquire



def basic_clean(article):
    """
    Lowercases, normalizes, and removes special characters from the article.
    """
    # lowercasing
    article = article.lower()
    # normalize by removing non-ascii characters
    # encode turns characters into ascii characters
    # decode turns ascii characters back into a string
    article = unicodedata.normalize('NFKD', article).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    # remove speial characters
    article = re.sub(r'[^a-z09\s]', '', article)
    
    return article




def tokenize(article):
    """
    Tokenizes a cleaned article (or a string).
    """
    # create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # use the tokenizer
    article = tokenizer.tokenize(article, return_str=True)
    
    return article



def stem(article):
    """
    Stem all words in an article (or a string).
    """
    # create the stemmer
    ps = nltk.porter.PorterStemmer()
    # use the stemmer, list comprehension uses the stemmer word-by-word
    stems = [ps.stem(word) for word in article.split()]
    # rejoin the stemmed words as an article
    article_stemmed = ''.join(stems)




def lemmatize(article):
    """
    Lemmatize all words in an article (or a string).
    """
    # the the most current lemma list
    nltk.download('wordnet')
    # create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    # use the lemmatizer, list comprehension uses the lemmatizer word-by-word
    lemmas = [wnl.lemmatize(word) for word in article.split()]
    # rejoin the lemmatized words as a article
    article_lemmatized = ''.join(lemmas)
    
    return article_lemmatized



def remove_stopwords(article):
    """
    Removes stopwords from an article (or a string).
    """
    # get the default list of stopwords
    stopword_list = stopwords.words('english')
    # split the article to prepare for removal of stopwords
    words = article.split()
    # remove stopwords
    filtered_stopwords = [word for word in words if word not in stopword_list]
    # rejoin the words into article
    article_without_stopwords = ''.join(filtered_stopwords)





    
    return article_without_stopwords
    
    return article_stemmed