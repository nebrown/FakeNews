#-------------------------------------------|
# Project: Fake News                        |
# File: DBManager.py                        |
#       -Provides an interface to access    |
#        and update a database of articles. |
# Date: 5/6/18                              |
#-------------------------------------------|

import sqlite3
import os

class DBManager:
    tableName = 'Articles'
    conn = None
    
    # initializes db connection on init
    def __init__(self, dbName):
        # self.dbName = dbNam
        try:
            os.remove(dbName+'.db')
        except OSError:
            pass
        self.conn = sqlite3.connect(dbName+'.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

    # Creates the database to store articles
    # Removes any previous
    def createTable(self):
        self.conn.execute("DROP TABLE IF EXISTS "+self.tableName)
        self.conn.execute("CREATE TABLE " + self.tableName + " (id INTEGER PRIMARY KEY, title TEXT NOT NULL, article TEXT)")

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
        self.conn.execute("INSERT INTO " + self.tableName + " (title, article) VALUES (?,?);", (title, article))

    # dump contents out to terminal
    def printAll(self):
        c=self.conn.cursor()
        c.execute("SELECT * from " + self.tableName)
        result=c.fetchall()
        print(result)

# Test code
#t = DBManager('test')
#t.createTable()
#t.add(('test', 'art'))
#t.test()