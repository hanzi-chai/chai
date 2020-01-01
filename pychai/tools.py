import yaml
import pkgutil

def load(path, withNumbers=True):
    """
    功能：从当前工作目录中加载 YAML 数据库
    输入：路径 path
    输出：yaml 解析器加载后的数据
    """
    return yaml.load(open(path, encoding='utf-8'), Loader=yaml.SafeLoader if withNumbers else yaml.BaseLoader)

def loadFromPackage(path, withNumbers=True):
    """
    功能：从模块包中加载 YAML 数据库
    输入：路径 path
    输出：yaml 解析器加载后的数据
    """
    return yaml.load(pkgutil.get_data(__package__, path).decode(), Loader=yaml.SafeLoader if withNumbers else yaml.BaseLoader)

def checkCompleteness(strokeDict):
    """
    功能：检查笔画定义完整性
    输入：笔画定义字典 strokeDict 形如{type:[strokes]}
    输出：缺失笔画列 lostStrokes 形如 [strokes]
    """
    allstrokes = [
        '横', '提', '竖', '竖钩', '撇', '点', '捺',
        '横钩', '横撇', '横折', '横折钩', '横斜钩', '横折提', '横折折',
        '横折弯', '横撇弯钩', '横折弯钩', '横折折撇', '横折折折', '横折折折钩',
        '竖提', '竖折', '竖弯', '竖弯钩', '竖折撇', '竖折折钩', '竖折折',
        '撇点', '撇折', '弯钩', '斜钩'
        ]
    strokeCategory = {}
    # 读取用户对笔画的大类进行的自定义
    for category, strokeTypeList in strokeDict.items():
        for strokeType in strokeTypeList:
            strokeCategory[strokeType] = category
    # 校验是否所有单笔画都有定义
    lostStrokes = [x for x in allstrokes if x not in strokeCategory]
    return lostStrokes

def expand(indexList):
    """
    功能：展开形如 [1, ..., 6] 的省略式的笔画索引列
    输入：笔画索引列 indexList
    输入：展开后的笔画索引列 returnList ，形如 [1, 2, 3, 4, 5, 6]
    """
    if '...' in indexList:
        splitList = [list(map(int, x.split(' ')))
                     for x in (' '.join(map(str, indexList))).split(' ... ')]
        returnList = splitList[0]
        for n in range(len(splitList) - 1):
            startNum = splitList[n][-1]
            stopNum = splitList[n+1][0]
            returnList.extend(list(range(startNum + 1, stopNum)))
            returnList.extend(splitList[n+1])
    else:
        returnList = list(map(int, indexList))
    return returnList

def nextRoot(n):
    """
    功能：给定字未拆完的部分，求拆出下一个字根的所有可能性
    输入：数 n
    输出：在数的二进制表示中左边第一位取 1 ，其余所有「1」的位上取 1 或取 0 
          的所有可能的数的列表
    备注：一个含有n笔的字可用一个十进制数2**n-1表达其笔画状态
          例如一个3笔的字可以用7来表示，其对应二进值是111
          对于字的任意切片，可同理表示，上字含首末笔的切片为101，对应十进值为5
          以下算法基于位运算
    """
    powerList = [0]
    while n: # 直到当前序列所有「1」位都被置0之前，做：
        # 找到右边第一个「1」，如1110010的右二位，将其置0，得余待检序列1110000
        t = n & (n-1)
        # 当前序列扣除余待检序列，获得当前位及其右边所有位，1110010-1110000=10
        m = n - t
        # 将余待检序列设为当前序列，用于下一loop
        n = t
        # 对列表中每一个已有位扩增当前位「1」，并以此列表扩增原列表
        powerList = powerList + [x + m for x in powerList]
        # 当前位的「0」选项，将会在下一位「1」扩增时扩增
    # 将所有不足笔数长度的序列剔除，表明所取切片必含输入切片的第一笔
    return powerList[len(powerList)//2:]
