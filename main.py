from utils import utils


def main():
    for line in utils.readFile('a280.tsp'):
        print(line, end='')


if __name__ == '__main__':
    main()
