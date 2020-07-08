from utils import io
from algo import nearest_neighbor
from os import listdir


def main():
    files = listdir('lib')
    for file in files:
        test = nearest_neighbor.nearest_neighbor(
            io.getData(file), file.split('.')[0])
        test.operate()


if __name__ == '__main__':
    main()
