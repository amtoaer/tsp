import math


class node:
    '''
    节点类
    '''

    def __init__(self, num: str, x: str, y: str):
        '''
        参数：
            num:编号
            x:横坐标
            y:纵坐标
        '''
        # 编号从0开始
        self.num = int(num)-1
        # 处理科学计数法
        self.x = int(x) if x.isdigit() else float(x)
        self.y = int(y) if y.isdigit() else float(y)
        # 边集，格式为[距离,终点]
        self.edges = []
        # 是否被访问
        self.isVisited = False


class base:
    '''
    算法基类
    '''

    def __init__(self, nodeList):
        '''
        参数：
            nodeList:io.getData(name)迭代器
        '''
        self.nodes = []
        for item in nodeList:
            self.nodes.append(node(item[0], item[1], item[2]))
        self.length = len(self.nodes)
        # 计算距离
        self.__getDistance()
        # 路径总距离初始化为0
        self.distance = 0

    def __getDistance(self):
        for i in range(self.length):
            for j in range(i):
                distance = math.sqrt(
                    pow(self.nodes[i].x-self.nodes[j].x, 2)+pow(self.nodes[i].y-self.nodes[j].y, 2))
                self.nodes[i].edges.append([distance, j])
                self.nodes[j].edges.append([distance, i])

    def printDistance(self):
        for item in self.nodes:
            print(item.num)
            print(item.edges)
