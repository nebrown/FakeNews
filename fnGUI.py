import sys
import os
from PyQt5 import (QtWidgets, QtCore)
from PyQt5.QtWidgets import qApp
from Update_Corpus import UpdateCorpus
# from RelatedSentenceFinding import SentenceMatching
import LsiArticleGrouping as lag
from  DBManager import DBManager

class TextViewWindow(QtWidgets.QMainWindow):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        self.text = text

        # centralize main widget contents
        # self.form_widget = TextViewContent(self.text)
        # self.setCentralWidget(self.form_widget)

        self.textLabel = QtWidgets.QLabel(text)
        self.textLabel.setWordWrap(True)
        self.scrollArea = QtWidgets.QScrollArea()

        self.scrollArea.setWidget(self.textLabel)
        self.setCentralWidget(self.scrollArea)

        # self.text = QtWidgets.QTextEdit(self)
        self.text = QtWidgets.QLabel(text)
        self.text.setMinimumSize(800, 800)
        self.text.setSizePolicy( QtWidgets.QSizePolicy.Expanding,  QtWidgets.QSizePolicy.Expanding)

        # Layout
        self.layout =  QtWidgets.QGridLayout()
        self.layout.addWidget(self.textLabel, 0, 0)
        self.layout.addWidget(self.text, 1, 0)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(5)

        self.setLayout(self.layout)   

        self.setMinimumSize(self.sizeHint())

# class TextViewContent(QtWidgets.QWidget):
#     def __init__(self, text, parent=None):
#         super().__init__(parent)
        # self.textShown = QtWidgets.QLabel()

        # self.scrollArea = QtWidgets.QScrollArea()

        # self.scrollArea.setWidget(self.textShown)
        # self.setCentralWidget(self.scrollArea)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        db = DBManager('corpus')

        #self.init_ui()
        self.currentCategory = "All"
        self.aboutText = "This software was developed by FakeNooz for CMPE 115 at UC Santa Cruz.\n"+\
                        "Authors:\n"+\
                        "Noah Brown\n"+\
                        "Benjamin Swanson\n"+\
                        "Naylan Adre\n"+\
                        "Jack Bauman\n"+\
                        "William"
        self.helpText = "To Use:\nFirst run collect articles to pull articles from "+\
                        "all sites listed in sitelist. After that, Aggregate will "+\
                        "apply NLP to cluster articles into topics and generates "+\
                        "summaries. Input a search term and press Search to have "+\
                        "the most related and most corroborated sentences returned."+\
                        "Input a URL and press URL Search for an article to get a list"+\
                        " of related articles.\nAny time after aggregating the summaries "+\
                        "and related articles of the 5 lsi topics can be viewed with the buttons"


        # centralize main widget contents
        self.form_widget = WindowContent(self.currentCategory)
        self.setCentralWidget(self.form_widget)

        # create menu bar and
        bar = self.menuBar()
        cat_T = bar.addMenu('Categories')
        help_T = bar.addMenu('Help')
        about_T = bar.addMenu('About')

        actions = []
        # for i in range(5):
        #     action = QtWidgets.QAction('{}'.format(i), self)
        #     actions.append(action)
        catActionAll = QtWidgets.QAction('All', self)
        catActionPol = QtWidgets.QAction('US Politics', self)
        catActionTech = QtWidgets.QAction('Technology', self)
        actions.append(catActionAll)
        actions.append(catActionPol)
        actions.append(catActionTech)

        # Cat_actionGroup = QtWidgets.QActionGroup(self)
        # Cat_actionGroup.addAction(QtWidgets.QAction('All', self))
        # Cat_actionGroup.addAction(QtWidgets.QAction('Politics', self))

        # create actions for tabs
        # Cat_action = QtWidgets.QAction('Action1', self)
        help_action = QtWidgets.QAction('Show Usage', self)
        about_action = QtWidgets.QAction('About the Team', self)

        # implement actions to tabs
        cat_T.addActions(actions)
        help_T.addAction(help_action)
        about_T.addAction(about_action)

        # add triggers to tabs
        # Cat_action.triggered.connect(self.TS_trigger)
        help_action.triggered.connect(self.Help_trigger)
        catActionAll.triggered.connect(lambda: self.SelectCat_trigger('All', db))
        catActionPol.triggered.connect(lambda: self.SelectCat_trigger('US_Politics', db))
        catActionTech.triggered.connect(lambda: self.SelectCat_trigger('Technology', db))
        about_action.triggered.connect(self.About_trigger)

        self.setStyleSheet(open("style.qss", "r").read())

    # dummy functions
    def SelectCat_trigger(self, newCat, db):
        print(newCat)
        self.form_widget.changeCategory(newCat)
        self.currentCategory = newCat
        db.createTable(newCat)

    def About_trigger(self):
        QtWidgets.QMessageBox.about(self, "About", self.aboutText)

    def Help_trigger(self):
        QtWidgets.QMessageBox.about(self, "Help", self.helpText)


