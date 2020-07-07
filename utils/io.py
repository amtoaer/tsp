import gzip
import os.path


def _readFile(name):
    '''
    一个用于返回tar.gz打包文件内容的迭代器
    参数：
        name:文件名
    返回：
        文件行迭代器
    '''
    path = os.path.join('lib', name)
    if os.path.exists(path):
        with gzip.open(path, 'r') as file:
            for line in file:
                yield line.decode('utf-8')
    else:
        print('file does not exist')
        exit(1)


def getData(name):
    '''
    用于得到节点编号和坐标信息的迭代器
    参数：
        name:文件名
    返回：
        [序号，x，y]迭代器
    '''
    for line in _readFile(name):
        tmp = line.split()
        if len(tmp) == 3 and tmp[0].isdigit():
            yield [tmp[0], tmp[1], tmp[2]]
