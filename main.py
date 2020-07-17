from utils import io
from algo import nearest_neighbor, greedy, opt, GA
from os import listdir



def main():
    files = listdir('lib')
    for file in files:
        nearest_neighbor.nearest_neighbor(
            io.getData(file), file.split('.')[0]).operate()
        greedy.greedy(io.getData(file), file.split('.')[0]).operate()
        opt.opt(io.getData(file), file.split('.')[0]).opt2()
        GA.GA(io.getData(file), file.split('.')[0]).find_best_path()



if __name__ == '__main__':
    main()
