# 继承QT designer 的 bill类,扩展其功能，实现账单功能
#
# create by：zhuyiming 2024.3.3


from PyQt5 import QtCore, QtWidgets
from UI.bill import Ui_Dialog
from functools import partial
from DataBase.BillDataBase import *
from datetime import datetime

class billExtend(Ui_Dialog, QtWidgets.QWidget):
    
    hided = QtCore.pyqtSignal()

    id = 0
    totalType = None
    billType = 0
    money = None
    dataType = 0   #0表示新增，1表示编辑

    def setUpdateParam(self, _id, _totalType, _billType, _money):
        ''' 更新时更新参数

        param id:数据id
        param totalType:总数据类型
        param billType:表单类型
        param money:金额
        
        '''
        self.totalType = _totalType
        self.id = _id
        self.billType = _billType
        self.money = _money
        self.dataType = 1
        self.tabWidget.setCurrentIndex(self.billType)
        if self.billType == 0:
            self.label_expenseType.setText(self.totalType)
            self.lineEdit_expenseVal.setText('%.2f'%self.money)
        elif self.billType == 1:
            self.label_incomeType.setText(self.totalType)
            self.lineEdit_incomeVal.setText('%.2f'%self.money)
        

    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        self.tab_change()
        self.initConnect(Dialog)
        #设置最小尺寸
        Dialog.setMinimumSize(800, 600)

        
    def InitControl(self, list, Layout):
        """ 初始化控件
        
        param list:默认list列表
        param Layout:当前布局对象
        """
        row = 0
        col = 0
        for items in list:
            for item in items:     
                print('itme is %s, row is %d, cols is %d'%(item, row, col))
                button = QtWidgets.QPushButton(item)
                Layout.addWidget(button, row, col)
                button.clicked.connect(partial(self.on_click_gridLayout, item))
                col = col +1
            row = row + 1
            col = 0

    def Clear(self):
        """ 清空数据

        param gridLayout:布局对象
        """
        self.lineEdit_incomeVal.setText('0.00')
        self.lineEdit_expenseVal.setText('0.00')

        self.label_expenseType.setText('其他')
        self.label_incomeType.setText('其他')

        self.tabWidget.setCurrentIndex(1)

    def initConnect(self, Dialog):
        """ 初始化连接

        param  Dialog:对话框对象
        """ 
        self.tabWidget.currentChanged.connect(self.tab_change)
        #确认触发事件
        self.pushButton_confirm.clicked.connect(lambda:self.on_click_select(Dialog))

    def on_click_gridLayout(self, name):
        """ 触发网格布局内控件

        param name:当前账单名称
        """
        self.billType =  self.tabWidget.currentIndex()
        self.totalType = name
        print('index is %d, name is %s'%(self.billType, name))
        if self.billType == 0:
            self.label_expenseType.setText(name)
        elif self.billType == 1:
            self.label_incomeType.setText(name)

    def on_click_select(self, dialog):
        """ 触发确认按钮

        param dialog:对话框对象
        """
        currentDate = datetime.now()
        if self.billType == 0:
           self.money = float(self.lineEdit_expenseVal.text())
           self.totalType = self.label_expenseType.text()
        elif self.billType == 1:
            self.money = float(self.lineEdit_incomeVal.text())
            self.totalType = self.label_incomeType.text()
        if self.dataType == 0:
            billDataBase.insert(currentDate.year, currentDate. month
                , currentDate.day, self.billType, self.totalType, self.money) 
        elif self.dataType == 1:
            print('id is %d, money is %f'%(self.id, self.money))
            billDataBase.update(self.id, self.money, self.totalType)
        dialog.hide() 
        self.hided.emit()

    def tab_change(self):
        """ 切换tab页触发事件

        param index:当前tab页索引
        """
        expensesList = [['餐饮','交通','购物','居住','娱乐'],
                      ['医疗','教育','人情','其他','零食'],
                      ['烟酒饮料','水果','水电煤','话费网费','日用品'],
                      ['护肤美容']]
        incomeList = [['工资','收红包','生活费','奖金','报销'],
                      ['兼职','借入款','投资收益','其他收入','生意收入'],
                      ['退款','提成','利息']]
        print('tab change')
        # if index == 0:
        self.InitControl(expensesList, self.expenseTypeLayout)

        # elif index == 1:
        self.InitControl(incomeList, self.incomeTypeLayout)  


        
        