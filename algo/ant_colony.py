from utils import base
import random
import copy

# 参数
'''
ALPHA:信息启发因子，值越大，则蚂蚁选择之前走过的路径可能性就越大
      ，值越小，则蚁群搜索范围就会减少，容易陷入局部最优
BETA:Beta值越大，蚁群越就容易选择局部较短路径，这时算法收敛速度会
     加快，但是随机性不高，容易得到局部的相对最优
'''
(ALPHA, BETA, RHO, Q) = (1.0, 2.0, 0.5, 100.0)
# 蚂蚁数量
ant_num = 50
# 城市数量、城市距离和信息素(全局变量)
city_num = 0
distance_graph = 0
pheromone_graph = 0


class Ant(object):
    # 蚂蚁类

    # 初始化
    def __init__(self, ID):

        self.ID = ID                 # ID
        self.__clean_data()          # 随机初始化出生点

    # 初始数据
    def __clean_data(self):

        self.path = []               # 当前蚂蚁的路径
        self.total_distance = 0.0    # 当前路径的总距离
        self.move_count = 0          # 移动次数
        self.current_city = -1       # 当前停留的城市
        self.open_table_city = [True for _ in range(city_num)]  # 探索城市的状态

        city_index = random.randint(0, city_num-1)  # 随机初始出生点
        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1

    # 选择下一个城市
    def __choice_next_city(self):

        next_city = -1
        select_citys_prob = [0.0 for _ in range(city_num)]  # 存储去下个城市的概率
        total_prob = 0.0

        # 获取去下一个城市的概率
        for i in range(city_num):
            if self.open_table_city[i]:
                try:
                    # 计算概率：与信息素浓度成正比，与距离成反比
                    select_citys_prob[i] = pow(pheromone_graph[self.current_city][i], ALPHA) * pow(
                        (1.0/distance_graph[self.current_city][i]), BETA)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError as e:
                    print('Ant ID: {ID}, current city: {current}, target city: {target}'.format(
                        ID=self.ID, current=self.current_city, target=i))

        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(city_num):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break
        if (next_city == -1):
            next_city = random.randint(0, city_num - 1)
            while ((self.open_table_city[next_city]) == False):
                next_city = random.randint(0, city_num - 1)

        return next_city

    # 计算路径总距离
    def __cal_total_distance(self):
        temp_distance = 0.0
        for i in range(1, city_num):
            start, end = self.path[i], self.path[i-1]
            temp_distance += distance_graph[start][end]

        # 回路
        end = self.path[0]
        temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance

    # 移动操作
    def __move(self, next_city):
        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1

    # 搜索路径
    def search_path(self):
        # 初始化数据
        self.__clean_data()

        # 搜素路径，遍历完所有城市为止
        while self.move_count < city_num:
            # 移动到下一个城市
            next_city = self.__choice_next_city()
            self.__move(next_city)

        # 计算路径总长度
        self.__cal_total_distance()


class ant_colony(base.base):
    def __init__(self, nodeList, subplot):
        # 为这三个全局变量赋值，便于在蚂蚁类中使用
        global city_num
        global distance_graph
        global pheromone_graph
        super().__init__(nodeList, subplot)
        # 城市距离
        distance_graph = self.edges
        # 城市数量
        city_num = self.length
        # 初始化信息素
        pheromone_graph = [[1.0]*self.length for _ in range(self.length)]
        # 迭代次数
        self.iter = 30
        # 初始化ant_num只蚂蚁
        self.ants = [Ant(ID) for ID in range(ant_num)]
        # 初始最优解
        self.best_ant = Ant(-1)
        # 初始化最好结果为无限大
        self.best_ant.total_distance = float('inf')

    def search_path(self):
        count = 0
        before = self.getTime()
        # 如果没有达到迭代次数
        while count < self.iter:
            # 遍历每一只蚂蚁
            for ant in self.ants:
                # 搜索一条路径
                ant.search_path()
                # 与当前最优蚂蚁比较
                if ant.total_distance < self.best_ant.total_distance:
                    # 更新最优解
                    self.best_ant = copy.deepcopy(ant)
            # 更新信息素
            self.__update_pheromone_gragh()
            count += 1
        # 迭代完成，得到结果
        self.time = self.getTime()-before
        self.distance = self.best_ant.total_distance
        # x,y用于记录走过的坐标
        x = []
        y = []
        for item in self.best_ant.path:
            x.append(self.nodes[item].x)
            y.append(self.nodes[item].y)
        # 最后回到原地
        x.append(self.nodes[self.best_ant.path[0]].x)
        y.append(self.nodes[self.best_ant.path[0]].y)
        self.drawEdges(x, y, 'purple')
        self.setText('ant colony', self.time, self.distance)

    def __update_pheromone_gragh(self):
        # 获取每只蚂蚁在其路径上留下的信息素
        temp_pheromone = [[0.0 for col in range(
            city_num)] for raw in range(city_num)]
        for ant in self.ants:
            for i in range(1, city_num):
                start, end = ant.path[i-1], ant.path[i]
                # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]

        # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * \
                    RHO + temp_pheromone[i][j]
