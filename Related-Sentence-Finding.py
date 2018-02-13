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
from Update_Corpus import UpdateCorpus

def main():
    #defines
    siteList = ["https://cnn.com", "https://washingtonpost.com"]

    #update corpus if command line arg
    #only do if sys.argv[1] exists
    if(sys.argv[1] == '-U'):
        UpdateCorpus(siteList)

    #make the dictionary and model
    dct = corpora.Dictionary.load("./Data/news.dict")
    tfidfCorpus = corpora.MmCorpus("./Data/news.mm")
    lsi = models.LsiModel.load("./Data/news.lsi")
    tfidf = models.TfidfModel(tfidfCorpus)
    
    #data structure to hold articles
    articles = []

    '''
    articlesPath = os.getcwd() + '/SampleArticles'
    for filename in os.listdir(articlesPath):
        with open(articlesPath+'/'+filename) as file:
            articles.append(file.read())
    '''

    
    numArticles = 30

    #why is this done here and in UpdateCorpus
    j = 0
    while j < len(siteList):
        url = siteList[j]

        # Get documents from selected website
        # Connect to site without caching (for testing only)
        print("\nAttempting to pull data from " + sys.argv[j] + ". . .")
        site = newspaper.build(url, is_memo = False)
        site.clean_memo_cache()
        print("Site name: " + site.brand)
        print("Site description: " + site.description)
        print("Site size: " + str(site.size()))

        # Download set of articles
        for i in range(numArticles):
            #Get articles from site
            try:
                site.articles[i].download()
                site.articles[i].parse()
                #check article has more than 200 characters to filter non-news
                if (len(site.articles[i].text) > 200):
                    print(str(i) + ": " + site.articles[i].title + "\n", end = "")
                    articles.append(site.articles[i].text)
            except newspaper.article.ArticleException:
                continue
            except IndexError:
                break
        j += 1;
    

    print("start nlp")
    sentences = []
    for article in articles:
        sentences.append(re.split('\. |\n|\.\"', article)) #TODO: Handle quotes that end with ."

    # Remove words that appear once
    vec_sentence = []
    for sentence in sentences[0]:
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

    #Print top 3 most related sentences
    print("end")
    for i in range(5):
        print(str(i) + ": " + sentences[0][simSum[i][0]])

# code to make run main if this file is being run not imported
if __name__ == "__main__":
    main()
