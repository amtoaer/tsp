from utils import base
import random


class nearest_neighbor(base.base):
    # 对base基类进行继承
    def __init__(self, nodeList, subplot):
        # 调用父类初始化函数
        super().__init__(nodeList, subplot)
        # 随机选择起点
        self.beginNum = random.randint(0, len(self.nodes)-1)
        # 保存当前节点
        self.currentNode = self.nodes[self.beginNum]
        # 保存当前编号
        self.currentNum = self.beginNum

    def operate(self):
        isVisited = [False]*len(self.nodes)
        x = []
        y = []
        x.append(self.currentNode.x)
        y.append(self.currentNode.y)
        while not len(x) == len(self.nodes)+1:
            # 得到最小距离与最小距离对应的终点
            minDistance = float('inf')
            end = -1
            for index in range(len(self.nodes)):
                if self.edges[self.currentNum][index] < minDistance and not isVisited[index]:
                    minDistance = self.edges[self.currentNum][index]
                    end = index
            # 总路径增加
            self.distance += minDistance
            # 当前点变更为最小距离的终点
            self.currentNode = self.nodes[end]
            # 当前编号变为最小距离终点的编号
            self.currentNum = end
            # 加入边
            x.append(self.currentNode.x)
            y.append(self.currentNode.y)
            # 标记当前点已经访问
            isVisited[self.currentNum] = True
        # 访问完全后回到起点,总距离需要加上回到起点的距离
        self.distance += self.edges[self.currentNum][self.beginNum]
        # 增加回到原点的边
        x.append(self.nodes[self.beginNum].x)
        y.append(self.nodes[self.beginNum].y)
        self.drawEdges(x, y)
