from utils import base
import random

class opt(base.base):
    # 对base基类进行继承
    def __init__(self, nodeList, questionName):
        # 调用父类初始化函数
        super().__init__(nodeList, questionName)
        # 设置标题（算法名）
        self.window.setTitle('2-opt')
        #设置算法停止参数
        self.max_count=1000
        #随机选择一条路作为初始路径
        self.path = [i for i in range(self.length)]
        random.shuffle(self.path)

    def update_beat_path(self): #更新最优路径
        count=0
        while count < self.max_count:
            repath = self.path.copy()
            a=random.randint(0,self.length-1)
            b = random.randint(0, self.length - 1)
            while abs(a-b)<1:
                b = random.randint(0, self.length - 1)
            if a>b:
                dis1,dis2=self.compare_dis(b,a)
                repath[b:a+1]=self.trversePath(repath[b:a+1])
            else:
                dis1,dis2=self.compare_dis(a,b)
                repath[a:b+1]=self.trversePath(repath[a:b+1])
            if dis2 >= dis1:
                count += 1
                continue
            else:
                count = 0
                self.path=repath


    def compare_dis(self,i,j):  #比较交换前后距离，由于只有与片段两旁节点与片段之间的距离会发生变化，故简单处理
        if i > 0 and j < len(self.path) - 1:
            dis1 =  self.edges[self.path[i - 1]][self.path[i]] + self.edges[self.path[j]][self.path[j + 1]]
            dis2 =  self.edges[self.path[i - 1]][self.path[j]] + self.edges[self.path[i]][self.path[j + 1]]
        elif i==0 and j < len(self.path) - 1:
            dis1 = self.edges[self.path[j]][self.path[j + 1]]
            dis2 = self.edges[self.path[i]][self.path[j + 1]]
        elif j==len(self.path) - 1 and i >0:
            dis1 = self.edges[self.path[i-1]][self.path[i]]
            dis2 = self.edges[self.path[i-1]][self.path[j]]
        else:
            dis1=dis2=0
        return dis1,dis2


    def get_distance(self,path):  #获得路径距离
        dis=0
        n=len(path)-1
        for i in range(n):
            dis += self.edges[path[i]][path[i+1]]
        if len(path)>=2:
            dis += self.edges[path[0]][path[n]]
        return dis

    def trversePath(self,path):  #列表反向排列
        n=len(path)
        t=n//2
        for i in range(t):
            temp=path[i]
            path[i]=path[n-1-i]
            path[n-1-i]=temp
        return path

    def opt2(self):    #2-opt求最优路径
        self.update_beat_path()
        print("最优路径:",self.path)
        self.window.setDistance(self.get_distance(self.path))
        for i in range(len(self.path)-1):
            node1 = self.nodes[self.path[i]]
            node2 = self.nodes[self.path[i+1]]
            self.window.drawEdge(node1.x,node1.y,node2.x,node2.y)
        if len(self.path)>2:
            node1 = self.nodes[self.path[0]]
            node2 = self.nodes[self.path[len(self.path)-1]]
            self.window.drawEdge(node1.x,node1.y,node2.x,node2.y)
        self.window.show()