import sys
import re
import newspaper
#suppress windows chunksize warning
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
import os

def main():
    dct = corpora.Dictionary.load("./Data/news.dict")
    tfidfCorpus = corpora.MmCorpus("./Data/news.mm")

    articles = []

    articlesPath = os.getcwd() + '/SampleArticles'
    for filename in os.listdir(articlesPath):
        with open(articlesPath+'/'+filename) as file:
            articles.append(file.read())

    sentences = []
    for article in articles:
        sentences.append(re.split('\. |\n|\.\"', article)) #TODO: Handle quotes that end with ."

    # Remove words that appear once
    vec_sentence = []
    for sentence in sentences[0]:
        for token in sentence:
            token = re.sub("[!?,.()\":]", "", token)
        vecSen = dct.doc2bow(sentence.lower().split())
        pprint(vecSen)
        tfidfSen = tfidfCorpus[vecSen]
        pprint(tfidfSen)
        vec_sentence.append(tfidfSen)

    #pprint(vec_sentence)

# code to make run main if this file is being run not imported
if __name__ == "__main__":
    main()