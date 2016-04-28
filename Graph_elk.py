#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'


import matplotlib.pyplot as plt

from matplotlib import style
import os


class graphserver(object):

    def __init__(self,graphdata):

        self.graphdata = graphdata

    def graph_Save(self,filename):
        style.use('ggplot')  #设置绘图背景色
        fig,ax=plt.subplots(figsize=(8, 6))
        x = self.graphdata[1]   #x轴数据
        ax.plot(x)
        xticklabels = self.graphdata[0]   #y轴数据
        ax.set_xticklabels(xticklabels)

        plt.xlabel("Error")            #x轴标注
        plt.ylabel("Error count")      #y轴标注
        newtitle="Error %s Logs count" %(filename)
        plt.title(newtitle)   #绘图标题
        filename = filename + '.png'
        savepath=os.path.join('./graph_images',filename)
        #plt.show()
        plt.savefig(savepath)


if __name__ == '__main__':

    c = graphserver([['2012','2015','2016','2017','2018','2019','2020'],[234,245,2345,2345,23,4242,1234]])

    c.graph_Save('aaaa')