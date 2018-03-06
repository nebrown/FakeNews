# Article_Subjectivity_Analysis
# Written by Benjamin Swanson 1/29/18
# Last edited: 1/29/18

import sys
from textblob import TextBlob
import newspaper

# Defines
numArticles = 30

# Check correct num arguments
if len(sys.argv) is not 2:
    sys.exit("Invalid number of arguments: Please give site address only.")
# Connect to site without caching (for testing only)
site = newspaper.build(sys.argv[1], is_memo = False)
site.clean_memo_cache()
print("\nSite name: " + site.brand)
print("Site description: " + site.description)
print("Site size: " + str(site.size()))


avgScore = 0
j = 0
for i in range(numArticles):
    #Get articles from site
    try:
        site.articles[i].download()
        site.articles[i].parse()
        

        #check article has more than 200 characters to filter non-news
        if (len(site.articles[i].text) > 200):
            print(str(i) + ": " + site.articles[i].title + ": ", end = "")
            # Evaluate subjectivity score
            tb = TextBlob(site.articles[i].text)
            avgScore += tb.subjectivity
            print(str(tb.subjectivity))
            j += 1
    except newspaper.article.ArticleException:
        continue

#get average
avgScore = avgScore / j
print("Average subjectivity: " + str(avgScore))