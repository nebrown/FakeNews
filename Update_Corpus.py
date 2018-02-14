import sys
import re
import newspaper
#suppress windows chunksize warning
import warnings
import OutputToFile as otf
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint


def UpdateCorpus(siteList, numArticles=4):
    # Defines
    documents = []

    j = 0
    while j < len(siteList):
        url = siteList[j]

        # Get documents from selected website
        # Connect to site without caching (for testing only)
        print("\nAttempting to pull data from " + siteList[j] + ". . .")
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
                    documents.append(site.articles[i].text)
            except newspaper.article.ArticleException:
                continue
            except IndexError:
                break
        j += 1;

    #sentences = []
    #for document in documents:
    #    sentences.append(re.split('\. |\n|\.\"', document)) #TODO: Handle quotes that end with ."

    #save all documents on to disk
    otf.SaveDocs(filename='documents.txt', sentences=documents)
    #List of common words to remove
    stoplist = set("for a of the and to in".split())
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

    # Remove words that appear once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            token = re.sub("[!?,.()\":]", "", token)
            frequency[token] += 1

    #texts = [[token for token in text if frequency[token] > 1] for text in texts]

    #pprint(texts)

    # Generate dictionary based on text
    dct = corpora.Dictionary(texts)
    dct.save("./Data/news.dict")

    # Bring documents into vector space using new dictionary
    corpus = [dct.doc2bow(text) for text in texts]

    # Get tfidf transform from corpus
    tfidf = models.TfidfModel(corpus)
    tfidf.save("./Data/news.tfidf")
    tfidfCorpus = tfidf[corpus]
    corpora.MmCorpus.serialize("./Data/news.mm", tfidfCorpus)

    # Use LSI to get topics
    lsi = models.LsiModel(tfidfCorpus, id2word=dct, num_topics = 5)
    lsi.save("./Data/news.lsi")
    #lsiCorpus = lsi[tfidfCorpus]
    pprint(lsi.print_topics(5))

if __name__ == "__main__":
    #remove the first argument, the script name
    sys.argv.pop(0)
    UpdateCorpus(sys.argv)
