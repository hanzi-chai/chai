import yaml

with open('GB.txt', 'r') as f:
    GB = [line.strip('\r\n') for line in f]

ZI = yaml.load(open('字.yaml'), Loader=yaml.BaseLoader)

def flat_and_filter(l):
    """
    输入：列表
    输出：将所有嵌套列表展开，并删去结构操作符
    """
    res = []
    for i in l:
        if isinstance(i, list):
            res.extend(flat_and_filter(i))
        else:
            res.append(i)
    res = list(filter(lambda x: x not in 'hzwmsepqjlcnuo', res))
    return res

def dependencies(char):
    """
    输入：字
    输出：计算一个字所依赖的所有其他字
    """
    l = flat_and_filter(ZI[char])
    while any(x in ZI for x in l):
        lnew = []
        for x in l:
            if x in ZI: lnew.append(ZI[x])
            else: lnew.append(x)
        l = flat_and_filter(lnew)
    return l

require = []

for number, char in enumerate(GB):
    if char not in ZI:
        require.append(char)
    else:
        for component in dependencies(char):
            require.append(component)

require = sorted(set(require), key=lambda x: len(x)*100000 + ord(x[0]))

with open('文~.yaml', 'w') as f:
    for component in require:
        f.write('%s: \n' % component)