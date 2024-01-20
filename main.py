from PyQt5 import QtCore,QtWidgets,QtGui
from UI.mainWindow import Ui_MainWindow
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    window = QtWidgets.QMainWindow()
    ui.setupUi(window)
    window .show()
    sys.exit(app.exec_())

