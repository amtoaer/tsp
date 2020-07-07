import gzip
import os.path


def readFile(name):
    path = os.path.join('lib', name)
    if os.path.exists(path):
        with gzip.open(path, 'r') as file:
            for line in file:
                yield line.decode('utf-8')
    else:
        print('file does not exist')
        exit(1)
