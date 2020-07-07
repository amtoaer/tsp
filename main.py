from utils import utils
import os
import re


def main():
    files = os.listdir('lib')
    length = len(files)
    count = dict()
    toMatch = 'EDGE_WEIGHT_TYPE[ ]{0,1}:(.+)$'
    for file in files:
        for line in utils.readFile(file):
            result = re.match(toMatch, line)
            if result != None:
                weight_type = result.groups()[0]
                if weight_type in count.keys():
                    count[weight_type] += 1
                else:
                    count[weight_type] = 1
    print('总共有{}个文件'.format(length))
    print('距离类型如下：')
    print(count)


if __name__ == '__main__':
    main()
