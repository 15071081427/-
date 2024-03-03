# 程序主入口，用于启动程序
#
# create by：zhuyiming 2024.3.3


from PyQt5 import QtCore,QtWidgets,QtGui
from mainWindow import MainWindowExtend
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindowExtend()
    window = QtWidgets.QMainWindow()
    mainWindow.setupUi(window)
    window.show()
    sys.exit(app.exec_())

