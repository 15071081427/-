# 继承QT designer 的 bill类,扩展其功能，实现账单功能
#
# create by：zhuyiming 2024.3.3


from PyQt5 import QtCore, QtGui, QtWidgets
from UI.bill import Ui_Dialog
from functools import partial
from DataBase.BillDataBase import BillSqlalchemy

class billExtend(Ui_Dialog):
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        if self.tabWidget.currentIndex() == 0:
            self.tab_change(0)
        else:
            self.tab_change(1)
        self.initConnect(Dialog)
        #设置最小尺寸
        Dialog.setMinimumSize(800, 600)

    def tab_change(self, index):
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
        if index == 0:
            self.InitControl(expensesList, self.expenseTypeLayout)

        elif index == 1:
            self.InitControl(incomeList, self.incomeTypeLayout)  
        
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

    def ClearLayout(self, gridLayout):
        """ 清空布局内部的控件

        param gridLayout:布局对象
        """
        while gridLayout.count():
            child = gridLayout.takeAt(0)
            if child.widget():
                print('name is %s'%(child.widget().text()))
                child.widget().deleteLater()

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
        index =  self.tabWidget.currentIndex()
        print('index is %d, name is %s'%(index, name))
        if index == 0:
            self.label_expenseType.setText(name)
        elif index == 1:
            self.label_incomeType.setText(name)

    def on_click_select(self, dialog):
        """ 触发确认按钮

        param dialog:对话框对象
        """
        dialog.hide()

        