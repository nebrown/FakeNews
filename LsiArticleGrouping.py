import sys
import os
import re
import shutil
import newspaper
#suppress windows chunksize warning
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities,summarization
from collections import defaultdict
from pprint import pprint

def GetArticleText(url):
    article = newspaper.Article(url)
    article.download()
    article.parse()
    return article.text

def SearchArticles(query, category="All"):
    totalTopics = 5
    chosenTopics = 5

    # Get dictionary, corpus, model
    dct = corpora.Dictionary.load("./Data/" + category + "/news.dict")
    tfidfCorpus = corpora.MmCorpus("./Data/" + category + "/news.mm")
    #lsi = models.LsiModel.load("./Data/" + category + "news.lsi")

    lsi = models.LsiModel(tfidfCorpus, id2word=dct, num_topics = totalTopics)

    # Perform similarity queries with topic terms
    index = similarities.MatrixSimilarity(lsi[tfidfCorpus])

    # Create uniformly weighted query from list of words
    vec_bow = dct.doc2bow(query.lower().split())

    # Pick articles most related to each topic
    sims = []
    sims.append(index[lsi[vec_bow]])

    # Sort by decreasing similarity to topics
    sortedSims = []
    for sim in sims:
        enum = list(enumerate(sim))
        sortedSims.append(sorted(enum, key=lambda item: -item[1]))
    #pprint(sortedSims)

    # Pull out top articles
    for i in range(len(sortedSims)):
        # print topic tags
        pprint(lsi.print_topic(i))
        pprint(sortedSims[i][:10])

    # Clear previous meta-docs
    try:
        docFolder = "./Data/Queries/" + category + "/"
        if os.path.exists(docFolder):
            shutil.rmtree(docFolder)
        os.makedirs(docFolder)
    except PermissionError:
        print("Windows permissions error.")
        return

    # Create meta-documents
    for i in range(len(sortedSims)):
        # Open folder to write to
        wf = open("./Data/Queries/" + category + "/fquery.txt", "w")
        wr = open("./Data/Queries/" + category + "/query.txt", "w")
        wf.write(lsi.print_topic(i))
        # Get top 10 related articles and write them in
        for j in range(10):
            articleNum = sortedSims[i][j][0]
            r = open("./Data/Docs/" + category + "/" + str(articleNum) + ".txt", "r")
            articleUrl = r.readline()
            articleTitle = r.readline()
            articleContents = r.read()
            wf.write("\n\n====================================")
            wf.write("\n" + str(j) + ": " + str(sortedSims[i][j][1]) + "\n")
            wf.write(articleUrl + articleTitle + articleContents)
            wr.write("\n" + articleContents + "\n")
            r.close()
        wr.close()
        wf.close()

    # Pull out highly relevant sentences
    for i in range(len(sortedSims)):
        topSentences = SimilarSentences("./Data/Queries/" + category + "/query.txt", category)
        w = open("./Data/Queries/" + category + "/squery.txt", "w")
        w.write("Query: " + query + "\n")
        for topSen in topSentences:
            w.write("\n" + topSen)
        w.close()

    print("Search completed.")


