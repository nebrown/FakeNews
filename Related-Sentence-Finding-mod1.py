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
    tfidfCorpus = models.TfidfModel.load("./Data/news.tfidf")

    articles = []

    articlesPath = os.getcwd() + '/SampleArticles'
    for filename in os.listdir(articlesPath):
        with open(articlesPath+'/'+filename) as file:
            articles.append(file.read())

    sentences = []
    for article in articles:
        #sentences.append(re.split("\.", article))
        sentences.append(re.split('\. |\n|\.\"', article)) 
        #TODO: Handle quotes that end with ."

    # TODO Rename variables
    vec_sentence = []
    scores = []
    for sentence in sentences[0]:
        print(sentence)
        for token in sentence:
            token = re.sub("[!?,.()\":]", "", token)
        vecSen = dct.doc2bow(sentence.lower().split())
        #only add to vec if vecSen is not empty
        #pprint(vecSen)
        tfidfSen = tfidfCorpus[vecSen]
        #pprint(tfidfSen)
        vec_sentence.append(tfidfSen)
  
    #iterate through vec_sen and find accumulated score
    for vector in vec_sentence:
        score = 0
        if len(vector) > 0:
            for pair in vector:
               score = score + pair[1]
            scores.append(score / len(vector))
        else:
            scores.append(0)

    #sort score with sentences
    i=0
    for score in scores:
        if score > 0.3:
            pprint(score)
            pprint(sentences[0][i])
                      
        i=i+1

    #pprint(scores)
    
    #print matched sentences
    j=0
    i=0
    matches=0
    for sentence[i] in sentences:
        for sentence[j] in sentences:
            compare(sentence[i],sentence[j])          
            if sentence[i] = sentence[j]:
                matches=matches+1
                pprint(sentences[i][k][matches])
            j=j+1
            i=i+1
    
    
    #TODO print 5 most matched sentences and 5 least matched, modified from above
        
# code to make run main if this file is being run not imported
if __name__ == "__main__":
    main()
