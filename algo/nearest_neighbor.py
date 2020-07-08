from utils import base
import random


class nearest_neighbor(base.base):
    # 对base基类进行继承
    def __init__(self, nodeList, questionName):
        # 调用父类初始化函数
        super().__init__(nodeList, questionName)
        # 随机选择起点
        self.beginNum = random.randint(0, self.length-1)
        # 保存当前节点
        self.currentNode = self.nodes[self.beginNum]
        # 当前节点设为已访问
        self.currentNode.isVisited = True
        # 设置标题（算法名）
        self.window.setTitle('nearest_neighbor')

    def isEnd(self):
        result = True
        for item in self.nodes:
            if not item.isVisited:
                result = False
                break
        return result

    def operate(self):
        while not self.isEnd():
            # 得到最小距离与最小距离对应的终点
            minDistance = float('inf')
            end = -1
            for item in self.currentNode.edges:
                if not self.nodes[item[1]].isVisited:
                    if item[0] < minDistance:
                        minDistance = item[0]
                        end = item[1]
            # 总路径增加
            self.distance += minDistance
            # 绘制边
            self.window.drawEdge(
                self.currentNode.x, self.currentNode.y, self.nodes[end].x, self.nodes[end].y)
            # 当前点变更为最小距离的终点
            self.currentNode = self.nodes[end]
            self.currentNode.isVisited = True
        # 访问完全后回到起点,总距离需要加上回到起点的距离
        for item in self.currentNode.edges:
            if item[1] == self.beginNum:
                self.distance += item[0]
                break
        # 增加回到原点的边
        self.window.drawEdge(self.currentNode.x, self.currentNode.y,
                             self.nodes[self.beginNum].x, self.nodes[self.beginNum].y)
        # 图中显示分数
        self.window.setDistance(self.distance)
        # 绘图
        self.window.show()
