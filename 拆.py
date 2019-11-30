import yaml
import time

time1 = 0
time2 = 0
complexity = {n: [] for n in range(1, 12)}

class Stroke:
    """
    笔画对象：
      - 类别（31 种）
      - 控制点列表（2 个至 6 个）
    注：类别和控制点详见 https://github.com/lanluoxiao/Chai/wiki/1-%E3%80%8C%E6%96%87%E3%80%8D%E6%95%B0%E6%8D%AE%E5%BA%93%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83）。
    """
    def __init__(self, object):
        self.type = object[0]
        controlList = []
        for point in object[1:]:
            controlList.append((int(point[0]), int(point[1])))
        self.controlList = controlList
    
    def __str__(self):
        return str(self.type) + ':' + str(self.controlList) + ' '

class Char:
    """
    汉字对象：
      - 名称
      - 笔画列表，每个元素是一个 Stroke 对象
    """
    def __init__(self, name, strokeList):
        self.name = name
        self.strokeList = strokeList
    
    def getLen(self):
        """
        输出：字的笔画数
        """
        return len(self.strokeList)
    
    def degenerate(self):
        """
        输出：退化后的字
        """
        return ' '.join([stroke.type for stroke in self.strokeList])

    def getPowerDict(self):
        """
        输出：字的所有非空切片
        """
        global time1
        start = time.time()
        n = self.getLen()
        # 生成掩码，二进制分别为 1，10，100……
        mask = [1<<(n-i-1) for i in range(n)]
        powerDict = {}
        for k in range(1, 2**n):
            sliceStrokeList = []
            # 数 k 与某个掩码按位与后，如果不为 0，那么说明某一位为 1
            # 此时添加这一位对应的笔画
            for idx, item in enumerate(mask):
                if k & item: sliceStrokeList.append(self.strokeList[idx])
            if k & (k-1): # k 不是 2 的幂，说明切片不是单笔画，寻找对应的字根
                deg = Char('', sliceStrokeList).degenerate()
                powerDict[k] = DEGENERACY.get(deg)
            else: # 切片是单笔画，根据「单笔画无毛」假设，无需寻找字根
                stroke = sliceStrokeList[0]
                powerDict[k] = Char(stroke.type, [Stroke([stroke.type])])
        end = time.time()
        time1 = time1 + end - start
        return powerDict

    def decompose(self):
        """
        输出：在给定字根集下，所有可能的拆分
        """
        global time2
        powerDict = self.getPowerDict()
        start = time.time()
        l = self.getLen()
        z = 2**l
        # 建立一个字典记录拆分状态，若已拆完则为真，否则为假
        uncompletedList = [(z - 1, )]
        completedList = []
        # 将拆分列表进行迭代，每次选取未拆完的一个对象，将最后一个组件拆分一次
        while uncompletedList:
            newUncompletedList = []
            for scheme in uncompletedList:
                residue = scheme[-1]
                rootList = filter(lambda x: powerDict[x], nextRoot(residue))
                for root in rootList:
                    if root != residue: # 没拆完
                        newUncompletedList.append(scheme[:-1] + (root, residue - root))
                    else: # 新拆出的字根和原有剩余一样大，说明已拆完
                        completedList.append(scheme)
            uncompletedList = newUncompletedList
        complexity[self.getLen()].append(len(completedList))
        # 开始择优
        schemeList = completedList
        # 根少优先
        minLen = min(len(x) for x in schemeList)
        schemeList = list(filter(lambda x: len(x) == minLen, schemeList))
        # 笔顺优先
        bestBishun = min(sum((bishun(n, z, l) for n in scheme), tuple()) for scheme in schemeList)
        schemeList = list(filter(lambda x: sum((bishun(n, z, l) for n in x), tuple()) == bestBishun, schemeList))
        # 取大优先
        bestScheme = max(schemeList, key=quda)
        end = time.time()
        time2 = time2 + end - start
        return tuple(powerDict[x] for x in bestScheme)
    
    def __str__(self):
        return self.name + '{\n\t' + '\n\t'.join(str(stroke) for stroke in self.strokeList) + '\n\t}'

