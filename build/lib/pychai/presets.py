# from .topology import topology

import yaml, pkgutil

topology = yaml.load(pkgutil.get_data(__package__, 'topology.yaml'), Loader=yaml.BaseLoader)

# 预置退化映射组件

def getStrokeList(objectChar):
    """
    功能：退化函数组件，提取出一个对象字的笔画序列
    输入：对象字
    输出：降维的可散列类对象
    """
    return ' '.join([stroke.type for stroke in objectChar.strokeList])

strokeSimplify = {
    '竖钩': '竖',
    '竖弯': '竖弯钩',
    '横折钩': '横折',
    '提': '横',
    '捺': '点',
    
}

def getStrokeListSimplified(objectChar):
    return ' '.join([strokeSimplify.get(stroke.type, stroke.type) for stroke in objectChar.strokeList])

def getTopoList(objectChar):
    """
    功能：退化函数组件，提取出一个对象字的拓扑
    输入：对象字
    输出：一个 n(n-1)/2 长度的字符串，n 为笔段个数
    """
    if objectChar.sourceName:
        ss = objectChar.sourceSlice
        l = topology[objectChar.sourceName]
        nestedList = [
            [
                relation for nrelation, relation in enumerate(row)
                if (1 << nrelation) & ss
            ]
            for nrow, row in enumerate(l)
            if (1 << nrow) & ss
        ]
    else:
        nestedList = topology[objectChar.name]
    return ' '.join(' '.join(x) for x in nestedList)

# 预置择优函数组件

def schemeLen(objectChar, scheme):
    """
    功能：拆分估值器，按拆分中切片多少进行估值
    输入：拆分
    输出：拆分估值
    """
    return len(scheme)

def schemeTopo(objectChar, scheme):
    """
    功能：估值器，按拆分中各切片的关系估值
    """
    lianFlag = False
    jiaoFlag = False
    l = objectChar.charlen
    ll = 1 << l
    topoList = topology[objectChar.name]
    schemeParsed = [tuple(k for k in range(l) if (ll >> (k + 1)) & num) for num in scheme]
    for n, strokeList in enumerate(schemeParsed):
        for n_, strokeList_ in enumerate(schemeParsed):
            if n_ <= n: continue
            for stroke in strokeList:
                for stroke_ in strokeList_:
                    if stroke < stroke_:
                        smaller, larger = stroke, stroke_
                    else:
                        smaller, larger = stroke_, stroke
                    relation = [x[-1:] for x in topoList[larger][smaller].split('_')]
                    if '连' in relation: lianFlag = True
                    if '交' in relation: jiaoFlag = True
    return 2 if jiaoFlag else 1 if lianFlag else 0

def schemeOrder(objectChar, scheme):
    """
    功能：拆分估值器，按拆分中切片符合笔顺程度进行估值，越符合，值越小
    输入：拆分，字对象（参数需求：笔画数）
    输出：拆分估值
    """
    l = objectChar.charlen
    mx = 1 << l
    schemeEval = sum((tuple(k for k in range(l) if (mx >> (k + 1)) & part) for part in scheme), tuple())
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
