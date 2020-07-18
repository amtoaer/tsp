import math
import matplotlib.pyplot as plt


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


class window:
    '''
    图形界面类
    '''

    def __init__(self, title):
        self.fig = plt.figure(figsize=(10, 6), clear=True)
        self.fig.canvas.set_window_title(title)
        self.axes = self.fig.subplots(2, 2)
        # 隐藏坐标轴
        # for i in range(2):
        #    for j in range(2):
        #        self.axes[i, j].xaxis.set_visible(False)
        #        self.axes[i, j].yaxis.set_visible(False)

    def show(self):
        '''
        完成绘图
        '''
        # plt.tight_layout(pad=1.08)
        # plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()


class base:
    '''
    算法基类
    参数：
        nodeList:io.getData(name)迭代器
        questionName:问题名
    '''

    def __init__(self, nodeList, subplot):
        self.nodes = []
        # 添加点集
        for item in nodeList:
            self.nodes.append(node(item[0], item[1], item[2]))
        # 将子图设置为类内成员
        self.subplot = subplot
        # 描点
        self.drawDot()
        # len(self.nodes)*len(self.nodes)邻接矩阵
        self.edges = [[0]*len(self.nodes) for i in range(len(self.nodes))]
        # 计算距离
        self.__getDistance()
        # 路径总距离初始化为0
        self.distance = 0

    def __getDistance(self):
        for i in range(len(self.nodes)):
            for j in range(i):
                distance = math.sqrt(
                    pow(self.nodes[i].x-self.nodes[j].x, 2)+pow(self.nodes[i].y-self.nodes[j].y, 2))
                self.edges[i][j] = distance
                self.edges[j][i] = distance

    def drawDot(self):
        x = []
        y = []
        for node in self.nodes:
            x.append(node.x)
            y.append(node.y)
        self.subplot.scatter(x, y, color='b', s=0.5)

    def drawEdges(self, x: list, y: list):
        self.subplot.plot(x, y)

    def drawEdge(self, x1, y1, x2, y2):
        self.subplot.plot([x1, x2], [y1, y2])
