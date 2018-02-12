import sys
from PyQt5 import QtWidgets


def window():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QWidget()
    mainWindow.setGeometry(100,100,500,300)


    # create features
    button1 = QtWidgets.QPushButton(mainWindow)
    label1 = QtWidgets.QLabel(mainWindow)

    # text for features
    button1.setText('Search')
    label1.setText('User Input for Articles')

    # feature placement
    label1.move(180,100)
    button1.move(180,150)

    mainWindow.setWindowTitle('Read FakeNooz')
    mainWindow.show()
    sys.exit(app.exec_())
    
window()
