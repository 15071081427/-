# 继承QT designer的mainWindow类,扩展其功能,实现主窗体
#
# create by：zhuyiming 2024.3.3

from PyQt5 import  QtWidgets
from timeAxis import timeAxis
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from UI.mainWindow import Ui_MainWindow
from bill import billExtend


class MainWindowExtend(Ui_MainWindow):

    def __init__(self):
        self.billDlg = QtWidgets.QDialog()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        fig, ax = timeAxis.init()
        canvas = FigureCanvas(fig)
        while self.timeAxisLayout.count():
            child = self.timeAxisLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()   
        self.timeAxisLayout.addWidget(canvas)

        self.CreateNewBill()
        self.CreateConnect()
        MainWindow.setMinimumSize(1024, 1024)

    def CreateConnect(self):
        """ 创建信道——槽连接
        """
        self.pushButton_account.clicked.connect(lambda:self.billDlg.show())
        


    def CreateNewBill(self):
        """ 在主窗体中构建bill类
        """
        bill = billExtend()   
        bill.setupUi(self.billDlg)