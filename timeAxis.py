# TimeAxis类,用于绘制时间轴
#
# create by：zhuyiming 2024.3.3

import matplotlib.pyplot as plt
from datetime import datetime
from DataBase.BillDataBase import billDataBase


class TimeAxis(object):

    def __init__(self):
        self.billInfo = None
        #设置默认x轴值为50
        self.width = 50
        #设置时间轴之间间隔为5
        self.change_rate = 5
        self.height = 0
        
    def initControl(self):
        """ 初始化时间轴布局

        return:画布及画布中的对象
        """
        fig, ax = plt.subplots(sharey=True, figsize=(1,2))
        #设置字体，避免中文乱码
        plt.rcParams['font.sans-serif']=['SimHei']
        return fig, ax

    def drawTimeAxis(self, ax):
        """ 绘制时间轴

        :param ax:画布中的对象
        """

        ax.cla()
        detaX = []
        detaY = []
        interval = 5
        for i in range(len(self.billInfo)):
            interval = interval+self.change_rate
            detaX.append(50)
            detaY.append(interval)
        ax.plot(detaX,detaY,'', linewidth =1, color = 'k'
                , marker='o', markersize=25)
        plt.axis('off')
        left_prop = self.width - 1
        right_prop = self.width + 1

        self.height = interval
        height = interval
        for item in self.billInfo: 
            print('totalType %s, height %f type is %d'%(item.totalType, height, item.billType)) 
            show_content = '%s %.2f'%(item.totalType, item.money)
            if item.billType == 1:   
                plt.text(left_prop, height, show_content, fontsize=15, horizontalalignment='center'
                          , verticalalignment='center', transform=ax.transData, color='red')
                # plt.text(left_prop, height, show_content, fontsize=15, horizontalalignment='center'
                #          , verticalalignment='center',transform=ax.transAxes, color='red')
            elif item.billType == 0: 
                # plt.text(right_prop, height, show_content, fontsize=15, horizontalalignment='center'
                #          , verticalalignment='center',transform=ax.transAxes, color='green')
                 plt.text(right_prop, height, show_content, fontsize=15, horizontalalignment='center'
                          , verticalalignment='center', transform=ax.transData, color='green')
            height = height-self.change_rate

    def drawSettings(self, ax, detaX, detaY, obj_left, obj_right):
        ''' 绘制删除和编辑

        param ax: 画布对象
        param detaX: x轴偏移
        param detaY: y轴偏移
        obj_left: 左侧文本框对象
        obj_right: 右侧文本框对象
        '''
        if obj_left:
            obj_left.remove()
        if obj_right:
            obj_right.remove()
        obj_left = plt.text(detaX-3, detaY, "删除", fontsize=15, horizontalalignment='center'
                          , verticalalignment='center', transform=ax.transData, color='red')
        obj_right = plt.text(detaX+3, detaY, "编辑", fontsize=15, horizontalalignment='center'
                          , verticalalignment='center', transform=ax.transData, color='green')
        return obj_left, obj_right


    def updateBill(self):
        """ 更新账单信息

        :return 数据库信息
        """
        year = datetime.now().year
        self.billInfo = billDataBase.queryYear(year) 
        print('bill info is %s'%self.billInfo)
        return self.billInfo

timeAxis = TimeAxis()       