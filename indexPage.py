from PyQt5 import  QtWidgets,QtCore
from timeAxis import timeAxis
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from UI.indexPage import Ui_indexPage
from bill import billExtend
from datetime import datetime
from DataBase.BillDataBase import billDataBase

class IndexPageExtend(Ui_indexPage):

    def __init__(self):
        self.billDlg = QtWidgets.QDialog()   #对话框对象
        self.ax = None                       #画布对象
        self.billInfo = None                 #账单信息
        self.bill = None                     #账单窗体类   
        self.obj_left = None                 #编辑文本框
        self.obj_right = None                #删除文本框

    def setupUi(self, DockWidget):
        super().setupUi(DockWidget)
        # MainWindow.setMinimumSize(1024, 1024)

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
        self.pushButton_account.clicked.connect(lambda:self.on_accountClicked())
        
    def CreateNewBill(self):
        """ 在主窗体中构建bill类
        """
        self.bill = billExtend()  
        self.bill.hided.connect(lambda:self.refresh())
        # 对话框设置成模态
        self.billDlg.setWindowModality(QtCore.Qt.ApplicationModal)

        self.bill.setupUi(self.billDlg)   

    def refresh(self):
        ''' 刷新界面
        '''
        print('updata bill begin')
        self.billInfo = timeAxis.updateBill()

        timeAxis.drawTimeAxis(self.ax)

        self.canvas.draw()

        # 重置月份
        month = datetime.now().month
        monthInfo = billDataBase.queryMonth(month)

        total_income = 0.00
        total_expense = 0.00
        for item in monthInfo:
            if item.billType == 0:
                total_expense += item.money
            elif item.billType == 1:
                total_income += item.money
        self.label_income.setText("%d月收入 %.2f"%(month, total_income))
        self.label_expense.setText("%d月支出 %.2f"%(month, total_expense))
        print('updata bill end')

    def on_accountClicked(self):
        ''' 触发记账控件
        '''
        self.bill.Clear()
        self.billDlg.show()


    def on_canvas_click(self, event):
        ''' 点击画布事件

        param event:事件
        '''
        height = len(self.billInfo)*5+5
        width = 50
        change_rate = 5
        x = 0
        y = 0
        if event.inaxes  is not None:
            x, y = event.xdata, event.ydata
            print('x is %f, y is %f'%(x, y))
        left_x = 0
        left_y = 0
        right_x = 0
        if self.obj_left:
            left_x, _ = self.obj_left.get_position() 
        if self.obj_right: 
            right_x, _ = self.obj_right.get_position() 
        for item in self.billInfo:
            # print('width is %f, heigth is %f'%(width, height))  
            # 弹出编辑和删除 
            if x > width - 0.1 and x < width + 0.1 \
                and y > height - 2 and y < height + 2:
                self.obj_left, self.obj_right = timeAxis.drawSettings(self.ax, width, height 
                    , self.obj_left, self.obj_right)
                self.canvas.draw()       
            elif y > height-2 and y < height+2:
                print('id is %d'%item.id)
                # 触发删除按钮
                if x > left_x-0.1 and x < left_x+0.1:  
                    print('print billinfo %s'%self.billInfo)          
                    billDataBase.delete(item.id)
                    self.refresh()
                # 触发编辑按钮
                elif x > right_x-0.1 and x < right_x+0.1:
                    self.bill.setUpdateParam(item.id, item.totalType, item.billType, item.money)
                    self.billDlg.show()

            height = height - change_rate

        if event.inaxes  is not None:
            x, y = event.xdata, event.ydata
            print('x is %f, y is %f'%(x, y))
