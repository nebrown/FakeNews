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
from nlp import NLPContainer

# sets up directory for data storage
def SetupDirectory(category="All"):
    # remove any previous data
    docFolder = "./Data/Docs/" + category +"/"
    try:
        if os.path.exists(docFolder):
            shutil.rmtree(docFolder)
        # make new dir
        os.makedirs(docFolder)
    except PermissionError:
        print("Windows permission error.")
        return
    return docFolder

# builds the site based off of url using newspaper
def GetDocs(url):
    print("\nAttempting to pull data from " + url + ". . .")
    site = newspaper.build(url, is_memo = False)
    site.clean_memo_cache()
    print("Site name: " + site.brand)
    print("Site description: " + site.description)
    print("Site size: " + str(site.size()))
    return site

# Saves document from newspaper
def SaveDocument(folder, url, title,text, index):
    f = open(folder + str(index) + ".txt", "w")
    f.write(url + "\n")
    f.write(title + "\n")
    f.write(text)
    f.close()

# Removes unwanted words from documents
def RemoveWords(documents):
    # Remove common words
    stoplist = set("for a of the and to in cnn npr".split())
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

    # Remove words that appear once
    frequency = defaultdict(int)
    for text in texts:
        #print(text)
        for i in range(len(text)):
            text[i] = re.sub("[!?,.()\":]", "", text[i])
            frequency[text[i]] += 1
        #print(text)

    # texts = [[token for token in text if frequency[token] > 1] for text in texts]
    return texts

# Runs and saves various NLP on texts
def RunNLP(texts):
    # Generate dictionary based on text
    dct = corpora.Dictionary(texts)
    # dct.save("./Data/" + category + "/news.dict")
    dct.save("./Data/news.dict")

    # Bring documents into vector space using new dictionary
    corpus = [dct.doc2bow(text) for text in texts]

    # Get tfidf transform from corpus
    # corpora.MmCorpus.serialize("./Data/" + category + "/news.corp", corpus),
    corpora.MmCorpus.serialize("./Data/news.corp", corpus)
    tfidf = models.TfidfModel(corpus)
    # tfidf.save("./Data/" + category + "/news.tfidf")
    tfidf.save("./Data/news.tfidf")

    tfidfCorpus = tfidf[corpus]
    # corpora.MmCorpus.serialize("./Data/" + category + "/news.mm", tfidfCorpus)
    corpora.MmCorpus.serialize("./Data/news.mm", tfidfCorpus)

    # Use LSI to get topics
    lsi = models.LsiModel(tfidfCorpus, id2word=dct, num_topics = 5)
    # lsi.save("./Data/" + category + "/news.lsi")
    lsi.save("./Data/news.lsi")

    #lsiCorpus = lsi[tfidfCorpus]
    pprint(lsi.print_topics(5))

def UpdateCorpus(siteList, category="All", numArticles=30):
    nlp = NLPContainer()
    # Defines
    documents = []

    docFolder = SetupDirectory()

    j = 0
    while j < len(siteList):
        url = siteList[j]

        # Get documents from selected website
        # Connect to site without caching (for testing only)
        site = GetDocs(url)

        # Download set of articles
        for i in range(numArticles):
            try:
                site.articles[i].download()
                site.articles[i].parse()
                #check article has more than 200 characters to filter non-news
                if (len(site.articles[i].text) > 400):
                    print(str(i) + ": " + site.articles[i].title + "\n", end = "")
                    documents.append(site.articles[i].text)
                    # Save docs
                    SaveDocument(docFolder, url, site.articles[i].title, site.articles[i].text, len(documents)-1)
            except newspaper.article.ArticleException:
                # Will skip over articles it has trouble pulling
                continue
            except UnicodeEncodeError:
                # Will prevent weird characters from stopping execution
                print("Unicode error in doc " + str(len(documents)))
                f.close()
                continue
            except IndexError:
                # Will end reading from sites with fewer than numArticles to read
                break
        j += 1;

    # Filter out words
    texts = RemoveWords(documents)

    # Run NLP    
    RunNLP(texts)
    

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
