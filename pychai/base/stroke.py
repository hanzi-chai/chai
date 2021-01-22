'''

'''

from functools import cached_property
from typing import List, Dict
from numpy import array
from .curve import Linear, Cubic

class Stroke:
    '''
    笔画
    '''
    def __init__(self, data: Dict):
        self.feature: str = data['feature']
        self.start: array = array(data['start'])
        self.curveList: List[Curve] = []
        for curveData in data['curveList']:
            curve = self.factory(curveData)
            self.curveList.append(curve)

    def factory(self, curveData):
        command = curveData['command']
        parameterList = curveData['parameterList']
        P0 = self.start
        if command == 'h':
            P1 = P0 + array(parameterList + [0])
            curve = Linear(P0, P1)
            self.start = P1
            return curve
        elif command == 'v':
            P1 = P0 + array([0] + parameterList)
            curve = Linear(P0, P1)
            self.start = P1
            return curve
        elif command == 'l':
            P1 = P0 + array(parameterList)
            curve = Linear(P0, P1)
            self.start = P1
            return curve
        else:
            P1 = P0 + array(parameterList[:2])
            P2 = P0 + array(parameterList[2:4])
            P3 = P0 + array(parameterList[4:])
            curve = Cubic(P0, P1, P2, P3)
            self.start = P3
            return curve

    @cached_property
    def linearizeLength(self):
        return sum(curve.linearizeLength() for curve in self.curveList)

    def __str__(self):
        return f'{self.feature}: {self.start} -> {self.curveList}'
