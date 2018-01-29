# Article_Subjectivity_Analysis
# Written by Benjamin Swanson 1/28/18
# Last edited: 1/28/18

import sys
from textblob import TextBlob
import newspaper

# Connect to site without caching (for testing only)
paper = newspaper.build(sys.argv[1], is_memo = False)
paper.clean_memo_cache()
print("\nSite name: " + paper.brand)
print("Site description: " + paper.description)

# List articles for user
for i in range(5):
    try:
        paper.articles[i].download()
        paper.articles[i].parse()
        print(str(i) + ": " + paper.articles[i].title)
    except TypeError:
        print(str(i) + ": Invalid")
j = input("Which article would you like to analyze? ")
first_article = paper.articles[int(j)]

"""
# Analyse first article on site
print("Site size: " + str(paper.size()))
try:
    first_article = paper.articles[5]
except IndexError:
    print("Error: Articles in cache ignored. Clear cache for more articles.")
    sys.exit()

first_article.download()
first_article.parse()
"""

print("\nArticle: " + first_article.title)
print("-----Article contents-----")
print(first_article.text)
print("-----End article-----\n")

# Create textblob with contents of article
tb = TextBlob(first_article.text)

# Print article subjectivity score and per-sentence score
print("Article subjectivity score: " + str(tb.subjectivity))
for s in tb.sentences:
    # Print first 3 words of s
    """words = s.tokens
    i = 0
    while i < 3 and i < len(words):
        print(words[i] + " ", end = "")
        i += 1
    if len(words) > 3:
        print(". . .")
    else:
        print(s[s.end_index])
"""
    print("\n" + str(s))
    # Print subjectivity score
    print("Score: " + str(s.subjectivity))