class WindowContent(QtWidgets.QWidget):


    def __init__(self, curCat, parent=None):
        super().__init__(parent)
            #self.init_ui()
        self.currentCategory = curCat

        #database manager
        db = DBManager('corpus')
        # db.createTable()

    # create features
        #self.button1 = QtWidgets.QPushButton('Search')
        self.button1 = QtWidgets.QPushButton('Collect Articles')
        # self.button2 = QtWidgets.QPushButton('Clear')
        self.button3 = QtWidgets.QPushButton('Aggregate')
        self.button4 = QtWidgets.QPushButton('Search')
        self.button5 = QtWidgets.QPushButton('URL Search')
        # self.button6 = QtWidgets.QPushButton('Set Category')

        self.relatedArticlesButton0 = QtWidgets.QPushButton('Topic 0 Articles')
        self.relatedArticlesButton1 = QtWidgets.QPushButton('Topic 1 Articles')
        self.relatedArticlesButton2 = QtWidgets.QPushButton('Topic 2 Articles')
        self.relatedArticlesButton3 = QtWidgets.QPushButton('Topic 3 Articles')
        self.relatedArticlesButton4 = QtWidgets.QPushButton('Topic 4 Articles')
        self.summaryButton0 = QtWidgets.QPushButton('Topic 0 Summary')
        self.summaryButton1 = QtWidgets.QPushButton('Topic 1 Summary')
        self.summaryButton2 = QtWidgets.QPushButton('Topic 2 Summary')
        self.summaryButton3 = QtWidgets.QPushButton('Topic 3 Summary')
        self.summaryButton4 = QtWidgets.QPushButton('Topic 4 Summary')
        self.exitButton = QtWidgets.QPushButton('Quit')
        self.label1 = QtWidgets.QLabel('Currently looking in Category '+self.currentCategory)
        self.label2 = QtWidgets.QLabel('')
        self.urlInput = QtWidgets.QLineEdit()
        self.urlInput.setPlaceholderText('Article URL')
        self.queryInput = QtWidgets.QLineEdit()
        self.queryInput.setPlaceholderText('Search terms')

        self.label1.setText('Currently looking in Category '+self.currentCategory)

        self.label1.setAlignment(QtCore.Qt.AlignCenter)

        # feature placement
        #label1.move(180,100)
        #button1.move(180,150)

        # container for features
        # horizontal
        urlInputBox = QtWidgets.QHBoxLayout()
        queryInputBox = QtWidgets.QHBoxLayout()
        h_box2 = QtWidgets.QHBoxLayout()
        h_box3 = QtWidgets.QHBoxLayout()
        h_box4 = QtWidgets.QHBoxLayout()

        urlInputBox.addWidget(self.urlInput)
        urlInputBox.addWidget(self.button5)

        queryInputBox.addWidget(self.queryInput)
        queryInputBox.addWidget(self.button4)


        #h_box1.addWidget(self.label1)
        #h_box1.addWidget(self.label2)

        # h_box2.addWidget(self.button1)
        # h_box2.addWidget(self.button2)
        h_box2.addWidget(self.button3)
        #h_box2.addWidget(self.button4)
        #h_box2.addWidget(self.button5)
        # h_box2.addWidget(self.button6)

        h_box3.addWidget(self.relatedArticlesButton0)
        h_box3.addWidget(self.relatedArticlesButton1)
        h_box3.addWidget(self.relatedArticlesButton2)
        h_box3.addWidget(self.relatedArticlesButton3)
        h_box3.addWidget(self.relatedArticlesButton4)

        h_box4.addWidget(self.summaryButton0)
        h_box4.addWidget(self.summaryButton1)
        h_box4.addWidget(self.summaryButton2)
        h_box4.addWidget(self.summaryButton3)
        h_box4.addWidget(self.summaryButton4)


        # vertical
        v_box = QtWidgets.QVBoxLayout()
        #v_box.addLayout(h_box1)
        v_box.addWidget(self.button1)
        v_box.addWidget(self.label1)
        v_box.addLayout(urlInputBox)
        v_box.addLayout(queryInputBox)
        v_box.addLayout(h_box2)
        v_box.addLayout(h_box3)
        v_box.addLayout(h_box4)
        v_box.addWidget(self.label2)
        v_box.addWidget(self.exitButton)

        # mainWindow settings
        self.setLayout(v_box)
        self.setWindowTitle('Read FakeNooz')

        # connections for buttons
        #self.button1.clicked.connect(self.searchArticles)
        self.button1.clicked.connect(lambda: self.runCorpus(db))
        # self.button2.clicked.connect(self.searchArticles)
        self.button3.clicked.connect(lambda: self.extractSentences(db))
        self.button4.clicked.connect(lambda: self.queryArticles(db))
        self.button5.clicked.connect(self.urlQuery)
        # self.button6.clicked.connect(self.setCategory)
        self.exitButton.clicked.connect(self.closeApp)
        self.relatedArticlesButton0.clicked.connect(lambda: self.showArticles(0))
        self.relatedArticlesButton1.clicked.connect(lambda: self.showArticles(1))
        self.relatedArticlesButton2.clicked.connect(lambda: self.showArticles(2))
        self.relatedArticlesButton3.clicked.connect(lambda: self.showArticles(3))
        self.relatedArticlesButton4.clicked.connect(lambda: self.showArticles(4))
        self.summaryButton0.clicked.connect(lambda: self.showSummary(0))
        self.summaryButton1.clicked.connect(lambda: self.showSummary(1))
        self.summaryButton2.clicked.connect(lambda: self.showSummary(2))
        self.summaryButton3.clicked.connect(lambda: self.showSummary(3))
        self.summaryButton4.clicked.connect(lambda: self.showSummary(4))

        # self.show()

    def showArticles(self, num):
        # output
        out = "Failed"
        try:
            with open('./Data/'+self.currentCategory+'/Aggregates/f' + str(num) + '.txt') as file:
                out = file.read()
        except FileNotFoundError:
            return
        self.outWindow = TextViewWindow(out)
        self.outWindow.show()

    def showSummary(self, num):
        # output
        out = "Failed"
        try:
            with open('./Data/'+self.currentCategory+'/Aggregates/s' + str(num) + '.txt') as file:
                out = file.read()
        except FileNotFoundError:
            return
        self.outWindow = TextViewWindow(out)
        self.outWindow.show()


    def changeCategory(self, newCat):
        # Find sitelist for category
        catSitelist = newCat + ".txt"
        for sitelist in os.listdir("./Sitelists"):
            # If found, update category
            if catSitelist == sitelist:
                self.currentCategory = newCat
                self.label1.setText('Currently looking in Category '+self.currentCategory)
                self.label1.update()
                print("Category set to: " + newCat)
                return
        # If failed to find sitelist for category
        print("Failed to find sitelist for category: " + newCat)

    def setCategory(self, db):
        # Find sitelist for category
        catSitelist = self.userInput.text() + ".txt"
        for sitelist in os.listdir("./Sitelists"):
            # If found, update category
            if catSitelist == sitelist:
                self.currentCategory = self.userInput.text()
                db.createTable(self.currentCategory)
                print("Category set to: " + self.userInput.text())
                return
        # If failed to find sitelist for category
        print("Failed to find sitelist for category: " + self.userInput.text())

    def urlQuery(self):
        print("Searching for related articles to: " + self.urlInput.text())
        text = lag.GetArticleText(self.urlInput.text())
        lag.SearchArticles(text, category=self.currentCategory)
        out = "Failed"
        with open('./Data/'+self.currentCategory+'/Queries/f0.txt') as file:
            out = file.read()
        self.outWindow = TextViewWindow(out)
        self.outWindow.show()

    def queryArticles(self, db):
        print("Searching for: " + self.queryInput.text() + "\nin category " + self.currentCategory)
        lag.SearchArticles(db, self.queryInput.text(), category=self.currentCategory)
        # output
        out = "Failed"
        with open('./Data/'+self.currentCategory+'/Queries/s0.txt') as file:
            out = file.read()
        self.outWindow = TextViewWindow(out)
        self.outWindow.show()

    def searchArticles(self):
        self.label2.setText('User has Inputted')
        sender = self.sender()
        if sender.text() == 'Search':
            print(self.userInput.text())
        if sender.text() == 'Clear':
            self.userInput.clear()

    def extractSentences(self, db):
        # make sure doc directory exists first
        if os.path.exists("./Data/"+self.currentCategory+"/Docs/"):
           #Run the grouping
           lag.GroupArticles(db, category=self.currentCategory)
        else:
            message = "Please run Colect Articles before Extracting Sentences"
            QtWidgets.QMessageBox.about(self, "Error", message)


    def runCorpus(self, db):

        # run with sitelist
        sitelist = []
        f = open("./Sitelists/" + self.currentCategory + ".txt", "r")
        line=f.readline()
        while line is not "":
            sitelist.append(line[:-1])
            line=f.readline()
        f.close()
        UpdateCorpus(db, sitelist, category=self.currentCategory)
        #SentenceMatching()

    def closeApp(self):
        # sys.exit()
        qApp.quit()

if __name__ == '__main__':

    #database manager
    db = DBManager('corpus')
    db.createTable('All')

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setWindowTitle('Read FakeNooz')
    mainWindow.setGeometry(100,100,500,300)
    mainWindow.show()
    sys.exit(app.exec_())
