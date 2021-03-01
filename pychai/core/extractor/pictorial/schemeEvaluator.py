'''
预置择优函数组件
'''

from typing import List, Tuple

from ....base import Component, Stroke


def bias(component: Component, scheme) -> float:
    '''
    按拆分方案的取大程度求值。在总笔画数量一定的情况下，靠前的字根笔画数越多，靠后的字根笔画数越少，数值越大

    设部件总共 L 笔，拆为 k 个字根，第 i 字根含 l_i 笔，则具体公式为：

    .. math::

       -\sum_{i=1}^k l_i (L+1)^{-i}

    '''

    return -sum(component.length**(-index) * bin(part)[2:].count('1') for index, part in enumerate(scheme))

def length(_: Component, scheme) -> int:
    '''
    求拆分方案中含字根的数量
    '''

    return len(scheme)

def order(component: Component, scheme) -> tuple:
    '''
    功能：拆分估值器，按拆分中切片符合笔顺程度进行估值，越符合，值越小
    输入：拆分，字对象（参数需求：笔画数）
    输出：拆分估值
    '''

    mx = 1 << component.length
    return sum((tuple(k for k in range(component.length) if (mx >> (k + 1)) & part) for part in scheme), tuple())

def topology(component: Component, scheme) -> tuple:
    r'''
    我们可以基于笔画关系定义字根关系。如果两个字根间有笔画相交，则为交；不交但有笔画为连，则为连；其余为散。这样定义出来的映射记为 :math:`\tilde{\mathcal R}(r_1,r_2)`\ ，然后定义发生交、连、散的次数分别为 :math:`u_1,u_2,u_3`\ 。字根数量不可能超过 :math:`L`\ ，所以我们定义

    .. math::

       \mathcal H(d)=u_1(L+1)^2+u_2(L+1)+u_3+\sum_{i=1}^k\operatorname{len}(p_i)(L+1)^{-i}

    这样，我们就能把「天」拆成「一大」，把「夫」拆成「二人」。
    '''
    connectionBetweenRootsCount = 0
    crossBewteenRootsCount = 0
    length = len(component.strokeList)
    topologyMatrix = component.topologyMatrix
    schemeParsed = [tuple(strokeIndex
        for strokeIndex in range(length)
            if (1 << (length - strokeIndex - 1)) & binary)
        for binary in scheme]
    enum = enumerate(schemeParsed)
    for n, strokeIndexList in enum:
        for n_, strokeIndexList_ in enum:
            if n_ <= n: continue
            isConnected = False
            isCrossed = False
            for stroke in strokeIndexList:
                for stroke_ in strokeIndexList_:
                    smaller = min(stroke, stroke_)
                    larger = max(stroke, stroke_)
                    relation = [x[-1:] for x in topologyMatrix[larger][smaller].split('_')]
                    if '连' in relation: isCrossed = True
                    if '交' in relation: isConnected = True
            if isConnected: connectionBetweenRootsCount += 1
            if isCrossed: crossBewteenRootsCount += 1
    return (connectionBetweenRootsCount, crossBewteenRootsCount)

def similarity(component: Component, scheme):
    '''
    功能：估值器，按拆分中各切片比例相似性估值（弃用）
    '''
    cpnStrokeList = component.strokeList
    length = len(cpnStrokeList)
    result: Tuple[int,...] = ()
    def binaryToIndexList(binary: int):
        indexList: List[int] = []
        for i in range(length):
            if 2 ** (length - 1 - i) & binary:
                indexList.append(i)
        return indexList
    for binary in scheme:
        originalStrokeList = component.binaryDict[binary].strokeList
        sliceStrokeList: List[Stroke] = []
        indexList = binaryToIndexList(binary)
        if len(indexList) > 1:
            for index in indexList:
                sliceStrokeList.append(cpnStrokeList[index])
            oFirstStrokeLength = originalStrokeList[0].linearizeLength
            sFirstStrokeLength = sliceStrokeList[0].linearizeLength
            oRatio = list(map(lambda x: x.linearizeLength / oFirstStrokeLength, originalStrokeList))
            sRatio = list(map(lambda x: x.linearizeLength / sFirstStrokeLength, sliceStrokeList))
            result += (sum(abs(oRatio[i] - sRatio[i]) for i in range(len(oRatio))),)
        else:
            result += (0,)
    return result
