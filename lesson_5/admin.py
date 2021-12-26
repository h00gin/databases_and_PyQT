import sys
from PyQt5 import QtWidgets
import py_form
import os

os.environ['QT_DEBUG_PLUGINS'] = '1'
os.environ['QT_PLUGIN_PATH'] = \
    "C:\\Users\\Анна\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages\\PyQt5\\Qt5\\plugins"


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = py_form.Ui_Administration()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(QtWidgets.QPushButton.clicked)
        self.ui.pushButton_2.clicked.connect(QtWidgets.QPushButton.clicked)
        self.ui.pushButton_3.clicked.connect(QtWidgets.QPushButton.clicked)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