def nextRoot(n):
    """
    输入：一个数
    输出：在数的二进制表示中所有「1」的位上取 1 或取 0 得到的所有可能的数
    意义：给定字未拆完的部分，求拆出下一个字根的所有可能性
    """
    powerList = [0]
    while n:
        m = n - (n & (n-1))
        n = n & (n-1)
        powerList = powerList + [x + m for x in powerList]
    return powerList[len(powerList)//2:]

def strokeNum(n):
    """
    """
    count = 0
    while n:
        n = n & (n-1)
        count = count + 1
    return count
    
def quda(scheme):
    """
    输入：一个拆分
    输出：对拆分的估值，估值越大越优先，这里采用的规则是「取大优先」
    """
    n = 0
    for index, char in enumerate(scheme):
        n += 10**(-index) * strokeNum(char)
    return n

def bishun(n, maximum, m):
    return tuple(k for k in range(m) if (maximum>>(k+1)) & n)

NAME = 'wubi98'
WEN = yaml.load(open('文.yaml'), Loader=yaml.BaseLoader)
ZI = yaml.load(open('字.yaml'), Loader=yaml.BaseLoader)
SCHEMA = yaml.load(open('preset/%s.schema.yaml' % NAME), Loader=yaml.BaseLoader)
DICT = yaml.load(open('preset/%s.dict.yaml' % NAME), Loader=yaml.BaseLoader)
ALIAS = yaml.load(open('preset/%s.alias.yaml' % NAME), Loader=yaml.BaseLoader)

def expand(indexList):
    """
    输入：在 xxx.alias.yaml 用户可以使用 ... 的简写形式，例如 1, ..., 6
    输入：将省略号展开，例如 1, 2, 3, 4, 5, 6
    """
    if '...' not in indexList:
        return list(map(int, indexList))
    else:
        splitList = [list(map(int, x.split(' '))) for x in (' '.join(indexList)).split(' ... ')]
        returnList = splitList[0]
        for n in range(len(splitList) - 1):
            startNum = splitList[n][-1]
            stopNum = splitList[n+1][0]
            returnList.extend(list(range(startNum + 1, stopNum)))
            returnList.extend(splitList[n+1])
        return returnList

# ROOTSET：字根名到键位的映射
ROOTSET = {}
# DEGENERACY：退化字根到字根的映射
DEGENERACY = {}
# 首先处理单笔画字根
ALLSTROKES = [ # 枚举所有的单笔画
    '横', '提', '竖', '竖钩', '撇', '点', '捺', # 单笔
    '横钩', '横撇', '横折', '横折钩', '横斜钩', '横折提', '横折折', '横折弯', '横撇弯钩', '横折弯钩', '横折折撇', '横折折折', '横折折折钩', # 以横为开始的折笔
    '竖提', '竖折', '竖弯', '竖弯钩', '竖折撇', '竖折折钩', '竖折折', # 以竖为开始的折笔
    '撇点', '撇折', '弯钩', '斜钩' # 其他折笔
    ]
strokeCategory = {}
# 读取用户对笔画的大类进行的自定义
for category, strokeTypeList in DICT['stroke'].items():
    for strokeType in strokeTypeList:
        strokeCategory[strokeType] = category
# 校验是否所有单笔画都有定义
lostStrokes = [x for x in ALLSTROKES if x not in strokeCategory]
if lostStrokes:
    raise ValueError('未定义的笔画：%s' % str(lostStrokes))

# 普通字根
for key, componentList in DICT['map'].items():
    for component in componentList:
        if component in DICT['stroke']: # 单笔画字根
            for strokeType in DICT['stroke'][component]:
                ROOTSET[strokeType] = key
        elif component in WEN: # 字根是「文」数据中的一个部件
            strokeList = [Stroke(stroke) for stroke in WEN[component]]
            char = Char(component, strokeList)
            ROOTSET[component] = key
            DEGENERACY[char.degenerate()] = char
        elif component in ALIAS: # 字根不是「文」数据库中的部件，但用户定义了它
            strokeList = []
            sourceChar, strokeIndexList = ALIAS[component]
            strokeIndexList = expand(strokeIndexList)
            sourceStrokeList = WEN[sourceChar]
            for index in strokeIndexList:
                strokeList.append(Stroke(sourceStrokeList[int(index)]))
            char = Char(component, strokeList)
            ROOTSET[component] = key
            DEGENERACY[char.degenerate()] = char
            # print(char.degenerate())
        elif component in ZI: # 这种情况对应着合体字根，暂不考虑，等写嵌套的时候再写
            pass

start = time.time()

COMPONENT = {}
for char in WEN:
    # if char == '下':
    strokeList = [Stroke(stroke) for stroke in WEN[char]]
    COMPONENT[char] = Char(char, strokeList).decompose()

CHARLIST = sorted(filter(lambda x: len(x) == 1, list(WEN.keys()) + list(ZI.keys())), key=ord)

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
            else: lnew.append(x)
        l = flat_and_filter(lnew)
    return l

with open('preset/%s.result.yaml' % NAME, 'w') as f:
    for charIndex, char in enumerate(CHARLIST):
        if char in WEN:
            scheme = COMPONENT[char]
        else:
            scheme = sum((COMPONENT.get(component, (Char(component, [[component]]), )) for component in dependencies(char)), tuple())
        if len(scheme) > 4:
            scheme = scheme[:3] + scheme[-1:]
        f.write(char + '\t' + ''.join(ROOTSET[component.name] for component in scheme) + '\n')
end = time.time()
print('拆分用时：', end - start)
print('幂集用时：', time1)
print('迭代用时：', time2)

complexity = {key: sum(value)/len(value) for key, value in complexity.items()}
with open('comp.txt', 'w') as f:
    for key, value in complexity.items():
        f.write('%d\t%d\n' % (key, value))