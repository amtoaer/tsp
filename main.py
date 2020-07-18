from utils import io, base
from algo import nearest_neighbor, greedy, opt, GA
from os import listdir


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


if __name__ == '__main__':
    main()
