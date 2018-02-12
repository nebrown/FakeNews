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
    #label1.move(180,100)
    #button1.move(180,150)

    # container for labels
    # horizontal
    h_box = QtWidgets.QHBoxLayout()
    h_box.addStretch()
    h_box.addWidget(label1)
    h_box.addStretch()

    # vertical
    v_box = QtWidgets.QVBoxLayout()
    v_box.addWidget(button1)
    v_box.addLayout(h_box)

    # mainWindow settings
    mainWindow.setLayout(v_box)
    mainWindow.setWindowTitle('Read FakeNooz')
    mainWindow.show()
    sys.exit(app.exec_())
    
window()
