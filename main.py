from utils import io
from algo import nearest_neighbor


def main():
    test = nearest_neighbor.nearest_neighbor(io.getData('d198.tsp.gz'), 'd198')
    test.operate()


if __name__ == '__main__':
    main()
