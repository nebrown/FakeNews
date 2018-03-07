import sys
import os
import re
import newspaper
#suppress windows chunksize warning
import warnings
# import OutputToFile as otf
import shutil
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
# from nlp import NLPContainer
from  DBManager import DBManager

# db = DBManager('corpus')
# db.createTable()

# sets up directory for data storage
def SetupDirectory(category="All"):
    # remove any previous data
    docFolder = "./Data/" + category +"/Docs/"
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
def SaveDocument(db, folder, url, title,text, index, category="All"):
    # Store on os
    f = open(folder + str(index) + ".txt", "w")
    f.write(url + "\n")
    f.write(title + "\n")
    f.write(text)
    f.close()

    # Store in db
    db.add((title,text, url, category, None, None))
    # db.printAll()


# Removes unwanted words from documents
def RemoveWords(documents):
    # Remove common words
    stoplist = set("for a of the and to in cnn npr image copyright \" ".split())
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

    # Remove words that appear once
    frequency = defaultdict(int)
    for text in texts:
        #print(text)
        for i in range(len(text)):
            text[i] = re.sub("[!?,.():]", "", text[i])
            frequency[text[i]] += 1
        #print(text)

    # texts = [[token for token in text if frequency[token] > 1] for text in texts]
    return texts

# Runs and saves various NLP on texts
def RunNLP(texts, category="All"):
    # Generate dictionary based on text
    dct = corpora.Dictionary(texts)
    # dct.save("./Data/" + category + "/news.dict")
    dct.save("./Data/"+category+"/news.dict")

    # Bring documents into vector space using new dictionary
    corpus = [dct.doc2bow(text) for text in texts]

    # Get tfidf transform from corpus
    # corpora.MmCorpus.serialize("./Data/" + category + "/news.corp", corpus),
    corpora.MmCorpus.serialize("./Data/"+category+"/news.corp", corpus)
    tfidf = models.TfidfModel(corpus)
    # tfidf.save("./Data/" + category + "/news.tfidf")
    tfidf.save("./Data/"+category+"/news.tfidf")

    tfidfCorpus = tfidf[corpus]
    # corpora.MmCorpus.serialize("./Data/" + category + "/news.mm", tfidfCorpus)
    corpora.MmCorpus.serialize("./Data/"+category+"/news.mm", tfidfCorpus)

    # Use LSI to get topics
    lsi = models.LsiModel(tfidfCorpus, id2word=dct, num_topics = 5)
    # lsi.save("./Data/" + category + "/news.lsi")
    lsi.save("./Data/"+category+"/news.lsi")

    #lsiCorpus = lsi[tfidfCorpus]
    pprint(lsi.print_topics(5))

# makes sure article was not previously found
def isRepeated(site, curArticleIdx):
    for i in range(curArticleIdx-1):
        #print("t1 = "+ site.articles[curArticleIdx].title+"\nt2 = "+site.articles[i].title)
        if(site.articles[curArticleIdx].title == site.articles[i].title or site.articles[curArticleIdx].text == site.articles[i].text):
            print("Found")
            return True 

    return False

def UpdateCorpus(db, siteList, category="All", numArticles=30):
    # nlp = NLPContainer()
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
        for i in range(min(numArticles, site.size())):
            try:
                site.articles[i].download()
                site.articles[i].parse()
                # check article has more than 200 characters to filter non-news
                # Remove double up
                if (len(site.articles[i].text) > 400):
                    if(isRepeated(site, i) == False):
                    #if(i==0 or (site.articles[i].text != site.articles[i-1].text)):
                        print(str(i) + ": " + site.articles[i].title + "\n", end = "")
                        documents.append(site.articles[i].text)
                        # Save docs
                        SaveDocument(db, docFolder, url, site.articles[i].title, site.articles[i].text, len(documents)-1)
            except newspaper.article.ArticleException:
                # Will skip over articles it has trouble pulling
                continue
            except UnicodeEncodeError:
                # Will prevent weird characters from stopping execution
                print("Unicode error in doc " + str(len(documents)))
                # f.close()
                continue
            except IndexError:
                # Will end reading from sites with fewer than numArticles to read
                break
        j += 1;

        #Check if no docs found
    if len(documents) == 0:
        print("No articles found.")
        return
    # Filter out words
    texts = RemoveWords(documents)
    db.printAll()
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

    # In for testing db
# SaveDocument('./', 'url', 'title','text', 2)