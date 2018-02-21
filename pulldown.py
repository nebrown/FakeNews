import newspaper

#simply returns URLS of newspaper categories
def pullDown(newspaperURL):
	try:
		paper = newspaper.build(newspaperURL)
	except:
		print("Cannot reach newspaper, invalid newspaper URL.")
	return paper.category_urls()

#tester
#print(pullDown("https://www.cnn.com"))
