import numpy as np
import re
from nltk.tokenize import word_tokenize
import itertools
from nltk.stem import WordNetLemmatizer, PorterStemmer
from collections import Counter
import sklearn.preprocessing
import nltk
import json
import string
import os,glob
import spacy
from nltk.corpus import stopwords
from random import shuffle

stop_words = stopwords.words('english')
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


POS = {
    'v': 'v', 'j': 'a', 's': 's','r': 'r',
    'n' : 'n' , 'a' : 'a'}

def remove_stopwords(text):
    text = ' '.join([each for each in word_tokenize(text) if each not in stop_words])
    return text


def stemWords(text):
    text_stemmed = ""
    pos_tags = [each[0].lower() for _ , each in nltk.pos_tag(text.split())]

    for i , word in enumerate(text.split()):
        _lemma = lemmatizer.lemmatize(word) \
                        if pos_tags[i] in POS.keys() \
                            else lemmatizer.lemmatize(word)
        text_stemmed+= _lemma + " "

    return text_stemmed



def replaceDigits(text):
    final_word = " ".join(word for word in text.split() if not any(c.isdigit() \
                                    for c in word))

    return final_word



def replacePunctuations(text):
    keep_punct = {'-' } # i.e. placeholders
    for punct in set(string.punctuation) - keep_punct :
        text = text.replace(punct, ' ')
    return text


def replaceContractions(text):
    _path = os.getcwd().split('word_sense_disambiguation/data')[0]
    _path = _path + 'word_sense_disambiguation/data/'
    text = re.sub(r"\'s", " is", text)
    c_map = json.load(open(_path+"contractions.json","rb")) # { key: [a,b] }
    tokens = text.split()
    for k,v in c_map.items():
        if k in text: text = text.replace(k, v[0])
    return text


def preprocessText(string , flag = None):
    string = string.strip().lower()
    string = replaceContractions(string)
    string = replacePunctuations(string)
    string = re.sub('\d+(\s*a\s*m\s+|p\s*m\s+)?',' ',string)
    string = replaceDigits(string)
    string = re.sub('\s+' , ' ' , string)
    return string
