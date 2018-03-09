#Jack Bauman
import sqlite3
import newspaper
from newspaper import Article

db = sqlite3.connect('articleDb.db')
c = db.cursor()

#creates table to store articles called 'articleTable'
def createTable():
	c.execute
	db.execute('CREATE TABLE IF NOT EXISTS articleTable (url TEXT, article TEXT, keywords LIST)')

#pass a URL, to database log:articleUrl, text of article, and keywords
def URLstoreArticle(articleUrl):
	art = Article(articleUrl)
	art.download()
	art.parse()
	artText = art.text  #obtain text

	art.nlp()
	keys = art.keywords	#obtain keywords
	
	c.execute('INSERT INTO articleTable(url, article, keywords) VALUES (?,?,?)',
		(articleUrl,artText,keys))
	db.commit()
	c.close()
	open.close()

#pass URl, text, and keywords for storage
def storeArticle(articleUrl,artText,keys):
	c.execute('INSERT INTO articleTable(url, article, keywords) VALUES (?,?,?)',
		(articleUrl,artText,keys))
	db.commit()
	c.close()
	open.close()

def pullArticle():
	c.execute('SELECT * FROM articleTable')
	return c.fetchall()

#pulls articles with a given keyword
def pullArticleWithKey(key):
	c.execute(str('SELECT * FROM articleTable WHERE instr(keywords, ' + str(key) +') > 0)'))
	return c.fetchall() 

 #testing
#createTable()
#URLstoreArticle('https://www.cnn.com/2018/03/09/politics/trump-kim-jong-un-north-korea-tillerson-intl/index.html')
