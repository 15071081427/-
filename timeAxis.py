# TimeAxis类,用于绘制时间轴
#
# create by：zhuyiming 2024.3.3

import matplotlib.pyplot as plt


class TimeAxis(object):
    data = []

    def init(self):
        """ 初始化时间轴布局

        return:画布及画布中的对象
        """
        fig, ax = plt.subplots(sharey=True, figsize=(7,4))
        y = [5,10,15,20,25,30,35,40]
        x = [4,4,4,4,4,4,4,4]
        ax.plot(x,y,'', linewidth = 3, color = 'k'
                , marker='.', markersize=12)
        plt.axis('off')
        return fig, ax

    def drawTimeAxis(self, ax):
        """ 绘制时间轴

        :param ax:画布中的对象
        """
        left_prop = 0.4
        right_prop = 0.6
        change_rate = 1/len(self.data)*1.0
        height = 0.9
        for item in self.data:
            if self.data.oritation == 'left':
                plt.text(left_prop, height, self.data.value, fontsize=15, horizontalalignment='center'
                         , verticalalignment='center',transform=ax.transAxes, color='red')
            elif self.data.oritation == 'right':
                plt.text(right_prop, height, self.data.value, fontsize=15, horizontalalignment='center'
                         , verticalalignment='center',transform=ax.transAxes, color='green')
            height = height-change_rate


timeAxis = TimeAxis()       