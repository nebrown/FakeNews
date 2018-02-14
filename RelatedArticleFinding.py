import sys
import re
import newspaper
#suppress windows chunksize warning
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint

def BenTheSwanman():
    #Get dict and corpus
    dct = corpora.Dictionary.load("./Data/news.dict")
    tfidfCorpus = corpora.MmCorpus("./Data/news.mm")

    #Form LDA Model
    lda =  models.LdaModel(tfidfCorpus, id2word=dct, num_topics = 5)

    #Get topics
    topicMatrix = lda.get_topics()

    #Test topic coherence
    coherenceModel = models.CoherenceModel(model=lda, corpus=tfidfCorpus, coherence='u_mass')
    coherence = coherenceModel.get_coherence_per_topic()
    indexedCoherence = []
    for i, c in enumerate(coherence):
        indexedCoherence.append((i, c))
    print(indexedCoherence)

    #Cut low scoring topics
    sortedCoherence = sorted(indexedCoherence, key=lambda item: -item[1])

    #Print Topics
    for i in range(len(sortedCoherence)):
        pprint(str(i) + ", " + str(sortedCoherence[i][0]) + ": " + str(sortedCoherence[i][1]))

    #Associate with articles
    for i in range(len(sortedCoherence)):
        print("")
        for topic in lda.get_topic_terms(sortedCoherence[i][0]):
            pprint(str(i) + ": " + dct[topic[0]] + ", " + str(topic[1]) + "; ")

if __name__ == "__main__":
    BenTheSwanman()