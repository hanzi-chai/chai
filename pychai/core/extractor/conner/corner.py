'''
计算四角缓存
'''

from typing import Dict, List, Set, Tuple

from numpy import abs, array
from numpy import ndarray as Point

from ....base import Component


def findCorner(component: Component) -> Tuple[int]:
    criticalPointList, fromStroke = findCriticalPoints(component)
    leftTop = array([0, 0])
    leftBottom = array([0, 100])
    rightTop = array([100, 0])
    rightBottom = array([100, 100])
    corners = []
    for p0 in (leftTop, rightTop, leftBottom, rightBottom):
        isNearest = lambda p1: not any(isNearThan(p2, p1, p0) for p2 in criticalPointList)
        nearests = filter(isNearest, criticalPointList)
        atCorner = min(nearests, key=lambda p: abs(p - p0)[1])
        corners.append(atCorner)
    return tuple([fromStroke[(atCorner[0], atCorner[1])] for atCorner in corners])

def isNearThan(p1: Point, p2: Point, p0: Point) -> bool:
    r10 = abs(p1 - p0)
    r20 = abs(p2 - p0)
    return r10[0] <= r20[0] and r10[1] <= r20[1] and (not all(p1 == p2))

def findCriticalPoints(component: Component) -> Tuple[List[Point], Dict[Tuple, int]]:
    points = []
    fromStroke = {}
    for index, stroke in enumerate(component.strokeList):
        for curve in stroke.curveList:
            for point in (curve.start, curve.end):
                if not any(all(point == another) for another in points):
                    fromStroke[(point[0], point[1])] = index
                    points.append(point)
    return points, fromStroke
