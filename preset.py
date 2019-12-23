# 预置退化映射组件

def getStrokeList(objectChar):
    """
    功能：退化函数组件，提取出一个对象字的笔画序列
    输入：对象字
    输出：降维的可散列类对象
    """
    return ' '.join([stroke.type for stroke in objectChar.strokeList])

def getTopoList(objectChar):
    """
    功能：退化函数组件，提取出一个对象字的笔画序列
    输入：对象字
    输出：待定
    """
    return ''

# 预置择优函数组件

def schemeLen(objectChar, scheme):
    """
    功能：拆分估值器，按拆分中切片多少进行估值
    输入：拆分
    输出：拆分估值
    """
    return len(scheme)

def schemeOrder(objectChar, scheme):
    """
    功能：拆分估值器，按拆分中切片符合笔顺程度进行估值，越符合，值越小
    输入：拆分，字对象（参数需求：笔画数）
    输出：拆分估值
    """
    charlen = objectChar.charlen
    m = charlen
    mx = 2**charlen
    schemeEval = sum((tuple(k for k in range(m) if (mx >> (k + 1)) & part) for part in scheme), tuple())
    return schemeEval

def schemeBias(objectChar, scheme):
    """
    功能：拆分估值器，按拆分中偏置程度估值，前端切片笔画数越多，值越大
    输入：拆分，字对象
    输出：拆分估值
    """
    schemeEval = sum(-1 * 10**(-index) * bin(part)[2:].count('1')
                        for index, part in enumerate(scheme))
    return schemeEval
