import sys
from PyQt5 import (QtWidgets, QtCore)

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, parent=None):
		super().__init__(parent)

		# centralize main widget contents
		self.form_widget = WindowContent()
		self.setCentralWidget(self.form_widget)

		# create menu bar and tabs
		bar = self.menuBar()
		TopSt_T = bar.addMenu('Top Stories')
		UsPol_T = bar.addMenu('US Politics')
		IntNews_T = bar.addMenu('International News')
		Search_T = bar.addMenu('Search')


		# create actions for tabs
		TS_action = QtWidgets.QAction('Action1', self)
		UP_action = QtWidgets.QAction('Action2', self)
		IN_action = QtWidgets.QAction('Action3', self)
		Search_action = QtWidgets.QAction('Action4', self)

		# implement actions to tabs
		TopSt_T.addAction(TS_action)
		UsPol_T.addAction(UP_action)
		IntNews_T.addAction(IN_action)
		Search_T.addAction(Search_action)

		# add triggers to tabs
		#TS_action.triggered.connect(self.TS_trigger)


class WindowContent(QtWidgets.QWidget):

	def __init__(self, parent=None):

		super().__init__(parent)

    	# create features
		self.button1 = QtWidgets.QPushButton('Search')
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
		self.button1.clicked.connect(self.searchArticles)
		self.button2.clicked.connect(self.searchArticles)
		self.exitButton.clicked.connect(self.closeApp)

	def searchArticles(self):
		self.label2.setText('User has Inputted')
		sender = self.sender()
		if sender.text() == 'Search':
			print(self.userInput.text())
		if sender.text() == 'Clear':
			self.userInput.clear()

	def closeApp(self):
		sys.exit()

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.show()
	sys.exit(app.exec_())
