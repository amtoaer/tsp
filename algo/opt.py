from utils import base
import random


class opt(base.base):
    # 对base基类进行继承
    def __init__(self, nodeList, questionName):
        # 调用父类初始化函数
        super().__init__(nodeList, questionName)
        # 设置算法停止参数
        self.max_count = 5000
        # 最优路径
        self.path = []
        self.init_path_nearest()


    # 初始化种群,最近邻贪心策略
    def init_path_nearest(self):
        # 随机初始化开始节点
        cur_point = random.randint(0, self.length-1)
        self.path.append(cur_point)
        index = 1
        # 访问标记
        visit = [0 for m in range(self.length)]
        visit[cur_point] = 1
        while index < self.length:
            next_p = self.get_nearest_neighbor(cur_point, visit)
            self.path.append(next_p)
            cur_point = next_p
            visit[next_p] = 1
            index += 1

    # 返回编号为n节点的最近节点,visit为各节点的访问记录
    def get_nearest_neighbor(self, n, visit):
        nearest_dis = float("inf")
        for i in range(self.length):
            if i != n and visit[i] == 0:
                if self.edges[i][n] < nearest_dis:
                    nearest_p = i
                    nearest_dis = self.edges[i][n]
        return nearest_p

    def update_beat_path(self):  # 更新最优路径
        count = 0
        while count < self.max_count:
            a = random.randint(0, self.length - 1)
            b = random.randint(0, self.length - 1)
            while abs(a - b) < 1:
                b = random.randint(0, self.length - 1)
            if a > b:
                a, b = b, a
            dis1, dis2 = self.compare_dis(a, b)
            if dis2 >= dis1:
                count += 1
                continue
            else:
                count = 0
                piece = self.path[a:b + 1]
                piece.reverse()
                self.path[a:b + 1] = piece

    def compare_dis(self, i, j):  # 比较交换前后距离，由于只有与片段两旁节点与片段之间的距离会发生变化，故简单处理
        if i > 0 and j < len(self.path) - 1:
            dis1 = self.edges[self.path[i - 1]][self.path[i]
                                                ] + self.edges[self.path[j]][self.path[j + 1]]
            dis2 = self.edges[self.path[i - 1]][self.path[j]
                                                ] + self.edges[self.path[i]][self.path[j + 1]]
        elif i == 0 and j < len(self.path) - 1:
            dis1 = self.edges[self.path[j]][self.path[j + 1]]
            dis2 = self.edges[self.path[i]][self.path[j + 1]]
        elif j == len(self.path) - 1 and i > 0:
            dis1 = self.edges[self.path[i-1]][self.path[i]]
            dis2 = self.edges[self.path[i-1]][self.path[j]]
        else:
            dis1 = dis2 = 0
        return dis1, dis2

    def get_distance(self, path):  # 获得路径距离
        dis = 0
        n = len(path)-1
        for i in range(n):
            dis += self.edges[path[i]][path[i+1]]
        if len(path) >= 2:
            dis += self.edges[path[0]][path[n]]
        return dis

    def opt2(self):  # 2-opt求最优路径
        before = self.getTime()
        self.update_beat_path()
        self.time = self.getTime()-before
        # print(self.time)
        self.distance = self.get_distance(self.path)
        # print(self.distance)
        # print("最优路径:", self.path)
        for i in range(len(self.path)-1):
            node1 = self.nodes[self.path[i]]
            node2 = self.nodes[self.path[i+1]]
            self.drawEdge(node1.x, node1.y, node2.x, node2.y, 'orange')
        if len(self.path) > 2:
            node1 = self.nodes[self.path[0]]
            node2 = self.nodes[self.path[len(self.path)-1]]
            self.drawEdge(node1.x, node1.y, node2.x, node2.y, 'orange')
        self.setText('2-opt', self.time, self.distance)
