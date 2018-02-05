import sys
import re
import newspaper
from gensim import corpora
from collections import defaultdict
from pprint import pprint

# Defines
numArticles = 10

# Check correct num arguments
if len(sys.argv) is not 3:
    sys.exit("Invalid number of arguments: Please give site address only.")
url = sys.argv[1]
query = sys.argv[2]

# Get documents from selected website
# Connect to site without caching (for testing only)
site = newspaper.build(url, is_memo = False)
site.clean_memo_cache()
print("\nSite name: " + site.brand)
print("Site description: " + site.description)
print("Site size: " + str(site.size()))

# Download set of articles
documents = []
for i in range(numArticles):
    #Get articles from site
    try:
        site.articles[i].download()
        site.articles[i].parse()
        #check article has more than 200 characters to filter non-news
        if (len(site.articles[i].text) > 200):
            print(str(i) + ": " + site.articles[i].title + ": ", end = "")
            documents.append(site.articles[i].text)
    except newspaper.article.ArticleException:
        continue

sentences = []
for document in documents:
    sentences.append(re.split('\. |\n|\.\"', document)) #TODO: Handle quotes that end with ."

pprint(sentences)

#List of common words to remove
stoplist = set("for a of the and to in".split())
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

# Remove words that appear once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

#pprint(texts)