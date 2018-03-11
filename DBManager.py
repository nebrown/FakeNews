#-------------------------------------------|
# Project: Fake News                        |
# File: DBManager.py                        |
#       -Provides an interface to access    |
#        and update a database of articles. |
# Date: 5/6/18                              |
#-------------------------------------------|

import sqlite3
import os
from pprint import pprint

class DBManager:
    tableName = 'Articles'
    conn = None
    
    # initializes db connection on init
    def __init__(self, dbName):
        # self.dbName = dbNam
        # try:
        #     os.remove(dbName+'.db')
        # except OSError:
        #     pass
        self.conn = sqlite3.connect(dbName+'.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

    # Creates the database to store articles
    # Removes any previous
    def createTable(self):
        self.conn.execute("DROP TABLE IF EXISTS "+self.tableName)
        self.conn.execute("CREATE TABLE " + self.tableName + " (id INTEGER PRIMARY KEY, title TEXT NOT NULL, article TEXT, source TEXT, category TEXT, topicIdx INT, score FLOAT)")

    # Change the tablename used to have multiple instances if needed
    # Potentially we could keep a counter to automatically allow new
    # instances to have their own db and provide destroy method
    def setTableName(slef, newName):
        self.tableName = newName

    # adds a row to the table
    # data is assumed to be a correctly formed list
    def add(self, data):
        title = data[0]
        article = data[1]
        source = data[2]
        category = data[3]
        topic = data[4]
        score = data[5]
        self.conn.execute("INSERT INTO " + self.tableName + " (title, article, source, category, topicIdx, score) VALUES (?,?,?,?,?,?);", (title, article, source, category, topic, score))

    # return all elements of a specified col
    def getAll(self, colName):
        c=self.conn.cursor()
        c.execute("SELECT DISTINCT "+colName+" FROM "+self.tableName)
        result = c.fetchall()
        return result

    # returns an article with id number from param
    def getID(self, id):
        # db is one indexed. add one to execute
        c = self.conn.cursor()
        c.execute("SELECT title, article, source, category FROM "+self.tableName+" WHERE id="+str(id +1))
        result = c.fetchall()
        return result[0]

    # dump contents out to terminal
    def printAll(self):
        c=self.conn.cursor()
        c.execute("SELECT * from " + self.tableName)
        result=c.fetchall()
        pprint(result)

# Test code
# t = DBManager('test')
# t.createTable()
# t.add(('title', 'article1', 'url', 'All', None, None))
# t.add(('title', 'article2', 'url', 'All', None, None))
# t.add(('title', 'article3', 'url', 'All', None, None))
# t.add(('title', 'article4', 'url', 'All', None, None))
# t.add(('title', 'article5', 'url', 'All', None, None))
# t.add(('title', 'article6', 'url', 'All', None, None))
# r = t.getID(2)
# print(r[0][0])
# pprint(r)
# t.printAll()
#t.test()