# 继承QT designer的mainWindow类,扩展其功能,实现主窗体
#
# create by：zhuyiming 2024.3.3

from PyQt5 import  QtWidgets,QtCore
from timeAxis import timeAxis
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
from UI.mainWindow import Ui_MainWindow
from bill import billExtend
from datetime import datetime
from DataBase.BillDataBase import billDataBase


class MainWindowExtend(Ui_MainWindow):

    def __init__(self):
        self.billDlg = QtWidgets.QDialog()
        self.ax = None
        self.billInfo = None
        self.bill = None
        self.obj_left = None
        self.obj_right = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        MainWindow.setMinimumSize(1024, 1024)
        # 重置月份
        month = datetime.now().month
        self.label_income.setText("%d月收入"%month)
        self.label_expense.setText("%d月支出"%month)

        # 绘制图表
        fig, self.ax = timeAxis.initControl()
        self.canvas = FigureCanvas(fig)
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        while self.timeAxisLayout.count():
            child = self.timeAxisLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()   
        self.timeAxisLayout.addWidget(self.canvas)

        self.refresh()

        self.CreateNewBill()
        self.CreateConnect()

    def CreateConnect(self):
        """ 创建信道——槽连接
        """
        self.pushButton_account.clicked.connect(lambda:self.billDlg.show())
        
    def CreateNewBill(self):
        """ 在主窗体中构建bill类
        """
        self.bill = billExtend()  
        self.bill.hided.connect(lambda:self.refresh())
        # 对话框设置成模态
        self.billDlg.setWindowModality(QtCore.Qt.ApplicationModal)

        self.bill.setupUi(self.billDlg)   

    def refresh(self):
        print('updata bill begin')
        self.billInfo = timeAxis.updateBill()

        timeAxis.drawTimeAxis(self.ax)

        self.canvas.draw()
        print('updata bill end')


    def on_canvas_click(self, event):
        height = len(self.billInfo)*5+5
        width = 50
        change_rate = 5
        if event.inaxes  is not None:
            x, y = event.xdata, event.ydata
            print('x is %f, y is %f'%(x, y))
        for item in self.billInfo:
            print('width is %f, heigth is %f'%(width, height))  
            # 弹出编辑和删除 
            if x > width - 0.1 and x < width + 0.1 \
                and y > height - 2 and y < height + 2:
                self.obj_left, self.obj_right = timeAxis.drawSettings(self.ax, width, height 
                    , self.obj_left, self.obj_right)
                self.canvas.draw()
                # self.bill.setUpdateParam(item.id, item.totalType, item.billType, item.money)
                # self.billDlg.show()
            height = height - change_rate

        if event.inaxes  is not None:
            x, y = event.xdata, event.ydata
            print('x is %f, y is %f'%(x, y))

