'''
计算拓扑缓存
'''

from numpy import array, cross, inf, stack
from numpy.linalg import norm, inv
from ..base import Component, Linear, Cubic

class Topology:
    '''
    拓扑计算器
    '''

    def __init__(self):
        self.TOL = 0.05

    def __relation(self, t1, t2):
        TOL = self.TOL
        def inner(t):
            return TOL < t < (1 - TOL)
        def outer(t):
            return -TOL < t < (1 + TOL)
        if inner(t1) and inner(t2):
            return '交'
        elif outer(t1) and outer(t2):
            # 均为「连」类，要进一步细分；
            c1 = '前' if t1 < TOL else '中' if t1 < 1 - TOL else '后'
            c2 = '前' if t2 < TOL else '中' if t2 < 1 - TOL else '后'
            return c1 + c2 + '连'
        else:
            return '散'

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
            return self.__relation(t1, t2)
        else:
            c1l = c1.linearize()
            c2l = c2.linearize()
            x = self._linear(c1l, c2l)
            if min(x) > -0.2 and max(x) < 1.2:
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
            return self.__relation(t1, t2)

    def _newton(self, f, J, x) -> None:
        epsilon = 0.000001
        n = 0
        while norm(f(x)) > epsilon:
            n += 1
            x -= inv(J(x)) @ f(x)
            if n > 100: break

    def __call__(self, component: Component):
        returnList = []
        strokeList = component.strokeList
        for n, stroke in enumerate(strokeList):
            row = []
            curveList = stroke.curveList
            for n_, stroke_ in enumerate(strokeList):
                if n_ >= n: continue
                curveList_ = stroke_.curveList
                relationList = []
                for curve in curveList:
                    for curve_ in curveList_:
                        relationList.append(self._relation(curve, curve_))
                # print(relationList)
                row.append('_'.join(relationList))
            # print('---')
            returnList.append(row)
        return returnList
