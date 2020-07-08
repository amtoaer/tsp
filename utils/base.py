import math
from tkinter import *


class node:
    '''
    节点类
    参数：
        num:编号
        x:横坐标
        y:纵坐标
    '''

    def __init__(self, num: str, x: str, y: str):
        # 编号从0开始
        self.num = int(num)-1
        # 处理科学计数法
        self.x = int(x) if x.isdigit() else float(x)
        self.y = int(y) if y.isdigit() else float(y)
        # 边集，格式为[距离,终点]
        self.edges = []
        # 是否被访问
        self.isVisited = False


class window:
    '''
    图形界面类
    '''

    def __init__(self):
        self.root = Tk()
        self.scale = 0
        self.myCanvas = Canvas(self.root, width=1000, height=600, bg='white')
        self.question = Label(self.root, text='init')
        self.distance = Label(self.root, text='init')

    def getScale(self, width, height):
        '''
        获取比例尺
        参数:
            width:最大宽度
            height:最大高度
        '''
        self.scale = min(1000/width, 600/height)

    def drawDot(self, x, y):
        '''
        按照比例描点
        参数:
            x:点的横坐标
            y:点的纵坐标
        '''
        tmpX = x*self.scale
        tmpY = y*self.scale
        self.myCanvas.create_oval(tmpX, tmpY, tmpX+1, tmpY+1, fill='black')

    def drawEdge(self, x1, y1, x2, y2):
        '''
        按照比例画线连接点一和点二
        参数:
            x1,y1:点一坐标
            x2,y2:点二坐标
        '''
        tmpX1 = x1*self.scale
        tmpY1 = y1*self.scale
        tmpX2 = x2*self.scale
        tmpY2 = y2*self.scale
        self.myCanvas.create_line(tmpX1, tmpY1, tmpX2, tmpY2, fill='red')

    def setDistance(self, distance):
        '''
        将总距离显示在窗口中
        参数:
            distance:总距离
        '''
        self.distance = Label(self.root, text='distance:{}'.format(distance))

    def setQuestion(self, question):
        '''
        将问题名显示在窗口中
        参数:
            question:问题名
        '''
        self.question = Label(self.root, text="question:{}".format(question))

    def setTitle(self, title):
        '''
        设置窗口标题
        参数:
            title:窗口标题
        '''
        self.root.title(title)

    def show(self):
        '''
        完成绘图
        '''
        self.myCanvas.pack()
        self.question.pack()
        self.distance.pack()
        self.root.mainloop()


class base:
    '''
    算法基类
    参数：
        nodeList:io.getData(name)迭代器
        questionName:问题名
    '''

    def __init__(self, nodeList, questionName):
        self.nodes = []
        self.window = window()
        # 添加点集
        for item in nodeList:
            self.nodes.append(node(item[0], item[1], item[2]))
        maxX = 0
        maxY = 0
        # 得到最大的宽和高，用于确定比例尺
        for item in self.nodes:
            if item.x > maxX:
                maxX = item.x
            if item.y > maxY:
                maxY = item.y
        self.window.getScale(maxX, maxY)
        # 描点
        for item in self.nodes:
            self.window.drawDot(item.x, item.y)
        self.length = len(self.nodes)
        # 计算距离
        self.__getDistance()
        # 路径总距离初始化为0
        self.distance = 0
        # 设置问题名
        self.window.setQuestion(questionName)

    def __getDistance(self):
        for i in range(self.length):
            for j in range(i):
                distance = math.sqrt(
                    pow(self.nodes[i].x-self.nodes[j].x, 2)+pow(self.nodes[i].y-self.nodes[j].y, 2))
                self.nodes[i].edges.append([distance, j])
                self.nodes[j].edges.append([distance, i])
