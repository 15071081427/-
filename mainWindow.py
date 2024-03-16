# 继承QT designer的mainWindow类,扩展其功能,实现主窗体
#
# create by：zhuyiming 2024.3.3

from PyQt5 import  QtWidgets,QtCore
from UI.mainWindow import Ui_MainWindow
from indexPage import IndexPageExtend


class MainWindowExtend(Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()

    def setupUi(self, MainWindow):
        dockWidget = QtWidgets.QFrame()
        indexPage = IndexPageExtend()
        indexPage.setupUi(dockWidget)
        super().setupUi(MainWindow)

        self.homePageLayout.addWidget(dockWidget)
        MainWindow.setMinimumSize(1024, 1024)
