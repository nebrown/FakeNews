#Objectivity_Analysis
#Written by Ben Swanson 1/28/18
#Last edited: 1/28/18

from textblob import TextBlob

#Get sentence
sentence = TextBlob("I love Ben so much, he is just the greatest guy ever.")
subjectivity = sentence.subjectivity
print(sentence + "\nscore: " + str(subjectivity))

paragraph = TextBlob("Johnny likes basketball. He plays every other day at the court dowwn the street. He plays with his friends. Johnny is a mentally stable genius who has huge, beautiful hands. I have the best words. Hillary Clinton is a whore and a demon who sucks people's souls.")
print("\n" + str(paragraph) + "\nfull score: " + str(paragraph.subjectivity))

parList = paragraph.sentences

for s in parList:
    print("\n" + str(s) + "\nsentence score: " + str(s.subjectivity))