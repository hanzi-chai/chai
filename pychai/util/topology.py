'''
计算拓扑缓存
'''

from typing import List
from numpy import array, cross, inf, stack
from numpy.linalg import norm, pinv
from ..base import Component, Curve, Linear

TOL = 0.05

def relationStr(t1: float, t2: float, c1: Curve, c2: Curve):
    '''根据 t1, t2 值确定两 Bezier 曲线的拓扑描述字符串
    '''
    if TOL < t1 < (1 - TOL) and TOL < t2 < (1 - TOL):
        return '交'
    elif -TOL < t1 < (1 + TOL) and -TOL < t2 < (1 + TOL):
        # 均为「连」类，要进一步细分；
        position1 = '前' if t1 < TOL else '中' if t1 < 1 - TOL else '后'
        position2 = '前' if t2 < TOL else '中' if t2 < 1 - TOL else '后'
        return position1 + position2 + '连'
    else:
        return position(c1, c2) + '散'

def linear(c1: Linear, c2: Linear):
    '''求一次 Bezier 曲线（直线段）交点的 t1, t2 值
    '''
    p1 = c1.P1 - c1.P0
    p2 = c2.P1 - c2.P0
    det = cross(p1, p2)
    if det == 0: return array([inf, inf])
    b = c2.P0 - c1.P0
    t1 = cross(b, p2) / det
    t2 = cross(b, p1) / det
    return array([t1, t2])

def relation(c1: Curve, c2: Curve):
    '''确定任意两条一次或三次 Bezier 曲线的拓扑描述
    '''
    if isinstance(c1, Linear) and isinstance(c2, Linear):
        t1, t2 = linear(c1, c2)
        return relationStr(t1, t2, c1, c2)
    else:
        c1l = c1.linearize()
        c2l = c2.linearize()
        x = linear(c1l, c2l)
        if -0.2 < x[0] < 1.2 or -0.2 < x[1] < 1.2:
            def f(a):
                t1, t2 = a
                return c1(t1) - c2(t2)
            c1p = c1.derivative()
            c2p = c2.derivative()
            def J(a):
                t1, t2 = a
                return stack((
                    c1p(t1), -c2p(t2)
                ), axis=1)
            newton(f, J, x)
        t1, t2 = x
        return relationStr(t1, t2, c1, c2)

def newton(f, J, x):
    '''牛顿迭代法求两 Bezier 曲线交点的 t1, t2 值。
    '''
    epsilon = 0.000001
    n = 0
    while norm(f(x)) > epsilon:
        n += 1
        x -= pinv(J(x)) @ f(x)
        if n > 100: break

def position(c1: Curve, c2: Curve):
    '''确定两曲线的位置关系

    输入：
        c1: 曲线一
        c2: 曲线二

    输出：
        str: 位置描述。
    '''
    start1 = c1.P0
    end1 = c1.P1 if isinstance(c1, Linear) else c1.P3
    start2 = c2.P0
    end2 = c2.P1 if isinstance(c2, Linear) else c2.P3
    x1 = [start1[0], end1[0]]
    y1 = [start1[1], end1[1]]
    x2 = [start2[0], end2[0]]
    y2 = [start2[1], end2[1]]
    def union(r1, r2):
        r1.sort()
        r2.sort()
        min1 = r1[0]
        max1 = r1[1]
        min2 = r2[0]
        max2 = r2[1]
        mid1 = (min1 + max1) / 2
        mid2 = (min2 + max2) / 2
        if min1 > mid2 and max2 < mid1:
            return -1
        elif min2 > mid1 and max1 < mid2:
            return 1
        else:
            return 0
    resultX = union(x1, x2)
    resultY = union(y1, y2)
    strX = '右' if resultX == -1 else '左' if resultX == 1 else ''
    strY = '下' if resultY == -1 else '上' if resultY == 1 else ''
    return strX + strY

