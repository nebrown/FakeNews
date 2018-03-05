import sys
import os
from PyQt5 import (QtWidgets, QtCore)
from Update_Corpus import UpdateCorpus
from RelatedSentenceFinding import SentenceMatching
import LsiArticleGrouping as lag

class Window(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.init_ui()
        self.currentCategory = "All"

    def init_ui(self):
        # create features
        #self.button1 = QtWidgets.QPushButton('Search')
        self.button1 = QtWidgets.QPushButton('Collect Articles')
        self.button2 = QtWidgets.QPushButton('Clear')
        self.button3 = QtWidgets.QPushButton('Extract Sentences')
        self.button4 = QtWidgets.QPushButton('Search')
        self.button5 = QtWidgets.QPushButton('Related Articles')
        self.button6 = QtWidgets.QPushButton('Set Category')
        self.exitButton = QtWidgets.QPushButton('Quit')
        self.label1 = QtWidgets.QLabel('User Input for Articles')
        self.label2 = QtWidgets.QLabel('No User Input')
        self.userInput = QtWidgets.QLineEdit()
        self.label1.setAlignment(QtCore.Qt.AlignCenter)

        # feature placement
        #label1.move(180,100)
        #button1.move(180,150)

        # container for features
        # horizontal
        inputBox = QtWidgets.QHBoxLayout()
        #h_box1 = QtWidgets.QHBoxLayout()
        h_box2 = QtWidgets.QHBoxLayout()

        inputBox.addWidget(self.userInput)

        #h_box1.addWidget(self.label1)
        #h_box1.addWidget(self.label2)

        h_box2.addWidget(self.button1)
        h_box2.addWidget(self.button2)
        h_box2.addWidget(self.button3)
        h_box2.addWidget(self.button4)
        h_box2.addWidget(self.button5)
        h_box2.addWidget(self.button6)

        # vertical
        v_box = QtWidgets.QVBoxLayout()
        #v_box.addLayout(h_box1)
        v_box.addWidget(self.label1)
        v_box.addLayout(inputBox)
        v_box.addLayout(h_box2)
        v_box.addWidget(self.label2)
        v_box.addWidget(self.exitButton)

        # mainWindow settings
        self.setLayout(v_box)
        self.setWindowTitle('Read FakeNooz')

        # connections for buttons
        #self.button1.clicked.connect(self.searchArticles)
        self.button1.clicked.connect(self.runCorpus)
        self.button2.clicked.connect(self.searchArticles)
        self.button3.clicked.connect(self.extractSentences)
        self.button4.clicked.connect(self.queryArticles)
        self.button5.clicked.connect(self.urlQuery)
        #self.button6.clicked.connect(self.setCategory)
        self.exitButton.clicked.connect(self.closeApp)

        self.show()

    def setQuery(self):
        # Find sitelist for category
        catSitelist = self.userInput.text() + ".txt"
        for sitelist in os.listdir("./Sitelists"):
            # If found, update category
            if catSitelist == sitelist:
                self.currentCategory = self.userInput.text()
                print("Category set to: " + self.userInput.text())
                break
        # If failed to find sitelist for category
        print("Failed to find sitelist for category: " + self.userInput.text())

    def urlQuery(self):
        print("Searching for related articles to: " + self.userInput.text())
        text = lag.GetArticleText(self.userInput.text())
        lag.SearchArticles(text, category=self.currentCategory)

    def queryArticles(self):
        print("Searching for: " + self.userInput.text() + "\nin category " + self.currentCategory)
        lag.SearchArticles(self.userInput.text(), category=currentCategory)

    def searchArticles(self):
        self.label2.setText('User has Inputted')
        sender = self.sender()
        if sender.text() == 'Search':
            print(self.userInput.text())
        if sender.text() == 'Clear':
            self.userInput.clear()

    def extractSentences(self):
    	#Run the grouping
    	lag.GroupArticles(category=self.currentCategory)

    def runCorpus(self):
        # run with sitelist
        sitelist = []
        #f = open("./" + self.currentCategory + "./Sitelists/" + self.currentCategory + ".txt", "r")
        f = open("./Sitelists/" + self.currentCategory + ".txt", "r")
        line=f.readline()
        while line is not "":
            sitelist.append(line[:-1])
            line=f.readline()
        f.close()
        UpdateCorpus(sitelist, category=self.currentCategory)
        #SentenceMatching()

    def closeApp(self):
        sys.exit()


app = QtWidgets.QApplication(sys.argv)
mainWindow = Window()
mainWindow.setGeometry(100,100,500,300)
sys.exit(app.exec_())
