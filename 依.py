import yaml

with open('GB.txt', 'r') as f:
    GB = [line.strip('\r\n') for line in f]

ZI = yaml.load(open('字.yaml'), Loader=yaml.BaseLoader)
WEN_ = yaml.load(open('文.raw.yaml'), Loader=yaml.BaseLoader)
MING = yaml.load(open('文.alias.yaml'), Loader=yaml.BaseLoader)

used = {}

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
    res = list(filter(lambda x: ord(x[0]) > 128, res))
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
            if x in ZI: 
                lnew.append(ZI[x])
                used[x] = 1
            else: lnew.append(x)
        l = flat_and_filter(lnew)
    return l

require = []

for number, char in enumerate(GB):
    if char not in ZI:
        require.append(char)
    else:
        used[char] = 1
        for component in dependencies(char):
            require.append(component)

print('未使用部件：', list(x for x in ZI if x not in used))
print('非法部件：')

require = sorted(set(require), key=lambda x: len(x)*100000 + ord(x[0]) + ord(x[-1])/100000)

with open('文.yaml', 'w') as f:
    f.write('# 汉字自动拆分系统「文」数据库\n# 本文件是「依.py」为嵌套表自动生成的依赖，无需手动编辑。\n')
    for component in require:
        if len(component) == 1:
            try:
                strokeList = WEN_[component]
            except KeyError:
                print(component)
                strokeList = []
        else:
            strokeList = []
            try:
                sourceChar, strokeIndexList = MING[component]
                sourceStrokeList = WEN_[sourceChar]
                for index in strokeIndexList:
                    strokeList.append(sourceStrokeList[int(index)])
            except Exception:
                print(component)
        f.write('%s: \n' % component)
        for i in strokeList:
            f.write('  - %s\n' % str(i).replace("'", ''))