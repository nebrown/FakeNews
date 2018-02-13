class OutputToFile():

	#Pass a list of sentences and creates a file
	def Output(sentences = []):
		f = open('outputfile.txt', 'w')
		for sentence in sentences:
			f.write(str(sentence) + ' ')
		f.close()
		return f

	#Pass two tuple lists, ver and unver and creates a file
	def OutputBoth(verSentences = [], unvSentences = []):
		f = open('outputfile.txt', 'w')
		f.write('Verfied News:' + '\n')
		for sentence in verSentences:
			sentence = tuple(sentence)
			f.write(str(sentence[0]) + ' [' + str(sentence[1]) + '] ')
		f.write('\n\n'+'Less Verified News:'+'\n')
		for sentence in unvSentences:
			sentence=tuple(sentence)
			f.write(str(sentence[0]) + ' [' + str(sentence[1]) + '] ')			
		f.close()
		return f

	#Pass two tuple lists and a file, ver and unver wrties to original file
	def OutputBoth(file, verSentences = [], unvSentences = []):
		with open(file, 'w') as f:
			f.write('Verfied News:' + '\n')
			for sentence in verSentences:
				sentence = tuple(sentence)
				f.write(str(sentence[0]) + ' [' + str(sentence[1]) + '] ')
			f.write('\n\n'+'Less Verified News:'+'\n')
			for sentence in unvSentences:
				sentence=tuple(sentence)
				f.write(str(sentence[0]) + ' [' + str(sentence[1]) + '] ')
			f.close()
			return f



	#tester below (remove later)
	#s = [("Little child.", 0.5), ("Running wild.",0.4), ("Can't you see.",0.2)]
	#d = [("Donald Trump sick as fuck.", 0.1)]
	#print(OutputBoth(s,d))