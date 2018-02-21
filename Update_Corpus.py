import sys
import os
import re
import newspaper
#suppress windows chunksize warning
import warnings
import OutputToFile as otf
import shutil
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint


def UpdateCorpus(siteList, numArticles=30):
    # Defines
    documents = []
    # Clear previous docs
    docFolder = "./Data/Docs/"
    if os.path.exists(docFolder):
        shutil.rmtree(docFolder)
    os.makedirs(docFolder)

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
                    # Save docs
                    f = open("./Data/Docs/" + str(len(documents)) + ".txt", "w")
                    f.write(url + "\n")
                    f.write(site.articles[i].title + "\n")
                    f.write(site.articles[i].text)
                    f.close()
            except newspaper.article.ArticleException:
                # Will skip over articles it has trouble pulling
                continue
            except UnicodeEncodeError:
                # Will prevent weird characters from stopping execution
                print("Unicode error in doc " + str(len(documents)))
                continue
            except IndexError:
                # Will end reading from sites with fewer than numArticles to read
                break
        j += 1;

    #sentences = []
    #for document in documents:
    #    sentences.append(re.split('\. |\n|\.\"', document)) #TODO: Handle quotes that end with ."

    #List of common words to remove
    stoplist = set("for a of the and to in he his she hers".split())
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

    # Remove words that appear once
    frequency = defaultdict(int)
    for text in texts:
        print(text)
        for i in range(len(text)):
            text[i] = re.sub("[!?,.()\":]", "", text[i])
            frequency[text[i]] += 1
        print(text)

    #texts = [[token for token in text if frequency[token] > 1] for text in texts]

    #pprint(texts)

    # Generate dictionary based on text
    dct = corpora.Dictionary(texts)
    dct.save("./Data/news.dict")

    # Bring documents into vector space using new dictionary
    corpus = [dct.doc2bow(text) for text in texts]

    # Get tfidf transform from corpus
    corpora.MmCorpus.serialize("./Data/news.corp", corpus),
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
    # Allow for user-defined sites
    if len(sys.argv) >= 2:
        UpdateCorpus(sys.argv[1:])
    # Otherwise use sitelist
    else:
        sitelist = []
        f = open("./sitelist.txt", "r")
        line = f.readline()
        while line is not "":
            sitelist.append(line[:-1])
            line = f.readline()
        f.close()
        UpdateCorpus(sitelist)
