import pandas as pd

path = './IC00.xls'
code = path[2:-4]
file = pd.read_excel(path)


if __name__ == '__main__':
    print(code)
    print(file)
