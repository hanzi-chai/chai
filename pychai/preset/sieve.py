'''
预置择优函数组件
'''

from ..base import Component

def bias(_: Component, scheme):
    '''
    功能：拆分估值器，按拆分中偏置程度估值，前端切片笔画数越多，值越大
    输入：拆分，字对象
    输出：拆分估值
    '''

    return -sum(100**(-index) * bin(part)[2:].count('1') for index, part in enumerate(scheme))

def length(_: Component, scheme):
    '''
    功能：拆分估值器，按拆分中切片多少进行估值
    输入：拆分
    输出：拆分估值
    '''

    return len(scheme)

def order(component: Component, scheme):
    '''
    功能：拆分估值器，按拆分中切片符合笔顺程度进行估值，越符合，值越小
    输入：拆分，字对象（参数需求：笔画数）
    输出：拆分估值
    '''

    l = len(component.strokeList)
    mx = 1 << l
    return sum((tuple(k for k in range(l) if (mx >> (k + 1)) & part) for part in scheme), tuple())

def topology(component: Component, scheme):
    '''
    功能：估值器，按拆分中各切片的关系估值
    '''
    hasConnection = False
    hasCross = False
    l = len(component.strokeList)
    topologyMatrix = component.topologyMatrix
    schemeParsed = [tuple(k for k in range(l) if (1 << (l - k - 1)) & num) for num in scheme]
    for n, strokeList in enumerate(schemeParsed):
        for n_, strokeList_ in enumerate(schemeParsed):
            if n_ <= n: continue
            for stroke in strokeList:
                for stroke_ in strokeList_:
                    smaller = min(stroke, stroke_)
                    larger = max(stroke, stroke_)
                    relation = [x[-1:] for x in topologyMatrix[larger][smaller].split('_')]
                    if '连' in relation: hasConnection = True
                    if '交' in relation: hasCross = True
    return 2 if hasCross else 1 if hasConnection else 0
