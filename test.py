with open('Desktop/笔画路径信息.txt', 'r') as f:
    l = [line.strip('\r\n').split('\t') for line in f]

methods = []

for i in l:
    pathList = i[2].split('; ')
    for path in pathList:
        method = path.split(' ')[-1]
        if method not in methods:
            methods.append(method)

for i in methods:
    print(i)