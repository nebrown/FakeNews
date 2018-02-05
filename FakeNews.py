from textblob import TextBlob
from gensim import corpora
import os

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 16:59:14 2018

@author: Owner
"""


def main():
    # list to hold all articles, we may run into memory issues
    articles = []

    # do file IO, read only, iterate through /Articles dir child of cwd
    articlesPath = os.getcwd() + '/Articles'
    for filename in os.listdir(articlesPath):
        with open(articlesPath+'/'+filename) as file:
            articles.append(file.read())
    print(file.closed)

    # Run NLP on each article
    # currently just prints polarity and subjectivity of the articles
    for index, article in enumerate(articles):
        blob = TextBlob(article)
        print(blob.sentiment, index, sep=", ")
        # print(article)
        # blob = TextBlob(text)
        # print(blob.tags)
        # print(blob.noun_phrases)
        # print(blob.sentences)
        # for sentence in blob.sentences:
        #    print(sentence.sentiment.polarity,
                    # sentence.sentiment.subjectivity, sep=", ");

# code to make run main if this file is being run not imported
if __name__ == "__main__":
    main()

# Can add quick testcode below here if needed but PLEASE REMOVE before pushing
