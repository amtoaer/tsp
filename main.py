from utils import io, base
from algo import nearest_neighbor, greedy, opt, GA, ant_colony
from os import listdir, path
from shutil import copyfile
from xlutils.copy import copy
from xlrd import open_workbook


def main():
    # 将原始文件拷贝一份作为结果
    copyfile(path.join('result', 'base.xls'),
             path.join('result', 'result.xls'))
    # 打开结果文件并用于写入
    rb = open_workbook(path.join('result', 'result.xls'))
    wb = copy(rb)
    # 获取表0
    ws = wb.get_sheet(0)
    # 需要写入的行
    row = 1
    # 列出lib目录下的数据集合
    files = listdir('lib')
    # 把文件名按照字典序排序
    files.sort()
    # 需要写入的数据
    data = []
    for file in files:
        window = base.window(file.split('.')[0])
        nn = nearest_neighbor.nearest_neighbor(
            io.getData(file), window.plot1)
        nn.operate()
        data += nn.getResult()
        gr = greedy.greedy(io.getData(file), window.plot2)
        gr.operate()
        data += gr.getResult()
        op = opt.opt(io.getData(file), window.plot3)
        op.opt2()
        data += op.getResult()
        ga = GA.GA(io.getData(file), window.plot4)
        ga.find_best_path()
        data += ga.getResult()
        an = ant_colony.ant_colony(io.getData(file), window.plot5)
        an.search_path()
        data += an.getResult()
        # 填excel表
        col = 2
        for index in range(len(data)):
            if index % 2:
                ws.write(row, col+4, data[index])
                col += 1
            else:
                ws.write(row, col, data[index])
        row += 1
        data.clear()
        window.show()
    # 保存excel文件
    wb.save(path.join('result', 'result.xls'))


if __name__ == '__main__':
    main()
