from utils import base
import random


class GA(base.base):
    # 对base基类进行继承
    def __init__(self, nodeList, subplot):
        # 调用父类初始化函数
        super().__init__(nodeList, subplot)
        # 种群数量
        self.POP_NUM = 30
        # 迭代次数
        self.GENERATE_TIME = 50
        # 交叉概率
        self.PC_MIN = 0.6
        self.PC_MAX_H = 0.9
        self.PC_MAX_M = 0.8
        self.PC_MAX_L = 0.7
        # 变异概率
        self.PM_MAX = 0.005
        self.PM_MIN_H = 0.003
        self.PM_MIN_M = 0.002
        self.PM_MIN_L = 0.001
        # 种群
        self.POPULATION = [
            [0 for i in range(self.length)] for j in range(self.POP_NUM)]

    # 返回编号为n节点的最近节点,visit为各节点的访问记录
    def get_nearest_neighbor(self, n, visit):
        nearest_dis = float("inf")
        for i in range(self.length):
            if i != n and visit[i] == 0:
                if self.edges[i][n] < nearest_dis:
                    nearest_p = i
                    nearest_dis = self.edges[i][n]
        return nearest_p

    # 最近邻算法,返回一条近似路径
    def nearest_neighbor_path(self):
        path = []
        # 随机初始化开始节点
        cur_point = random.randint(0, self.length - 1)
        path.append(cur_point)
        index = 1
        # 访问标记
        visit = [0 for m in range(self.length)]
        visit[cur_point] = 1
        while index < self.length:
            next_p = self.get_nearest_neighbor(cur_point, visit)
            path.append(next_p)
            cur_point = next_p
            visit[next_p] = 1
            index += 1
        return path

    # 比较交换前后距离，获得片段两旁节点与片段之间的前后距离
    def compare_dis(self, i, j, path):
        if i > 0 and j < len(path) - 1:
            dis1 = self.edges[path[i - 1]][path[i]
                   ] + self.edges[path[j]][path[j + 1]]
            dis2 = self.edges[path[i - 1]][path[j]
                   ] + self.edges[path[i]][path[j + 1]]
        elif i == 0 and j < len(path) - 1:
            dis1 = self.edges[path[0]][path[self.length-1]] + self.edges[path[j]][path[j + 1]]
            dis2 = self.edges[path[j]][path[self.length-1]] + self.edges[path[i]][path[j + 1]]
        elif j == len(path) - 1 and i > 0:
            dis1 = self.edges[path[i - 1]][path[i]] + self.edges[path[j]][path[0]]
            dis2 = self.edges[path[i - 1]][path[j]] + self.edges[path[i]][path[0]]
        else:
            dis1 = dis2 = 0
        return dis1, dis2

    # 采用2近似算法获得初始路径
    def opt2_path(self):
        #贪心初始化
        path = self.nearest_neighbor_path()
        count = 0
        max_count = 5000
        while count < max_count:
            a = random.randint(0, self.length - 1)
            b = random.randint(0, self.length - 1)
            while abs(a - b) < 1:
                b = random.randint(0, self.length - 1)
            if a > b:
                a, b = b, a
            dis1, dis2 = self.compare_dis(a, b, path)
            if dis2 >= dis1:
                count += 1
                continue
            else:
                count = 0
                piece = path[a:b + 1]
                piece.reverse()
                path[a:b + 1] = piece
        return path

    def find(self, x: int,root):
        r = x
        # 找到x的根节点
        while root[r] != r:
            r = root[r]
        i = x
        # 路径压缩
        while i != r:
            tmp = root[i]
            root[i] = r
            i = tmp
        return r

    def join(self, x: int, y: int,root):
        # 追溯到两个根节点
        root1 = self.find(x,root)
        root2 = self.find(y,root)
        # 令其中一个根节点归属于另一个
        root[root2] = root1

    #获得一条最短链接路径
    def short_connecting_path(self):
        best_edges=[]
        degrees = [0] * self.length
        # distanceList按距离从小到大存储所有边
        distanceList = []
        for i in range(self.length):
            for j in range(i):
                distanceList.append([self.edges[i][j], i, j])
        distanceList = sorted(distanceList, key=lambda x: x[0])
        root = [0] * self.length
        # 每个节点的根节点初始化为自己
        for index in range(self.length):
            root[index] = index
        count = 0
        for item in distanceList:
            # 跳出条件
            if count == self.length-1:
                break
            # 两点具有不同的根节点
            if self.find(item[1],root) != self.find(item[2],root):
                # 两点度均小于2
                if degrees[item[1]] < 2 and degrees[item[2]] < 2:
                    # 两点的度+=1
                    degrees[item[1]] += 1
                    degrees[item[2]] += 1
                    # 计数加一
                    count += 1
                    # 将两点的根节点设置为相同
                    self.join(item[1], item[2],root)
                    best_edges.append([item[1],item[2]])

        # 用于标记两个度为1的点
        flag1 = flag2 = -1
        for index in range(self.length):
            if degrees[index] == 1:
                # 度+=1
                degrees[index] += 1
                flag2 = flag1
                flag1 = index
                # 找到该两个点
                if flag1 != -1 and flag2 != -1:
                    break
        #将得到的边转换成路径
        path=[]
        path.append(flag1)
        cur_point = flag1
        visit = [0 ]*(self.length-1)
        while len(path) < self.length:
            for i in range(len(best_edges)):
                if visit[i]==0:
                    edge = best_edges[i]
                    if edge[0]==cur_point:
                        path.append(edge[1])
                        cur_point = edge[1]
                        visit[i] = 1
                        break
                    elif edge[1]==cur_point:
                        path.append(edge[0])
                        cur_point = edge[0]
                        visit[i] = 1
                        break
        return path

    # 初始化种群,贪心策略
    def init_pop(self):
        for i in range(self.POP_NUM):
            if i < 0.1*self.POP_NUM:
                 self.POPULATION[i] = self.short_connecting_path()
            # else:
            #     self.POPULATION[i] = self.nearest_neighbor_path()
            else:
                self.POPULATION[i] = self.opt2_path()

    # 得到路径path的距离
    def get_distance(self, path):
        dis = 0
        for i in range(len(path)):
            if i < len(path)-1:
                dis += self.edges[path[i]][path[i+1]]
            else:
                dis += self.edges[path[i]][path[0]]
        return dis

    # 得到当前种群中个体的适应度列表，最大适应度和平均适应度
    def get_fitness(self):
        fitness = [0 for i in range(self.POP_NUM)]
        sum = 0
        max_fitness = float("-inf")
        for i in range(self.POP_NUM):
            fitness[i] = 1/self.get_distance(self.POPULATION[i])
            sum += fitness[i]
            if fitness[i] > max_fitness:
                max_fitness = fitness[i]
        aver_fitness = sum/self.POP_NUM
        return fitness, max_fitness, aver_fitness

    # 计算当前种群中个体的选择概率，返回累计概率列表
    def calculate_selectp(self):
        fitness = [0 for i in range(self.POP_NUM)]
        q = [0 for i in range(self.POP_NUM)]
        sum = 0
        for i in range(self.POP_NUM):
            fitness[i] = 1/self.get_distance(self.POPULATION[i])
            sum += fitness[i]
        for i in range(self.POP_NUM):
            if i == 0:
                q[i] = fitness[i]/sum
            else:
                q[i] = q[i-1]+fitness[i]/sum
        return q

    # 选择函数
    def select(self):
        # 获取种群中的最优个体
        min_dis = self.get_distance(self.POPULATION[0])
        best = 0
        for i in range(1, self.POP_NUM):
            dis = self.get_distance(self.POPULATION[i])
            if dis < min_dis:
                best = i
                min_dis = dis
        ACE = self.POPULATION[best]
        select_population = [
            [0 for x in range(self.length)] for y in range(self.POP_NUM)]
        # 保留精英个体
        select_population[0] = ACE
        Q = self.calculate_selectp()
        for i in range(1, self.POP_NUM):
            # 随机产生0-1的数
            p = random.random()
            for j in range(len(Q)):
                if Q[j] >= p:
                    select_population[i] = self.POPULATION[j]
                    break
        self.POPULATION = select_population

    # 获取population种群中的最优个体及索引
    def get_best_individual(self, population):
        min_dis = float("inf")
        best_p = 0
        for i in range(len(population)):
            if self.get_distance(population[i]) < min_dis:
                min_dis = self.get_distance(population[i])
                best_individual = population[i]
                best_p = i
        return best_individual, best_p

    # 获取population种群中的最差个体及索引
    def get_worst_individual(self, population):
        max_dis = float("-inf")
        worst_p = 0
        for i in range(len(population)):
            if self.get_distance(population[i]) > max_dis:
                max_dis = self.get_distance(population[i])
                worst_individual = population[i]
                worst_p = i
        return worst_individual, worst_p

    # 杂交操作，g为当前迭代的次数
    def crossover(self, g):
        select_parents = []
        child_population = []
        fitness, max_fitness, aver_fitness = self.get_fitness()
        if g <= self.GENERATE_TIME/4:
            pc_max = self.PC_MAX_H
        elif g <= self.GENERATE_TIME*3/4:
            pc_max = self.PC_MAX_M
        else:
            pc_max = self.PC_MAX_L
        for i in range(self.POP_NUM):
            if fitness[i] < aver_fitness:
                pc = pc_max
            else:
                pc = pc_max-(pc_max-self.PC_MIN)*(g/(2*self.GENERATE_TIME) +
                                                  (fitness[i]-aver_fitness)/(2*(max_fitness-0.95*aver_fitness)))
            if random.random() < pc:
                select_parents.append(self.POPULATION[i])
            else:
                child_population.append(self.POPULATION[i])
        i = 0
        while i < len(select_parents):
            # 不足两位亲代则直接添加
            if i+1 == len(select_parents):
                child_population.append(select_parents[i])
            else:
                parent1 = select_parents[i]
                parent2 = select_parents[i+1]
                child1 = []
                child2 = []
                visit1 = [0 for x in range(self.length)]
                visit2 = [0 for x in range(self.length)]
                cur_city1 = random.randint(0, self.length-1)
                cur_city2 = random.randint(0, self.length - 1)
                child1.append(cur_city1)
                child2.append(cur_city2)
                visit1[cur_city1] = 1
                visit2[cur_city2] = 1
                while len(child1) < self.length:
                    pos1 = parent1.index(cur_city1)
                    pos2 = parent2.index(cur_city1)
                    if pos1 < self.length-1:
                        next_pos1 = pos1+1
                    else:
                        next_pos1 = 0
                    if pos2 < self.length-1:
                        next_pos2 = pos2+1
                    else:
                        next_pos2 = 0
                    if (visit1[parent1[next_pos1]] == 0 and visit1[parent2[next_pos2]] == 0 and (self.edges[cur_city1][parent1[next_pos1]] <= self.edges[cur_city1][parent2[next_pos2]])) or (visit1[parent1[next_pos1]] == 0 and visit1[parent2[next_pos2]] == 1):
                        child1.append(parent1[next_pos1])
                        visit1[parent1[next_pos1]] = 1
                        cur_city1 = parent1[next_pos1]
                    elif (visit1[parent1[next_pos1]] == 0 and visit1[parent2[next_pos2]] == 0 and (self.edges[cur_city1][parent1[next_pos1]] > self.edges[cur_city1][parent2[next_pos2]])) or (visit1[parent1[next_pos1]] == 1 and visit1[parent2[next_pos2]] == 0):
                        child1.append(parent2[next_pos2])
                        visit1[parent2[next_pos2]] = 1
                        cur_city1 = parent2[next_pos2]
                    else:
                        # 两个下一节点均被访问，则在当前节点找未被访问的最近的节点
                        next_city = self.get_nearest_neighbor(
                            cur_city1, visit1)
                        child1.append(next_city)
                        visit1[next_city] = 1
                        cur_city1 = next_city
                while len(child2) < self.length:
                    pos1 = parent1.index(cur_city2)
                    pos2 = parent2.index(cur_city2)
                    if pos1 > 0:
                        next2_pos1 = pos1-1
                    else:
                        next2_pos1 = len(parent1)-1
                    if pos2 > 0:
                        next2_pos2 = pos2-1
                    else:
                        next2_pos2 = len(parent2)-1
                    if (visit2[parent1[next2_pos1]] == 0 and visit2[parent2[next2_pos2]] == 0 and (self.edges[cur_city2][parent1[next2_pos1]] <= self.edges[cur_city2][parent2[next2_pos2]])) or (visit2[parent1[next2_pos1]] == 0 and visit2[parent2[next2_pos2]] == 1):
                        child2.append(parent1[next2_pos1])
                        visit2[parent1[next2_pos1]] = 1
                        cur_city2 = parent1[next2_pos1]
                    elif (visit2[parent1[next2_pos1]] == 0 and visit2[parent2[next2_pos2]] == 0 and (self.edges[cur_city2][parent1[next2_pos1]] > self.edges[cur_city2][parent2[next2_pos2]])) or (visit2[parent1[next2_pos1]] == 1 and visit2[parent2[next2_pos2]] == 0):
                        child2.append(parent2[next2_pos2])
                        visit2[parent2[next2_pos2]] = 1
                        cur_city2 = parent2[next2_pos2]
                    else:
                        # 两个上一个节点均被访问，则在当前节点找未被访问的最近的节点
                        next_city = self.get_nearest_neighbor(
                            cur_city2, visit2)
                        child2.append(next_city)
                        visit2[next_city] = 1
                        cur_city2 = next_city

                child_population.append(child1)
                child_population.append(child2)
            i += 2
        # 将子代种群中最差的更新为亲代种群中的最优个体
        best_individual, best_p = self.get_best_individual(self.POPULATION)
        worst_individual, worst_p = self.get_worst_individual(child_population)
        child_population[worst_p] = best_individual
        self.POPULATION = child_population

    # 突变,参数g为迭代次数
    def mutationover(self, g):
        if g <= self.GENERATE_TIME/4:
            pm_min = self.PM_MIN_L
        elif g <= self.GENERATE_TIME*3/4:
            pm_min = self.PM_MIN_M
        else:
            pm_min = self.PM_MIN_H
        fitness, max_fitness, aver_fitness = self.get_fitness()
        for i in range(len(self.POPULATION)):
            if fitness[i] < aver_fitness:
                pm = pm_min
            else:
                pm = pm_min + (self.PM_MAX-pm_min)*(g/(2*self.GENERATE_TIME) +
                                                    (fitness[i]-aver_fitness)/(2*(max_fitness-0.95*aver_fitness)))
            if random.random() < pm:
                j = random.randint(0, self.length-1)
                k = random.randint(0, self.length-1)
                while abs(j-k) < 1:
                    k = random.randint(0, self.length-1)
                if k < j:
                    j, k = k, j
                list_temp = self.POPULATION[i][j:k+1]
                list_temp.reverse()
                self.POPULATION[i][j:k + 1] = list_temp

    # 显示最优路径
    def show_beat_path(self, path):
        self.distance = self.get_distance(path)
        # print(self.distance)
        self.setText('GA', self.time, self.distance)
        for i in range(len(path)-1):
            node1 = self.nodes[path[i]]
            node2 = self.nodes[path[i+1]]
            self.drawEdge(node1.x, node1.y, node2.x, node2.y, 'red')
        if len(path) > 1:
            node1 = self.nodes[path[0]]
            node2 = self.nodes[path[len(path)-1]]
            self.drawEdge(node1.x, node1.y, node2.x, node2.y, 'red')

    # 找近似最优路径
    def find_best_path(self):
        before = self.getTime()
        self.init_pop()
        for i in range(self.GENERATE_TIME):
            self.select()
            self.crossover(i)
            self.mutationover(i)
        best_path, best_p = self.get_best_individual(self.POPULATION)
        self.time = self.getTime()-before
        # print(self.time)
        self.show_beat_path(best_path)
