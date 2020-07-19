<h1 align="center">算法设计与分析课设</h1>

> 初版使用`tkinter`为每个问题的每个算法绘图。后听从老师建议，使用`matplotlib`重构了绘图模块，将同一问题的多个算法绘制在同一个窗口，便于对比分析。

## 仓库介绍

这是一份算法设计与分析课设的模板，目前实现了：

+ `tsplib`文件数据的读取
+ 节点类的初始化
+ 算法基类的初始化
+ 图像的绘制

## 使用截图

![image-20200719130312884](https://raw.githubusercontent.com/amtoaer/images/master/others/image-20200719130312884.png)

## 目录结构

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

## 实现原理

1. 读取`tsplib`文件数据

   首先使用`gzip.open(path,'r')`直接读取打包的`gz`文件，实现一个返回数据所有行的迭代器。

   不难发现，我们需要的数据都是以`序号 x坐标 y坐标`给出的，故考虑使用`str.split()`尝试对每行进行分割，如果分割长度为3且分割后的第一个数据为数字（过滤符合长度条件的文字分割）则为合法数据，以`list`结构返回。

2. 节点类的初始化

   得到文件数据后，需要将其写入到节点列表中，因此需要实现节点类，包括以下五种数据：

   + 编号
   + 横坐标
   + 纵坐标

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
   def __getDistance(self):
       for i in range(len(self.nodes)):
           for j in range(i):
               distance = math.sqrt(
                   pow(self.nodes[i].x-self.nodes[j].x, 2)+pow(self.nodes[i].y-self.nodes[j].y, 2))
               self.edges[i][j] = distance
               self.edges[j][i] = distance
   ```

   最后封装了部分绘图函数，用于给子视图进行绘图。

4. 图像的绘制

   使用`matplotlib`实现`window`类并拆分四个子视图。在主函数中调用时，将四个视图分别作为参数传递给四个算法，算法内部完成绘制，最后通过`window.show()`函数完成图像展示。

   ```python
   def main():
       files = listdir('lib')
       for file in files:
           window = base.window(file.split('.')[0])
           nearest_neighbor.nearest_neighbor(
               io.getData(file), window.axes[0, 0]).operate()
           greedy.greedy(io.getData(file), window.axes[0, 1]).operate()
           opt.opt(io.getData(file), window.axes[1, 0]).opt2()
           GA.GA(io.getData(file), window.axes[1, 1]).find_best_path()
           window.show()
   ```

   

## 注意事项（重要）

**虽然在模板中已经完成了大部分工作，使得用户可以直接进行算法的编写，但还是需要注意以下问题：**

+ 算法运行时间的统计

  算法运行时间通常通过算法运行前后的时间差得到，举例如下：

  ```python
  before = self.getTime()
  # 算法开始
  # ......
  # 算法结束
  self.time = self.getTime() - before
  ```

+ 需要手动调用的函数

  + `self.setText(title, time, distance)`

    其中`title`为子图名称，`time`为运行时间，`distance`为总距离，往往在算法最后调用。通常的调用方法为：

    ```python
    self.setText('算法名', self.time, self.distance)
    ```

  + `self.drawEdges(x: list, y: list, color: str)`或`self.drawEdge(x1, y1, x2, y2, color: str)`

    其中`drawEdges`用于连接连续多个点，举例：

    ```python
    # 使用红色线条依次连接(1,1)-(2,4)-(3,9)-(1,1)
    self.drawEdges([1,2,3,1],[1,4,9,1],'red')
    ```

    而`drawEdge`用于连接两个点，举例：

    ```python
    # 使用绿色线条连接(1,1)-(2,4)
    self.drawEdge(1,1,2,4,'green')
    ```

    通常情况下，只有完全按照行走路线求解的算法（如`nearest neighbor`）才能够使用`drawEdges()`，其他算法应使用`drawEdge()`。