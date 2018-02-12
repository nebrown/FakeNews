#Related Articles Search
#Jack Bauman
#Last edited Feb 12, 2018

#DOn't touch yet still fixing
import sys
import newspaper

#takes in a (mainArticle), and a list of (articles) and dispenses related articles URLS in a list
def findRelatedArticles(mainArticle, articles=[]):
	relatedArticles = []	
	relatedArtcileURLs = []
	mainArticle.parse()
	mainArticle.nlp()
	mainArticleKeywords = Article(mainArticle).keywords 					#generates keywords for main article
	for nextArticle in articles:											#iterates through article list
		matchScore = 0
		nextArticle.parse()
		nextArticle.nlp()
		nextArticleKeywords = Article(nextArticle).keywords
		for mainKey in mainArticleKeywords:
			for nextKey in nextArticleKeywords:
				if str(mainKey)==str(nextKey): 								#compares keyword matches in articles
					matchScore += 1
		if matchScore > 2:													#if articles has (high threshhold) mathces, prepends to output list
			relatedArticles.prepend(nextArticle)
			relatedArticleURLs.prepend(nextArticle.url)
		elif matchScore>0:													#if article has (low threshold) matches, appends to output list
			relatedArticles.append(nextArticle)
			relatedArticleURLs.append(nextArticle.url)
	return relatedArticlesURLS												#returns URL list

#for testing, takes in a sample of 10 articles from cnn, runs findRelatedArticles() on the 1st with next 9 as possible relatives
def main():																
	paper = newspaper.build('http://cnn.com')
	mainArticle = paper.articles[1].download()
	nextArticles = []
	for a in range(2,10):
		nextArticles.append(paper.articles[a].download())
	related = findRelatedArticles(mainArticle, nextArticles)
	if len(related) == 0:
		print("No related articles found.")
	else:
		print("Related articles:")
		for relative in related:
			print(str(relative))
