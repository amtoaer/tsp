from utils import io, base
from algo import nearest_neighbor, greedy, opt, GA
from os import listdir


def main():
    files = listdir('lib')
    for file in files:
        window = base.window(file.split('.')[0])
        nearest_neighbor.nearest_neighbor(
            io.getData(file), window.axes[0, 0]).operate()
        window.show()


if __name__ == '__main__':
    main()
