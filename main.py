from utils import io
from algo import nearest_neighbor, greedy
from os import listdir


def main():
    files = listdir('lib')
    for file in files:
        nearest_neighbor.nearest_neighbor(
            io.getData(file), file.split('.')[0]).operate()
        greedy.greedy(io.getData(file), file.split('.')[0]).operate()


if __name__ == '__main__':
    main()
