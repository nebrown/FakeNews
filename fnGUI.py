import sys
from PyQt5 import (QtWidgets, QtCore)
from Update_Corpus import UpdateCorpus
from RelatedSentenceFinding import SentenceMatching

class Window(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.init_ui()

    def init_ui(self):
        # create features
        #self.button1 = QtWidgets.QPushButton('Search')
        self.button1 = QtWidgets.QPushButton('Collect Articles')
        self.button2 = QtWidgets.QPushButton('Clear')
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
        self.exitButton.clicked.connect(self.closeApp)

        self.show()

    def searchArticles(self):
        self.label2.setText('User has Inputted')
        sender = self.sender()
        if sender.text() == 'Search':
            print(self.userInput.text())
        if sender.text() == 'Clear':
            self.userInput.clear()

    def runCorpus(self):
        # run with sitelist
        sitelist = []
        f = open("./sitelist.txt", "r")
        line=f.readline()
        while line is not "":
            sitelist.append(line[:-1])
            line=f.readline()
        f.close()
        #UpdateCorpus(sitelist)
        SentenceMatching()

    def closeApp(self):
        sys.exit()


app = QtWidgets.QApplication(sys.argv)
mainWindow = Window()
mainWindow.setGeometry(100,100,500,300)
sys.exit(app.exec_())