def topology(component: Component) -> List[List[str]]:
    '''生成 Component 对象的拓扑描述矩阵

    输入：
        component: Component对象

    输出：
        List[List[str]]: 拓扑描述矩阵的左下三角。形如下：
        [
            [],
            [`笔画2与笔画1的拓扑描述`],
            [`笔画3与笔画1的拓扑描述`,`笔画3与笔画2的拓扑描述`],
            [`笔画4与笔画1的拓扑描述`,`笔画4与笔画2的拓扑描述`,`笔画4与笔画3的拓扑描述`],
            ...
            [`笔画n与笔画1的拓扑描述`,`笔画n与笔画2的拓扑描述`,...,`笔画n与笔画n-1的拓扑描述`],
        ]
    '''
    returnList = []
    strokeList = component.strokeList
    for n in range(0, len(strokeList)):
        row = []
        stroke = strokeList[n]
        feature = stroke.feature
        hengOrShu = feature == '横' or feature == '竖'
        curveList = stroke.curveList
        for n_ in range(0, n):
            stroke_ = strokeList[n_]
            feature_ = stroke_.feature
            curveList_ = strokeList[n_].curveList
            relationList = []
            for curve in curveList:
                for curve_ in curveList_:
                    relationList.append(relation(curve, curve_))
            lengthRelation = ''
            if hengOrShu and feature == feature_:
                lengthRelation = '&短' if curveList[0].linearizeLength() < curveList_[0].linearizeLength() else '&长'
            row.append(feature_, feature, '_'.join(relationList) + lengthRelation)
        returnList.append(row)
    return returnList

def topologyRevers(topologyStr: str):
    '''拓扑描述取反，即笔顺交换之后的拓扑描述。

    参数：
        topologyStr: 原拓扑描述字符串

    输出：
        str: 取反后的拓扑描述字符串。例如输入「右散」则输出「左散」，输入「前中连」则输出「中前连」
        输入「前前连_右散」则输出「前前连_左散」。
    '''
    if '_' in topologyStr:
        tmp  = []
        for item in topologyStr.split('_'):
            tmp.append(topologyRevers(item))
        return '_'.join(tmp)
    elif topologyStr == '交' or topologyStr == '散':
        return topologyStr
    elif '连' in topologyStr:
        return topologyStr[1] + topologyStr[0] + topologyStr[2]
    else:
        if '左' in topologyStr:
            topologyStr = topologyStr.replace('左', '右')
        else:
            topologyStr = topologyStr.replace('右', '左')
        if '上' in topologyStr:
            topologyStr = topologyStr.replace('上', '下')
        else:
            topologyStr = topologyStr.replace('下', '上')
        if '长' in topologyStr:
            topologyStr = topologyStr.replace('长', '短')
        else:
            topologyStr = topologyStr.replace('短', '长')
        return topologyStr

def strokeTopologySimplify(strokeFeature1: str, strokeFeature2: str, topologyStr: str):
    '''拓扑简化。（暂弃用）

    输入：
        strokeFeature1: 前一笔的笔画类型
        strokeFeatrue2: 后一笔的笔画类型
        topologyStr: 两笔之间的拓扑描述字符串

    输出：
        str: 简化后的拓扑描述。
    '''
    if strokeFeature1 == '横' or strokeFeature1 == '提':
        topologyStr = topologyStr.replace('前中连', '下散')
        topologyStr = topologyStr.replace('后中连', '上散')
        topologyStr = topologyStr.replace('中前连', '左散')
        topologyStr = topologyStr.replace('中后连', '右散')
    elif strokeFeature1 == '竖' or strokeFeature1 == '竖钩':
        topologyStr = topologyStr.replace('前中连', '右散')
        topologyStr = topologyStr.replace('后中连', '左散')
        topologyStr = topologyStr.replace('中前连', '上散')
        topologyStr = topologyStr.replace('中后连', '下散')
    elif strokeFeature2 == '横' or strokeFeature2 == '提':
        topologyStr = topologyStr.replace('前中连', '右散')
        topologyStr = topologyStr.replace('后中连', '左散')
        topologyStr = topologyStr.replace('中前连', '上散')
        topologyStr = topologyStr.replace('中后连', '下散')
    elif strokeFeature2 == '竖' or strokeFeature2 == '竖钩':
        topologyStr = topologyStr.replace('前中连', '下散')
        topologyStr = topologyStr.replace('后中连', '上散')
        topologyStr = topologyStr.replace('中前连', '左散')
        topologyStr = topologyStr.replace('中后连', '右散')
    else:
        # TODO: 撇点捺与折类笔画的关系简化
        pass
    return topologyStr

def componentTopologySimplify(component: Component):
    '''对 Component 对象所有拓扑关系执行拓扑简化。（暂弃用）
    '''
    strokeList = component.strokeList
    for topoRowN in range(0, len(strokeList)):
        stroke = strokeList[topoRowN]
        feature = stroke.feature
        topoRow = component.topologyMatrix[topoRowN]
        for topoColN in range(0, topoRowN):
            stroke_ = strokeList[topoColN]
            feature_ = stroke_.feature
            topoRow[topoColN] = strokeTopologySimplify(feature, feature_, topoRow[topoColN])
    return
