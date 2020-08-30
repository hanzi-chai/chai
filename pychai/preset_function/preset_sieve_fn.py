from pychai.classes import Char
from pychai.data import TOPOLOGY
"""预置择优函数组件"""
def schemeBias(char: Char, scheme):
    """
    功能：拆分估值器，按拆分中偏置程度估值，前端切片笔画数越多，值越大
    输入：拆分，字对象
    输出：拆分估值
    """
    schemeEval = sum(-1 * 10**(-index) * bin(part)[2:].count('1')
                        for index, part in enumerate(scheme))
    return schemeEval

def schemeLen(char: Char, scheme):
    """
    功能：拆分估值器，按拆分中切片多少进行估值
    输入：拆分
    输出：拆分估值
    """
    return len(scheme)

def schemeOrder(char: Char, scheme):
    """
    功能：拆分估值器，按拆分中切片符合笔顺程度进行估值，越符合，值越小
    输入：拆分，字对象（参数需求：笔画数）
    输出：拆分估值
    """
    l = len(char.strokeList)
    mx = 1 << l
    schemeEval = sum((tuple(k for k in range(l) if (mx >> (k + 1)) & part) for part in scheme), tuple())
    return schemeEval

def schemeTopo(char: Char, scheme):
    """
    功能：估值器，按拆分中各切片的关系估值
    """
    lianFlag = False
    jiaoFlag = False
    l = len(char.strokeList)
    ll = 1 << l
    topoList = TOPOLOGY[char.name]
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
