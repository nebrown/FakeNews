#-------------------------------------------|
# Project: Fake News                        |
# File: dbtest.py	                        |
#       -Tests the functionality of the db  |
# Date: 5/6/18                              |
#-------------------------------------------|

import os
from .. import DBManager

# score for running total of tests passed
total = 0
numTests = 1

# test creation
db = DBManager(test)

if os.path.isfile('./test.db'):
	total = total+1

# createTable to add to
db.createTable()

db.add(('title1', 'article1', 'url1', 'Cat1', None, None))
db.add(('title2', 'article2', 'url2', 'Cat2', 0, 1.4))
db.add(('title3', 'article3', 'url3', 'Cat3', 12, 3.8))
db.add(('title4', 'article4', 'url4', 'Cat4', 4, 7))
db.add(('title5', 'article5', 'url5', 'Cat5', 2, 'Fail'))

# What happens when adding before create table, 

if(total == numTests):
	print('All tests passed')