def GroupArticles(category = "All"):
    totalTopics = 5
    chosenTopics = 5
    numSentences = 25

    # Get dictionary, corpus, model
    dct = corpora.Dictionary.load("./Data/" + category + "/news.dict")
    tfidfCorpus = corpora.MmCorpus("./Data/" + category + "/news.mm")
    #lsi = models.LsiModel.load("./Data/news.lsi")

    lsi = models.LsiModel(tfidfCorpus, id2word=dct, num_topics = totalTopics)

    # Get topic top terms in 
    lsiTopics = lsi.show_topics(num_topics=chosenTopics, num_words=100, formatted=False)
    topics = []
    for i in range(len(lsiTopics)):
        topics.append( [(dct.token2id[topic[0]], topic[1]) for topic in lsiTopics[i][1]] )
    #pprint(topics)

    # Perform similarity queries with topic terms
    index = similarities.MatrixSimilarity(lsi[tfidfCorpus])

    # Pick articles most related to each topic
    sims = []
    for topic in topics:
        sims.append(index[lsi[topic]])

    # Sort by decreasing similarity to topics
    sortedSims = []
    for sim in sims:
        enum = list(enumerate(sim))
        sortedSims.append(sorted(enum, key=lambda item: -item[1]))
    #pprint(sortedSims)

    # Pull out top articles
    for i in range(len(sortedSims)):
        # print topic tags
        pprint(lsi.print_topic(i))
        pprint(sortedSims[i][:10])

    # Clear previous meta-docs
    try:
        docFolder = "./Data/Aggregates/" + category + "/"
        if os.path.exists(docFolder):
            shutil.rmtree(docFolder)
        os.makedirs(docFolder)
    except PermissionError:
        print("Windows permissions error.")
        return

    # Create meta-documents
    for i in range(len(sortedSims)):
        # Open folder to write to
        wf = open("./Data/Aggregates/" + category + "/f" + str(i) + ".txt", "w")
        wr = open("./Data/Aggregates/" + category + "/" + str(i) + ".txt", "w")
        wf.write(lsi.print_topic(i))
        # Get top 10 related articles and write them in
        for j in range(numSentences):
            articleNum = sortedSims[i][j][0]
            r = open("./Data/Docs/" category + "/" + str(articleNum) + ".txt", "r")
            articleUrl = r.readline()
            articleTitle = r.readline()
            articleContents = r.read()
            wf.write("\n\n====================================")
            wf.write("\n" + str(j) + ": " + str(sortedSims[i][j][1]) + "\n")
            wf.write(articleUrl + articleTitle + articleContents)
            wr.write("\n" + articleContents + "\n")
            r.close()
        wr.close()
        wf.close()

    # Pull out highly relevant sentences
    for i in range(len(sortedSims)):
        topSentences = SimilarSentences("./Data/Aggregates/" + category + "/" + str(i) + ".txt", category)
        w = open("./Data/Aggregates/" + category + "/s" + str(i) + ".txt", "w")
        w.write("Keywords: " + lsi.print_topic(i) + "\n")
        topSummary = ""
        for topSen in topSentences:
            w.write("\n" + topSen)
            # Get rid of numbers
            splitSen = topSen.split(":")
            topText = ""
            for sen in splitSen[1:]:
                topText = topText + sen
            topSummary = topSummary + " " + topText
        # Create summary
        sumText = summarization.summarizer.summarize(topSummary)
        w.write("\nSummary:\n" + sumText)
        w.close()

    print("Extraction completed.")


def SimilarSentences(aggregatePath, category):
    dct = corpora.Dictionary.load("./Data/" + category + "/news.dict")
    tfidfCorpus = corpora.MmCorpus("./Data/" + category + "/news.mm")
    lsi = models.LsiModel.load("./Data/" + category + "/news.lsi")
    tfidf = models.TfidfModel(tfidfCorpus)

    # Get aggregate document
    f = open(aggregatePath, "r")
    agg = f.read()
    f.close()

    sentences = []
    senList = re.split('\. |\n|\.\"', agg)
    for sentence in senList:
        if len(sentence) > 2:
            sentences.append(sentence) #TODO: Handle quotes that end with ."

    # Remove words that appear once
    vec_sentence = []
    for sentence in sentences:
        for token in sentence:
            token = re.sub("[!?,.()\":]", "", token)
        vecSen = dct.doc2bow(sentence.lower().split())
        #pprint(vecSen)
        tfidfSen = tfidf[vecSen]
        #pprint(tfidfSen)
        vec_sentence.append(tfidfSen)

    #pprint(vec_sentence)

    # init similarity query from lsi transform of sentences to compare to
    index = similarities.MatrixSimilarity(lsi[vec_sentence])
    
    # Get running scores for each sentence
    i = 0
    simSum = []
    for vecSen in vec_sentence:
        sims = index[lsi[vecSen]]
        # sum similarities
        thisSum = [i, 0]
        for sim in sims:
            thisSum = [i, thisSum[1]+sim]
        simSum.append(thisSum)
        i += 1
    # Sort sentence sums
    simSum = sorted(simSum, key=lambda item: -item[1])
    #pprint(simSum)

    #Print most related sentences
    #print("\n")
    #pprint(sentences)
    topSentences = []
    for i in range(15):
        topSentences.append(str(i) + ", " + str(simSum[i][0]) + ", " + str(simSum[i][1]) + ": " + sentences[simSum[i][0]] + "\n")

    return topSentences


if __name__ == "__main__":
    GroupArticles()