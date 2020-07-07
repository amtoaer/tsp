<h1 align="center">算法设计与分析课设</h1>

## 介绍

这是一份算法设计与分析课设的模板，目前实现了：

+ `tsplib`文件数据的读取
+ 节点类的初始化
+ 算法基类的初始化

## 结构

```python
.
├── algo # 算法文件夹
│   ├── __init__.py # 包标记
│   └── nearest_neighbor.py # 示例算法
├── lib # tsplib文件夹
│   └── *.tsp.gz # 需要操作的tsplib数据集
├── main.py # 主程序
├── README.md # 说明文档
└── utils # 工具库
    ├── __init__.py # 包标记
    ├── base.py # 节点类和算法基类
    └── io.py # 读取tsplib数据集
```

## 详情

1. 读取`tsplib`文件数据

   首先使用`gzip.open(path,'r')`直接读取打包的`gz`文件，实现一个返回数据所有行的迭代器。

   不难发现，我们需要的数据都是以`序号 x坐标 y坐标`给出的，故考虑使用`str.split()`尝试对每行进行分割，如果分割长度为3且分割后的第一个数据为数字（过滤符合长度条件的文字分割）则为合法数据，以`list`结构返回。

2. 节点类的初始化

   得到文件数据后，需要将其写入到节点列表中，因此需要实现节点类，包括以下五种数据：

   + 编号
   + 横坐标
   + 纵坐标
   + 边集合
   + 访问标记

   其中需要注意的是坐标的读取，因为有少数几组`tsplib`数据的坐标是以科学计数法形式给出的，所以该处需要单独处理。

   查阅资料得知科学计数法的字符串可以通过`float(str)`转换为浮点数，故实现如下：

   ```python
   self.x = int(x) if x.isdigit() else float(x)
   self.y = int(y) if y.isdigit() else float(y)
   ```

3. 算法基类的初始化

   考虑将算法中读取`tsplib`数据的部分分离，作为算法基类，主要需要实现点集的添加和距离的计算。

   算法基类中需要包括若干点，实现方式是遍历上文提到的返回`list`结构的迭代器，批量初始化`node`类并插入到`nodes`中：

   ```python
   # 其中nodeList为迭代器
   self.nodes = []
   for item in nodeList:
       self.nodes.append(node(item[0], item[1], item[2]))
   ```

   接着使用距离公式求任意两点间的距离：

   > 注意：这里使用普通的距离公式是因为需要求解的数据集的边权重类型均为`EUC_2D`（即2D欧式距离），如果有其他类型则不能使用该公式求解，具体统计见[该次提交](https://github.com/amtoaer/tsp/tree/f1e0a53a1e4e03d12048fac798cb5dc7e8a0cd1d)：
   >
   > ![image-20200707232942086](https://allwens-work.oss-cn-beijing.aliyuncs.com/bed/image-20200707232942086.png)

   ```python
   def getDistance(self):
       self.length = len(self.nodes)
       for i in range(self.length):
           for j in range(i):
               distance = math.sqrt(
                   pow(self.nodes[i].x-self.nodes[j].x, 2)+pow(self.nodes[i].y-self.nodes[j].y, 2))
               self.nodes[i].edges.append([distance, j])
               self.nodes[j].edges.append([distance, i])
   ```

   

