'''
计算拓扑缓存
'''

from numpy import array, cross, inf, stack
from numpy.linalg import norm, pinv
from ..base import Component, Linear

class Topology:
    '''
    拓扑计算器
    '''

    def __init__(self):
        self.TOL = 0.05

    def _relationStr(self, t1, t2, c1, c2):
        TOL = self.TOL
        def inner(t):
            return TOL < t < (1 - TOL)
        def outer(t):
            return -TOL < t < (1 + TOL)
        if inner(t1) and inner(t2):
            return '交'
        elif outer(t1) and outer(t2):
            # 均为「连」类，要进一步细分；
            position1 = '前' if t1 < TOL else '中' if t1 < 1 - TOL else '后'
            position2 = '前' if t2 < TOL else '中' if t2 < 1 - TOL else '后'
            return position1 + position2 + '连'
        else:
            return self._position(c1, c2) + '散'

    def _linear(self, c1, c2):
        p1 = c1.P1 - c1.P0
        p2 = c2.P1 - c2.P0
        det = cross(p1, p2)
        if det == 0: return array([inf, inf])
        b = c2.P0 - c1.P0
        t1 = cross(b, p2) / det
        t2 = cross(b, p1) / det
        return array([t1, t2])

    def _relation(self, c1, c2):
        if isinstance(c1, Linear) and isinstance(c2, Linear):
            t1, t2 = self._linear(c1, c2)
            return self._relationStr(t1, t2, c1, c2)
        else:
            c1l = c1.linearize()
            c2l = c2.linearize()
            x = self._linear(c1l, c2l)
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
                self._newton(f, J, x)
            t1, t2 = x
            return self._relationStr(t1, t2, c1, c2)

    def _newton(self, f, J, x) -> None:
        epsilon = 0.000001
        n = 0
        while norm(f(x)) > epsilon:
            n += 1
            x -= pinv(J(x)) @ f(x)
            if n > 100: break

    def _position(self, c1, c2):
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

    def __call__(self, component: Component):
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
                        relationList.append(self._relation(curve, curve_))
                lengthRelation = ''
                if hengOrShu and feature == feature_:
                    lengthRelation = '_短' if curveList[0].linearizeLength() < curveList_[0].linearizeLength() else '_长'
                row.append('_'.join(relationList) + lengthRelation)
            returnList.append(row)
        return returnList
