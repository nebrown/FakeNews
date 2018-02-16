#Related Articles Search
#Jack Bauman
#Last edited Feb 16, 2018

import sys
import newspaper
from newspaper import Article

#takes in a (mainArticle), and a list of (articles) and dispenses related articles URLS in a list
def findRelatedArticles(mainArticle, articles):	
	relatedArticleURLs = []
	#mainArticle.download()
	mainArticle.parse()
	mainArticle.nlp()
	mainArticleKeywords = mainArticle.keywords 					#generates keywords for main article
	for nextArticle in articles:											#iterates through article list
		matchScore = 0
		#nextArticle.download()
		nextArticle.parse()
		nextArticle.nlp()
		nextArticleKeywords = nextArticle.keywords
		for mainKey in mainArticleKeywords:
			for nextKey in nextArticleKeywords:
				if str(mainKey)==str(nextKey): 								#compares keyword matches in articles
					matchScore += 1
		if matchScore > 2:													#if articles has (high threshhold) mathces, prepends to output list
			relatedArticleURLs.insert(0,nextArticle.url)
		elif matchScore>1:													#if article has (low threshold) matches, appends to output list
			relatedArticleURLs.append([nextArticle.title,nextArticle.url,nextArticle.keywords])
	return relatedArticleURLs												#returns URL list

#for testing, takes a sample of 10 articles from cnn, runs findRelatedArticles() on the 1st with next 9 as possible relatives
def main():														
	paper = newspaper.build('http://www.cnn.com/')
	nextArticles = []
	mainArticle = Article('http://www.cnn.com/2018/02/09/sport/winter-olympics-opening-ceremony-intl/index.html')
	
	nextArticles.append(Article('http://www.cnn.com/2018/02/09/asia/north-korea-olympic-defection-fears-intl/index.html'))
	nextArticles.append(Article('http://www.cnn.com/2018/02/09/politics/pence-south-korea-olympics/index.html'))
	nextArticles.append(Article('http://www.cnn.com/2018/02/09/asia/india-modi-israel-palestinian-visit-intl/index.html'))
	nextArticles.append(Article('http://www.cnn.com/2018/02/08/asia/military-parade-north-korea-intl/index.html'))
	nextArticles.append(Article('https://www.cnn.com/2018/02/16/us/shooter-profile-invs/index.html'))
	nextArticles.append(Article('https://www.cnn.com/videos/tv/2018/02/16/newsstream-intv-stout-moonchung-olympics.cnn'))
	nextArticles.append(Article('https://www.cnn.com/2018/02/16/sport/jamaican-womens-bobsled-red-stripe/index.html'))
	nextArticles.append(Article('https://www.cnn.com/2018/02/16/sport/wojtek-wolski-winter-olympics-2018/index.html'))

	mainArticle.download()
	for a in nextArticles:
		a.download()
	related = findRelatedArticles(mainArticle, nextArticles)
	if len(related) == 0:
		print("No related articles found.")
	else:
		print("Related articles:")
		for relative in related:
			print(str(relative[0]) + ': ' + str(relative[1]))

main()
