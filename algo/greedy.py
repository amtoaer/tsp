from utils import base


class greedy(base.base):
    def __init__(self, nodeList, subplot):
        super().__init__(nodeList, subplot)
        self.degrees = [0]*self.length
        self.distanceList = []
        for i in range(self.length):
            for j in range(i):
                self.distanceList.append([self.edges[i][j], i, j])
        # distanceList按距离从小到大存储所有边
        self.distanceList = sorted(self.distanceList, key=lambda x: x[0])
        self.root = [0]*self.length
        # 每个节点的根节点初始化为自己
        for index in range(self.length):
            self.root[index] = index
        self.setTitle('greedy')

    def find(self, x: int):
        r = x
        # 找到x的根节点
        while self.root[r] != r:
            r = self.root[r]
        i = x
        # 路径压缩
        while i != r:
            tmp = self.root[i]
            self.root[i] = r
            i = tmp
        return r

    def join(self, x: int, y: int):
        # 追溯到两个根节点
        root1 = self.find(x)
        root2 = self.find(y)
        # 令其中一个根节点归属于另一个
        self.root[root2] = root1

    def operate(self):
        flag = []
        for item in self.distanceList:
            # 跳出条件
            if len(flag) == self.length-1:
                break
            # 两点具有不同的根节点
            if self.find(item[1]) != self.find(item[2]):
                # 两点度均小于2
                if self.degrees[item[1]] < 2 and self.degrees[item[2]] < 2:
                    # 两点的度+=1
                    self.degrees[item[1]] += 1
                    self.degrees[item[2]] += 1
                    # 总距离增加
                    self.distance += item[0]
                    # 将两点的根节点设置为相同
                    self.join(item[1], item[2])
                    # 画边
                    self.drawEdge(
                        self.nodes[item[1]].x, self.nodes[item[1]].y, self.nodes[item[2]].x, self.nodes[item[2]].y)
        # 用于标记两个度为1的点
        flag1 = flag2 = -1
        for index in range(self.length):
            if self.degrees[index] == 1:
                # 度+=1
                self.degrees[index] += 1
                flag2 = flag1
                flag1 = index
                # 找到该两个点
                if flag1 != -1 and flag2 != -1:
                    break
        # 将该两点相连
        self.drawEdge(
            self.nodes[flag1].x, self.nodes[flag1].y, self.nodes[flag2].x, self.nodes[flag2].y)
        # 总距离加上该段距离
        self.distance += self.edges[flag1][flag2]
