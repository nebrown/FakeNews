import sys
import os
from PyQt5 import (QtWidgets, QtCore)
from PyQt5.QtWidgets import qApp
from Update_Corpus import UpdateCorpus
from RelatedSentenceFinding import SentenceMatching
import LsiArticleGrouping as lag

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        #self.init_ui()
        self.currentCategory = "All"
        self.aboutText = "Fuck off"
        self.helpText = "To Use:\nFirst run collect articles to pull articles from "+\
                        "all sites listed in sitelist. After that, Aggregate will "+\
                        "apply NLP to cluster articles into topics and generates "+\
                        "summaries. Input a search term and press Search to have "+\
                        "the most related and most corroborated sentences returned."+\
                        "Input a URL and press URL Search for an article to get a list of related articles"

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
        catActionPol = QtWidgets.QAction('Politics', self)
        actions.append(catActionAll)
        actions.append(catActionPol)

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
        catActionAll.triggered.connect(lambda: self.SelectCat_trigger('All'))
        catActionPol.triggered.connect(lambda: self.SelectCat_trigger('US_Politics'))
        about_action.triggered.connect(self.About_trigger)

    # dummy functions
    def SelectCat_trigger(self, newCat):
        print(newCat)
        self.form_widget.changeCategory(newCat)
        self.currentCategory = newCat

    def About_trigger(self):
        QtWidgets.QMessageBox.about(self, "About", self.aboutText)

    def Help_trigger(self):
        QtWidgets.QMessageBox.about(self, "Help", self.helpText)        


class WindowContent(QtWidgets.QWidget):


    def __init__(self, curCat, parent=None):
        super().__init__(parent)
            #self.init_ui()
        self.currentCategory = curCat

    # create features
        #self.button1 = QtWidgets.QPushButton('Search')
        self.button1 = QtWidgets.QPushButton('Collect Articles')
        # self.button2 = QtWidgets.QPushButton('Clear')
        self.button3 = QtWidgets.QPushButton('Aggregate')
        self.button4 = QtWidgets.QPushButton('Search')
        self.button5 = QtWidgets.QPushButton('URL Search')
        # self.button6 = QtWidgets.QPushButton('Set Category')
        self.exitButton = QtWidgets.QPushButton('Quit')
        self.label1 = QtWidgets.QLabel('Currently looking in Category '+self.currentCategory)
        self.label2 = QtWidgets.QLabel('No User Input')
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

        # vertical
        v_box = QtWidgets.QVBoxLayout()
        #v_box.addLayout(h_box1)
        v_box.addWidget(self.button1)
        v_box.addWidget(self.label1)
        v_box.addLayout(urlInputBox)
        v_box.addLayout(queryInputBox)
        v_box.addLayout(h_box2)
        v_box.addWidget(self.label2)
        v_box.addWidget(self.exitButton)

        # mainWindow settings
        self.setLayout(v_box)
        self.setWindowTitle('Read FakeNooz')

        # connections for buttons
        #self.button1.clicked.connect(self.searchArticles)
        self.button1.clicked.connect(self.runCorpus)
        # self.button2.clicked.connect(self.searchArticles)
        self.button3.clicked.connect(self.extractSentences)
        self.button4.clicked.connect(self.queryArticles)
        self.button5.clicked.connect(self.urlQuery)
        # self.button6.clicked.connect(self.setCategory)
        self.exitButton.clicked.connect(self.closeApp)

        # self.show()

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

    def setCategory(self):
        # Find sitelist for category
        catSitelist = self.userInput.text() + ".txt"
        for sitelist in os.listdir("./Sitelists"):
            # If found, update category
            if catSitelist == sitelist:
                self.currentCategory = self.userInput.text()
                print("Category set to: " + self.userInput.text())
                return
        # If failed to find sitelist for category
        print("Failed to find sitelist for category: " + self.userInput.text())

    def urlQuery(self):
        print("Searching for related articles to: " + self.urlInput.text())
        text = lag.GetArticleText(self.urlInput.text())
        lag.SearchArticles(text, category=self.currentCategory)

    def queryArticles(self):
        print("Searching for: " + self.queryInput.text() + "\nin category " + self.currentCategory)
        lag.SearchArticles(self.queryInput.text(), category=self.currentCategory)

    def searchArticles(self):
        self.label2.setText('User has Inputted')
        sender = self.sender()
        if sender.text() == 'Search':
            print(self.userInput.text())
        if sender.text() == 'Clear':
            self.userInput.clear()

    def extractSentences(self):
        # make sure doc directory exists first
        if os.path.exists("./Data/"+self.currentCategory+"/Docs/"):
           #Run the grouping
           lag.GroupArticles(category=self.currentCategory)
        else:
            message = "Please run Colect Articles before Extracting Sentences"
            QtWidgets.QMessageBox.about(self, "Error", message)


    def runCorpus(self):
        # run with sitelist
        sitelist = []
        f = open("./Sitelists/" + self.currentCategory + ".txt", "r")
        line=f.readline()
        while line is not "":
            sitelist.append(line[:-1])
            line=f.readline()
        f.close()
        UpdateCorpus(sitelist, category=self.currentCategory)
        #SentenceMatching()

    def closeApp(self):
        # sys.exit()
        qApp.quit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setWindowTitle('Read FakeNooz')
    mainWindow.setGeometry(100,100,500,300)
    mainWindow.show()
    sys.exit(app.exec_())
